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
            print("HOLA")
            eapi = pyeapi.client.Node(eapi_param)
            self.connection = eapi
            return 201
        except Exception:
            return 404


    def editInterface(self, int_name, desc, ip, mask):
        maskBits = IPAddress(mask).netmask_bits()
        command = self.connection.run_commands(['enable', 'configure', 'interface {}'.format(int_name),
                                                'ip address {}/{}'.format(ip, maskBits),
                                                'description {}'.format(desc)])
        print(command)
