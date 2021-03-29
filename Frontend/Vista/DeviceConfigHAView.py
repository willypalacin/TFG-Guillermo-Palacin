from tkinter import *
from tkinter import ttk
import tkinter as tk




class DeviceConfigHAView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, interfaces, dataVrrp):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.interfaces = interfaces
        self.dataVrrp = dataVrrp
        self.resizable(width=True, height=True)

        #self.configure(background="#D9D9D9")
        self.geometry("570x450+301+233")
        self.title("Config Routing de {}.".format(name))
        self.update()
        self.createView(name)




    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')

        vrrpTituloLabel = Label(self)
        vrrpTituloLabel.place(relx=0.333, rely=0.089, height=21, width=203)
        vrrpTituloLabel.configure(font="-family {Andale Mono} -size 19")
        vrrpTituloLabel.configure(foreground="#000000")
        vrrpTituloLabel.configure(text='VRRP en {}'.format(self.name))

        self.intVRRPCombo = ttk.Combobox(self)
        self.intVRRPCombo.place(relx=0.255, rely=0.267, relheight=0.047
                , relwidth=0.235)
        self.intVRRPCombo.configure(takefocus="", state='readonly', values=self.interfaces)
        self.intVRRPCombo.configure(text="Activar", font="-family {Andale Mono} -size 11")
        self.intVRRPCombo.current(0)

        intVRRPLabel = Label(self)
        intVRRPLabel.place(relx=0.05, rely=0.267, height=19, width=95)
        intVRRPLabel.configure(font="-family {Andale Mono} -size 12")
        intVRRPLabel.configure(relief="flat")
        intVRRPLabel.configure(anchor='w')
        intVRRPLabel.configure(justify='left')
        intVRRPLabel.configure(text="Interfaz VRRP")

        ipLabel  = Label(self)
        ipLabel.place(relx=0.088, rely=0.533, height=19, width=70)
        ipLabel.configure(font="-family {Andale Mono} -size 12")
        ipLabel.configure(relief="flat")
        ipLabel.configure(anchor='w')
        ipLabel.configure(justify='left')
        ipLabel.configure(text='''IP Standby''')


        labelGrupo = Label(self)
        labelGrupo.place(relx=0.05, rely=0.4, height=19, width=102)
        labelGrupo.configure(font="-family {Andale Mono} -size 12")
        labelGrupo.configure(relief="flat")
        labelGrupo.configure(anchor='w')
        labelGrupo.configure(justify='left')
        labelGrupo.configure(text='''Grupo standby''')

        values = []
        for i in range (0, 30):
            values.append(i)
        self.numGrupoCombo = ttk.Combobox(self)
        self.numGrupoCombo.place(relx=0.23, rely=0.4, relheight=0.047
                , relwidth=0.077)
        self.numGrupoCombo.configure(takefocus="", values=values)
        self.numGrupoCombo.current(0)

        self.ipEntry = Entry(self)
        self.ipEntry.place(relx=0.246, rely=0.533, relheight=0.06
                , relwidth=0.221)
        self.ipEntry.configure(takefocus="", background="#ABE0FF")
        self.ipEntry.configure(cursor="fleur")

        priLabel = Label(self)
        priLabel.place(relx=0.331, rely=0.4, height=19, width=70)
        priLabel.configure(font="-family {Andale Mono} -size 12")
        priLabel.configure(relief="flat")
        priLabel.configure(anchor='w')
        priLabel.configure(justify='left')
        priLabel.configure(text='''Prioridad''')

        self.chk = IntVar()

        self.preemActivado = Checkbutton(self, var=self.chk, offvalue= 0, onvalue=1)
        self.preemActivado.place(relx=0.246, rely=0.667, relwidth=0.125
                , relheight=0.0, height=21)
        self.preemActivado.configure(takefocus="", font="-family {Andale Mono} -size 12")
        self.preemActivado.configure(text='''Activar''')

        self.priEntry = Entry(self)
        self.priEntry.place(relx=0.454, rely=0.4, relheight=0.047, relwidth=0.063)

        self.priEntry.configure(takefocus="", background="#ABE0FF")
        self.priEntry.configure(cursor="ibeam")

        preemLabel= Label(self)
        preemLabel.place(relx=0.093, rely=0.67, height=19, width=65)

        preemLabel.configure(font="-family {Andale Mono} -size 12")
        preemLabel.configure(relief="flat")
        preemLabel.configure(anchor='w')
        preemLabel.configure(justify='left')
        preemLabel.configure(text='''Preemtion''')

        btnAccept = tk.Button(self,
                    text='Accept',
                    image=imgBtnAccept, compound='center',
                    fg="white", font=("Andale Mono", 10),
                    command=lambda:self.acceptClick())
        btnAccept.image = imgBtnAccept
        btnAccept.place(relx=0.1, rely=0.8)
        btnCancel = tk.Button(self, text='Cancel',
                           image=imgBtnCancel,font=("Andale Mono", 10) ,
                           compound='center', fg="white", command=lambda: self.destroy())
        btnCancel.image = imgBtnCancel
        btnCancel.place(relx=0.3, rely=0.8)

        paramLabel = Label(self)
        paramLabel.place(relx=0.5, rely=0.211, relheight=0.05, relwidth=0.502)
        paramLabel.configure(font="-family {Andale Mono} -size 15")
        paramLabel.configure(text="Config Actual")

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        textbox = Text(self)
        textbox.place(relx=0.6, rely=0.27, relheight=0.7, relwidth=0.4)
        textbox.insert(INSERT, self.dataVrrp)
        # attach textbox to scrollbar
        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)

        raya = tk.Canvas(self)
        raya.place(relx=0.57, rely=0.226, relheight=0.651
                , relwidth=0.001)
        raya.configure(borderwidth="2")
        raya.configure(highlightbackground="#000000")
        raya.configure(insertbackground="black")
        raya.configure(relief="ridge")

    def acceptClick(self):
        data = {
           "vrrp":{
              "{}".format(self.intVRRPCombo.get()):{
                 "ipVrrp":"{}".format(self.ipEntry.get()),
                 "preempt": self.chk.get(),
                 "grupo":"{}".format(self.numGrupoCombo.get()),
                 "priority":"{}".format(self.priEntry.get())
              }
           }
        }
        print(data)
        self.controller.createVrrp(self, data, self.name)
