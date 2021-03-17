from tkinter import *
from tkinter import ttk
import tkinter as tk


class DeviceConfigRoutingView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, interfaces):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.interfaces = interfaces
        self.resizable(width=False, height=False)
        self.title("Config Routing de {}.".format(name))
        self.update()
        self.createView(name)


    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        self.image = imgLineaBg

        topFrame = Frame(self)
        topFrame.pack(side=TOP)
        titLabel=Label(topFrame, text="Configuración Routing de {}".format(name), font=("Andale Mono",18))
        titLabel.pack(side=TOP, pady=(20,0))
        leftFrame = Frame(self)
        tituloDinamico=Label(leftFrame, text="Routing dinámico", font=("Andale Mono",15))
        tituloDinamico.pack(side=TOP, pady=(20,20))
        tituloOSPF=Label(leftFrame, text="OSPF", font=("Andale Mono",15))
        tituloOSPF.pack(side=TOP, pady=(5,20))
        leftFrame.pack(side=LEFT)
        pidRidFrame = Frame(leftFrame)
        pidFrame = Frame(pidRidFrame)
        pidLabel=Label(pidFrame, text="PID", font=("Andale Mono",12))
        pidLabel.pack(side=TOP)
        pidEntry = Entry(pidFrame,bg="#ABE0FF", width=3)
        pidEntry.pack(side=BOTTOM)
        pidFrame.pack(side=LEFT)
        ridFrame = Frame(pidRidFrame)
        ridLabel=Label(ridFrame, text="Router ID", font=("Andale Mono",12))
        ridLabel.pack(side=TOP)
        ridEntry = Entry(ridFrame,bg="#ABE0FF", width=7)
        ridEntry.pack(side=BOTTOM, padx=20)
        ridFrame.pack(side=RIGHT)
        pidRidFrame.pack(padx=20, pady=(0,20))
        interfaceAreaFrame = Frame(leftFrame)

        Label(interfaceAreaFrame, text="Interface", font=("Andale Mono",12)).grid(row=0, column=0)
        Label(interfaceAreaFrame, text="AreaID", font=("Andale Mono",12)).grid(row=0, column=1)
        Label(interfaceAreaFrame, text="Interface", font=("Andale Mono",12)).grid(row=0, column=2)
        Label(interfaceAreaFrame, text="AreaID", font=("Andale Mono",12)).grid(row=0, column=3)
        col = 0
        row = 1
        chkValue = tk.BooleanVar()
        checkboxes = {}
        for int in self.interfaces:
            checkboxes.update({int: {'activa': IntVar()}})
            checkbox = tk.Checkbutton(interfaceAreaFrame ,text=int, font=("Andale Mono",8), var=checkboxes[int]['activa'], offvalue= 0, onvalue=1)
            #checkboxes.append(checkbox)
            checkbox.grid(row=row, column=col)
            col = (col + 1)%4
            aid = Entry(interfaceAreaFrame,bg="#ABE0FF",name=int.lower(),width=2, font=("Andale Mono",7))
            aid.grid(row=row, column=col)
            checkboxes[int]['areaId'] = aid
            col = (col + 1)%4
            if col == 0:
                row = row + 1
        interfaceAreaFrame.pack(padx=(20,0),pady=(0, 20))
        rightFrame = Frame(self)
        tituloEstatico=Label(rightFrame, text="Routing Estático", font=("Andale Mono",15))
        tituloEstatico.pack(side=TOP, pady=(0,10))
        tituloEstatico=Label(rightFrame, text="Añadir ruta por defecto", font=("Andale Mono",12))
        tituloEstatico.pack(side=TOP, pady=(0,20))


        rutaFrame = Frame(rightFrame)
        gatewayFrame = Frame(rutaFrame)
        gatewayLabel=Label(gatewayFrame, text="Gateway", font=("Andale Mono",12))
        gatewayLabel.pack(side=TOP)
        gatewayEntry = Entry(gatewayFrame,bg="#ABE0FF", width=9)
        gatewayEntry.pack(side=BOTTOM)
        gatewayFrame.pack(side=LEFT)
        metricaFrame = Frame(rutaFrame)
        metricaLabel=Label(metricaFrame, text="Metrica", font=("Andale Mono",12))
        metricaLabel.pack(side=TOP)
        metricaEntry = Entry(metricaFrame,bg="#ABE0FF", width=4)
        metricaEntry.pack(side=BOTTOM)
        metricaFrame.pack(side=RIGHT)
        rutaFrame.pack()

        tituloEstatico=Label(rightFrame, text="Añadir ruta estática", font=("Andale Mono",12)).pack(pady=(20,0))
        lineaFrame = Frame(rightFrame)
        redMaskFrame = Frame(lineaFrame)
        redFrame = Frame(redMaskFrame)
        redLabel = Label(redFrame, text="Red", font=("Andale Mono",12)).pack(side=TOP)
        redEntry = Entry(redFrame,bg="#ABE0FF", width=9)
        redEntry.pack(side=BOTTOM)
        redFrame.pack(side=LEFT)
        maskFrame = Frame(redMaskFrame)
        maskLabel = Label(maskFrame, text="/", font=("Andale Mono",12)).pack(side=TOP)
        maskEntry = Entry(maskFrame,bg="#ABE0FF", width=3)
        maskEntry.pack(side=BOTTOM)
        maskFrame.pack(side=RIGHT)
        redMaskFrame.pack(side=LEFT)

        gwMetrFrame = Frame(lineaFrame)
        gwFrame = Frame(gwMetrFrame)
        gwLabel = Label(gwFrame, text="Gateway", font=("Andale Mono",12)).pack(side=TOP)
        gwEntry = Entry(gwFrame,bg="#ABE0FF", width=5)
        gwEntry.pack(side=BOTTOM)
        gwFrame.pack(side=LEFT)
        metrFrame = Frame(gwMetrFrame)
        metrLabel = Label(metrFrame, text="Metrica", font=("Andale Mono",12)).pack(side=TOP)
        metrEntry = Entry(metrFrame, width=3, bg="#ABE0FF")
        metrEntry.pack(side=BOTTOM)
        metrFrame.pack(side=RIGHT)
        gwMetrFrame.pack(side=RIGHT, pady=10)
        lineaFrame.pack()
        buttonFrame = Frame(self)
        rightFrame.pack(side=RIGHT, padx=(40,20))
        btnAccept = tk.Button(leftFrame,
                    text='Accept',
                    image=imgBtnAccept, compound='center',
                    fg="white", font=("Andale Mono", 10),
                    command=lambda:self.controller.createRouting(self, checkboxes, pidEntry.get(), ridEntry.get(), self.name))
        btnAccept.image = imgBtnAccept
        btnAccept.pack(side=LEFT, padx=(80,0), pady=(25, 10))
        btnCancel = tk.Button(leftFrame, text='Cancel',
                           image=imgBtnCancel,font=("Andale Mono", 10) ,
                           compound='center', fg="white", command=lambda: self.destroy())
        btnCancel.image = imgBtnCancel
        btnCancel.pack(side=RIGHT, padx=(0, 100), pady=(25, 10))


    def fillDataIntoDict(self, intf, desc, ip, mask):
        return {
            "int_name": intf,
            "description": desc,
            "ip": ip,
            "mask": "255.255.255.0"
        }
