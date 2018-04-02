from tkinter import Button, Label, LabelFrame, Listbox
from tkinter.ttk import Button, Label, Labelframe


class StaffMeetingList(Labelframe):
    """Contains data of selected student"""
    def __init__(self, window, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.listbox = Listbox(self)
        self.listbox.grid(row=0, column=0, columnspan=2)
        self.button1 = Button(self, text="Dodaj zespół")
        self.button1.grid(row=1, column=0)
        self.button2 = Button(self, text="Usuń zespół")
        self.button2.grid(row=1,column=1)
