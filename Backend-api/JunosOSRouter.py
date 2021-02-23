from Device import Device
from ncclient import manager
import jinja2, json
from netaddr import IPAddress

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
            print("HOLA")
            return 201
        except:
            return 404

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
