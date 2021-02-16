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

    def getName(self):
        return self.name
    def getType(self):
        return self.type


        #print(type(connection))
