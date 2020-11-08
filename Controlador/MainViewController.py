from tkinter import *
from Vista.AddDeviceView import AddDeviceView
from Vista.MainView import MainView
from Vista.ConsoleView import ConsoleView
from Modelo.Device import Device

class MainViewController:

    def __init__(self):
        self.mainView = MainView(self)
        ConsoleView(self.mainView)
        self.mainView.mainloop()

    def clickedAddDevice(self, window):
        AddDeviceView(self, window)


    def addNewDevice(self, window, name, ip):
        dispositivo = Device(name, ip)

        window.destroy()
