from tkinter import *
from tkinter import ttk
import tkinter as tk


class AddDeviceView(tk.Toplevel):
    def __init__(self, controller, rootWindow):
        super().__init__(rootWindow, height=300, width=300)
        self.title("Anadir dispositivo")
        self.controller = controller
        self.entryName, self.entryIp, \
        self.portEntry, self.usnEntry, \
        self.passEntry, self.typeEntry, self.statusLabel = \
        self.createWindow()

    def fillDataIntoDict(self):
        return {
            "name": self.entryName.get(),
            "ip": self.entryIp.get(),
            "port": self.portEntry.get(),
            "usnm": self.usnEntry.get(),
            "pass": self.passEntry.get(),
            "type": self.typeEntry.get().replace(" ", "_").lower()
        }

    def createWindow(self):
        nameDevice = Label(self, text="Nombre: ").pack()
        entryName = Entry(self)
        entryName.pack()
        ipDevice = Label(self, text="IP/mask: ").pack()
        entryIp = Entry(self)
        entryIp.pack()
        port = Label(self, text="Port ").pack()
        portEntry = Entry(self)
        portEntry.pack()
        usn = Label(self, text="Username ").pack()
        usnEntry = Entry(self)
        usnEntry.pack()
        usn = Label(self, text="Password ").pack()
        passEntry = Entry(self)
        passEntry.pack()
        type = Label(self, text=" Type").pack()
        typeEntry = ttk.Combobox(self, state="readonly")
        typeEntry.pack()
        typeEntry["values"] = ["Cisco IOS", "JunosOS", "Cisco Nexus", "Huawei"]
        statusLabel = Label(self, text="Comprobando conexion...")
        statusLabel.pack_forget()


        acceptButton = Button(self, text="Aceptar",
                              command=lambda: self.controller.addNewDevice(self,
                                              self.fillDataIntoDict()))
        cancelButton = Button(self, text="Cancel", command=lambda: self.destroy())
        acceptButton.pack(side=LEFT, padx=80)
        cancelButton.pack(side=RIGHT, padx=80)

        return entryName, entryIp, portEntry, usnEntry, passEntry, typeEntry, statusLabel
