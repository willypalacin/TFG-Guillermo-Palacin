from tkinter import *
from Vista.AddDeviceView import AddDeviceView
from Vista.MainView import MainView
import requests
from Modelo.Device import Device

BASE = "http://127.0.0.1:5000/"

class MainViewController:

    def __init__(self):
        self.mainView = MainView(self)
        self.mainView.mainloop()

    def clickedAddDevice(self, window):
        AddDeviceView(self, window)

    def addNewDevice(self, window,data):
        window.statusLabel.pack()
        window.statusLabel.config(fg="black", text = "Estableciendo conexion...")
        response = requests.put(BASE + "device/{}".format(data["name"]), data)
        if response.status_code == 404:
            window.statusLabel.config(fg="red", text = "No se ha encontrado dispositivo")
        else:
            dispositivo = Device(data["name"], data["ip"])
            self.mainView.paintDevice()
            window.destroy()



import requests



#data = [{"likes": 100, "name": "jose mari", "views": 1000}, {"likes": 98, "name": "Antonio", "views": 1000},{"likes": 75, "name": "Puri", "views": 1000},
#{"likes": 2345, "name": "Jose", "views": 1000}]
