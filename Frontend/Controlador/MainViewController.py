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
from Vista.DeviceConfigAclView import DeviceConfigAclView
from Vista.DeviceConfigSwitchPortView import DeviceConfigSwitchPortView
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

    def showOspfIntf(self, window):
        header = {
            'Interfaz': 'interface',
            'Area': 'area',
            'IP Interfaz': 'ip_address_mask',
            'Coste': 'cost',
            'State': 'state',
        }
        response = requests.get(BASE + "devices/show/ospf/interfaces")
        DeviceShowsView(window, self, json.loads(response.text),header, "Visualizacion \n Interfaces OSPF", 4, 5)
        print(response.text)

    def showVrrp(self, window):
        header = {
            'Interfaz': 'interface',
            'Grupo': 'group',
            'Estado': 'state',
            'Tiempo': 'time',
            'Master_IP': 'master_ip',
            'IP Grupo': 'group_ip'
        }
        response = requests.get(BASE + "devices/show/vrrp")
        DeviceShowsView(window, self, json.loads(response.text),header, "Visualizacion \n VRRP", 4, 5)
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

    def clickedDeviceAcl(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigAclView(window,self, name, interfaces['interfaces'], ["BlaBlaBla"])

    def clickedDeviceHA(self, window, name):
        interfaces = self.getInterfacesList(name)
        response = requests.get(BASE + "device/{}/protocols/vrrp".format(name))
        DeviceConfigHAView(window, self, name, interfaces['interfaces'], response.content)

    def clickedDeviceSwitchPort(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigSwitchPortView(window, self, name, interfaces['interfaces'])

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

    def getSyncDevices(self, url):
        BASE = url
        response = requests.get(BASE + "devices/names")
        print(response.content)
        return json.loads(response.content)


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

    def createAcl(self ,window, data, name):
        response = requests.put(BASE + "device/{}/acl".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")

    def createSwitchPort(self, window, data, name):
        response = requests.put(BASE + "device/{}/switchport".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")
