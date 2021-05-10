from Device import Device
import json, pyeapi
import yaml
from netaddr import IPAddress
import datetime
import re


class AristaSwitch(Device):
    def __init__(self, name, ip, type, username, password, port):
        Device.__init__(self, name, ip, type, username, password, port)

    def checkConnectivity(self):
        print(type(self.ip))
        print('{} {} {} {} {} '.format(self.ip, self.port, self.username, self.password, self.name))
        try:
            eapi_param = pyeapi.client.connect(
                transport='https',
                host=self.ip,
                username=self.username,
                password=self.password,
                port=443,
                timeout=2
            )
            eapi = pyeapi.client.Node(eapi_param)
            self.connection = eapi
            return 201, "Dispositivo {} anadido satisfactoriamente".format(self.name)
        except Exception:
            return 404, "No se ha encontrado ningun dispositivo con IP {}".format(self.ip)


    def editInterface(self, int_name, desc, ip, mask):
        try:
            maskBits = IPAddress(mask).netmask_bits()
            if "vlan" not in int_name.lower():
                command = self.connection.run_commands(['enable', 'configure', 'interface {}'.format(int_name), 'no switchport',
                                                    'ip address {}/{}'.format(ip, maskBits),
                                                    'description {}'.format(desc)])
            else:
                command = self.connection.run_commands(['enable', 'configure', 'interface {}'.format(int_name),
                                                    'ip address {}/{}'.format(ip, maskBits),
                                                    'description {}'.format(desc)])
            return "Interfaz {} configurada correctamente en {}".format(int_name, self.name), 201

        except:
                return "Error al configurar Interfaz en {} ".format(self.name), 404




    def getInterfacesList(self):
        try:
            #version_info = eapi.run_commands(['enable', 'configure', 'interface Loopback11', 'ip address 1.2.2.2/24'])
            interfaces = self.connection.run_commands(['enable', 'show ip interface brief'])[1]['interfaces']
            data = {'interfaces': []}
            for key in interfaces:
                if key != 'defaults':
                    data['interfaces'].append(key)

            return json.dumps(data), 201

        except Exception:
            return {}, 404

    def getOspfData(self):
        data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}
        try:
            response = self.connection.run_commands('show ip ospf')
            if response[0]['vrfs'] != {}:
                data['ospf']['processId'] = str((list(response[0]['vrfs']['default']['instList'].keys())[0]))
                data['ospf']['routerId']= response[0]['vrfs']['default']['instList'][data['ospf']['processId']]['routerId']
                response = self.connection.run_commands('show ip ospf interface')
                #if response[0]['vrfs']:
                #data['ospf']['interfaces'].update({self.currentInterface: {}})
                for intf in response[0]['vrfs']['default']['instList'][data['ospf']['processId']]['interfaces']:
                    dataInterfaz= response[0]['vrfs']['default']['instList'][data['ospf']['processId']]['interfaces'][intf]
                    data['ospf']['interfaces'].update({intf: {}})
                    data['ospf']['interfaces'][intf]['ip'] = dataInterfaz['interfaceAddress']
                    data['ospf']['interfaces'][intf]['mask'] = dataInterfaz['interfaceMask']
                    data['ospf']['interfaces'][intf]['coste'] = dataInterfaz['cost']
                    data['ospf']['interfaces'][intf]['priority'] = dataInterfaz['priority']
                    data['ospf']['interfaces'][intf]['deadTimer'] = dataInterfaz['helloInterval']
                    data['ospf']['interfaces'][intf]['helloTimer'] = dataInterfaz['deadInterval']
                    data['ospf']['interfaces'][intf]['area'] = dataInterfaz['area']

            return yaml.dump(data, default_flow_style=False), 201
                    #data['ospf']['routerId']= response[0]['vrfs']['default']['instList'][str(pid)]
        except Exception as e:
            print("DEVUELVE ESTO")
            return yaml.dump(data, default_flow_style=False), 404


    def createOspf(self, data):

        try:
            response = self.connection.run_commands('show ip ospf')
            if response[0]['vrfs'] != {}:
                pid= int(list(response[0]['vrfs']['default']['instList'].keys())[0])
                self.connection.run_commands(['enable', 'configure', 'no router ospf {}'.format(pid)])

            commands = ['enable', 'configure', 'router ospf {}'.format(data['ospf']['processId']), 'router-id {}'.format(data['ospf']['routerId'])]
            for intf in data['ospf']['interfaces']:
                if data['ospf']['interfaces'][intf]:
                    commands.append('interface {}'.format(intf))
                    commands.append('ip ospf area {}'.format(data['ospf']['interfaces'][intf]['area']))
                    commands.append('ip ospf cost {}'.format(data['ospf']['interfaces'][intf]['coste']))
                    commands.append('ip ospf hello-interval {}'.format(data['ospf']['interfaces'][intf]['helloTimer']))
                    commands.append('ip ospf dead-interval {}'.format(data['ospf']['interfaces'][intf]['deadTimer']))
                    commands.append('ip ospf dead-interval {}'.format(data['ospf']['interfaces'][intf]['priority']))
            ospf_creation = self.connection.run_commands(commands)
            return "El proceso OSPF se ha creado correctamente en {}".format(self.name), 201
        #print (ospf_creation)
        except Exception as e:
            return '{}'.format(e), 404
    def createVlans(self, data):
        try:
            commands = ["enable", "configure"]
            if data['vlanId']:
                commands.append("vlan {}".format(data['vlanId']))
                if data['vlanNom']:
                    commands.append("name {}".format(data['vlanNom']))
                else:
                    commands.append("name Vlan{}".format(data['vlanId']))
            if data['layer3']:
                if data['layer3']['ip']:
                    commands.append("interface vlan {}".format(data['vlanId']))
                    commands.append("ip address {}".format(data['layer3']['ip']))
                    commands.append("no shutdown".format(data['layer3']['ip']))
            vlan = self.connection.run_commands(commands)
            return "VLANs Creadas correctamente en {}".format(self.name), 201
        except Exception as e:
            return '{}'.format(e), 404

    def createPortChannel(self, data):
        try:
            commands = ['enable', 'configure']
            commands.append('interface port-channel {}'.format(data['numPortChannel'], 'exit'))
            for intf in data['interfaces']:
                commands.append("interface {}".format(intf))
                commands.append("channel-group {} mode {}".format(data['numPortChannel'], data['mode']))
                commands.append("exit")
            createPortChannel = self.connection.run_commands(commands)
            return "LACP configurado correctamente en {}".format(self.name), 201
        except Exception as e:
            return '{}'.format(e), 404

    def createSwitchPort(self, data):
        try:
            commands = ['enable', 'configure']
            for intf in data:
                commands.append("interface {}".format(intf))
                commands.append("switchport")
                commands.append("switchport mode {}".format(data[intf]['mode']))
                if "access" in data[intf]['mode']:
                    commands.append("switchport access vlan {} ".format(data[intf]['vlans']))
                else:
                    commands.append("switchport trunk allowed vlan {} ".format(data[intf]['vlans']))
            createL2int = self.connection.run_commands(commands)
            return "Enlace configurado correctamente", 201
        except Exception as e:
            return '{}'.format(e), 404

    def createStaticRouting(self, data):
        try:
            commands = ["enable", "configure"]
            string = ""
            if data['intf']:
                if data['metric']:
                    string = "ip route {} {} metric {}".format(data['red'], data['intf'] , data['metric'])
                else:
                    string = "ip route {} {}".format(data['red'], data['intf'])
            else:
                if data['gw']:
                    if data['metric']:
                        string = "ip route {} {} metric {}".format(data['red'], data['gw'] , data['metric'])
                    else:
                        string = "ip route {} {}".format(data['red'], data['gw'])
            commands.append(string)
            response = self.connection.run_commands(commands)
            return "Ruta creada correctamente en {}".format(self.name), 201
            #print (ospf_creation)
        except Exception as e:
            return "{}".format(e), 404



    def createAcl(self, data):
        commands = ["enable", "configure"]
        print(data)
        try:
            inout = "in"
            string = ""
            for rule in data:
                if data[rule]['rule']['num'] != '':
                    if "accept" in data[rule]['rule']['action']:
                        data[rule]['rule']['action']  = "permit"
                    if "discard" in data[rule]['rule']['action']:
                        data[rule]['rule']['action']  = "deny"
                    if data[rule]['rule']['protocol'] == '':
                        data[rule]['rule']['protocol'] = 'ip'
                    if data[rule]['rule']['protocol'] == '' and data[rule]['rule']['destAddr'] == '' and data[rule]['rule']['destPort'] == '':
                        commands.append("ip access-list standard {}".format(rule))
                        commands.append('{} {} {}'.format(data[rule]['rule']['num'], data[rule]['rule']['action'], data[rule]['rule']['sourceAddr']))
                    else:
                        commands.append("ip access-list {}".format(rule))
                        string = '{} {} {} {} {}'.format(data[rule]['rule']['num'], data[rule]['rule']['action'], data[rule]['rule']['protocol'],data[rule]['rule']['sourceAddr'], data[rule]['rule']['destAddr'])
                        if "ip" not in  data[rule]['rule']['protocol']:
                            string = string + " eq " +  data[rule]['rule']['destPort']
                        commands.append(string)

                if data[rule]['interfaz']['nombre'] != '':
                    commands.append("interface {}".format(data[rule]['interfaz']['nombre']))
                    if "output" in data[rule]['interfaz']['apply']:
                        inout = "out"
                    commands.append("ip access-group {} {}".format(rule, inout))
                createAcl = self.connection.run_commands(commands)
                return "ACL creada correctamente en {}".format(self.name), 201
        except Exception as e:
            return "Error al crear ACL en {}".format(self.name), 404


    def createVrrp(self, data):
        try:
            commands = ['enable', 'configure']
            for intf in data['vrrp']:
              commands.append("interface {}".format(intf))
              commands.append("vrrp {} priority-level {}".format(data['vrrp'][intf]['grupo'], data['vrrp'][intf]['priority']))
              commands.append("vrrp {} ipv4 {}".format(data['vrrp'][intf]['grupo'], data['vrrp'][intf]['ipVrrp']))
              print(data)
              if data['vrrp'][intf]['preempt'] != 0:
                   commands.append("vrrp {} {}".format(data['vrrp'][intf]['grupo'], 'preempt'))
              print(commands)
              creationVrrp = self.connection.run_commands(commands)
              return "VRRP configurado correctamente en {}".format(self.name), 201
        except Exception as e:
         return "Necesitas configurar la interfaz primero para activar VRRP", 404

    def showInterfaces(self):
        try:
            interfaces = self.connection.run_commands(['enable', 'show interfaces'])[1]['interfaces']
            showInterfaces = []

            for intf in interfaces:
                ip = '-'
                print(intf)
                if interfaces[intf]['interfaceAddress'] != []:
                    if "primaryIp" in interfaces[intf]['interfaceAddress'][0].keys():
                        ip = interfaces[intf]['interfaceAddress'][0]['primaryIp']['address']
                data = {
                        'nombre': intf,
                        'adminStatus' : interfaces[intf]['interfaceStatus'],
                        'proStatus' : interfaces[intf]['lineProtocolStatus'],
                        'ip':ip
                    }
                showInterfaces.append(data)
            return showInterfaces
        except:
            return []

    def showIpRoute(self):
        try:
            ipRoutes = self.connection.run_commands(['enable', 'show ip route'])[1]

            showIpRoute = []

            for route in ipRoutes['vrfs']['default']['routes']:
                data = {}
                for via in ipRoutes['vrfs']['default']['routes'][route]['vias']:
                    data['protocolo'] = ipRoutes['vrfs']['default']['routes'][route]['routeType']
                    data['gateway_if'] = via['interface']
                    if 'nexthopAddr' in via.keys():
                        data['gateway'] = via['nexthopAddr']
                    else:
                        data['gateway'] = ''
                    data['red'] = route
                    if 'preference' in ipRoutes['vrfs']['default']['routes'][route].keys():
                        data['distancia'] = ipRoutes['vrfs']['default']['routes'][route]['preference']
                    else:
                        data['distancia'] = ''
                    if 'metric' in ipRoutes['vrfs']['default']['routes'][route].keys():
                        data['metrica'] =  ipRoutes['vrfs']['default']['routes'][route]['metric']
                    else:
                        data['metrica'] = ''


                    showIpRoute.append(data)

            return showIpRoute
        except:
            return {}

    def showOspfNeigh(self):
        showOspfNeigh = []
        try:
            ospfNeigh = self.connection.run_commands(['enable', 'show ip ospf neighbor'])[1]
            print
            for neigh in ospfNeigh['vrfs']['default']['instList']:
                for entry in ospfNeigh['vrfs']['default']['instList'][neigh]['ospfNeighborEntries']:
                    data = {'neighbor_id': entry['routerId'],
                            'priority': entry['priority'],
                            'state': '{}/{}'.format(entry['adjacencyState'].upper(), entry['drState']),
                            'dead_time': datetime.datetime.fromtimestamp(entry['inactivity']).strftime('%S'),
                            'address': entry['interfaceAddress'],
                            'interface': entry['interfaceName']
                    }
                    showOspfNeigh.append(data)
            return showOspfNeigh
        except Exception as e:
            return []
    def showVlan(self):
        try:
            vlanShow = self.connection.run_commands(['enable', 'show vlan'])[1]
            showVlan = []
            for vlan in vlanShow['vlans']:
                data = {
                    'vlan_id': vlan,
                    'name': vlanShow['vlans'][vlan]['name'],
                    'status': vlanShow['vlans'][vlan]['status'],
                    'interfaces': []
                }
                for intf in vlanShow['vlans'][vlan]['interfaces']:
                    data['interfaces'].append(intf)
                showVlan.append(data)
            return showVlan
        except Exception as e:
            return []

    def showOspfIntf(self):
        try:
            showOspfRun = self.connection.run_commands(['enable', 'show ip ospf interface brief'])[1]
            showOspf= []
            for instance in showOspfRun['vrfs']['default']['instList']:
                for intf in showOspfRun['vrfs']['default']['instList'][instance]['interfaces']:
                    data = {
                            'interface': intf,
                            'area': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['area'],
                            'ip_address_mask': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['interfaceAddress'],
                            'cost': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['cost'],
                            'state': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['state'],
                            'neighbors_fc': '0/0'
                    }
                    showOspf.append(data)
            return showOspf
        except Exception as e:
            return []

    def showVrrp(self):
        try:
            showVrrpRun = self.connection.run_commands(['enable', 'show vrrp'])[1]
            showVrrp= []
            for vr in showVrrpRun['virtualRouters']:
                data = {
                    'interface': vr['interface'],
                    'group': vr['groupId'],
                    'state': vr['state'],
                    'time': vr['skewTime'],
                    'master_ip': vr['masterAddr'],
                    'group_ip': vr['virtualIp']
                }
                showVrrp.append(data)
            return showVrrp
        except:
            return []
