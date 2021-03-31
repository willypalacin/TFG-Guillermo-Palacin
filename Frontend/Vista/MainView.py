import tkinter as tk
from tkinter import *


class MainView(tk.Tk):
    def __init__(self, mainViewController):
        tk.Tk.__init__(self)
        self.mainViewController = mainViewController
        self.devices = []
        self.configure(background='#4F535A')
        self.consoleView = None
        self.errorMessagesLabels = []
        self.mainFrame = self.paintMainWindow()
        self.prueba = 1


    def paintMainWindow(self):
        self.title("Network define")
        self.geometry("1700x1000")
        #self.attributes("-fullscreen", True)
        #self.resizable(width=False, height=False)
        self.update()

        btnAddImg = PhotoImage(file = 'Vista/assets/btn_anadir.png')
        btnRemImg = PhotoImage(file = 'Vista/assets/btn_eliminar.png')
        rightButtonsImg = PhotoImage(file = 'Vista/assets/right_buttons.png')

        leftFrame = Frame(self, background="#4F535A", pady=20)
        leftFrame.pack(side=LEFT)
        topFrame = Frame(leftFrame,background='#4F535A',width=self.winfo_width()/1.5)
        topFrame.pack(side=TOP, expand=1, fill=X, padx=39)

        addDeviceBtn = Button(topFrame, height=26, width=26, borderwidth=0,command=lambda:self.mainViewController.clickedAddDevice(self), image=btnAddImg, padx=0,pady=0)
        addDeviceBtn.pack(side=LEFT)
        addDeviceBtn.image = btnAddImg

        removeDeviceBtn = Button(topFrame, height=26, width=26, borderwidth=0,command=self.mostrarConfig, image=btnRemImg, padx=0,pady=0)
        removeDeviceBtn.pack(side=LEFT, padx= 20)
        removeDeviceBtn.image = btnRemImg

        mainFrame = Frame(leftFrame, background='white', highlightcolor="black", width=int(self.winfo_width()/1.5), height=int(self.winfo_height()/1.3))
        mainFrame.pack(expand=1, fill=BOTH, padx=40, pady=30)


        rightFrame = Frame(self, background="#4F535A", width=int(self.winfo_width()/2.5))
        rightFrame.pack(side=RIGHT, fill=Y)

        butonOptionsFrame = Frame(rightFrame,background="#4F535A",height=int() ,width=int(self.winfo_width()/3.5),highlightbackground="white", highlightthickness=1)
        butonOptionsFrame.pack(side=TOP, fill=BOTH)

        showConfigBtn = Button(butonOptionsFrame, text="Mostrar Configuración",borderwidth=0,command=self.mostrarConfig, image=rightButtonsImg,highlightthickness=0, bd = 0, fg="black", compound='center', font=("Helvetica", 15))
        showConfigBtn.image = rightButtonsImg
        showConfigBtn.pack(pady=(40,20))

        showCurrentBtn = Button(butonOptionsFrame, borderwidth=0,command=self.mostrarConfig, image=rightButtonsImg,highlightthickness=0, bd = 0)
        showCurrentBtn.image = rightButtonsImg
        showCurrentBtn.pack(pady=20)

        showCurrentBtn = Button(butonOptionsFrame, borderwidth=0,command=self.mostrarConfig, image=rightButtonsImg,highlightthickness=0, bd = 0)
        showCurrentBtn.image = rightButtonsImg
        showCurrentBtn.pack(pady=(20,40))

        self.consoleView = Frame(rightFrame,background="black",width=int(self.winfo_width()/3.5),height=int(self.winfo_height()/2.7),highlightbackground="white", highlightthickness=1)

        labelConsole =  Label(self.consoleView, text="—————————————————  Consola  —————————————————", fg="White", bg='black',font=("Helvetica", 12))
        labelConsole.pack(side=TOP)

        self.consoleView.pack(side=BOTTOM, fill=BOTH, expand=1)

        return mainFrame

    def addMessageToConsole(self, text, color):
        label = Label(self.consoleView, text=text, fg=color, bg='black',font=("Helvetica", 12))
        label.pack(side=BOTTOM)
        self.errorMessagesLabels.append(label)

        for errorMsg in self.errorMessagesLabels:
            errorMsg.pack_forget()

        for errorMsg in reversed(self.errorMessagesLabels):
            errorMsg.pack(side=BOTTOM)
        self.consoleView.update()



    def moveDevice(self, event, myCanvas,circle):
        component=event.widget
        locx, locy = component.winfo_x(), component.winfo_y()
        #w , h =self.winfo_width(),self.winfo_height()
        mx ,my =component.winfo_width(),component.winfo_height()
        xpos=(locx+event.x)
        ypos=(locy+event.y)
        myCanvas.place(x=xpos, y=ypos)


    def mostrarConfig(self):
        self.mainViewController.clickedMostrarConfiguracion(self)



    def paintDevice(self, name):
        myCanvas = Canvas(self.mainFrame, height=97, width=97, bg="white")
        myCanvas.place(x=50, y=50)
        circle = myCanvas.create_oval(3, 3,99,99 ,fill="#00A2FF",  outline='red')
        myCanvas.create_text(50,50,text=name, font=("Andale Mono", 16), fill="white")
        myCanvas.bind('<B1-Motion>', lambda event: self.moveDevice(event, myCanvas, circle))
        myCanvas.bind('<Double-Button-1>', lambda event: self.mainViewController.clickedConfigurationDevice(self, event, name))
        self.devices.append(myCanvas)
        self.update()
        #devices.append(self.myCanvas)
