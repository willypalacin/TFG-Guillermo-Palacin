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
        self.clickLine = 0
        self.mouseX = 0
        self.mouseY = 0

    def paintMainWindow(self):
        self.title("TFG-Guillermo-Palacin")
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



        mainFrame = Canvas(leftFrame, background='white', highlightcolor="black", width=int(self.winfo_width()/1.5), height=int(self.winfo_height()/1.3))
        mainFrame.pack(expand=1, fill=BOTH, padx=40, pady=30)
        m = Menu(self, tearoff = False)
        m.add_command(label ="Añadir Linea", command = lambda: self.createLine())
        m.add_command(label ="Añadir Texto")
        m.add_separator()
        mainFrame.bind('<Button-2>', lambda event: self.showMenu(event,m))


        rightFrame = Frame(self, background="#4F535A", width=int(self.winfo_width()/2.5))
        rightFrame.pack(side=RIGHT, fill=Y)

        butonOptionsFrame = Frame(rightFrame,background="#4F535A",height=int() ,width=int(self.winfo_width()/3.5),highlightbackground="white", highlightthickness=1)
        butonOptionsFrame.pack(side=TOP, fill=BOTH)


        showConfigBtn = Button(butonOptionsFrame,borderwidth=0 ,height=50, width=225,command=self.mostrarConfig, image=rightButtonsImg)
        showConfigBtn["bg"] = "#4F535A"
        showConfigBtn["border"] = "0"
        showConfigBtn.pack(pady=(40,20))
        showConfigBtn.image = rightButtonsImg
        label = Label(butonOptionsFrame, text="Mostrar Configuracion", bg="#F2F2F2")
        label.place(relx=0.29, rely = 0.25)

        showCurrentBtn = Button(butonOptionsFrame, height=50, width=225, image=rightButtonsImg)
        showCurrentBtn.pack(pady=(20,40))
        showCurrentBtn["bg"] = "#4F535A"
        showCurrentBtn["border"] = "0"
        showCurrentBtn.image = rightButtonsImg
        label = Label(butonOptionsFrame, text="Guardar Configuracion", bg="#F2F2F2")
        label.place(relx=0.28, rely = 0.653)

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
            self.mainViewController.devices[dev] = {}


    def showMenu(self,event, m):
        try:
            m.tk_popup(event.x_root, event.y_root)
            self.mouseX = event.x_root
            self.mouseY = event.y_root
        finally:
            m.grab_release()

    def createLine(self):
        global x1, y1
        global numLin
        if self.clickLine == 0:
            print("entra")
            x1 = self.mouseX
            y1 = self.mouseY
            self.clickLine = 1
        else:
            x2 = self.mouseX
            y2 = self.mouseY
            self.clickLine = 0
            self.mainFrame.create_line(x1, y1, x2, y2, fill = "black", width = 1, tags="l")

            print("{}-{}  {}-{}".format(x1,y1,x2,y2))




    def paintDevice(self, name):
        myCanvas = Canvas(self.mainFrame, height=97, width=97, bg="white")
        myCanvas.place(x=50, y=50)
        circle = myCanvas.create_oval(3, 3,99,99 ,fill="#00A2FF",  outline='red', tags=name)
        m = Menu(myCanvas, tearoff = False)
        m.add_command(label ="Eliminar", command= lambda: myCanvas.delete(name))
        m.add_separator()
        myCanvas.create_text(50,50,text=name, font=("Andale Mono", 14), fill="white")
        myCanvas.bind('<B1-Motion>', lambda event: self.moveDevice(event, myCanvas, circle))
        myCanvas.bind('<Double-Button-1>', lambda event: self.mainViewController.clickedConfigurationDevice(self, event, name))
        myCanvas.bind('<Button-2>', lambda event: self.showMenu(event,m))
        self.devices.append(myCanvas)
        self.update()
