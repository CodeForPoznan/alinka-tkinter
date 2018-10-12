<<<<<<< HEAD
import os
from configparser import ConfigParser

from tkinter import Button, END, Entry, Frame, Label, LabelFrame, StringVar, Toplevel
=======
from tkinter import Button, Frame, LabelFrame, Text
>>>>>>> master
from tkinter.font import Font
from tkinter.ttk import Combobox, Treeview

from backend.database import School, Staff


class SettingsWindow:

    '''Toplevel widget for settings - name of center, specialist, schools'''

    def __init__(self, window, **kwargs):
        self.window = window
<<<<<<< HEAD
        self.base = base
        self.config = self.read_config()
        self.name = StringVar()
        self.name.trace('w', self.track_changes)
=======
>>>>>>> master
        self.my_font = Font(size=16)

        self.name_label_frame = LabelFrame(self.window, text="Nazwa poradni")
        self.name_label_frame.grid(row=0, column=0)
        self.name_text = Entry(
            self.name_label_frame,
            width=50,
            textvariable=self.name
        )
        self.name_text.grid(row=0, column=0)
        self.name_accept_button = Button(
            self.name_label_frame,
            text="Zachowaj",
            command=self.save_config_data
        )
        self.name_accept_button.grid(row=1, column=0)

        self.staff_label_frame = LabelFrame(self.window, text="Specjaliści")
        self.staff_label_frame.grid(row=1, column=0)

        self.staff_table = Treeview(
            self.staff_label_frame,
            columns=("name", "speciality")
        )
        self.staff_table.grid(row=0, column=0)
        self.staff_table.heading("#1", text="imię i nazwisko")
        self.staff_table.heading('#2', text="specjalizacja")
        self.staff_table.column('#1', width=300)
        self.staff_table.column('#2', width=300)
        self.staff_table['show'] = 'headings'
        # self.staff_table.bind('<FocusOut>', self.after_staff_selection)

        self.staff_buttons = Frame(self.staff_label_frame)
        self.staff_buttons.grid(row=1, column=0)

        self.new_specialist_button = Button(self.staff_buttons, text="Nowy")
        self.new_specialist_button.grid(row=0, column=0)
        self.edit_specialist_button = Button(
            self.staff_buttons,
            text="Edytuj",
            state='disabled'
        )
        self.edit_specialist_button.grid(row=0, column=1)
        self.delete_specialist_button = Button(
            self.staff_buttons,
            text="Usuń",
            state='disabled'
        )
        self.delete_specialist_button.grid(row=0, column=2)

        self.school_label_frame = LabelFrame(self.window, text="Szkoły")
        self.school_label_frame.grid(row=2, column=0)

        self.school_table = Treeview(
            self.school_label_frame,
            columns=("name", "sort")
        )
        self.school_table.grid(row=0, column=0)
        self.school_table.heading("#1", text="nazwa szkoły")
        self.school_table.heading('#2', text="rodzaj szkoły")
        self.school_table.column('#1', width=450)
        self.school_table.column('#2', width=150)
        self.school_table['show'] = 'headings'

        self.school_buttons = Frame(self.school_label_frame)
        self.school_buttons.grid(row=1, column=0)

        self.new_school_button = Button(self.school_buttons, text="Dodaj", command=self.add_new_school)
        self.new_school_button.grid(row=0, column=0)
        self.edit_school_button = Button(self.school_buttons, text="Edytuj", state='disabled')
        self.edit_school_button.grid(row=0, column=1)
        self.delete_school_button = Button(self.school_buttons, text="Usuń", state='disabled')
        self.delete_school_button.grid(row=0, column=2)

        self.close_button = Button(
            self.window,
            text="Zamknij",
            font=self.my_font,
            width=20,
            command=self.close
        )
        self.close_button.grid(row=3, column=0)

        self.insert_config_data(self.config)
        self.insert_staff_from_DB_to_Table()
        self.insert_schools_from_DB_to_Table()

    def track_changes(self, event, *args):
        '''track if name of Support Center has been changed'''
        if 'name' in self.config.items():
            if self.name.get() == self.config['name']:
                self.name_accept_button.config(state='disabled')
            else:
                self.name_accept_button.config(state='active')

    def insert_config_data(self, config):
        for fieldname, value in config.items():
            if fieldname == "name":
                self.name.set(value)

    def save_config_data(self):
        config_dir = os.path.dirname(os.path.abspath(__name__))
        config_file = "alinka.ini"
        file = open(os.path.join(config_dir, config_file), 'w')
        config = ConfigParser()
        config.add_section('Center')
        config.set('Center', 'name', self.name.get())
        config.write(file)
        self.name_accept_button['state'] = 'disabled'

    def read_config(self):
        init = {}
        directory = os.path.dirname(os.path.abspath(__name__))
        init_file = os.path.join(directory, "alinka.ini")
        config = ConfigParser()
        config.read(init_file)
        sections = config.sections()
        if not sections:
            return {}
        else:
            for section in sections:
                options = config.options(section)
                for option in options:
                    init[option] = config.get(section, option)
        return init

    def insert_staff_from_DB_to_Table(self):
        for teacher in Staff.select():
            self.staff_table.insert('', 'end', values=(teacher.name, teacher.speciality))
    
    def insert_schools_from_DB_to_Table(self):
        for school in School.select():
            self.school_table.insert('', 'end', values=(school.name, school.sort))

    def add_new_school(self):
        new_school_window = Toplevel()
        new_school_window.title("Dodaj szkołę")
        school_frame = LabelFrame(new_school_window, text="Dodaj szkołę")
        school_frame.grid(row=0, column=0, columnspan=2)

        name_label = Label(school_frame, text="Nazwa szkoły:")
        name_label.grid(row=0, column=0)
        name_entry = Entry(school_frame)
        name_entry.grid(row=1, column=0)
        sort_label = Label(school_frame, text="Rodzaj szkoły:")
        sort_label.grid(row=2, column=0)
        sort_box = Combobox(school_frame)
        sort_box.grid(row=3, column=0)
        sort_box['values'] = ('tralalala', 'bucik')
        address_label = Label(school_frame, text="adres i numer")
        address_label.grid(row=4, column=0)
        address_entry = Entry(school_frame)
        address_entry.grid(row=5, column=0)
        zipcode_label = Label(school_frame, text="Kod pocztowy i miejscowość")
        zipcode_label.grid(row=6, column=0)
        zipcode_entry = Entry(school_frame)
        zipcode_entry.grid(row=7, column=0)

        save_button = Button(new_school_window, text="Zapisz")
        save_button.grid(row=1, column=0)
        discard_button = Button(
            new_school_window,
            text="Anuluj"
            # command=new_school_window.destroy()
            )
        discard_button.grid(row=1, column=1)

        
    
    def close(self):
        self.window.destroy()
