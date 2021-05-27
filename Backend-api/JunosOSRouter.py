from Device import Device
from ncclient import manager
import jinja2, json
from netaddr import IPAddress
import xmltodict
import yaml
from jnpr.junos import Device as Dev
from lxml import etree
import json
import jxmlease

class JunosOSRouter(Device):
    def __init__(self, name, ip, type, username, password, port):
        Device.__init__(self, name, ip, type, username, password, port)


    def checkConnectivity(self):
        try:
            connection = manager.connect(host=self.ip, port=int(self.port),
                                     username=self.username, password=self.password, hostkey_verify=False,
                                     device_params={'name': 'junos'}, allow_agent=False,
                                     look_for_keys=False, timeout=15)

            self.connection = connection
            self.pyez = Dev(host=self.ip, user=self.username, passwd=self.password, port=int(self.port))
            self.pyez.open()

            print("HOLA")
            return 201, "Dispositivo {} anadido satisfactoriamente".format(self.name)
        except:
            return 404, "No se ha encontrado ningun dispositivo con IP {}".format(self.ip)

    def editInterface(self, int_name, desc, ip, mask):
        maskBits = IPAddress(mask).netmask_bits()
        f = open('Templates/JunosOS/junos_interface.j2')
        text = f.read()
        template = jinja2.Template(text)
        config_netconf = template.render(int_name=int_name, ip=ip,
                                 mask=maskBits, description=desc)
        print(config_netconf)

        try:
            netconf_reply = self.connection.edit_config(target='candidate', config=config_netconf)
            print(netconf_reply)
            print(self.connection.commit())
            return "Interfaz {} configurada correctamente en {}".format(int_name, self.name), 201
        except:
            return "Error al configurar Interfaz en {} ".format(self.name), 404

    def getInterfacesList(self):
        try:
            data = {'interfaces': []}
            res = self.connection.command('show interfaces' , format='xml')
            #hola = ET.fromstring(res)
            data_xml = xmltodict.parse(str(res))

            for key in data_xml['rpc-reply']['interface-information']['physical-interface']:
                data['interfaces'].append(key['name'])
            print(data_xml)
            return json.dumps(data), 201
        except:
            return {}, 404


    def getOspfData(self):
        data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}
        try:
            rpc = self.pyez.rpc.get_ospf_interface_information({'format':'json'}, extensive=True)
            for intf in rpc['ospf-interface-information'][0]['ospf-interface']:
                intName = intf['interface-name'][0]['data']
                data['ospf']['interfaces'].update({intName:{}})
                data['ospf']['interfaces'][intName]['area'] = intf['ospf-area'][0]['data']
                data['ospf']['interfaces'][intName]['priority'] = intf['router-priority'][0]['data']
                data['ospf']['interfaces'][intName]['coste'] = intf['interface-cost'][0]['data']
                data['ospf']['interfaces'][intName]['ip'] = intf['interface-address'][0]['data']
                data['ospf']['interfaces'][intName]['helloTimer'] = intf['hello-interval'][0]['data']
                data['ospf']['interfaces'][intName]['deadTimer'] = intf['dead-interval'][0]['data']

            return yaml.dump(data, default_flow_style=False), 201
        except Exception as e:
            return yaml.dump(data, default_flow_style=False), 404


    def createVlans(self,data):
        try:
            f = open('Templates/JunosOS/junos_vlan_interface.j2')
            text = f.read()
            template = jinja2.Template(text)
            netconf_data = template.render(vlan_id = data['vlanId'], vlan_name=data['vlanNom'], ip= data['layer3']['ip'])
            #print(netconf_data)
            netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
            self.connection.commit()
            return "VLANs creadas correctamente en {}".format(self.name), 201

        except Exception as e:
            return "{}".format(e), 404

    def createStaticRouting(self, data):
        try:
            f = open('Templates/JunosOS/junos_static_routing.j2')
            text = f.read()
            template = jinja2.Template(text)
            netconf_data = template.render(ip=data['red'], gw = data['gw'], metric=data['metric'])
            netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
            self.connection.commit()
            return "Ruta creada correctamente en {}".format(self.name), 201
        except Exception as e:
            self.connection.rollback(rollback=0)
            self.connection.commit()
            return "{}".format(e), 404


    def createOspf(self, data):
        try:
            f = open('Templates/JunosOS/junos_ospf.j2')
            text = f.read()
            template = jinja2.Template(text)
            netconf_data = template.render(rid = data['ospf']["routerId"], interfaces=data['ospf']["interfaces"])
            print(netconf_data)
            netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
            self.connection.commit()
            return 'OSPF Configurado correctamente en {}'.format(self.name), 201
        except Exception as e:
            netconf_reply =  self.connection.rollback(rollback=0)
            self.connection.commit()
            return '{}'.format(e), 404

    def createVrrp(self, data):
        try:
             f = open('Templates/JunosOS/junos_vrrp.j2')
             text = f.read()
             interfaces = self.showInterfaces()
             intName = list(data['vrrp'].keys())[0]
             for intf in interfaces:
                 print("NOMBRE: " + intf['nombre'])
                 print("intName: " + intName)
                 print("ip: " + intf['ip'])
                 print("\n\n")
                 if intf['nombre'] == intName:
                     template = jinja2.Template(text)
                     config_netconf = template.render(int_name=intName, ip_int=intf['ip'],
                                                     group=data['vrrp'][intName]['grupo'], priority=data['vrrp'][intName]['priority'],
                                                     preempt=data['vrrp'][intName]['preempt'], virtual_ip=data['vrrp'][intName]['ipVrrp'])
                     print(config_netconf)
                     netconf_reply = self.connection.edit_config(target='candidate', config=config_netconf)
                     print(netconf_reply)
                     self.connection.commit()
                     return "VRRP configurado correctamente en {}".format(self.name), 201

        except Exception as e:
            print(e)
            netconf_reply =  self.connection.rollback(rollback=0)
            self.connection.commit()
            return "Necesitas configurar la interfaz primero para activar VRRP", 404

    def createPortChannel(self, data):
        try:
            f = open('Templates/JunosOS/junos_port_channel.j2')
            text = f.read()
            template = jinja2.Template(text)
            vlans = []
            netconf_data = template.render(num_pc = data['numPortChannel'], mode=data['mode'], interfaces=data['interfaces'])
            print(netconf_data)
            netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
            self.connection.commit()
            return "LACP configurado correctamente en {}".format(self.name), 201

        except Exception as e:
            return 'Las interfaces seleccionadas no son compatibles con LACP', 404

    def createSwitchPort(self, data):
        try:
            print(data)
            f = open('Templates/JunosOS/junos_interfaz_n2.j2')
            text = f.read()
            template = jinja2.Template(text)
            vlans = []
            for intf in data:
                if data[intf]['vlans'] != '':
                    if "-" in data[intf]['vlans']:
                        aux = data[intf]['vlans'].split("-")
                        for i in range(int(aux[0]), int(aux[1])+1):
                            vlans.append(i)
                    else:
                        if "," in data[intf]['vlans']:
                            vlans = data[intf]['vlans'].split(",")
                        else:
                            if data[intf]['vlans'] != '':
                                vlans.append(data[intf]['vlans'])
                netconf_data = template.render(intf = intf.split(".")[0], mode=data[intf]['mode'], vlans = vlans)
                netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
            self.connection.commit()
            return "Enlace creado correctamente", 201
        except Exception as e:
            netconf_reply =  self.connection.rollback(rollback=0)
            self.connection.commit()
            return "{}".format(e), 404

    def createAcl(self, data):
        try:
            f = open('Templates/JunosOS/junos_acl.j2')
            text = f.read()
            template = jinja2.Template(text)
            for rule in data:
                netconf_data = template.render(nombre_acl = rule,
                                               num=data[rule]['rule']['num'],
                                               sa=data[rule]['rule']['sourceAddr'],
                                               da=data[rule]['rule']['destAddr'],
                                               protocol=data[rule]['rule']['protocol'],
                                               action = data[rule]['rule']['action'],
                                               dest_port=data[rule]['rule']['destPort'],
                                               intf= data[rule]['interfaz']['nombre'],
                                               inout=data[rule]['interfaz']['apply'])
                netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
                self.connection.commit()
                return "ACL creada correctamente en {}".format(self.name), 201

        except Exception as e:
            netconf_reply =  self.connection.rollback(rollback=0)
            self.connection.commit()
            return '{}'.format(e), 404



    def showInterfaces(self):
        try:
            rpc = self.pyez.rpc.get_interface_information(terse=True, normalize=True)
            rpc_xml = etree.tostring(rpc, pretty_print=True, encoding='unicode')
            interfaces = rpc.findall('.//physical-interface')
            showInterfaces = []

            for intf in interfaces:
                logicalIntf = intf.findall('./logical-interface')
                for intfLog in logicalIntf:
                    nom = intfLog.find('./name').text
                    adminStatus = intfLog.find('./admin-status').text
                    proStatus = intfLog.find('./oper-status').text
                    ip = "-"
                    try:
                        ip = intfLog.find('./address-family/interface-address/ifa-local').text
                        data = {
                                'nombre': nom,
                                'adminStatus' : adminStatus,
                                'proStatus' : proStatus,
                                'ip' : ip,
                        }
                        showInterfaces.append(data)
                    except:
                        pass

            return showInterfaces
        except:
            return {}

    def showIpRoute(self):
        try:
            showIpRoute = []

            #showIpRoute.append(data)
            rpc = self.pyez.rpc.get_route_information({'format':'json'})
            #rpc_xml = etree.tostring(rpc, pretty_print=True, encoding='unicode')
            for route in rpc['route-information'][0]['route-table']:
                for rt in route['rt']:
                    data = {
                            'protocolo' : '',
                            'red' : '',
                            'distancia': '',
                            'metrica': '',
                            'gateway': '',
                            'gateway_if': ''
                    }
                    data['red'] = rt['rt-destination'][0]['data'] #red
                    data['protocolo'] = rt['rt-entry'][0]['protocol-name'][0]['data'] #protocolo
                    if "metric" in rt['rt-entry'][0].keys():
                        data['metrica'] = rt['rt-entry'][0]['metric'][0]['data']
                    else:
                        print('')
                    if "preference" in rt['rt-entry'][0].keys():
                        data['distancia'] = rt['rt-entry'][0]['preference'][0]['data']
                    if "nh" in rt['rt-entry'][0].keys():
                        if "to" in rt['rt-entry'][0]['nh'][0].keys():
                            data['gateway'] = rt['rt-entry'][0]['nh'][0]['to'][0]['data']
                        if "via" in rt['rt-entry'][0]['nh'][0].keys():
                            data['gateway_if'] = rt['rt-entry'][0]['nh'][0]['via'][0]['data']
                    showIpRoute.append(data)
            return showIpRoute
        except:
            return {}

    def showOspfNeigh(self):
        showOspfNeigh = []
        try:
            rpc = self.pyez.rpc.get_ospf_neighbor_information({'format':'json'}, extensive=True)
            for neigh in rpc['ospf-neighbor-information'][0]['ospf-neighbor']:
                data = {
                    'neighbor_id': neigh['neighbor-id'][0]['data'],
                    'priority': neigh['neighbor-priority'][0]['data'],
                    'state':  neigh['ospf-neighbor-state'][0]['data'],
                    'dead_time': neigh['activity-timer'][0]['data'],
                    'address': neigh['neighbor-address'][0]['data'],
                    'interface': neigh['interface-name'][0]['data'] }
                showOspfNeigh.append(data)
            return showOspfNeigh
        except:
            return []


    def showVlan(self):
        try:
            rpc = self.pyez.rpc.get_vlan_information({'format':'json'})
            showVlan = []
            for vlan in rpc['l2ng-l2ald-vlan-instance-information'][0]['l2ng-l2ald-vlan-instance-group']:
                data = {
                    'vlan_id': vlan['l2ng-l2rtb-vlan-tag'][0]['data'],
                    'name': vlan['l2ng-l2rtb-vlan-name'][0]['data'],
                    'status': 'active',
                    'interfaces': []
                }
                for intf in vlan['l2ng-l2rtb-vlan-member']:
                    data['interfaces'].append(intf['l2ng-l2rtb-vlan-member-interface'][0]['data'])
                showVlan.append(data)
            return showVlan
        except:
            return []

    def showOspfIntf(self):
        try:
            showOspfInt = []
            rpc = self.pyez.rpc.get_ospf_interface_information({'format':'json'}, extensive=True)
            for intf in rpc['ospf-interface-information'][0]['ospf-interface']:
                data = {'interface': '',
                        'area': '',
                        'ip_address_mask': '',
                        'cost': '',
                        'state': '',
                        'neighbors_fc': '0/0'}
                data['interface'] = intf['interface-name'][0]['data']
                data['area'] = intf['ospf-area'][0]['data']
                data['state'] = intf['ospf-interface-state'][0]['data']
                data['cost'] = intf['interface-cost'][0]['data']
                data['ip_address_mask'] = intf['interface-address'][0]['data']
                showOspfInt.append(data)
            return showOspfInt
        except:
            return []

    def showVrrp(self):
        try:
            showVrrp = []
            rpc = self.pyez.rpc.get_vrrp_information({'format':'json'}, extensive=True)
            for intf in rpc['vrrp-information'][0]['vrrp-interface']:
                data = {
                    'interface': '',
                    'group': '',
                    'state': '',
                    'time': '',
                    'master_ip': '',
                    'group_ip': ''
                }
                if "interface" in intf.keys():
                    data['interface']=  intf['interface'][0]['data']
                if "group" in intf.keys():
                    data['group'] = intf['group'][0]['data']
                if "vrrp-state" in intf.keys():
                    data['state'] = intf['vrrp-state'][0]['data']
                if "advertisement-timer" in intf.keys():
                    data['time']=intf['advertisement-timer'][0]['data']
                if "master-router" in intf.keys():
                    data['master_ip'] = intf['master-router'][0]['data']
                if "preempt-hold" in intf.keys():
                    data['group_ip'] =  intf['preempt-hold'][0]['vip'][0]['data']
                showVrrp.append(data)
            return showVrrp
        except Exception as e:
            return []
