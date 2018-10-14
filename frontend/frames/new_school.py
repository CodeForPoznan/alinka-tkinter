from tkinter import Button, Entry, Frame, Label, LabelFrame
from tkinter.ttk import Combobox

from backend.database import School


class NewSchool():
    def __init__(self, window):
        self.window = window
        self.school_frame = LabelFrame(self.window, text="Dodaj szkołę")
        self.school_frame.grid(row=0, column=0, columnspan=2)

        self.name_label = Label(self.school_frame, text="Nazwa szkoły:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(self.school_frame)
        self.name_entry.grid(row=1, column=0)
        self.sort_label = Label(self.school_frame, text="Rodzaj szkoły:")
        self.sort_label.grid(row=2, column=0)
        self.sort_box = Combobox(self.school_frame)
        self.sort_box.grid(row=3, column=0)
        self.address_label = Label(self.school_frame, text="adres i numer")
        self.address_label.grid(row=4, column=0)
        self.address_entry = Entry(self.school_frame)
        self.address_entry.grid(row=5, column=0)
        self.zipcode_label = Label(
            self.school_frame,
            text="Kod pocztowy i miejscowość"
        )
        self.zipcode_label.grid(row=6, column=0)
        self.zipcode_entry = Entry(self.school_frame)
        self.zipcode_entry.grid(row=7, column=0)

        self.save_button = Button(self.window, text="Zapisz")
        self.save_button.grid(row=1, column=0)
        self.discard_button = Button(
            self.window,
            text="Anuluj",
            command=self.window.destroy
            )
        self.discard_button.grid(row=1, column=1)
