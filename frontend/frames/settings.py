import os
from configparser import ConfigParser

from tkinter import Button, END, Entry, Frame, LabelFrame, StringVar, Toplevel
from tkinter.font import Font
from tkinter.ttk import Treeview


class SettingsWindow():
    '''Toplevel widget for settings - name of center, specialist, schools'''
    def __init__(self, window, base, **kwargs):
        self.window = window
        self.base = base
        self.config = self.read_config()
        self.name = StringVar()
        self.name.trace('w', self.track_changes)
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
        self.staff_table.column('#1', width=200)
        self.staff_table.column('#2', width=200)
        self.staff_table['show'] = 'headings'

        self.staff_buttons = Frame(self.staff_label_frame)
        self.staff_buttons.grid(row=1, column=0)

        self.new_specialist_button = Button(self.staff_buttons, text="Nowy")
        self.new_specialist_button.grid(row=0, column=0)
        self.edit_specialist_button = Button(
            self.staff_buttons,
            text="Edytuj"
        )
        self.edit_specialist_button.grid(row=0, column=1)
        self.delete_specialist_button = Button(
            self.staff_buttons,
            text="Usuń"
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
        self.school_table.column('#1', width=200)
        self.school_table.column('#2', width=200)
        self.school_table['show'] = 'headings'

        self.school_buttons = Frame(self.school_label_frame)
        self.school_buttons.grid(row=1, column=0)

        self.new_school_button = Button(self.school_buttons, text="Dodaj")
        self.new_school_button.grid(row=0, column=0)
        self.edit_school_button = Button(self.school_buttons, text="Edytuj")
        self.edit_school_button.grid(row=0, column=1)
        self.delete_school_button = Button(self.school_buttons, text="Usuń")
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

    def track_changes(self, event, *args):
        '''track if name in entry has been changed'''
        if 'name' in self.config.items():
            if self.name.get() == self.config['name']:
                self.name_accept_button.config(state='disabled')
            else:
                self.name_accept_button.config(state='active')

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

    def close(self):
        self.window.destroy()
