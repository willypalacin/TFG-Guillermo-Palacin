from tkinter import *
from Vista.AddDeviceView import AddDeviceView
from Vista.DeviceConfigView import DeviceConfigView
from Vista.DeviceConfigRoutingView import DeviceConfigRoutingView
from Vista.MainView import MainView
from Vista.DeviceConfigInterfacesView import DeviceConfigInterfacesView
from Vista.DeviceConfigHAView import DeviceConfigHAView
from Vista.MostrarConfigView import MostrarConfigView
from Vista.DeviceShowsView import DeviceShowsView
from Vista.DeviceConfigVlansView import DeviceConfigVlansView
from Vista.DeviceConfigPortChannelView import DeviceConfigPortChannelView
import requests, json
import yaml
from Modelo.Device import Device


BASE = "http://127.0.0.1:5000/"


class MainViewController:


    def __init__(self):
        self.dispositivos = {}
        self.mainView = MainView(self)
        self.mainView.mainloop()


    def clickedAddDevice(self, window):
        AddDeviceView(self, window)

    def showInterfacesAll(self, window):
        header =  {
            "Interfaz":"nombre",
            "IP":"ip",
            "Status_Admin":"adminStatus",
            "Protocolo":"proStatus"
        }
        response = requests.get(BASE + "devices/show/interfaces/all")
        DeviceShowsView(window, self, json.loads(response.text),header, "Visualización Interfaces", 4, 5)
        print(response.text)

    def showIpRoute(self, window):
        response = requests.get(BASE + "devices/show/ip/route")
        header =  {
            "Protocolo":"protocolo",
            "Red":"red",
            "Next_GW":"gateway",
            "Interfaz":"gateway_if",
            "Metrica":"metrica",
            "Distancia":"distancia"
        }
        DeviceShowsView(window, self, json.loads(response.text),header, "Visualización Tabla Rutas", 4, 5)
        print(response.text)

    def showOspfNeigh(self, window):
        response = requests.get(BASE + "devices/show/ospf/neighbors")
        header =  {
            "Red":"address",
            "Interfaz":"interface",
            "ID_Vecino":"neighbor_id",
            "Dead_Timer":"dead_time",
            "Estado":"state",
            "Prioridad":"priority"
        }
        DeviceShowsView(window, self, json.loads(response.text),header, "Visualización Vecinos OSPF", 4, 5)

        print(response.text)

    def showVlan(self, window):
        header = {
          'VLAN_ID': 'vlan_id',
          'Nombre': 'name',
          'Status': 'status',
          'Interfaces': 'interfaces'
        }
        response = requests.get(BASE + "devices/show/vlan")
        DeviceShowsView(window, self, json.loads(response.text),header, "Visualización VLANs", 4, 5)
        print(response.text)


    def clickedDeviceVlans(self, window,name):
        DeviceConfigVlansView(window,self, name, "blabla\nblabla")

    def clickedMostrarConfiguracion(self, window):
        MostrarConfigView(self, window)

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

    def clickedDevicePortChannel(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigPortChannelView(window, self, name,interfaces['interfaces'], "blablabla\nblabla")


    def clickedDeviceHA(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigHAView(window, self, name, interfaces['interfaces'], "blabla \n bla \n bla")

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

    def createVlans(self ,window, data, name):
        response = requests.put(BASE + "device/{}/n2/vlans".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")

    def createVrrp(self ,window, data, name):
        response = requests.put(BASE + "device/{}/ha/vrrp".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")

    def createPortChannel(self ,window, data, name):
        response = requests.put(BASE + "device/{}/n2/lacp".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")





















#data = [{"likes": 100, "name": "jose mari", "views": 1000}, {"likes": 98, "name": "Antonio", "views": 1000},{"likes": 75, "name": "Puri", "views": 1000},
#{"likes": 2345, "name": "Jose", "views": 1000}]
