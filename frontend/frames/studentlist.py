from tkinter import  Button, LabelFrame, Label, Listbox
from tkinter.ttk import Button, Labelframe, Label


class StudentList(Labelframe):
    """Contains list of student in database"""
    def __init__(self, window, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.listbox = Listbox(self)
        self.listbox.grid(row=0, column=0)
        self.button = Button(self, text="Usuń wpis")
        self.button.grid(row=1, column=0)

