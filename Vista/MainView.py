
from tkinter import *


class MainView(Tk):
    def __init__(self, mainViewController):
        Tk.__init__(self)
        self.mainViewController = mainViewController
        self.paintMainWindow()


    def paintMainWindow(self):
        self.title("Network define")
        self.geometry("1280x1000")
        self.update()
        frame1 = LabelFrame(self,text="Menu", background='white', height=5, relief=RIDGE, highlightcolor="black", highlightbackground="black", pady=1, bd=5 )

        frame1.pack(side=TOP, fill=X)

        applyButton = Button(frame1, text="Apply")
        applyButton.pack(side=RIGHT, padx=80)
        syncButton = Button(frame1, text="Sync")
        syncButton.pack(side=RIGHT)

        addDeviceButton = Button(frame1, text="Anadir Dispositivo", command=lambda: self.mainViewController.clickedAddDevice(self))
        addDeviceButton.pack(side=LEFT)
