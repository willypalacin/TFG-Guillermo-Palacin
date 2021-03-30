from Device import Device
import jinja2, json
import requests
import yaml
import re

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
                                    verify=True)
            return 201, "Dispositivo {} anadido satisfactoriamente".format(self.name)
        except:
            return 404, "No se ha encontrado ningun dispositivo con IP {}".format(self.ip)

    def editInterface(self, int_name, desc, ip, mask):
        #self.connection.enable()
        #self.connection.config_mode('config t')
        #cmd = ['int Loopback 834', 'ip address 1.1.1.1 255.255.255.255']


        data = {'interfaces': []}

        #dataResponse = json.loads(response.text)
        f = open('Templates/CiscoIOS/cisco_interfaces.j2')
        text = f.read()
        template = jinja2.Template(text)
        config = template.render(int_name=int_name,
                                 ip=ip,
                                 mask=mask, description=desc)

        response = requests.put(self.baseUrl + "ietf-interfaces:interfaces/interface={}".format(int_name),
                                auth=self.auth ,headers=self.connection, data = config, verify=True)
        if response.text == '':
            print("si")

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
                                        headers=self.connection, verify=True)


            dataResponse = json.loads(response.text)

            rid = []
            pid = []

            for intf in dataResponse['Cisco-IOS-XE-native:interface']:
                for i in range(0,len(dataResponse['Cisco-IOS-XE-native:interface'][intf])):
                    print(dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip'].keys())
                    if 'Cisco-IOS-XE-ospf:router-ospf' in dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip'].keys():
                        intName = '{}{}'.format(intf, dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['name'])
                        data['ospf']['interfaces'].update({intName : {}})
                        dataOspf=dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip']['Cisco-IOS-XE-ospf:router-ospf']['ospf']
                        print(dataOspf)
                        data['ospf']['interfaces'][intName]['area'] = dataOspf['process-id'][0]['area'][0]['area-id']
                        data['ospf']['interfaces'][intName]['helloTimer'] = dataOspf['hello-interval']
                        data['ospf']['interfaces'][intName]['coste'] = dataOspf['cost']
                        data['ospf']['interfaces'][intName]['deadTimer'] = dataOspf['dead-interval']
                        data['ospf']['interfaces'][intName]['priority'] = dataOspf['priority']

            response = requests.get(self.baseUrl + "Cisco-IOS-XE-native:native/router/router-ospf" , auth=self.auth,
                                        headers=self.connection, verify=True)
            dataResponse = json.loads(response.text)
            if 'ospf' in dataResponse['Cisco-IOS-XE-ospf:router-ospf'].keys():
                for process in range(0,len(dataResponse['Cisco-IOS-XE-ospf:router-ospf']['ospf']['process-id'])):
                    pid.append(dataResponse['Cisco-IOS-XE-ospf:router-ospf']['ospf']['process-id'][process]['id'])
                    rid.append(dataResponse['Cisco-IOS-XE-ospf:router-ospf']['ospf']['process-id'][process]['router-id'])
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
                                        rid = data['ospf']["routerId"])
                response = requests.put(self.baseUrl + 'Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospf:router-ospf/ospf/process-id={}'.format(data['ospf']['processId']),
                                        auth=self.auth,
                                        headers=self.connection,
                                        data = config, verify=False)
            for intf in data['ospf']['interfaces']:
                if data['ospf']['interfaces'][intf]:
                    match = re.match(r"([a-z]+)([0-9]+)", intf, re.I)
                    if match:
                        items = match.groups()
                        text = f1.read()
                        template = jinja2.Template(text)
                        config = template.render(pid= int(data['ospf']["processId"]),
                                                 int_name=items[0], int_num=items[1],
                                                 hello = data['ospf']['interfaces'][intf]['helloTimer'],
                                                 dead = data['ospf']['interfaces'][intf]['deadTimer'],
                                                 priority = data['ospf']['interfaces'][intf]['priority'],
                                                 cost = int(data['ospf']['interfaces'][intf]['coste']),
                                                 area =  data['ospf']['interfaces'][intf]['area'])
                        requests.delete(self.baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}/ip/router-ospf'.format(items[0], items[1]), auth=self.auth,headers=self.connection, verify=False)

                        response = requests.put(self.baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}'.format(items[0], items[1]),
                                                auth=self.auth,
                                                headers=self.connection,
                                                data = config, verify=False)
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
            return "Necesitas configurar la interfaz primero para activar VRRP", 500
