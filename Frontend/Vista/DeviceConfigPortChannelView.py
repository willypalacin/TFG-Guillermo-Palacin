from tkinter import *
from tkinter import ttk
import tkinter as tk


class DeviceConfigPortChannelView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, interfaces, dataPortChannel):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.dataPortChannel = dataPortChannel
        self.interfaces = interfaces
        self.resizable(width=True, height=True)
        #self.configure(background="#D9D9D9")
        self.geometry("650x450")
        self.title("Config Routing de {}.".format(name))
        self.update()
        self.data = {
            "numPortChannel": 1,
            "mode": "active",
            "interfaces": []
        }
        self.createView(name)


    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        self.image = imgLineaBg

        labTit = tk.Label(self)
        labTit.place(relx=0.37, rely=0.089, height=21, width=174)
        labTit.configure(font="-family {Andale Mono} -size 15")
        labTit.configure(text="Configuracion Port-Channel")

        labInt = tk.Label(self)
        labInt.place(relx=0.145, rely=0.244, height=21, width=180)
        labInt.configure(font="-family {Andale Mono} -size 13")
        labInt.configure(text='''Habilitar Interfaces''')
        self.chk = [IntVar(), IntVar(), IntVar(), IntVar()]
        self.combos = []




        pc1Combo = ttk.Combobox(self)
        pc1Combo.place(relx=0.081, rely=0.378, relheight=0.047
                , relwidth=0.172)
        pc1Combo.configure(takefocus="", values=self.interfaces, state='readonly', font="-family {Andale Mono} -size 11")
        pc1Combo.current(0)
        self.combos.append(pc1Combo)


        chk1But = Checkbutton(self, var=self.chk[0], offvalue= 0, onvalue=1)
        chk1But.place(relx=0.032, rely=0.378, relwidth=0.032
                , relheight=0.0, height=21)
        chk1But.configure(takefocus="")


        chk2But = Checkbutton(self, var=self.chk[1], offvalue= 0, onvalue=1)
        chk2But.place(relx=0.29, rely=0.378, relwidth=0.032
                , relheight=0.0, height=21)
        chk2But.configure(takefocus="")


        pc2Combo = ttk.Combobox(self)
        pc2Combo.place(relx=0.081, rely=0.489, relheight=0.047
                , relwidth=0.172)
        pc2Combo.configure(takefocus="", values=self.interfaces, state='readonly', font="-family {Andale Mono} -size 11")
        pc2Combo.current(0)



        chk3But = Checkbutton(self, var=self.chk[2], offvalue= 0, onvalue=1)
        chk3But.place(relx=0.032, rely=0.489, relwidth=0.032
                , relheight=0.0, height=21)
        chk3But.configure(takefocus="")


        chk4But = Checkbutton(self, var=self.chk[3], offvalue= 0, onvalue=1)
        chk4But.place(relx=0.29, rely=0.489, relwidth=0.032
                , relheight=0.0, height=21)
        chk4But.configure(takefocus="")


        pc3Combo = ttk.Combobox(self)
        pc3Combo.place(relx=0.338, rely=0.378, relheight=0.047
                , relwidth=0.172)
        pc3Combo.configure(takefocus="", values=self.interfaces, state='readonly', font="-family {Andale Mono} -size 11")
        pc3Combo.current(0)
        self.combos.append(pc3Combo)
        self.combos.append(pc2Combo)

        pc4Combo = ttk.Combobox(self)
        pc4Combo.place(relx=0.338, rely=0.489, relheight=0.047
                , relwidth=0.172)
        pc4Combo.configure(takefocus="", values=self.interfaces, state='readonly', font="-family {Andale Mono} -size 11")
        pc4Combo.current(0)
        self.combos.append(pc4Combo)

        label2 = tk.Label(self)
        label2.place(relx=0.032, rely=0.644, height=21, width=46)
        label2.configure(text='''Grupo''')
        label2.configure(font="-family {Andale Mono}")

        self.pcNum = tk.Entry(self)
        self.pcNum.place(relx=0.129, rely=0.644, height=25, relwidth=0.087)
        self.pcNum.configure(background="white")
        self.pcNum.configure(disabledforeground="#a3a3a3")
        self.pcNum.configure(font="TkFixedFont")
        self.pcNum.configure(foreground="#000000")
        self.pcNum.configure(insertbackground="black", text="1")

        label3 = tk.Label(self)
        label3.place(relx=0.274, rely=0.644, height=21, width=35)
        label3.configure(text='''Modo''')
        label3.configure(font="-family {Andale Mono}")

        self.actPassCombo = ttk.Combobox(self)
        self.actPassCombo.place(relx=0.354, rely=0.644, relheight=0.047
                , relwidth=0.122)
        self.actPassCombo.configure(takefocus="", values=["Active", "Passive"], state='readonly')
        self.actPassCombo.current(0)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        textbox = Text(self)
        textbox.place(relx=0.58, rely=0.27, relheight=0.7, relwidth=0.4)
        textbox.insert(INSERT, self.dataPortChannel)
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
        print("Hola")

        self.data['numPortChannel'] = self.pcNum.get()
        self.data['mode'] = self.actPassCombo.get()
        j = 0
        for i in self.chk:
            if i.get() == 1:
                self.data['interfaces'].append(self.combos[j].get())
            j = j + 1
        print(self.data)
        self.controller.createPortChannel(self, self.data, self.name)
