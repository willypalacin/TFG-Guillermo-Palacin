from Device import Device
from ntc_templates.parse import parse_output
from netmiko import ConnectHandler
import jinja2, json
import requests
import yaml
import re
from ipaddress import IPv4Network
from ipaddress import IPv4Address


class IOSRouter(Device):
    def __init__(self, name, ip, type, username, password, port):
        Device.__init__(self, name, ip, type, username, password, port)
        self.baseUrl = "https://{}:{}/restconf/data/".format(ip, port)
        self.connection = {
          'Accept': 'application/yang-data+json',
          'Content-Type': 'application/yang-data+json',
          'Authorization': 'Basic Y2lzY286Y2lzY29fMTIzNCE='
        }
        self.auth=('{}'.format(self.username), '{}'.format(self.password))
        self.c_netmiko = ConnectHandler(host = self.ip, username=self.username,
                                         password=self.password,
                                         device_type = 'cisco_ios',
                                         port=22, timeout=10)

    def createLoopbackTesting(self, int_name, name, ip, mask):
        self.connection.enable()
        #self.connection.config_mode('config t')
        #cmd = ['int Loopback 834', 'ip address 1.1.1.1 255.255.255.255']
        f = open('Templates/cisco_ios.tmpl')
        text = f.read()
        template = jinja2.Template(text)
        config = template.render(int_name=int_name, name=name, ip=ip, mask=mask).split('\n')
        print ("CONFIG: \n: {}".format(config))
        output = self.connection.send_config_set(config)
        print('\nConfiguration applied: \n\n' + output)

    def checkConnectivity(self):
        try:
            response = requests.get(self.baseUrl + "Cisco-IOS-XE-native:native/hostname",
                                    auth=self.auth,
                                    headers=self.connection,
                                    verify=False)
            self.c_netmiko.enable()
            return 201, "Dispositivo {} anadido satisfactoriamente".format(self.name)
        except:
            return 404, "No se ha encontrado ningun dispositivo con IP {}".format(self.ip)

    def editInterface(self, int_name, desc, ip, mask):
        #self.connection.enable()
        #self.connection.config_mode('config t')
        #cmd = ['int Loopback 834', 'ip address 1.1.1.1 255.255.255.255']


        data = {'interfaces': []}

        #dataResponse = json.loads(response.text)
        try:
            f = open('Templates/CiscoIOS/cisco_interfaces.j2')
            text = f.read()
            template = jinja2.Template(text)
            config = template.render(int_name=int_name,
                                     ip=ip,
                                     mask=mask, description=desc)

            response = requests.put(self.baseUrl + "ietf-interfaces:interfaces/interface={}".format(int_name),
                                    auth=self.auth ,headers=self.connection, data = config, verify=False)
            return "Interfaz {} configurada correctamente en {}".format(int_name, self.name), 201

        except:
            return "Error al configurar Interfaz en {} ".format(self.name), 404


    def getInterfacesList(self):
        try:
            response = requests.get(self.baseUrl + "ietf-interfaces:interfaces", auth=self.auth,
                                        headers=self.connection, verify=False)
            data = {'interfaces': []}
            dataResponse = json.loads(response.text)
            for intf in dataResponse['ietf-interfaces:interfaces']['interface']:
                data['interfaces'].append(intf['name'])
            print(data)
            return data, 201
        except:
            return {}, 404

    def getOspfData(self):
        data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}
        try:
                response = requests.get(self.baseUrl + "Cisco-IOS-XE-native:native/interface" , auth=self.auth,
                                            headers=self.connection, verify=False)


                dataResponse = json.loads(response.text)

                rid = []
                pid = []
                for intf in dataResponse['Cisco-IOS-XE-native:interface']:
                    for i in range(0,len(dataResponse['Cisco-IOS-XE-native:interface'][intf])):
                        if 'ip' in dataResponse['Cisco-IOS-XE-native:interface'][intf][i].keys():
                            print(dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip'].keys())
                            if 'Cisco-IOS-XE-ospf:ospf' in dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip'].keys():
                                intName = '{}{}'.format(intf, dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['name'])
                                data['ospf']['interfaces'].update({intName : {}})
                                dataOspf=dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip']['Cisco-IOS-XE-ospf:ospf']
                                print("DataOSPF")
                                print(dataOspf.keys())
                                data['ospf']['interfaces'][intName]['area'] = dataOspf['process-id'][0]['area']
                                if "hello-interval" in dataOspf.keys():
                                    data['ospf']['interfaces'][intName]['helloTimer'] = dataOspf['hello-interval']
                                    print(dataOspf['process-id'][0]['area'])
                                if "cost" in dataOspf.keys():
                                    data['ospf']['interfaces'][intName]['coste'] = dataOspf['cost']
                                if "dead-interval" in dataOspf.keys():
                                    data['ospf']['interfaces'][intName]['deadTimer'] = dataOspf['dead-interval']['value']
                                if "priority" in dataOspf.keys():
                                    data['ospf']['interfaces'][intName]['priority'] = dataOspf['priority']
                                print(data)

                response = requests.get(self.baseUrl + "Cisco-IOS-XE-native:native/router/ospf" , auth=self.auth,
                                            headers=self.connection, verify=False)
                dataResponse = json.loads(response.text)
                print(response.text)
                print(dataResponse['Cisco-IOS-XE-ospf:ospf'])

                for process in range(0,len(dataResponse['Cisco-IOS-XE-ospf:ospf'])):
                    pid.append(dataResponse['Cisco-IOS-XE-ospf:ospf'][process]['id'])
                    rid.append(dataResponse['Cisco-IOS-XE-ospf:ospf'][process]['router-id'])
                data['ospf']['routerId'] = str(rid).strip("[]''")
                data['ospf']['processId'] = str(pid).strip("[]")

                return yaml.dump(data, default_flow_style=False), 201
                    #data['ospf']['routerId']= response[0]['vrfs']['default']['instList'][str(pid)]
        except Exception as e:
            return yaml.dump(data, default_flow_style=False), 404

    def createOspf(self, data):
        try:
            f1 = open('Templates/CiscoIOS/cisco_ospf_interfaces.j2')
            f2 = open('Templates/CiscoIOS/cisco_ospf_process.j2')

            if data['ospf']['processId']:
                text = f2.read()
                template = jinja2.Template(text)
                config = template.render(pid= int(data['ospf']["processId"]),
                                        rid = data['ospf']["routerId"], default_info=data['ospf']['default-originate'])
                print(config)
                print(data['ospf']['default-originate'])
                try:
                    response = requests.put(self.baseUrl + 'Cisco-IOS-XE-native:native/router'.format(data['ospf']['processId']),
                                            auth=self.auth,
                                            headers=self.connection,
                                            data = config, verify=False)
                except:
                    return 'Ya existe un proceso con router-id {}'.format(data['ospf']["routerId"]), 404

            for intf in data['ospf']['interfaces']:
                if data['ospf']['interfaces'][intf]:
                    match = re.match(r"([a-z]+)([0-9]+)", intf, re.I)
                    if data['ospf']['interfaces'][intf]['helloTimer'] == '':
                        data['ospf']['interfaces'][intf]['helloTimer'] = '10'
                    if data['ospf']['interfaces'][intf]['deadTimer'] == '':
                        data['ospf']['interfaces'][intf]['deadTimer'] = '40'
                    if match:
                        items = match.groups()
                        text = f1.read()
                        template = jinja2.Template(text)
                        config = template.render(pid= int(data['ospf']["processId"]),
                                                 hello = data['ospf']['interfaces'][intf]['helloTimer'],
                                                 dead = data['ospf']['interfaces'][intf]['deadTimer'],
                                                 priority = data['ospf']['interfaces'][intf]['priority'],
                                                 cost = data['ospf']['interfaces'][intf]['coste'],
                                                 area =  data['ospf']['interfaces'][intf]['area'])
                        try:
                            requests.delete(self.baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}/ip/Cisco-IOS-XE-ospf:ospf'.format(items[0], items[1]), auth=self.auth,headers=self.connection, verify=False)
                        except:
                            pass

                        response = requests.put(self.baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}/ip/Cisco-IOS-XE-ospf:ospf'.format(items[0], items[1]),
                                                auth=self.auth,
                                                headers=self.connection,
                                                data = config, verify=False)
                        print(config)
                        print(response.text)
                        if("errors" not in response.text):
                            print(response.text)
                            return "OSPF configurado correctamente en {}".format(self.name), 201
                        else:
                            return "{}".format(json.loads(response.text)['errors']['error'][0]["error-message"]), 404
        except Exception as e:
            return '{}'.format(e), 404

    def createVrrp(self, data):
        try:
            f = open('Templates/CiscoIOS/cisco_vrrp.j2')
            for intf in data['vrrp']:
                match = re.match(r"([a-z]+)([0-9]+)", intf, re.I)
                if match:
                    items = match.groups()
                    text = f.read()
                    template = jinja2.Template(text)
                    config_restconf = template.render(group=data['vrrp'][intf]['grupo'], priority=data['vrrp'][intf]['priority'],
                                             preempt=data['vrrp'][intf]['preempt'], virtual_ip=data['vrrp'][intf]['ipVrrp'])

                    response = requests.put(self.baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}/vrrp'.format(items[0], items[1]),
                                            auth=self.auth,
                                            headers=self.connection,
                                            data = config_restconf, verify=False)
                    if "errors" not in response.text:
                        return "VRRP configurado correctamente en {}".format(self.name), 201
                    else:
                        return "Comando incosistente, recuerda que la IP virtual, debe pertenecer a la IP de la interfaz", 404
        except:
            return "Necesitas configurar la interfaz primero para activar VRRP", 404

    def createStaticRouting(self, data):
        try:
            f = open('Templates/CiscoIOS/cisco_static_routing.j2')
            netmask = IPv4Network(data['red']).netmask
            text = f.read()
            template = jinja2.Template(text)
            config = template.render(intf=data['intf'],
                                     ip=data['red'].split("/")[0],
                                     mask=netmask, metric=data['metric'], gw=data['gw'])
            response = requests.put(self.baseUrl + "Cisco-IOS-XE-native:native/ip/route/ip-route-interface-forwarding-list={},{}".format(data['red'].split("/")[0], netmask),
                                    auth=self.auth,headers=self.connection, data = config, verify=False)

            return "Ruta creada correctamente en {}".format(self.name), 201
        except Exception as e:
            return "{}".format(e), 404



    def createAcl(self, data):
        try:
            f = open('Templates/CiscoIOS/cisco_acl.j2')
            text = f.read()
            template = jinja2.Template(text)

            f2 = open('Templates/CiscoIOS/cisco_acl_interface.j2')
            text = f2.read()
            template2 = jinja2.Template(text)

            tipoAcl = "standard"
            inout = "in"
            for rule in data:
                if data[rule]['rule']['num'] != '':
                    if data[rule]['rule']['protocol'] != '' or data[rule]['rule']['destAddr'] != '' or data[rule]['rule']['destPort']!= '':
                        tipoAcl = "extended"
                    if "accept" in data[rule]['rule']['action']:
                        data[rule]['rule']['action']  = "permit"
                    if "discard" in data[rule]['rule']['action']:
                        data[rule]['rule']['action']  = "deny"


                    netmaskSa = IPv4Network(data[rule]['rule']['sourceAddr']).netmask
                    wildcardSa = (str(IPv4Address(int(IPv4Address(netmaskSa))^(2**32-1))))
                    netmaskDa = IPv4Network(data[rule]['rule']['sourceAddr']).netmask
                    wildcardDa = (str(IPv4Address(int(IPv4Address(netmaskDa))^(2**32-1))))
                    restconfDataAcl = template.render(wildcard_sa = wildcardSa,
                                                   wildcard_da=wildcardDa,
                                                   tipo_acl = tipoAcl,
                                                   nombre_acl = rule,
                                                   num=data[rule]['rule']['num'],
                                                   sa=data[rule]['rule']['sourceAddr'].split("/")[0],
                                                   da=data[rule]['rule']['destAddr'].split("/")[0],
                                                   protocol=data[rule]['rule']['protocol'],
                                                   action = data[rule]['rule']['action'],
                                                   dest_port=data[rule]['rule']['destPort'])
                    response = requests.patch(self.baseUrl + 'Cisco-IOS-XE-native:native/ip/access-list',
                                            auth=self.auth,
                                            headers=self.connection,
                                            data = restconfDataAcl, verify=False)
                if "output" in data[rule]['interfaz']['apply']:
                    inout = "out"
                if data[rule]['interfaz']['nombre']:
                    match = re.match(r"([a-z]+)([0-9]+)", data[rule]['interfaz']['nombre'], re.I)
                    if match:
                        items = match.groups()
                        restconfDataAclInt = template2.render(inout = inout, nombre_acl = rule)
                        response = requests.put(self.baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}/ip/access-group'.format(items[0], items[1]),
                                                auth=self.auth,
                                                headers=self.connection,
                                                data = restconfDataAclInt, verify=False)
            return "ACL creada correctamente en {}".format(self.name), 201
        except Exception as e:
            return "Error al crear ACL en {}".format(self.name), 404

    def showInterfaces(self):
         try:
             interfaces = self.c_netmiko.send_command('show ip int brief')

             vlan_parsed = parse_output(platform="cisco_ios", command="show ip interface brief", data=interfaces)
             showInterfaces = []
             for intf in vlan_parsed:
                 data = {
                         'nombre': intf['intf'],
                         'adminStatus' : intf['status'],
                         'proStatus' : intf['proto'],
                         'ip' : intf['ipaddr'],
                 }
                 showInterfaces.append(data)
             return showInterfaces
         except:
             return []

    def showIpRoute(self):
         try:
             command = self.c_netmiko.send_command('show ip route')
             ipRoute = parse_output(platform="cisco_ios", command="show ip route", data=command)
             showIpRoute = []
             for route in ipRoute:
                 data =  {
                         'protocolo' : route['protocol'],
                         'red' : route['network'] + "/"+ route['mask'],
                         'distancia': route['metric'],
                         'metrica': route['distance'],
                         'gateway': route['nexthop_ip'],
                         'gateway_if': route['nexthop_if']
                     }
                 showIpRoute.append(data)
             return showIpRoute
         except:
             return {}
    def showOspfNeigh(self):
        try:
            ospfNeigh = self.c_netmiko.send_command('show ip ospf neighbor')
            ospfNeighParsed = parse_output(platform="cisco_ios", command="show ip ospf neighbor", data=ospfNeigh)
            return ospfNeighParsed
        except:
            return []

    def showVlan(self):
        try:
            vlanShow = self.c_netmiko.send_command('show vlan')
            vlanShowParsed = parse_output(platform="cisco_ios", command="show vlan", data=vlanShow)
            return showVlanParsed
        except:
            return []

    def showOspfIntf(self):
        try:
            showOspfInt = self.c_netmiko.send_command('show ip ospf interface brief')
            showOspfIntParsed = parse_output(platform="cisco_ios", command="show ip ospf interface brief", data=showOspfInt)
            return showOspfIntParsed
        except:
            return []

    def showVrrp(self):
        try:
            vrrpData = self.c_netmiko.send_command('show vrrp brief').split("\n")
            showVrrp = []
            i = 0
            for vrrp in vrrpData:
                if i != 0:
                    line = re.split("\\s+", vrrp)
                    data = {
                        'interface': line[0],
                        'group': line[1],
                        'state': line [5],
                        'time': line[3],
                        'master_ip': line[6],
                        'group_ip': line[7]
                    }
                    showVrrp.append(data)
                i = i + 1
                print(showVrrp)
            return showVrrp
        except:
            return []
