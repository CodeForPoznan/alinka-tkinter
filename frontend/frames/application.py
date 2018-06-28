from tkinter import Button, Checkbutton, Entry, Label, LabelFrame
from tkinter.ttk import Button, Checkbutton, Combobox, Entry, Label, Labelframe, Style

from frontend.values import reasons, application, timespan


class Application(Labelframe):
    """Contains data reffering to application"""
    def __init__(self, window, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.name_of_applicant_n_lab = Label(self, text="Wnioskodawcy (mianownik)")
        self.name_of_applicant_n_lab.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='e')
        self.name_of_applicant_n = Entry(self, width = 40)
        self.name_of_applicant_n.grid(row=0, column=3, columnspan=4, padx=5, pady=5, sticky='w')

        self.name_of_applicant_g_lab = Label(self, text="Wnioskodawcy (dopełniacz)")
        self.name_of_applicant_g_lab.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='e')
        self.name_of_applicant_g = Entry(self, width = 40)
        self.name_of_applicant_g.grid(row=1, column=3, columnspan=4, padx=5, pady=5, sticky='w')
        
        self.zip_code_lab = Label(self, text="Kod")
        self.zip_code_lab.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.zip_code = Entry(self, width=7)
        self.zip_code.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        self.city_lab = Label(self, text="Miejscowość")
        self.city_lab.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.city = Entry(self, width=20)
        self.city.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        self.address_lab = Label(self,text="Adres")
        self.address_lab.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.address = Entry(self)
        self.address.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        self.application_subject_lab = Label(self, text="           Wniosek o")
        self.application_subject_lab.grid(row=2, column=3, padx=5, pady=5)
        self.application_subject = Combobox(self, width=40, values=application)
        self.application_subject.grid(row=2, column=4, columnspan=3, padx=5, pady=5)
        
        self.application_reason_lab = Label(self, text="Z uwagi na")
        self.application_reason_lab.grid(row=3, column=3, padx=5, pady=5, sticky='e')
        self.application_reason = Combobox(self, width=40, postcommand=self.get_reason, exportselection=False)
        self.application_reason.grid(row=3, column=4, columnspan=2, padx=5, pady=5)
        self.application_reason2_lab = Label(self, text="Z uwagi na")
        self.application_reason2_lab.grid(row=4, column=3, padx=5, pady=5, sticky='e')
        self.application_reason2 = Combobox(self, width=40, values=reasons)
        self.application_reason2.grid(row=4, column=4, columnspan=2, padx=5, pady=5)

        self.timespan_lab = Label(self, text="Na okres")
        self.timespan_lab.grid(row=5, column=3, padx=5, pady=5, sticky='e')
        self.timespan = Combobox(self, values=timespan)
        self.timespan.grid(row=5, column=4, pady=5)
        self.timespan_ind = Entry(self, width=18)
        self.timespan_ind.grid(row=5, column=5, pady=5)
    
    def get_reason(self):
        if self.application_subject.get() == "kształcenie specjalne":
            self.application_reason['values'] = reasons[0:-2]
            self.application_reason2['values'] = reasons[0:-2]
        if self.application_subject.get() in [
            "indywidualne roczne przygotowanie przedszkolne",
            "indywidualne nauczanie"
            ]:
            self.application_reason['values'] = reasons[-2:]
        if self.application_subject.get() in [
            "zajęcia rewalidacyjno-wychowawcze indywidualne",
            "zajęcia rewalidacyjno-wychowawcze zespołowe"
            ]:
            self.application_reason['values'] = (reasons[3],)
        if self.application_subject.get() == "wczesne wspomaganie rozwoju":
            self.application_reason['values'] = reasons[:9]
        
    def insert_application_data(self, student):
        for entry, key in zip(
            [
                self.name_of_applicant_n,
                self.name_of_applicant_g,
                self.zip_code,
                self.city,
                self.address,
                self.application_subject,
                self.application_reason,
                self.application_reason2,
                self.timespan,
                self.timespan_ind
            ],
            [
                'applicant_n',
                'applicant_g',
                'applicant_zipcode',
                'applicant_city',
                'applicant_address',
                'subject',
                'reason',
                'reason2',
                'timespan',
                'timespan_ind'
            ]
            ):
            entry.delete(0, 'end')
            entry.insert(0, student[key])

    def clear(self):
        for entry in [
            self.name_of_applicant_n,
            self.name_of_applicant_g,
            self.zip_code,
            self.city,
            self.address,
            self.application_subject,
            self.application_reason,
            self.application_reason2,
            self.timespan,
            self.timespan_ind
            ]:
            entry.delete(0, 'end')
