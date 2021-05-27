from tkinter import *
from tkinter import ttk
import tkinter as tk


class DeviceConfigVlansView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, dataVlans):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.dataVlans = dataVlans
        self.resizable(width=True, height=True)
        #self.configure(background="#D9D9D9")
        self.geometry("530x450")
        self.title("Config Routing de {}.".format(name))
        self.update()
        self.data = {
            "vlanId": "",
            "vlanNom": "",
            "layer3": {
                "ip": ""
        }}
        self.createView(name)


    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        self.image = imgLineaBg

        titLabel = Label(self)
        titLabel.place(relx=0.18, rely=0.089, height=21, width=389)
        titLabel.configure(font="-family {Andale Mono} -size 17")
        titLabel.configure(text="Configuracion de VLANs en {}".format(self.name))

        vidLabel = Label(self)
        vidLabel.place(relx=0.083, rely=0.27, height=19, width=65)
        vidLabel.configure(font="-family {Andale Mono}")
        vidLabel.configure(relief="flat")
        vidLabel.configure(anchor='w')
        vidLabel.configure(justify='left')
        vidLabel.configure(text='''VLAN ID''')

        self.vidEntry = Entry(self)
        self.vidEntry.place(relx=0.217, rely=0.267, height=25, relwidth=0.123)
        self.vidEntry.configure(background="#ABE0FF")
        self.vidEntry.configure(font="-family {Andale Mono}")


        nomLabel= Label(self)
        nomLabel.place(relx=0.05, rely=0.41, height=19, width=90)
        nomLabel.configure(font="-family {Andale Mono}")
        nomLabel.configure(relief="flat")
        nomLabel.configure(anchor='w')
        nomLabel.configure(justify='left')
        nomLabel.configure(text='''Nombre VLAN''')

        self.nomEntry = Entry(self)
        self.nomEntry.place(relx=0.25, rely=0.4, height=25, relwidth=0.157)
        self.nomEntry.configure(background="#ABE0FF")
        self.nomEntry.configure(font="TkFixedFont")


        sviLabel = Label(self)
        sviLabel.place(relx=0.1, rely=0.533, height=19, width=195)
        sviLabel.configure(font="-family {Andale Mono} -size  15")
        sviLabel.configure(relief="flat")
        sviLabel.configure(anchor='w')
        sviLabel.configure(justify='left')
        sviLabel.configure(text='''Habilitar Int. Virtual''')

        self.sviEntryIp = Entry(self)
        self.sviEntryIp.place(relx=0.117, rely=0.644, height=25, relwidth=0.157)
        self.sviEntryIp.configure(background="#ABE0FF")
        self.sviEntryIp.configure(disabledforeground="#a3a3a3")
        self.sviEntryIp.configure(font="TkFixedFont")


        self.sviEntryMask = Entry(self)
        self.sviEntryMask.place(relx=0.33, rely=0.644, height=25, relwidth=0.057)
        self.sviEntryMask.configure(background="#ABE0FF")
        self.sviEntryMask.configure(font="TkFixedFont")


        auxLabel = Label(self)
        auxLabel.place(relx=0.267, rely=0.644, height=21, width=34)
        auxLabel.configure(text='''/''')

        ipLabel = Label(self)
        ipLabel.place(relx=0.05, rely=0.644, height=21, width=34)
        ipLabel.configure(font="-family {Andale Mono}")
        ipLabel.configure(text='''IP''')

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        textbox = Text(self)
        textbox.place(relx=0.58, rely=0.27, relheight=0.7, relwidth=0.4)
        textbox.insert(INSERT, self.dataVlans)
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
        raya.place(relx=0.55, rely=0.226, relheight=0.651
                , relwidth=0.001)
        raya.configure(borderwidth="2")
        raya.configure(highlightbackground="#000000")
        raya.configure(insertbackground="black")
        raya.configure(relief="ridge")

    def acceptClick(self):
        self.data['vlanId']= int(self.vidEntry.get())
        self.data['vlanNom'] = self.nomEntry.get()
        if self.sviEntryIp.get() != '' and self.sviEntryMask.get() != '':
            self.data['layer3']['ip'] = "{}/{}".format(self.sviEntryIp.get(), self.sviEntryMask.get())
        print(self.data)
        self.controller.createVlans(self, self.data, self.name)
