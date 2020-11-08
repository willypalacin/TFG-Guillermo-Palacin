from tkinter import *
import tkinter as tk


class ConsoleView(tk.Frame):
    def __init__(self, mainWindow):
        super().__init__(mainWindow, background="black", width=mainWindow.winfo_width()/4)
        self.paintConsoleWindow(mainWindow)

    def paintConsoleWindow(self, mainWindow):

        self.pack(side = RIGHT, fill = Y)

        #self.place(relx = 0.5)


        #self.mainloop()
