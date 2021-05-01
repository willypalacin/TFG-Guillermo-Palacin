
from tkinter import *
from tkinter import ttk
import tkinter as tk


class DeviceConfigStaticRoutingView(tk.Toplevel):
    def __init__(self, rootWindow,controller, name, dataIntf):
        super().__init__(rootWindow, height=673, width=762, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.name = name
        self.dataIntf = dataIntf
        self.resizable(width=True, height=True)
        #self.configure(background="#D9D9D9")
        self.geometry("322x450")
        self.title("Config Routing Statico de {}.".format(name))
        self.update()
        self.createView(name)


    def createView(self, name):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        titLabel = Label(self)
        titLabel.place(relx=0.09, rely=0.079, height=19, width=300)
        titLabel.configure(font="-family {Andale Mono} -size 15")
        titLabel.configure(text="Routing estático")


        self.redEntry = tk.Entry(self)
        self.redEntry.place(relx=0.146, rely=0.267, height=25, relwidth=0.323)

        self.redEntry.configure(font="-family {Andale Mono} -size 12", background="#ABE0FF")


        labelDestino = tk.Label(self)
        labelDestino.place(relx=0.342, rely=0.178, height=25, width=84)
        labelDestino.configure(font="-family {Andale Mono} -size 12")
        labelDestino.configure(text="Red Destino")

        aux = tk.Label(self)
        aux.place(relx=0.559, rely=0.267, height=19, width=15)
        aux.configure(font="TkDefaultFont")
        aux.configure(text="/")

        self.maskEntry = tk.Entry(self)
        self.maskEntry.place(relx=0.652, rely=0.267, height=25, relwidth=0.075)
        self.maskEntry.configure(background="#ABE0FF")

        labelAux = tk.Label(self)
        labelAux.place(relx=0.3, rely=0.356, height=21, width=120)
        labelAux.configure(text="IP Next Gateway", font="-family {Andale Mono}")

        self.nexGwEntry = tk.Entry(self)
        self.nexGwEntry.place(relx=0.311, rely=0.444, height=25, relwidth=0.323)
        self.nexGwEntry.configure(background="#ABE0FF")
        self.nexGwEntry.configure(font="TkFixedFont")

        labelIntf = tk.Label(self)
        labelIntf.place(relx=0.31, rely=0.533, height=21, width=130)
        labelIntf.configure(text='Interfaz de Salida', font="-family {Andale Mono} -size 12")

        self.comboIntf = ttk.Combobox(self)
        self.comboIntf.place(relx=0.28, rely=0.6, relheight=0.047
                , relwidth=0.382)
        self.comboIntf.configure(values=self.dataIntf)


        metricaLabel = tk.Label(self)
        metricaLabel.place(relx=0.373, rely=0.689, height=21, width=54)
        metricaLabel.configure(font="-family {Andale Mono} -size 12")
        metricaLabel.configure(text='Metrica')

        self.metricaEntry = tk.Entry(self)
        self.metricaEntry.place(relx=0.404, rely=0.756, height=25, relwidth=0.106)
        self.metricaEntry.configure(font="-family {Andale Mono} -size 12", background="#ABE0FF")

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
        btnCancel.place(relx=0.55, rely=0.94)


    def acceptClick(self):
        data = {
                "red": '{}/{}'.format(self.redEntry.get(), self.maskEntry.get()),
                "gw": '{}'.format(self.nexGwEntry.get()),
                "intf": '{}'.format(self.comboIntf.get()),
                "metric": '{}'.format(self.metricaEntry.get())
        }
        print(data)

        self.controller.createStaticRouting(self, data, self.name)
