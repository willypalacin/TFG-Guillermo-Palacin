from Device import Device
from ncclient import manager
import jinja2, json
from netaddr import IPAddress
import xmltodict

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
            res = self.connection.command('show interfaces ge-0/0/* terse' , format='xml')
            #hola = ET.fromstring(res)
            data_xml = xmltodict.parse(str(res))

            for key in data_xml['rpc-reply']['interface-information']['physical-interface']:
                data['interfaces'].append(key['name'])

            return json.dumps(data), 201
        except:
            return {}, 404

    def createOspf(self, data):
        try:
            f = open('Templates/JunosOS/junos_ospf.j2')
            text = f.read()
            template = jinja2.Template(text)
            netconf_data = template.render(rid = data["RouterId"], interfaces=data["interfaces"])
            netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
            self.connection.commit()
            return 'OSPF Configurado correctamente en {}'.format(self.name), 201
        except Exception as e:
            return '{}'.format(e), 404
