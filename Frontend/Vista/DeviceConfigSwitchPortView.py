from tkinter import *
from tkinter import ttk
import tkinter as tk


class DeviceConfigSwitchPortView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, dataIntf):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.dataIntf = dataIntf
        self.resizable(width=True, height=True)
        #self.configure(background="#D9D9D9")
        self.geometry("400x380")
        self.title("Config SwitchPort de {}.".format(name))
        self.update()
        self.createView(name)


    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        titLabel = Label(self)
        titLabel.place(relx=0.12, rely=0.079, height=19, width=300)
        titLabel.configure(font="-family {Andale Mono} -size 15")
        titLabel.configure(text="Configuracion de enlaces")

        self.intCombo = ttk.Combobox(self)
        self.intCombo.place(relx=0.325, rely=0.263, relheight=0.06
                , relwidth=0.333)
        self.intCombo.configure(takefocus="")
        self.intCombo.configure(values=self.dataIntf, state='readonly', font="-family {Andale Mono} -size 10")
        self.intCombo.current(0)

        labelInt = Label(self)
        labelInt.place(relx=0.375, rely=0.184, height=19, width=84)
        labelInt.configure(font="-family {Andale Mono} -size 12")
        labelInt.configure(text="Interfaz")

        labelModo = tk.Label(self)
        labelModo.place(relx=0.4, rely=0.368, height=19, width=64)
        labelModo.configure(font="-family {Andale Mono} -size 12")
        labelModo.configure(text="Modo")

        self.modeCombo = ttk.Combobox(self)
        self.modeCombo.place(relx=0.375, rely=0.447, relheight=0.055
                , relwidth=0.233)
        self.modeCombo.configure(values=["access", "trunk"])
        self.modeCombo.current(0)

        vlanLabel = tk.Label(self)
        vlanLabel.place(relx=0.275, rely=0.579, height=21, width=200)
        vlanLabel.configure(font="-family {Andale Mono} -size 12")
        vlanLabel.configure(text="VLAN(s) permitidas (,) (-)")

        self.vlanEntry = tk.Entry(self)
        self.vlanEntry.place(relx=0.4, rely=0.658, height=25, relwidth=0.21)
        self.vlanEntry.configure(background="#ABE0FF")
        self.vlanEntry.configure(font="-family {Andale Mono} -size 12")

        btnAccept = tk.Button(self,
                    text='Accept',
                    image=imgBtnAccept, compound='center',
                    fg="white", font=("Andale Mono", 10),
                    command=lambda:self.acceptClick())
        btnAccept.image = imgBtnAccept
        btnAccept.place(relx=0.3, rely=0.84)
        btnCancel = tk.Button(self, text='Cancel',
                           image=imgBtnCancel,font=("Andale Mono", 10) ,
                           compound='center', fg="white", command=lambda: self.destroy())
        btnCancel.image = imgBtnCancel
        btnCancel.place(relx=0.5, rely=0.84)

    def acceptClick(self):
        data = {}
        data[self.intCombo.get()]= {
                "mode": '{}'.format(self.modeCombo.get()),
                "vlans": '{}'.format(self.vlanEntry.get())
        }
        print(data)

        self.controller.createSwitchPort(self, data, self.name)
