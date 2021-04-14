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
        maskBits = IPAddress(mask).netmask_bits()
        if "vlan" not in int_name.lower():
            command = self.connection.run_commands(['enable', 'configure', 'interface {}'.format(int_name), 'no switchport',
                                                'ip address {}/{}'.format(ip, maskBits),
                                                'description {}'.format(desc)])
        else:
            command = self.connection.run_commands(['enable', 'configure', 'interface {}'.format(int_name),
                                                'ip address {}/{}'.format(ip, maskBits),
                                                'description {}'.format(desc)])


        print(command)

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
            print("RESPONSEEEE")
            print(response)
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
                print("ENTRA")
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
            interfaces = self.connection.run_commands(['enable', 'show ip interface brief'])[1]['interfaces']
            showInterfaces = []
            for intf in interfaces:
                data = {
                        'nombre': intf,
                        'adminStatus' : interfaces[intf]['interfaceStatus'],
                        'proStatus' : interfaces[intf]['lineProtocolStatus'],
                        'ip' : interfaces[intf]['interfaceAddress']['ipAddr']['address'],
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
