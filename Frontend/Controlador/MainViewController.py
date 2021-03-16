from tkinter import *
from Vista.AddDeviceView import AddDeviceView
from Vista.DeviceConfigView import DeviceConfigView
from Vista.MainView import MainView
import requests, json
from Modelo.Device import Device
from Vista.DeviceConfigInterfacesView import DeviceConfigInterfacesView

BASE = "http://127.0.0.1:5000/"

class MainViewController:

    def __init__(self):
        self.dispositivos = {}
        self.mainView = MainView(self)
        self.mainView.mainloop()


    def clickedAddDevice(self, window):
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

    def createInterface(self, window, name, data):
        response = requests.put(BASE + "device/{}/interfaces/interface".format(name), json.dumps(data))
        if(response.status_code == 200):
            print("Config aplicada correctamente")
            window.destroy()
    def getInterfacesList(self, name):
        response = requests.get(BASE + "device/{}/interfaces/list".format(name))
        print (json.loads(response.content))
        return json.loads(response.content)














#data = [{"likes": 100, "name": "jose mari", "views": 1000}, {"likes": 98, "name": "Antonio", "views": 1000},{"likes": 75, "name": "Puri", "views": 1000},
#{"likes": 2345, "name": "Jose", "views": 1000}]
