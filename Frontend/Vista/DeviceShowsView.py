from tkinter import *
from tkinter import ttk
import tkinter as tk




class DeviceShowsView(tk.Toplevel):
    def __init__(self, rootWindow,controller, data, tituloRow, mainTitle, row, col):
        super().__init__(rootWindow, height=570, width=600, bg="white", highlightbackground="#00A2FF", highlightthickness=4)
        self.controller = controller
        self.tituloRow = tituloRow
        self.mainTitle = mainTitle
        self.data = data
        self.resizable(width=True, height=True)
        #self.configure(background="#D9D9D9")
        self.geometry("670x500")
        self.title("{}".format(self.mainTitle))
        self.update()
        self.createView()




    def createView(self):
        imgBtnAccept = PhotoImage(file = 'Vista/assets/btn_accept_config.png')
        imgBtnCancel = PhotoImage(file = 'Vista/assets/btn_cancel_config.png')
        imgLineaBg = PhotoImage(file = 'Vista/assets/linea_bg.png')
        self.image = imgLineaBg

        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        j = 1
        Label(scrollable_frame, text="{}".format(self.mainTitle),font="-family {Andale Mono} -size 20").grid(column=2, row=0, columnspan=5)

        for device in self.data:
            labl = Label(scrollable_frame, text="{}".format(device))
            labl.configure(font="-family {Andale Mono} -size 15")
            labl.grid(column=2, row=j, pady=20)
            j = j+1
            i = 0
            line = 0
            for header in self.tituloRow:
                labl = Label(scrollable_frame, text="{}".format(header))
                labl.configure(font=('Helvetica', 12, 'bold'))
                labl.grid(column=i, row=j)

                aux = j + 1
                for line in self.data[device]:
                    labl = Label(scrollable_frame, text="{}".format(str(line[self.tituloRow[header]])))
                    labl.configure(font=('Andale Mono', 11))
                    labl.grid(column=i, row=aux )
                    aux = aux +1
                i = i +1
            j = aux

            i = 0



        #container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill="y")
