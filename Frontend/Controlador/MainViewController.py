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
from Vista.DeviceConfigStaticRoutingView import DeviceConfigStaticRoutingView
import requests, json
import yaml
from Modelo.Device import Device


BASE = "http://127.0.0.1:5000/"


class MainViewController:


    def __init__(self):
        self.devices = {}
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
        data = {}
        for device in self.devices:
            response = requests.get(BASE + "device/{}/interfaces".format(device))
            data.update(json.loads(response.text))
        DeviceShowsView(window, self, data,header, "Visualización Interfaces", 4, 5)
        print(response.text)

    def showIpRoute(self, window):
        data = {}
        for device in self.devices:
            response = requests.get(BASE + "device/{}/route".format(device))
            data.update(json.loads(response.text))
        header =  {
            "Protocolo":"protocolo",
            "Red":"red",
            "Next_GW":"gateway",
            "Interfaz":"gateway_if",
            "Metrica":"metrica",
            "Distancia":"distancia"
        }
        DeviceShowsView(window, self, data ,header, "Visualización Tabla Rutas", 4, 5)
        print(response.text)

    def showOspfNeigh(self, window):
        data = {}
        for device in self.devices:
            response = requests.get(BASE + "device/{}/ospf/neighbors".format(device))
            data.update(json.loads(response.text))
        header =  {
            "Red":"address",
            "Interfaz":"interface",
            "ID_Vecino":"neighbor_id",
            "Dead_Timer":"dead_time",
            "Estado":"state",
            "Prioridad":"priority"
        }
        DeviceShowsView(window, self, data,header, "Visualización Vecinos OSPF", 4, 5)

        print(response.text)

    def showVlan(self, window):
        header = {
          'VLAN_ID': 'vlan_id',
          'Nombre': 'name',
          'Status': 'status',
          'Interfaces': 'interfaces'
        }
        data = {}
        for device in self.devices:
            response = requests.get(BASE + "device/{}/vlans".format(device))
            data.update(json.loads(response.text))
        DeviceShowsView(window, self, data,header, "Visualización VLANs", 4, 5)
        print(response.text)

    def showOspfIntf(self, window):
        header = {
            'Interfaz': 'interface',
            'Area': 'area',
            'IP Interfaz': 'ip_address_mask',
            'Coste': 'cost',
            'State': 'state',
        }
        data = {}
        for device in self.devices:
            response = requests.get(BASE + "device/{}/ospf/interfaces".format(device))
            data.update(json.loads(response.text))
        DeviceShowsView(window, self, data,header, "Visualizacion \n Interfaces OSPF", 4, 5)
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
        data = {}
        for device in self.devices:
            response = requests.get(BASE + "device/{}/vrrp".format(device))
            print(response.text)
            data.update(json.loads(response.text))
        DeviceShowsView(window, self, data,header, "Visualizacion \n VRRP", 4, 5)




    def clickedDeviceVlans(self, window,name):
        response = requests.get(BASE + "device/{}/vlans".format(name))
        DeviceConfigVlansView(window,self, name, yaml.dump(json.loads(response.content)))

    def clickedMostrarConfiguracion(self, window):
        MostrarConfigView(self, window)

    def addNewDevice(self, window,data):
        window.statusLabel.pack()
        window.statusLabel.config(fg="black", text = "Estableciendo conexion...")
        response = requests.post(BASE + "device/{}".format(data["name"]), data)
        if response.status_code == 201:
            self.devices[data["name"]] = data
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

    def clickedDeviceStaticRouting(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigStaticRoutingView(window, self, name, interfaces['interfaces'])

    def clickedDevicePortChannel(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigPortChannelView(window, self, name,interfaces['interfaces'], "blablabla\nblabla")

    def clickedDeviceAcl(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigAclView(window,self, name, interfaces['interfaces'], ["BlaBlaBla"])

    def clickedDeviceHA(self, window, name):
        interfaces = self.getInterfacesList(name)
        response = requests.get(BASE + "device/{}/vrrp".format(name))
        DeviceConfigHAView(window, self, name, interfaces['interfaces'], yaml.dump(json.loads(response.content), default_flow_style=False))

    def clickedDeviceSwitchPort(self, window, name):
        interfaces = self.getInterfacesList(name)
        DeviceConfigSwitchPortView(window, self, name, interfaces['interfaces'])

    def createInterface(self, window, name, data):
        response = requests.put(BASE + "device/{}/interfaces".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")


    def getInterfacesList(self, name):
        response = requests.get(BASE + "device/{}/interfaces".format(name))
        data = {'interfaces': []}
        for intf in json.loads(response.content)[name]:
            data['interfaces'].append(intf['nombre'])
        return data

    def getOspfData(self, name):
        response = requests.get(BASE + "device/{}/ospf".format(name))
        return response.content

    def getSyncDevices(self, url):
        BASE = url
        response = requests.get(BASE + "devices/names")
        print(response.content)
        return json.loads(response.content)


    def createRouting(self ,window, data, name):
        response = requests.put(BASE + "device/{}/ospf".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")

    def createVlans(self ,window, data, name):
        response = requests.put(BASE + "device/{}/vlans".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")

    def createVrrp(self ,window, data, name):
        response = requests.put(BASE + "device/{}/vrrp".format(name), json.dumps(data))
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

    def createStaticRouting(self, window, data, name):
        response = requests.put(BASE + "device/{}/static".format(name), json.dumps(data))
        if response.status_code == 201:
            self.mainView.addMessageToConsole(response.content, "Green")
            window.destroy()
        else:
            self.mainView.addMessageToConsole(response.content, "Red")
