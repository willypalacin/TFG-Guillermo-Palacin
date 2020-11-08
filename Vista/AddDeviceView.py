from tkinter import *
import tkinter as tk

class AddDeviceView(tk.Toplevel):
    def __init__(self, controller, rootWindow):
        super().__init__(rootWindow, height=300, width=300)
        self.title("Anadir dispositivo")
        self.controller = controller
        self.createWindow()

    def createWindow(self):
        nameDevice = Label(self, text="Nombre: ").pack()
        entryName = Entry(self)
        entryName.pack()
        ipDevice = Label(self, text="IP/mask: ").pack()
        entryIp = Entry(self)
        entryIp.pack()

        acceptButton = Button(self, text="Aceptar",
                              command=lambda: self.controller.addNewDevice(self,
                                              entryIp.get(),
                                              entryName.get()))
        cancelButton = Button(self, text="Cancel", command=lambda: self.destroy())
        acceptButton.pack(side=LEFT, padx=80)
        cancelButton.pack(side=RIGHT, padx=80)
