from tkinter import Button, LabelFrame, Label, Listbox, Toplevel
from tkinter.ttk import Button, Labelframe, Label, Treeview


class SettingsWindow():
    def __init__(self, **kwargs):
        self.window = Toplevel()
        self.staff_frame =  Labelframe(self.window, text="Pracownicy poradni")
        self.staff_frame.grid(row=0, column=0)

        self.box = Treeview(self.staff_frame, columns=("1", "2"))
        self.box.heading("1", text="Imię i nazwisko")
        self.box.heading("2", text="Specjalność")
        self.box.grid(row=0, column=0)
        self.add_new = Button(self.staff_frame, text="Nowy pracownik")
        self.add_new.grid(row=1, column=0)
