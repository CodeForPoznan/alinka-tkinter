from tkinter import Button, Checkbutton, Entry, Label, LabelFrame
from tkinter.ttk import Button, Checkbutton, Entry, Label, Labelframe


class Application(Labelframe):
    """Contains data reffering to application"""
    def __init__(self, window, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.name_of_applicant_n_lab = Label(self, text="Wnioskodawcy (mianownik)")
        self.name_of_applicant_n_lab.grid(row=0, column=0)
        self.name_of_applicant_n = Entry(self, width = 40)
        self.name_of_applicant_n.grid(row=0, column=1, columnspan=4)

        self.name_of_applicant_g_lab = Label(self, text="Wnioskodawcy (dopełniacz)")
        self.name_of_applicant_g_lab.grid(row=1, column=0)
        self.name_of_applicant_g = Entry(self, width = 40)
        self.name_of_applicant_g.grid(row=1, column=1, columnspan=4)

        self.the_same_button = Button(self, text="Adres jak wyżej")
        self.the_same_button.grid(row=2, column=0)
        
        self.zip_code_lab = Label(self, text="Kod")
        self.zip_code_lab.grid(row=2, column=1)
        self.zip_code = Entry(self, width=7)
        self.zip_code.grid(row=2, column=2)

        self.address_lab = Label(self,text="Adres")
        self.address_lab.grid(row=2, column=3)
        self.address = Entry(self)
        self.address.grid(row=2, column=4)