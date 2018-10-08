import os

from tkinter import Button, font, Frame, PhotoImage


class ButtonFrame(Frame):
    '''Frame with buttons'''

    width = 31
    height = 31

    def __init__(self, window, base, **kwargs):
        super().__init__(window, **kwargs)
        self.base = base
        self.font = font.Font(size=16)

        module_directory = os.path.dirname(os.path.abspath(__file__))
        wheel = PhotoImage(file=os.path.join(module_directory, "wheel.png"))
        eraser = PhotoImage(file=os.path.join(module_directory, "eraser.png"))
        floppy = PhotoImage(file=os.path.join(module_directory, "floppy.png"))
        exit = PhotoImage(file=os.path.join(module_directory, "exit.png"))

        self.settings_button = Button(self, image=wheel)
        self.settings_button.image = wheel
        self.settings_button.config(width=self.width, height=self.height)
        self.settings_button.grid(row=0, column=0)
        self.save_button = Button(self, image=floppy)
        self.save_button.image = floppy
        self.save_button.config(width=self.width, height=self.height)
        self.save_button.grid(row=0, column=1)
        self.clear_button = Button(self, image=eraser)
        self.clear_button.image = eraser
        self.clear_button.config(width=self.width, height=self.height)
        self.clear_button.grid(row=0, column=2)
        self.create_decision_button = Button(
            self,
            text="Orzeczenie",
            font=self.font
        )
        self.create_decision_button.grid(row=0, column=3, padx=(30, 0))
        self.create_decree_button = Button(
            self,
            text="Zarządzenie",
            font=self.font
            )
        self.create_decree_button.grid(row=0, column=4)
        self.create_protokol_button = Button(
            self,
            text="Protokół",
            font=self.font
            )
        self.create_protokol_button.grid(row=0, column=5, padx=(0, 30))
        self.close_button = Button(self, image=exit)
        self.close_button.image = exit
        self.close_button.config(width=self.width, height=self.height)
        self.close_button.grid(row=0, column=6)
