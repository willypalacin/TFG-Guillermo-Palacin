from Device import Device
from netmiko import ConnectHandler
import jinja2, json

class IOSRouter(Device):
    def __init__(self, name, ip, type, username, password, port):
        Device.__init__(self, name, ip, type, username, password, port)


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
            connection = ConnectHandler(host = self.ip, username=self.username,
                                        password=self.password,
                                        device_type = self.type,
                                        port=self.port)
            self.connection = connection
            return 201
        except:
            return 404

    def editInterface(self, int_name, desc, ip, mask):
        self.connection.enable()
        #self.connection.config_mode('config t')
        #cmd = ['int Loopback 834', 'ip address 1.1.1.1 255.255.255.255']
        f = open('Templates/cisco_ios.tmpl')
        text = f.read()
        template = jinja2.Template(text)
        config = template.render(int_name=int_name,
                                 name=self.name, ip=ip,
                                 mask=mask, description=desc).split('\n')
        print ("CONFIG: \n: {}".format(config))
        output = self.connection.send_config_set(config)
        print('\nConfiguration applied: \n\n' + output)

    def getInterfacesList(self):
        try:
            self.connection.enable()
            output = self.connection.send_command('show ip interface brief').split('\n')
            data = {'interfaces': []}
            for i in range (1, len(output)):
                data['interfaces'].append(output[i].split(" ")[0])
            return data, 201
        except:
            return {}, 404
