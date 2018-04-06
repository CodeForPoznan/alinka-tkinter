from tkinter import Button, Entry, LabelFrame, Label, Listbox, Toplevel
from tkinter.ttk import Button, Entry, Labelframe, Label, Treeview


class SettingsWindow():
    def __init__(self, **kwargs):
        self.window = Toplevel()
        self.staff_frame =  Labelframe(self.window, text="Pracownicy poradni")
        self.staff_frame.grid(row=0, column=0)

        self.name_lab = Label(self.staff_frame, text="Imię i nazwisko")
        self.name_lab.grid(row=0, column=0)
        self.name_entry = Entry(self.staff_frame, width=27)
        self.name_entry.grid(row=0, column=1)
        
        self.speciality_lab = Label(self.staff_frame, text="Specjalność")
        self.speciality_lab.grid(row=0, column=2)
        self.speciality_entry = Entry(self.staff_frame, width=27)
        self.speciality_entry.grid(row=0, column=3)

        self.add_new = Button(self.staff_frame, text="Dodaj", command=self.insert_into_tree)
        self.add_new.grid(row=0, column=4)        

        self.box = Treeview(self.staff_frame, columns=["1", "2"])
        self.box.heading("#0", text="Nr")
        self.box.heading("#1", text="Imię i nazwisko")
        self.box.heading("#2", text="Specjalność")
        self.box.column("#0", width=30)
        self.box.column("#1", width=300)
        self.box.column("#2", width=300)
        self.box.grid(row=1, column=0, columnspan=5)

    def insert_into_tree(self):
        
        self.box.insert('', 'end', text="nr_jeden", values=(self.name_entry.get(), self.speciality_entry.get()))
    
