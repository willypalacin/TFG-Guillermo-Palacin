from Device import Device
import json, pyeapi
from netaddr import IPAddress


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
        command = self.connection.run_commands(['enable', 'configure', 'interface {}'.format(int_name), 'no switchport',
                                                'ip address {}/{}'.format(ip, maskBits),
                                                'description {}'.format(desc)])
        print(command)

    def getInterfacesList(self):
        try:
            #version_info = eapi.run_commands(['enable', 'configure', 'interface Loopback11', 'ip address 1.2.2.2/24'])
            interfaces = self.connection.api('interfaces').getall()
            data = {'interfaces': []}
            for key in interfaces:
                if key != 'defaults':
                    data['interfaces'].append(key)

            return json.dumps(data), 201

        except Exception:
            return {}, 404

    def createOspf(self, data):
        try:
            commands = ['enable', 'configure', 'router ospf {}'.format(data['ProcessId']), 'router-id {}'.format(data['RouterId'])]
            for intf in data['interfaces']:
                commands.append('interface {}'.format(intf))
                commands.append('ip ospf area {}'.format(data['interfaces'][intf]))
            ospf_creation = self.connection.run_commands(commands)
            return "El proceso OSPF se ha creado correctamente en {}".format(self.name), 201
        #print (ospf_creation)
        except Exception as e:
            return '{}'.format(e), 404
