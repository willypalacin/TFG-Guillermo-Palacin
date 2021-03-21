from tkinter import *
from Vista.AddDeviceView import AddDeviceView
from Vista.DeviceConfigView import DeviceConfigView
from Vista.DeviceConfigRoutingView import DeviceConfigRoutingView
from Vista.MainView import MainView
import requests, json
import yaml
from Modelo.Device import Device
from Vista.DeviceConfigInterfacesView import DeviceConfigInterfacesView

BASE = "http://127.0.0.1:5000/"

class MainViewController:

    def __init__(self):
        self.dispositivos = {}
        self.mainView = MainView(self)
        self.mainView.mainloop()


    def clickedAddDevice(self, window):
        #DeviceConfigRoutingView(window, self, "R1", ["GigabitEthernet1", "GigabitEthernet2"])
        AddDeviceView(self, window)



    def addNewDevice(self, window,data):
        window.statusLabel.pack()
        window.statusLabel.config(fg="black", text = "Estableciendo conexion...")
        response = requests.post(BASE + "device/{}".format(data["name"]), data)
        if response.status_code == 201:
            self.dispositivos[data["name"]] = data
            self.mainView.paintDevice(data["name"])
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            window.statusLabel.config(fg="red", text = "No se ha encontrado dispositivo")
            self.mainView.addMessageToConsole(response.content, "Red")

    def clickedConfigurationDevice(self, window, event, name):
        DeviceConfigView(self, window, name)
        #print("HOLQ")
    def clickedDeviceRouting(self, window, name):
        interfaces = self.getInterfacesList(name)
        dataOspf = self.getOspfData(name)


        DeviceConfigRoutingView(window, self, name, interfaces['interfaces'], dataOspf)

    def createInterface(self, window, name, data):
        response = requests.put(BASE + "device/{}/interfaces/interface".format(name), json.dumps(data))
        if(response.status_code == 200):
            print("Config aplicada correctamente")
            window.destroy()
    def getInterfacesList(self, name):
        response = requests.get(BASE + "device/{}/interfaces/list".format(name))
        print (json.loads(response.content))
        return json.loads(response.content)

    def getOspfData(self, name):
        response = requests.get(BASE + "device/{}/protocols/ospf".format(name))
        return response.content

    def createRouting(self ,window, data, name):
        response = requests.put(BASE + "device/{}/protocols/ospf".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")



















#data = [{"likes": 100, "name": "jose mari", "views": 1000}, {"likes": 98, "name": "Antonio", "views": 1000},{"likes": 75, "name": "Puri", "views": 1000},
#{"likes": 2345, "name": "Jose", "views": 1000}]
