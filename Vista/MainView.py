import tkinter as tk
from tkinter import *


class MainView(tk.Tk):
    def __init__(self, mainViewController):
        tk.Tk.__init__(self)
        self.mainViewController = mainViewController
        self.devices = []
        self.configure(background='#4F535A')
        self.paintMainWindow()


    def hola(self):
        print("PULSADO")

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

        addDeviceBtn = Button(topFrame, height=26, width=26, borderwidth=0,command=self.hola, image=btnAddImg, padx=0,pady=0)
        addDeviceBtn.pack(side=LEFT)
        addDeviceBtn.image = btnAddImg

        removeDeviceBtn = Button(topFrame, height=26, width=26, borderwidth=0,command=self.hola, image=btnRemImg, padx=0,pady=0)
        removeDeviceBtn.pack(side=LEFT, padx= 20)
        removeDeviceBtn.image = btnRemImg

        mainFrame = Frame(leftFrame, background='white', highlightcolor="black", width=int(self.winfo_width()/1.5), height=int(self.winfo_height()/1.3))
        mainFrame.pack(expand=1, fill=BOTH, padx=40, pady=30)

        rightFrame = Frame(self, background="#4F535A", width=int(self.winfo_width()/2.5))
        rightFrame.pack(side=RIGHT, fill=Y)

        butonOptionsFrame = Frame(rightFrame,background="#4F535A",height=int(self.winfo_height()/2) ,width=int(self.winfo_width()/3.5),highlightbackground="white", highlightthickness=1)
        butonOptionsFrame.pack(side=TOP, fill=BOTH)

        showCurrentBtn = Button(butonOptionsFrame, borderwidth=0,command=self.hola, image=rightButtonsImg,highlightthickness=0, bd = 0)
        showCurrentBtn.image = rightButtonsImg
        showCurrentBtn.pack(pady=(40,20))

        showCurrentBtn = Button(butonOptionsFrame, borderwidth=0,command=self.hola, image=rightButtonsImg,highlightthickness=0, bd = 0)
        showCurrentBtn.image = rightButtonsImg
        showCurrentBtn.pack(pady=20)

        showCurrentBtn = Button(butonOptionsFrame, borderwidth=0,command=self.hola, image=rightButtonsImg,highlightthickness=0, bd = 0)
        showCurrentBtn.image = rightButtonsImg
        showCurrentBtn.pack(pady=(20,40))

        consoleView = Frame(rightFrame,background="black",width=int(self.winfo_width()/3.5),height=int(self.winfo_height()/2.7),highlightbackground="white", highlightthickness=1)
        consoleView.pack(side=BOTTOM, fill=BOTH, expand=1)






        #addDeviceButton = Button(frame1, text="Anadir Dispositivo", command=lambda: self.mainViewController.clickedAddDevice(self))
        #addDeviceButton.pack(side=LEFT)
        #self.paintDevice()

    def moveDevice(self, event, myCanvas,circle):
        component=event.widget
        locx, locy = component.winfo_x(), component.winfo_y()
        #w , h =self.winfo_width(),self.winfo_height()
        mx ,my =component.winfo_width(),component.winfo_height()
        xpos=(locx+event.x)
        ypos=(locy+event.y)
        myCanvas.place(x=xpos, y=ypos)


    def paintDevice(self):
        myCanvas = Canvas(self)

        circle = myCanvas.create_oval(100-50, 120-50,100+50, 120+50 ,fill="blue")
        myCanvas.pack()
        myCanvas.bind('<B1-Motion>', lambda event: self.moveDevice(event, myCanvas, circle))
        #devices.append(self.myCanvas)
