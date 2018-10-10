import re
from tkinter import Entry, Label, StringVar
from tkinter.ttk import Labelframe, Combobox

from backend.database import School


class StudentData(Labelframe):

    """Contains data of selected student"""

    def __init__(self, window, base, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.base = base
        self.pesel_string = StringVar()
        self.pesel_string.set('')
        self.pesel_string.trace('w', lambda *args: self.pesel_validation())
        self.birth_date = ""

        self.name_of_student_n_lab = Label(self, text="Imię i nazwisko (m)")
        self.name_of_student_n_lab.grid(
            row=0,
            column=0,
            sticky='e',
            padx=5,
            pady=5
        )
        self.name_of_student_n_entry = Entry(self, width=41)
        self.name_of_student_n_entry.grid(
            row=0,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky='w'
        )

        self.name_of_student_g_lab = Label(self, text="Imię i nazwisko (d)")
        self.name_of_student_g_lab.grid(
            row=1,
            column=0,
            sticky='e',
            padx=5,
            pady=5
        )
        self.name_of_student_g_entry = Entry(self, width=41)
        self.name_of_student_g_entry.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky='w'
        )

        self.pesel_lab = Label(self, text="PESEL")
        self.pesel_lab.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.pesel_entry = Entry(
            self,
            textvariable=self.pesel_string,
            width=12
        )
        self.pesel_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        self.id_of_student = Label(self, text="Teczka")
        self.id_of_student.grid(row=2, column=2, padx=5, pady=5, sticky='e')
        self.id_of_student_entry = Entry(self, width=7)
        self.id_of_student_entry.grid(row=2, column=3, padx=5, pady=5)

        self.birth_place_lab = Label(self, text="Miejsce urodzenia")
        self.birth_place_lab.grid(
            row=3,
            column=0,
            sticky='e',
            padx=5,
            pady=5
        )
        self.birth_place_entry = Entry(self, width=25)
        self.birth_place_entry.grid(
            row=3,
            column=1,
            sticky='w',
            padx=5,
            pady=5
        )

        self.city_of_student_lab = Label(self, text="Miejscowość")
        self.city_of_student_lab.grid(
            row=4,
            column=0,
            sticky='e',
            padx=5,
            pady=5
        )
        self.city_of_student_entry = Entry(self, width=25)
        self.city_of_student_entry.grid(
            row=4,
            column=1,
            sticky='w',
            padx=5,
            pady=5
        )

        self.zip_code_of_student_lab = Label(self, text="Kod")
        self.zip_code_of_student_lab.grid(
            row=4,
            column=2,
            padx=5,
            pady=5,
            sticky='e'
        )
        self.zip_code_of_student_entry = Entry(self, width=7)
        self.zip_code_of_student_entry.grid(row=4, column=3, padx=5, pady=5)

        self.address_of_student_lab = Label(self, text="Adres dziecka")
        self.address_of_student_lab.grid(
            row=5,
            column=0,
            sticky='e',
            padx=5,
            pady=5
        )
        self.address_of_student_entry = Entry(self, width=25)
        self.address_of_student_entry.grid(
            row=5,
            column=1,
            sticky='w',
            padx=5,
            pady=5
        )

        self.sort_of_school_lab = Label(self, text="Rodzaj szkoły")
        self.sort_of_school_lab.grid(
            row=6,
            column=0,
            sticky='e',
            padx=5,
            pady=5
        )
        self.sort_of_school_box = Combobox(
            self,
            postcommand=self.list_of_sorts,
            exportselection=False
        )
        self.sort_of_school_box.bind(
            "<<ComboboxSelected>>",
            self.clear_all_selection
        )
        self.sort_of_school_box.grid(
            row=6,
            column=1,
            sticky='w',
            padx=5,
            pady=5
        )

        self.school_lab = Label(self, text="Szkoła:")
        self.school_lab.grid(row=7, column=0, sticky='e', padx=5, pady=5)
        self.school = Combobox(
            self,
            width=40,
            postcommand=self.list_of_schools,
            exportselection=False
        )
        self.school.grid(
            row=7,
            column=1,
            columnspan=4,
            sticky='w',
            padx=5,
            pady=5
        )
        self.school.bind("<<ComboboxSelected>>", self.list_of_schools())

        self.profession_lab = Label(self, text="Zawód")
        self.profession_lab.grid(row=8, column=0, sticky='e', padx=5, pady=5)
        self.profession_entry = Entry(self, width=25)
        self.profession_entry.grid(row=8, column=1, sticky='w', padx=5, pady=5)

        self.class_lab = Label(self, text="Klasa")
        self.class_lab.grid(row=8, column=2, padx=5, pady=5, sticky='e')
        self.class_entry = Entry(self, width=7)
        self.class_entry.grid(row=8, column=3)

    def list_of_schools(self):
        sort = self.sort_of_school_box.get()
        self.school['values'] = [
            i.name
            for i in School.select().where(School.sort == sort)
        ]
        self.school.select_clear()

    def list_of_sorts(self):
        self.sort_of_school_box['values'] = sorted(
            i.sort for i in School.select().distinct()
        )

    def clear_all_selection(self, event):
        self.school.select_clear()
        self.sort_of_school_box.select_clear()

    def pesel_validation(self):
        # validation of number of digit
        pesel = str(self.pesel_string.get())
        if not (re.match('^[0-9]{4}[0-3]{1}[0-9]{6}$', pesel)):
            self.pesel_entry.config(background="red")
            return 1

        # validation of control digit and correct birth date
        cyfra_kontrolna = int(pesel[10])
        multiplier = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        suma = 0
        for i in range(0, 10):
            suma += int(pesel[i]) * multiplier[i]
        if suma % 10 == cyfra_kontrolna:
            self.pesel_entry.config(background="green")
            self.birth_date = self.birth_data_from_pesel(pesel)
            if self.birth_date == "wrong PESEL":
                self.pesel_entry.config(background="red")
                return 1
            return 0
        else:
            self.pesel_entry.config(background="red")
            self.birth_date = ""
            return 1

    def birth_data_from_pesel(self, pesel):
        if pesel[2] in ["0", "1"]:
            year = "19" + pesel[0:2]
            month = pesel[2:4]
        elif pesel[2] in ["2", "3"]:
            year = "20" + pesel[0:2]
            month = str(int(pesel[2:4]) - 20)
        elif pesel[2] in ["4", "5"]:
            year = "21" + pesel[0:2]
            month = str(int(pesel[2:4]) - 40)
        elif pesel[2] in ["6", "7"]:
            year = "22" + pesel[0:2]
            month = str(int(pesel[2:4]) - 60)
        elif pesel[2] in ["8", "9"]:
            year = "18" + pesel[0:2]
            month = str(int(pesel[2:4]) - 80)
        else:
            return "wrong PESEL"
        day = pesel[4:6]
        if 0 >= int(month) >= 13 or 0 >= int(day) >= 31:
            return "wrong PESEL"
        if len(month) == 1:
            month = "0" + month
        return ".".join([day, month, year])

    def insert_actual_data(self, student):
        '''insert data into form'''
        for key, entry in {
            'name_n': self.name_of_student_n_entry,
            'name_g': self.name_of_student_g_entry,
            'pesel': self.pesel_entry,
            'birth_place': self.birth_place_entry,
            'casebook': self.id_of_student_entry,
            'zip_code': self.zip_code_of_student_entry,
            'city': self.city_of_student_entry,
            'address': self.address_of_student_entry,
            'profession': self.profession_entry,
            'class_': self.class_entry,
            'school_sort': self.sort_of_school_box,
            'school_name': self.school
        }:
            entry.delete(0, 'end')
            entry.insert(0, getattr(student, key))

    def clear(self):
        for entry in [
            self.name_of_student_n_entry,
            self.name_of_student_g_entry,
            self.pesel_entry,
            self.birth_place_entry,
            self.id_of_student_entry,
            self.zip_code_of_student_entry,
            self.city_of_student_entry,
            self.address_of_student_entry,
            self.profession_entry,
            self.class_entry,
            self.sort_of_school_box,
            self.school
        ]:
            entry.delete(0, 'end')
