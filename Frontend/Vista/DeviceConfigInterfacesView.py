from tkinter import *
from tkinter import ttk
import tkinter as tk


class DeviceConfigInterfacesView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, interfaces):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.interfaces = interfaces
        self.title("Config interfaces de {}.".format(name))
        self.update()
        self.createView(name)


    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        topFrame = Frame(self)
        topFrame.pack(side=TOP)
        titLabel=Label(topFrame, text="Configuración de Interfaces de {}".format(name), font=("Andale Mono",18))
        titLabel.pack(side=TOP, pady=(20,20))
        centerFrame = Frame(self)
        centerFrame.pack(side=LEFT)

        frameInterface = Frame(self)
        frameInterface.pack()
        Label(frameInterface, text="Selecciona Interfaz", font=("Andale Mono",12)).pack(side=TOP)
        intEntry = ttk.Combobox(frameInterface, state="readonly")
        intEntry.pack(side = LEFT, pady=(10,20))
        intEntry["values"] = self.interfaces['interfaces']

        frameIp = Frame(self)
        frameIp.pack()

        Label(frameIp, text="Introduce IP y máscara", font=("Andale Mono",12)).pack(side=LEFT)
        frameEntryIpMask = Frame(self)
        frameEntryIpMask.pack(pady=(10,20))
        ipEntry = Entry(frameEntryIpMask,highlightbackground="#00A2FF", highlightthickness=1, width=9)
        ipEntry.pack(side=LEFT)
        maskEntry = Entry(frameEntryIpMask,highlightbackground="#00A2FF", highlightthickness=1, width=2)
        maskEntry.pack(side=RIGHT)
        Label(frameEntryIpMask, text=" / ", font=("Andale Mono",18)).pack(side=RIGHT)

        frameDescription = Frame(self)
        frameDescription.pack(pady=(10,20))
        Label(frameDescription, text="Descripción de la interfaz", font=("Andale Mono",12)).pack()

        descriptonEntry = Entry(frameDescription,highlightbackground="#00A2FF", highlightthickness=1, width=25)
        descriptonEntry.pack(side = BOTTOM, pady=(10,0))
        frameButtons = Frame(self)
        frameButtons.pack(pady=10)
        btnAccept = tk.Button(frameButtons,
                    text='Accept',
                    image=imgBtnAccept, compound='center',
                    fg="white", font=("Andale Mono", 10),
                    command=lambda:self.controller.createInterface(self, self.name, self.fillDataIntoDict(intEntry.get(),
                                                                                                          descriptonEntry.get(),
                                                                                                          ipEntry.get(),
                                                                                                          maskEntry.get()
                                                                                                          )))
        btnAccept.image = imgBtnAccept
        btnAccept.pack(side=LEFT, padx=20)
        btnCancel = tk.Button(frameButtons, text='Cancel',
                           image=imgBtnCancel,font=("Andale Mono", 10) ,
                           compound='center', fg="white", command=lambda: self.destroy())
        btnCancel.image = imgBtnCancel
        btnCancel.pack(side=RIGHT, padx=20)

    def fillDataIntoDict(self, intf, desc, ip, mask):
        return {
            "int_name": intf,
            "description": desc,
            "ip": ip,
            "mask": "255.255.255.0"
        }
