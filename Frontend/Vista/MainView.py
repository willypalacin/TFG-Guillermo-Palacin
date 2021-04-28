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

        btnAddImg = PhotoImage(file = 'Vista/assets/btn_router.png')
        btnRemImg = PhotoImage(file = 'Vista/assets/btn_delete.png')
        btnSyncImg = PhotoImage(file = 'Vista/assets/btn_sync.png')
        rightButtonsImg = PhotoImage(file = 'Vista/assets/right_buttons.png')

        leftFrame = Frame(self, background="#4F535A", pady=20)
        leftFrame.pack(side=LEFT)
        topFrame = Frame(leftFrame,background='#4F535A',width=self.winfo_width()/1.5)
        topFrame.pack(side=TOP, expand=1, fill=X, padx=39)

        addDeviceBtn = Button(topFrame, height=58, width=58, borderwidth=0,command=lambda:self.mainViewController.clickedAddDevice(self), image=btnAddImg, padx=0,pady=0)
        addDeviceBtn.pack(side=LEFT)
        addDeviceBtn.image = btnAddImg

        syncDeviceBtn = Button(topFrame, height=58, width=58, borderwidth=0,command=self.syncButton, image=btnSyncImg, padx=0,pady=0)
        syncDeviceBtn.pack(side=LEFT, padx= 20)
        syncDeviceBtn.image = btnSyncImg

        removeDeviceBtn = Button(topFrame, height=58, width=58, borderwidth=0,command=self.mostrarConfig, image=btnRemImg, padx=0,pady=0)
        removeDeviceBtn.pack(side=LEFT, padx=0 )
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

        showCurrentBtn = Button(butonOptionsFrame,text="Exportar Template" ,borderwidth=0,command=self.mostrarConfig, image=rightButtonsImg,highlightthickness=0, bd = 0, fg="black", compound='center', font=("Helvetica", 15))
        showCurrentBtn.image = rightButtonsImg
        showCurrentBtn.pack(pady=20)

        showCurrentBtn = Button(butonOptionsFrame,text="Importar Configuracion" ,borderwidth=0,command=self.mostrarConfig, image=rightButtonsImg,highlightthickness=0, bd = 0, fg="black", compound='center', font=("Helvetica", 15))
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

    def syncButton(self):
         imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
         imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
         top = Toplevel(self)
         top.geometry("400x190")
         top.resizable(width=False, height=False)
         titLabel = Label(top)
         titLabel.pack(side=TOP, pady=15)
         titLabel.configure(font="-family {Andale Mono} -size 18", text="Sincronizar dispositivos")

         ipBackendLabel = Label(top)
         ipBackendLabel.pack(pady=10)
         ipBackendLabel.configure(font="-family {Andale Mono} -size 12", text="Introducir IP:puerto Backend")

         self.ipEntry = Entry(top)
         self.ipEntry.pack(pady=5)
         self.ipEntry.configure(background="#ABE0FF")
         self.ipEntry.insert(END, 'http://127.0.0.1:5000/')

         frame = Frame(top)
         frame.pack(side=BOTTOM, pady=(0,10))


         btnAccept = tk.Button(frame,
                     text='Accept',
                     image=imgBtnAccept, compound='center',
                     fg="white", font=("Andale Mono", 10),
                     command=lambda:self.syncClick())
         btnAccept.pack(side=LEFT, padx=(50, 40))
         btnAccept.image = imgBtnAccept

         btnCancel = tk.Button(frame, text='Cancel',
                            image=imgBtnCancel,font=("Andale Mono", 10) ,
                            compound='center', fg="white", command=lambda: self.destroy())
         btnCancel.image = imgBtnCancel
         btnCancel.pack(side=RIGHT, padx=(10, 50))

    def syncClick(self):
        devices = self.mainViewController.getSyncDevices(self.ipEntry.get())
        for dev in devices:
            self.paintDevice(dev)

    def drawLine(self,event):
        x, y = event.x, event.y
        if canvas.oldCoords:
            x1, y1 = canvas.oldCoords
            canvas.create_line(x, y, x1, y1)
        canvas.oldCoords = x, y

    def paintDevice(self, name):
        myCanvas = Canvas(self.mainFrame, height=97, width=97, bg="white")
        myCanvas.place(x=50, y=50)
        circle = myCanvas.create_oval(3, 3,99,99 ,fill="#00A2FF",  outline='red')
        myCanvas.create_text(50,50,text=name, font=("Andale Mono", 16), fill="white")
        myCanvas.old_coords = None
        myCanvas.bind('<B1-Motion>', lambda event: self.moveDevice(event, myCanvas, circle))
        myCanvas.bind('<Double-Button-1>', lambda event: self.mainViewController.clickedConfigurationDevice(self, event, name))
        myCanvas.bind('<Motion>', lambda event: self.drawLine(event))
        self.devices.append(myCanvas)
        self.update()
        #devices.append(self.myCanvas)
