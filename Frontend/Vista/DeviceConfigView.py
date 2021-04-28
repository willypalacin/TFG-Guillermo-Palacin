from tkinter import *
from tkinter import ttk
import tkinter as tk
from Vista.DeviceConfigInterfacesView import DeviceConfigInterfacesView
from Vista.MostrarConfigView import MostrarConfigView

class DeviceConfigView(tk.Toplevel):
    def __init__(self, controller, rootWindow, name):
        super().__init__(rootWindow, height=700, width=560, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.title("Configuracion de {}.".format(name))
        self.update()

        btnBlue = PhotoImage(file = 'Vista/assets/rect_blue_4.png')
        topFrame = Frame(self, bg="white")
        topFrame.pack(side=TOP)
        Label(topFrame, text="Configuracion de {}.".format(name), font=("Andale Mono",16)).pack(side=BOTTOM, pady=(20,10))

        leftFrame = Frame(self, bg="white")
        leftFrame.pack(side=LEFT)
        Label(leftFrame, text="N3", font=("Andale Mono",17)).pack(side=TOP, pady=(20,10))

        btnIntf = tk.Button(leftFrame, text='Conf Interfaces \n y subinterfaces',
                           image=btnBlue, command=lambda:self.clickedViewInt() ,compound='center', fg="white", width=self.winfo_width()/6)
        btnIntf.image=btnBlue
        btnIntf.pack(padx=10, pady=10)

        btnRouting = tk.Button(leftFrame, text='Routing Dinámico',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.controller.clickedDeviceRouting(self, self.name))
        btnRouting.image=btnBlue
        btnRouting.pack(padx=10, pady=10)

        btnDhcp = tk.Button(leftFrame, text='Routing Estático',
                           image=btnBlue, compound='center', fg="white")
        btnDhcp.image=btnBlue
        btnDhcp.pack(padx=70, pady=10)

        btnHA = tk.Button(leftFrame, text='High Availability',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.controller.clickedDeviceHA(self, self.name))
        btnHA.image=btnBlue
        btnHA.pack(padx=10, pady=10)

        btnDhcp = tk.Button(leftFrame, text='ACLs',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.controller.clickedDeviceAcl(self, self.name))
        btnDhcp.image=btnBlue
        btnDhcp.pack(padx=70, pady=(10,40))




        rightFrame = Frame(self, bg="white")
        rightFrame.pack(side=RIGHT)
        Label(rightFrame, text="N2", font=("Andale Mono",17)).pack(side=TOP, padx=(30,70))

        btnVlan = tk.Button(rightFrame, text='Creacion VLANs',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.controller.clickedDeviceVlans(self, self.name))
        btnVlan.image=btnBlue
        btnVlan.pack(padx=(30,70), pady=10)

        btnAgg = tk.Button(rightFrame, text='Agregación Enlaces',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.controller.clickedDevicePortChannel(self, self.name))
        btnAgg.image=btnBlue
        btnAgg.pack(padx=(30,70),pady=10)

        btnSTP = tk.Button(rightFrame, text='Configuracion SwitchPort',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.controller.clickedDeviceSwitchPort(self, self.name))
        btnSTP.image=btnBlue

        btnSTP.pack(padx=(30,70),pady=10)

    def clickedViewInt(self):
        interfaces = self.controller.getInterfacesList(self.name)
        DeviceConfigInterfacesView(self, self.controller, self.name, interfaces)




    def hola(self):
        print("HOLA")
