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
                                     look_for_keys=False, timeout=3)

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

        try:
            netconf_reply = self.connection.edit_config(target='candidate', config=config_netconf)
            print(netconf_reply)
            self.connection.commit()
            return 201
        except:
            return 404

    def getInterfacesList(self):
        try:
            data = {'interfaces': []}
            res = self.connection.command('show interfaces' , format='xml')
            #hola = ET.fromstring(res)
            data_xml = xmltodict.parse(str(res))

            for key in data_xml['rpc-reply']['interface-information']['physical-interface']:
                data['interfaces'].append(key['name'])

            return json.dumps(data), 201
        except:
            return {}, 404


    def getOspfData(self):
        data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}
        get_filter = """
            <configuration>
                <routing-options>
                </routing-options>
                <protocols>
                    <ospf>
                    </ospf>
                </protocols>
            </configuration>
        """
        try:
            nc_get_reply = self.connection.get(('subtree', get_filter))
            print (nc_get_reply)
            dict =  xmltodict.parse(str(nc_get_reply))
            if 'router-id' in dict['rpc-reply']['data']['configuration']['routing-options']:
                data['ospf']['routerId'] = dict['rpc-reply']['data']['configuration']['routing-options']['router-id']
                data['ospf']['processId'] = '0'
                for intf in dict['rpc-reply']['data']['configuration']['protocols']['ospf']['area']:
                    data['ospf']['interfaces'].update({intf['interface']['name']: {}})
                    intName = intf['interface']['name']
                    data['ospf']['interfaces'][intName]['area'] = intf['name'].split('.')[3]
                    data['ospf']['interfaces'][intName]['helloTimer'] =intf['interface']['hello-interval']
                    data['ospf']['interfaces'][intName]['coste'] = intf['interface']['metric']
                    data['ospf']['interfaces'][intName]['deadTimer'] = intf['interface']['dead-interval']
                    data['ospf']['interfaces'][intName]['priority'] = intf['interface']['priority']

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
            return "Error al crear VLANs, no puede haber dos Vlans con el mismo prefijo de red", 404


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
            return '{}'.format(e), 404

    def createVrrp(self, data):
        try:
             f = open('Templates/JunosOS/junos_vrrp.j2')
             text = f.read()
             intName = list(data['vrrp'].keys())[0]
             print(data)
             get_filter = """
             <configuration>
                 <interfaces>

                 </interfaces>
             </configuration>
             """
             nc_get_reply = self.connection.get(('subtree', get_filter))

             ip_int = ""
             dict_int = xmltodict.parse(str(nc_get_reply))

             for intf in dict_int['rpc-reply']['data']['configuration']['interfaces']['interface']:

                if intf['name'] == intName:
                    ip_int = intf['unit']['family']['inet']['address']['name']
                    template = jinja2.Template(text)
                    config_netconf = template.render(int_name=intName, ip_int=ip_int,
                                             group=data['vrrp'][intName]['grupo'], priority=data['vrrp'][intName]['priority'],
                                             preempt=data['vrrp'][intName]['preempt'], virtual_ip=data['vrrp'][intName]['ipVrrp'])
                    print(config_netconf)
                    netconf_reply = self.connection.edit_config(target='candidate', config=config_netconf)
                    print(netconf_reply)
                    self.connection.commit()
                    return "VRRP configurado correctamente en {}".format(self.name), 201

        except Exception as e:
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
            return 'Las interfaces seleccionadas no son compatibles con LACP'

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
                try:
                    nom = intf.find('./name').text
                    adminStatus = intf.find('./logical-interface/admin-status').text
                    proStatus = intf.find('./logical-interface/oper-status').text
                    ip = "-"
                    try:
                        ip = intf.find('./logical-interface/address-family/interface-address/ifa-local').text
                    except:
                        pass
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
                    'interface': intf['interface'][0]['data'],
                    'group': intf['group'][0]['data'],
                    'state': intf['vrrp-state'][0]['data'],
                    'time': intf['advertisement-timer'][0]['data'],
                    'master_ip': intf['master-router'][0]['data'],
                    'group_ip': intf['preempt-hold'][0]['vip'][0]['data']
                }
                showVrrp.append(data)
            return showVrrp
        except Exception as e:
            return []
