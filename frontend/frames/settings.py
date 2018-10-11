from tkinter import Button, Frame, LabelFrame, Text
from tkinter.font import Font
from tkinter.ttk import Treeview


class SettingsWindow:

    '''Toplevel widget for settings - name of center, specialist, schools'''

    def __init__(self, window, **kwargs):
        self.window = window
        self.my_font = Font(size=16)

        self.name_label_frame = LabelFrame(self.window, text="Nazwa poradni")
        self.name_label_frame.grid(row=0, column=0)

        self.name_text = Text(self.name_label_frame, height=5, width=57)
        self.name_text.grid(row=0, column=0)
        self.name_accept_button = Button(
            self.name_label_frame,
            text="Zachowaj"
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

    def close(self):
        self.window.destroy()
