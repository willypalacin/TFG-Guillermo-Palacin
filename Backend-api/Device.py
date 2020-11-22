from netmiko import ConnectHandler
import jinja2


class Device():
    def __init__(self, name, ip, type, username, password, port):
        self.name = name
        self.ip = ip
        self.type = type
        self.username = username
        self.password = password
        self.port = port
        self.connection = None


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

    def createLoopbackTesting(self, ip, mask, name, int_name):
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


        #print(type(connection))
