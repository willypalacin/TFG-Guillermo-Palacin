from tkinter import *
from tkinter import ttk
import tkinter as tk




class DeviceConfigRoutingView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, interfaces, dataOspf):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.interfaces = interfaces
        self.dataOspf = dataOspf
        self.resizable(width=True, height=True)
        #self.configure(background="#D9D9D9")
        self.geometry("530x450")
        self.title("Config Routing de {}.".format(name))
        self.update()
        self.data = {'ospf': {
                             'routerId': '0', 'processId': '1',
                             'interfaces': {}}}
        self.createView(name)




    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        self.image = imgLineaBg

        titulo = Label(self)
        titulo.place(relx=0.4, rely=0.09, height=21, width=114)
        titulo.configure(disabledforeground="#a3a3a3")
        titulo.configure(font="-family {Andale Mono} -size 19")
        titulo.configure(foreground="#000000")
        titulo.configure(text="OSPF en {}".format(self.name))

        paramLabel = Label(self)
        paramLabel.place(relx=0.155, rely=0.211, relheight=0.05, relwidth=0.202)
        paramLabel.configure(font="-family {Andale Mono} -size 15")
        paramLabel.configure(text="Parámetros")

        paramLabel = Label(self)
        paramLabel.place(relx=0.6, rely=0.211, relheight=0.05, relwidth=0.302)
        paramLabel.configure(font="-family {Andale Mono} -size 15")
        paramLabel.configure(text="Config Actual")

        ridLabel = Label(self)
        ridLabel.place(relx=0.04, rely=0.345, relheight=0.05, relwidth=0.11)
        ridLabel.configure(text="Router ID",font="-family {Andale Mono} -size 10")

        self.ridEntry = Entry(self)
        self.ridEntry.place(relx=0.17, rely=0.34, relheight=0.05
                , relwidth=0.12)
        self.ridEntry.configure(takefocus="", background="#ABE0FF")
        self.ridEntry.configure(cursor="ibeam", font="-family {Andale Mono} -size 10")

        pidLabel = Label(self)
        pidLabel.place(relx=0.3, rely=0.345, relheight=0.05, relwidth=0.11)
        pidLabel.configure(text="PID",font="-family {Andale Mono} -size 10")

        self.pidEntry = Entry(self)
        self.pidEntry.place(relx=0.4, rely=0.34, relheight=0.05
                , relwidth=0.05)
        self.pidEntry.configure(takefocus="", background="#ABE0FF")
        self.pidEntry.configure(cursor="ibeam", font="-family {Andale Mono} -size 10")

        paramLabel = Label(self)
        paramLabel.place(relx=0.015, rely=0.475, relheight=0.05, relwidth=0.5)
        paramLabel.configure(font="-family {Andale Mono} -size 15")
        paramLabel.configure(text="Interfaces OSPF")

        self.interfacesCombo = ttk.Combobox(self)
        self.interfacesCombo.place(relx=0.05, rely=0.6, relheight=0.05, relwidth=0.27)
        self.interfacesCombo.configure(values=self.interfaces, state='readonly', font="-family {Andale Mono} -size 10")
        self.interfacesCombo.current(0)
        self.currentInterface = self.interfacesCombo.get()
        self.interfacesCombo.bind("<<ComboboxSelected>>", self.comboboxCambio)
        self.interfacesCombo.bind("<Button-1>", self.changeCurrent)
        self.chk = IntVar()
        self.activarInterfaz = Checkbutton(self, var=self.chk, offvalue= 0, onvalue=1)
        self.activarInterfaz.place(relx=0.35, rely=0.6, relwidth=0.150,  relheight=0.05)
        self.activarInterfaz.configure(takefocus="")
        self.activarInterfaz.configure(text="Activar", font="-family {Andale Mono} -size 11")

        areaLabel = Label(self)
        areaLabel.place(relx=0.05, rely=0.7, relheight=0.05, relwidth=0.12)
        areaLabel.configure(font="-family {Andale Mono} -size 11")
        areaLabel.configure(text="Area")

        self.areaEntry = Entry(self)
        self.areaEntry.place(relx=0.21, rely=0.7, relheight=0.05
                , relwidth=0.05)
        self.areaEntry.configure(takefocus="", background="#ABE0FF")
        self.areaEntry.configure(cursor="ibeam", font="-family {Andale Mono} -size 10")

        costeLabel = Label(self)
        costeLabel.place(relx=0.015, rely=0.77, relheight=0.05, relwidth=0.2)
        costeLabel.configure(font="-family {Andale Mono} -size 11")
        costeLabel.configure(text="Coste OSPF")

        self.costeEntry = Entry(self)
        self.costeEntry.place(relx=0.21, rely=0.77, relheight=0.05
                , relwidth=0.05)
        self.costeEntry.configure(takefocus="", background="#ABE0FF")
        self.costeEntry.configure(cursor="ibeam", font="-family {Andale Mono} -size 10")

        helloLabel = Label(self)
        helloLabel.place(relx=0.015, rely=0.84, relheight=0.05, relwidth=0.2)
        helloLabel.configure(font="-family {Andale Mono} -size 11")
        helloLabel.configure(text="Hello Timer")

        self.helloEntry = Entry(self)
        self.helloEntry.place(relx=0.21, rely=0.84, relheight=0.05
                , relwidth=0.05)
        self.helloEntry.configure(takefocus="", background="#ABE0FF")
        self.helloEntry.configure(cursor="ibeam", font="-family {Andale Mono} -size 10")

        priLabel = Label(self)
        priLabel.place(relx=0.3, rely=0.73, relheight=0.05, relwidth=0.15)
        priLabel.configure(font="-family {Andale Mono} -size 11")
        priLabel.configure(text="Prioridad")

        self.priEntry = Entry(self)
        self.priEntry.place(relx=0.47, rely=0.73, relheight=0.05
                , relwidth=0.05)
        self.priEntry.configure(takefocus="", background="#ABE0FF")
        self.priEntry.configure(cursor="ibeam", font="-family {Andale Mono} -size 10")

        deadLabel = Label(self)
        deadLabel.place(relx=0.3, rely=0.81, relheight=0.05, relwidth=0.15)
        deadLabel.configure(font="-family {Andale Mono} -size 11")
        deadLabel.configure(text="Dead Timer")

        self.deadEntry = Entry(self)
        self.deadEntry.place(relx=0.47, rely=0.81, relheight=0.05
                , relwidth=0.05)
        self.deadEntry.configure(takefocus="", background="#ABE0FF")
        self.deadEntry.configure(cursor="ibeam", font="-family {Andale Mono} -size 10")

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        textbox = Text(self)
        textbox.place(relx=0.58, rely=0.27, relheight=0.7, relwidth=0.4)
        textbox.insert(INSERT, self.dataOspf)
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
        self.currentInterface = self.interfacesCombo.get()
        self.data['ospf']['interfaces'].update({self.currentInterface: {}})
        self.data['ospf']['processId'] = self.pidEntry.get()
        self.data['ospf']['routerId'] = self.ridEntry.get()
        if self.chk.get():
            self.data['ospf']['interfaces'][self.currentInterface]['area'] = self.areaEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['coste'] = self.costeEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['helloTimer'] = self.helloEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['deadTimer'] = self.deadEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['priority'] = self.priEntry.get()
        self.controller.createRouting(self, self.data, self.name)



    def changeCurrent(self, event):
        self.currentInterface = self.interfacesCombo.get()
        if self.chk.get():
            self.data['ospf']['interfaces'].update({self.currentInterface: {}})

            self.data['ospf']['interfaces'][self.currentInterface]['area'] = self.areaEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['coste'] = self.costeEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['helloTimer'] = self.helloEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['deadTimer'] = self.deadEntry.get()
            self.data['ospf']['interfaces'][self.currentInterface]['priority'] = self.priEntry.get()

    def comboboxCambio(self,event):
        self.update()
