from netmiko import ConnectHandler
import jinja2
from abc import ABC, abstractmethod


class Device(ABC):
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

    @abstractmethod
    def checkConnectivity(self):
        pass
    @abstractmethod
    def editInterface(self, int_name, desc, ip, mask):
        pass



        #print(type(connection))
