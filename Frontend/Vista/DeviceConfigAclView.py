from tkinter import *
from tkinter import ttk
import tkinter as tk


class DeviceConfigAclView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, interfaces, dataAcl):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.dataAcl = dataAcl
        self.interfaces = interfaces
        self.resizable(width=True, height=True)
        #self.configure(background="#D9D9D9")
        self.geometry("650x617")
        self.title("Config ACL de {}.".format(name))
        self.update()

        self.createView(name)


    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        self.image = imgLineaBg

        labelTit = Label(self)
        labelTit.place(relx=0.314, rely=0.054, height=24, width=300)
        labelTit.configure(text="Creacion de ACLs en {}".format(self.name))
        labelTit.configure(font="-family {Andale Mono} -size 19")

        labelNom = tk.Label(self)
        labelNom.place(relx=0.068, rely=0.162, height=23, width=110)
        labelNom.configure(text='''Nombre ACL''')
        labelNom.configure(font="-family {Andale Mono}")

        self.nomAclEntry = Entry(self)
        self.nomAclEntry.place(relx=0.26, rely=0.162, height=25, relwidth=0.161)
        self.nomAclEntry.configure(background="#ABE0FF")



        labelSec = Label(self)
        labelSec.place(relx=0.17, rely=0.266, height=24, width=91)
        labelSec.configure(text='''Nº Sec''')
        labelSec.configure(font="-family {Andale Mono}")

        tSeparator = ttk.Separator(self)
        tSeparator.place(relx=0.136, rely=0.216,  relheight=0.42)
        tSeparator.configure(orient="vertical")

        tSeparator2 = ttk.Separator(self)
        tSeparator2.place(relx=0.136, rely=0.287,  relwidth=0.042)

        self.snEntry = Entry(self)
        self.snEntry.place(relx=0.30, rely=0.265, height=25
                , relwidth=0.071)
        self.snEntry.configure(background="#ABE0FF")

        TSeparator2_1 = ttk.Separator(self)
        TSeparator2_1.place(relx=0.136, rely=0.378,  relwidth=0.053)

        saLabel = tk.Label(self)
        saLabel.place(relx=0.204, rely=0.36, height=23, width=62)
        saLabel.configure(font="-family {Andale Mono} -size 12")
        saLabel.configure(text='''IP Origen''')

        self.saEntry = tk.Entry(self)
        self.saEntry.place(relx=0.314, rely=0.355, height=25, relwidth=0.145)
        self.saEntry.configure(background="#ABE0FF")

        daLabel = tk.Label(self)
        daLabel.place(relx=0.204, rely=0.45, height=24, width=70)
        daLabel.configure(font="-family {Andale Mono} -size 12")
        daLabel.configure(text='''IP Destino''')

        self.daEntry = tk.Entry(self)
        self.daEntry.place(relx=0.32, rely=0.45, height=25, relwidth=0.145)
        self.daEntry.configure(background="#ABE0FF")


        proLabel = tk.Label(self)
        proLabel.place(relx=0.204, rely=0.541, height=23, width=56)
        proLabel.configure(text="Protocol")
        proLabel.configure(font="-family {Andale Mono} -size 12")

        self.proCombo = ttk.Combobox(self)
        self.proCombo.place(relx=0.309, rely=0.541, relheight=0.037
                , relwidth=0.083)
        self.proCombo.configure(values=['ip','tcp','udp'])
        self.proCombo.configure(takefocus="")

        tSeparator3 = ttk.Separator(self)
        tSeparator3.place(relx=0.136, rely=0.468,  relwidth=0.053)

        tSeparator4 = ttk.Separator(self)
        tSeparator4.place(relx=0.136, rely=0.558,  relwidth=0.054)

        portLabel = tk.Label(self)
        portLabel.place(relx=0.402, rely=0.541, height=23, width=56)
        portLabel.configure(font="-family {Andale Mono} -size 12")
        portLabel.configure(text="Puerto")


        tSeparator4_1 = ttk.Separator(self)
        tSeparator4_1.place(relx=0.137, rely=0.63,  relwidth=0.068)

        self.portEntry = Entry(self)
        self.portEntry.place(relx=0.489, rely=0.535, height=25, relwidth=0.05)
        self.portEntry.configure(background="#ABE0FF")
        self.portEntry.configure(font="-family {Andale Mono} -size 10")


        self.actionCombo = ttk.Combobox(self)
        self.actionCombo.place(relx=0.309, rely=0.6105, relheight=0.039
                , relwidth=0.113)
        self.actionCombo.configure(values=['accept','discard'], font="-family {Andale Mono} -size 10")
        self.actionCombo.current(0)


        actionLabel = tk.Label(self)
        actionLabel.place(relx=0.201, rely=0.6105, height=24, width=56)
        actionLabel.configure(text='''Action''')
        actionLabel.configure(font="-family {Andale Mono} -size 12")

        intLabel = tk.Label(self)
        intLabel.place(relx=0.062, rely=0.682, height=23, width=110)
        intLabel.configure(text='''Interfaz''')
        intLabel.configure(font="-family {Andale Mono} -size 12")

        tSeparator5 = ttk.Separator(self)
        tSeparator5.place(relx=0.139, rely=0.714,  relheight=0.121)
        tSeparator5.configure(orient="vertical")

        tSeparator6 = ttk.Separator(self)
        tSeparator6.place(relx=0.139, rely=0.763,  relwidth=0.046)

        nomIntLabel = tk.Label(self)
        nomIntLabel.place(relx=0.201, rely=0.747, height=23, width=56)
        nomIntLabel.configure(text='''Nombre''')
        nomIntLabel.configure(font="-family {Andale Mono} -size 12")


        self.nomIntCombo = ttk.Combobox(self)
        self.nomIntCombo.place(relx=0.294, rely=0.747, relheight=0.037
                , relwidth=0.113)
        self.nomIntCombo.configure(values=self.interfaces)
        self.nomIntCombo.configure(takefocus="")

        self.direccionCombo = ttk.Combobox(self)
        self.direccionCombo.place(relx=0.31, rely=0.812, relheight=0.037
                , relwidth=0.113)
        self.direccionCombo.configure(values=['input','output'])
        self.direccionCombo.current(0)


        dirLabel = tk.Label(self)
        dirLabel.place(relx=0.201, rely=0.812, height=23, width=65)
        dirLabel.configure(text='''Direccion''')
        dirLabel.configure(font="-family {Andale Mono} -size 11")




        tSeparator6_1 = ttk.Separator(self)
        tSeparator6_1.place(relx=0.139, rely=0.825,  relwidth=0.046)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        textbox = Text(self)
        textbox.place(relx=0.60, rely=0.27, relheight=0.7, relwidth=0.3)
        textbox.insert(INSERT, self.dataAcl)
        # attach textbox to scrollbar
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)

        btnAccept = tk.Button(self,
                    text='Accept',
                    image=imgBtnAccept, compound='center',
                    fg="white", font=("Andale Mono", 10),
                    command=lambda:self.acceptClick())
        btnAccept.image = imgBtnAccept
        btnAccept.place(relx=0.08, rely=0.94)
        btnCancel = tk.Button(self, text='Cancel',
                           image=imgBtnCancel,font=("Andale Mono", 10) ,
                           compound='center', fg="white", command=lambda: self.destroy())
        btnCancel.image = imgBtnCancel
        btnCancel.place(relx=0.25, rely=0.94)
        raya = tk.Canvas(self)
        raya.place(relx=0.58, rely=0.226, relheight=0.651
                , relwidth=0.001)
        raya.configure(borderwidth="2")
        raya.configure(highlightbackground="#000000")
        raya.configure(insertbackground="black")
        raya.configure(relief="ridge")

    def acceptClick(self):
        protocol = ''
        if "ip" not in self.proCombo.get():
            protocol = self.proCombo.get()
        data = {
         self.nomAclEntry.get(): {
            "rule": {
                "num": self.snEntry.get(),
                "sourceAddr": self.saEntry.get(),
                "destAddr": self.daEntry.get(),
                "protocol": protocol,
                "destPort": self.portEntry.get(),
                "action": self.actionCombo.get()
            },
            "interfaz": {
                "nombre": self.nomIntCombo.get(),
                "apply": self.direccionCombo.get()
            }

        }}
        self.controller.createAcl(self, data, self.name)
