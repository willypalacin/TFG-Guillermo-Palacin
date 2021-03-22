from Device import Device
from netmiko import ConnectHandler
import jinja2, json
import requests

class IOSRouter(Device):
    def __init__(self, name, ip, type, username, password, port):
        Device.__init__(self, name, ip, type, username, password, port)
        self.baseUrl = "https://{}:{}/restconf/data/".format(ip, port)
        self.connection = {
          'Accept': 'application/yang-data+json',
          'Content-Type': 'application/yang-data+json',
          'Authorization': 'Basic Y2lzY286Y2lzY29fMTIzNCE='
        }
        self.auth=('developer', 'C1sco12345')

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
        self.connection.enable()
        #self.connection.config_mode('config t')
        #cmd = ['int Loopback 834', 'ip address 1.1.1.1 255.255.255.255']


        headers = {
          'Accept': 'application/yang-data+json',
          'Content-Type': 'application/yang-data+json',
          'Authorization': 'Basic Y2lzY286Y2lzY29fMTIzNCE='
        }


        data = {'interfaces': []}

        #dataResponse = json.loads(response.text)
        f = open('/Templates/CiscoIOS/cisco_interfaces.j2')
        text = f.read()
        template = jinja2.Template(text)
        config = template.render(int_name=int_name,
                                 ip=ip,
                                 mask=mask, description=desc)

        response = requests.put(url + "ietf-interfaces:interfaces/interface={}".format(int_name),
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

    def createOspf(self, data):
        f = open('Templates/CiscoIOS/cisco_ospf.j2')
        text = f.read()
        template = jinja2.Template(text)
        config = template.render(pid= data['ProcessId'],
                                 rid=data['RouterId'],
                                 interfaces=data['interfaces']).split('\n')
        output = self.connection.send_config_set(config)
        if '%' in output:
            start = output.find("%")
            substring = output[start:start+60]
            return substring, 404
        else:
            return 'OSPF configurado correctamentamente en {}'.format(self.name), 201
