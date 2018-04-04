from tkinter import Button, Entry, Label, LabelFrame
from tkinter.ttk import Button, Entry, Label, Labelframe, Combobox, Separator

class StudentData(Labelframe):
    """Contains data of selected student"""
    def __init__(self, window, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.name_of_student_n_lab = Label(
            self, 
            text="Imię i nazwisko dziecka (mianownik)"
            )
        self.name_of_student_n_lab.grid(row=0, column=0, columnspan=2)
        self.name_of_student_n_entry = Entry(self, width=40)
        self.name_of_student_n_entry.grid(row=0, column=2, columnspan=2)

        self.name_of_student_g_lab = Label(
            self,
            text="Imię i nazwisko dziecka (dopełniacz)"
            )
        self.name_of_student_g_lab.grid(row=1, column=0, columnspan=2)
        self.name_of_student_g_entry = Entry(self, width=40)
        self.name_of_student_g_entry.grid(row=1,column=2, columnspan=2)

        self.pesel_lab = Label(self, text="PESEL")
        self.pesel_lab.grid(row=2,column=0)
        self.pesel_entry = Entry(self, width=12)
        self.pesel_entry.grid(row=2, column=1)

        self.birth_place_lab = Label(self, text="Miejsce urodzenia")
        self.birth_place_lab.grid(row=2, column=2)
        self.birth_place_entry = Entry(self)
        self.birth_place_entry.grid(row=2, column=3)

        self.zip_code_of_student_lab = Label(self, text="Kod")
        self.zip_code_of_student_lab.grid(row=4, column=0)
        self.zip_code_of_student_entry = Entry(self, width=7)
        self.zip_code_of_student_entry.grid(row=4, column=1)

        self.address_of_student_lab = Label(
            self,
            text="Adres dziecka"
            )
        self.address_of_student_lab.grid(row=4, column=2)
        self.address_of_student_entry = Entry(self)
        self.address_of_student_entry.grid(row=4, column=3)

        # self.line = Separator(self, orient="horizontal")
        # self.line.grid(row=5, column=0)

        self.sort_of_school_lab = Label(self, text="Rodzaj szkoły")
        self.sort_of_school_lab.grid(row=6, column=0)
        self.sort_of_school_box = Combobox(self)
        self.sort_of_school_box.grid(row=6, column=1)

        self.city_of_school_lab = Label(self, text="Miejscowość")
        self.city_of_school_lab.grid(row=6, column=2)
        self.city_of_scholl_box = Combobox(self)
        self.city_of_scholl_box.grid(row=6, column=3)

        self.school_lab = Label(self, text="Szkoła:")
        self.school_lab.grid(row=7, column=0)
        self.school = Combobox(self)
        self.school.grid(row=7, column=1)
        
        self.button = Button(self, text="jjjj")
        self.button.grid(row=8, column=0)
