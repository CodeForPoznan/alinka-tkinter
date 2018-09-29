from tkinter import Button, font, Frame, PhotoImage

class ButtonFrame(Frame):
    '''Frame with buttons'''
    def __init__(self, window, base, **kwargs):
        Frame.__init__(self, window, **kwargs)
        self.base = base
        self.wheel = PhotoImage(file="./frontend/frames/wheel.png")
        self.eraser = PhotoImage(file="./frontend/frames/eraser.png")
        self.floppy = PhotoImage(file="./frontend/frames/floppy.png")
        self.exit = PhotoImage(file="./frontend/frames/exit.png")
        self.font = font.Font(size=16)
        self.width = 31
        self.height = 31

        self.settings_button = Button(self, image=self.wheel)
        self.settings_button.config(width=self.width, height=self.height)
        self.settings_button.grid(row=0, column=0)
        self.save_button = Button(self, image=self.floppy)
        self.save_button.config(width=self.width, height=self.height)
        self.save_button.grid(row=0, column=1)
        self.clear_button = Button(self, image=self.eraser)
        self.clear_button.config(width=self.width, height=self.height)
        self.clear_button.grid(row=0, column=2)

        self.decision_create = Button(self, text="Orzeczenie", font=self.font)
        self.decision_create.grid(row=0, column=3, padx=(30, 0))
        self.decree_create = Button(self, text="Zarządzenie", font=self.font)
        self.decree_create.grid(row=0, column=4)
        self.protokol_create = Button(self, text="Protokół", font=self.font)
        self.protokol_create.grid(row=0, column=5, padx=(0, 30))
        self.close_button = Button(self, image=self.exit)
        self.close_button.config(width=self.width, height=self.height)
        self.close_button.grid(row=0, column=6)


