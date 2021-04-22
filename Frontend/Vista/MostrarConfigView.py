from tkinter import *
from tkinter import ttk
import tkinter as tk


class MostrarConfigView(tk.Toplevel):
    def __init__(self, controller, rootWindow):
        super().__init__(rootWindow, height=700, width=560, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.title("Mostrar configuracion")
        self.update()

        btnBlue = PhotoImage(file = 'Vista/assets/btn_verde.png')
        topFrame = Frame(self, bg="white")
        topFrame.pack(side=TOP)
        Label(topFrame, text="Visualizar configuración", font=("Andale Mono",16)).pack(side=BOTTOM, pady=(20,10))

        leftFrame = Frame(self, bg="white")
        leftFrame.pack(side=LEFT)

        btnIntf = tk.Button(leftFrame, text='Ver resumen \n Interfaces',
                           image=btnBlue, command=lambda:self.showInterfaces() ,compound='center', fg="white", width=self.winfo_width()/6)
        btnIntf.image=btnBlue
        btnIntf.pack(padx=10, pady=10)

        btnRouting = tk.Button(leftFrame, text='Ver Tabla\n Rutas',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.showIpRouteClick())
        btnRouting.image=btnBlue
        btnRouting.pack(padx=10, pady=10)

        btnHA = tk.Button(leftFrame, text='Ver vecinos \n OSPF',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.showOspfNeighClick())
        btnHA.image=btnBlue
        btnHA.pack(padx=10, pady=10)

        btnDhcp = tk.Button(leftFrame, text='Ver interfaces OSPF',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.showOspfIntfClick())
        btnDhcp.image=btnBlue
        btnDhcp.pack(padx=70, pady=(10,40))

        btnVrrp = tk.Button(leftFrame, text='Ver VRRP',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.showVrrpClick())
        btnVrrp.image=btnBlue
        btnVrrp.pack(padx=70, pady=(10,40))

        rightFrame = Frame(self, bg="white")
        rightFrame.pack(side=RIGHT)


        btnVlan = tk.Button(rightFrame, text='Ver VLANs',
                           image=btnBlue, compound='center', fg="white", command=lambda:self.showVlansClick())
        btnVlan.image=btnBlue
        btnVlan.pack(padx=(30,70), pady=10)

        btnAgg = tk.Button(rightFrame, text='Agregación Enlaces',
                           image=btnBlue, compound='center', fg="white")
        btnAgg.image=btnBlue
        btnAgg.pack(padx=(30,70),pady=10)

        btnSTP = tk.Button(rightFrame, text='Spanning-Tree',
                           image=btnBlue, compound='center', fg="white")
        btnSTP.image=btnBlue

        btnSTP.pack(padx=(30,70),pady=10)

    def showInterfaces(self):
        self.controller.showInterfacesAll(self)

    def showIpRouteClick(self):
        self.controller.showIpRoute(self)

    def showOspfNeighClick(self):
        self.controller.showOspfNeigh(self)

    def showVlansClick(self):
        self.controller.showVlan(self)

    def showOspfIntfClick(self):
        self.controller.showOspfIntf(self)

    def showVrrpClick(self):
        self.controller.showVrrp(self)
