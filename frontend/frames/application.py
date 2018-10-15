from tkinter import Label
from tkinter.ttk import Button, Combobox, Entry, Labelframe

from backend.models import StaffMeeting
from frontend.values import reasons, application, timespan


class Application(Labelframe):

    """Contains data reffering to application"""

    def __init__(self, window, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.name_of_applicant_n_lab = Label(self, text="Wnioskodawcy (m)")
        self.name_of_applicant_n_lab.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky='e'
        )
        self.name_of_applicant_n = Entry(self, width=40)
        self.name_of_applicant_n.grid(
            row=0,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky='w'
        )

        self.name_of_applicant_g_lab = Label(self, text="Wnioskodawcy (d)")
        self.name_of_applicant_g_lab.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky='e'
        )
        self.name_of_applicant_g = Entry(self, width=40)
        self.name_of_applicant_g.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky='w'
        )

        self.city_lab = Label(self, text="Miejscowość")
        self.city_lab.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.city = Entry(self, width=20)
        self.city.grid(
            row=3,
            column=1,
            columnspan=2,
            padx=5,
            pady=5,
            sticky='w'
        )

        self.zip_code_lab = Label(self, text="Kod")
        self.zip_code_lab.grid(row=3, column=2, padx=5, pady=5, sticky='e')
        self.zip_code = Entry(self, width=7)
        self.zip_code.grid(row=3, column=3, padx=5, pady=5, sticky='w')

        self.address_lab = Label(self, text="Adres")
        self.address_lab.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.address = Entry(self)
        self.address.grid(
            row=4,
            column=1,
            columnspan=2,
            padx=5,
            pady=5,
            sticky='w'
        )

        self.same = Button(self, text="Adres jak wyżej")
        self.same.grid(row=4, column=2, columnspan=2)

        self.application_subject_lab = Label(self, text="           Wniosek o")
        self.application_subject_lab.grid(
            row=6,
            column=0,
            padx=5,
            pady=5,
            sticky='e'
        )
        self.application_subject = Combobox(self, width=40, values=application)
        self.application_subject.grid(
            row=6,
            column=1,
            columnspan=3,
            padx=5,
            pady=5
        )
        self.application_subject.bind(
            '<<ComboboxSelected>>',
            self.choosed_subject
        )

        self.application_reason_lab = Label(self, text="Z uwagi na")
        self.application_reason_lab.grid(
            row=7,
            column=0,
            padx=5,
            pady=5,
            sticky='e'
        )
        self.application_reason = Combobox(
            self,
            width=40,
            postcommand=self.get_reason,
            exportselection=False
        )
        self.application_reason.bind(
            '<<ComboboxSelected>>',
            self.clear_all_selection
        )
        self.application_reason.grid(
            row=7,
            column=1,
            columnspan=3,
            padx=5,
            pady=5
        )
        self.application_reason2_lab = Label(self, text="Z uwagi na")
        self.application_reason2_lab.grid(
            row=8,
            column=0,
            padx=5,
            pady=5,
            sticky='e'
        )
        self.application_reason2 = Combobox(self, width=40, values=reasons)
        self.application_reason2.bind(
            '<<ComboboxSelected>>',
            self.clear_all_selection
        )
        self.application_reason2.grid(
            row=8,
            column=1,
            columnspan=3,
            padx=5,
            pady=5
        )

        self.timespan_lab = Label(self, text="Na okres")
        self.timespan_lab.grid(row=9, column=0, padx=5, pady=5, sticky='e')
        self.timespan = Combobox(self, values=timespan)
        self.timespan.bind('<<ComboboxSelected>>', self.clear_all_selection)
        self.timespan.grid(row=9, column=1, pady=5, padx=5, sticky='w')
        self.timespan_ind = Entry(self, width=18)
        self.timespan_ind.grid(
            row=9,
            column=2,
            columnspan=2,
            padx=5,
            pady=5,
            sticky='w'
        )

    def get_reason(self):
        if self.application_subject.get() == "kształcenie specjalne":
            self.application_reason['values'] = reasons[0:-2]
            self.application_reason2['values'] = reasons[0:-2]
            self.timespan_ind.config(state='disabled')
            self.timespan.config(state='active')
            self.application_reason2.config(state='active')
        if self.application_subject.get() in [
            "indywidualne roczne przygotowanie przedszkolne",
            "indywidualne nauczanie"
        ]:
            self.application_reason['values'] = reasons[-2:]
            self.timespan.config(state='disabled')
            self.timespan_ind.config(state='active')
            self.application_reason2.config(state='disabled')
        if self.application_subject.get() in [
            "zajęcia rewalidacyjno-wychowawcze indywidualne",
            "zajęcia rewalidacyjno-wychowawcze zespołowe"
        ]:
            self.application_reason['values'] = (reasons[3],)
            self.timespan.config(state='disabled')
            self.timespan_ind.config(state='disabled')
            self.application_reason2.config(state='disabled')
        if self.application_subject.get() == "wczesne wspomaganie rozwoju":
            self.application_reason['values'] = reasons[:9]
            self.timespan_ind.config(state='disabled')
            self.timespan.config(state='active')
            self.timespan['values'] = [timespan[4]]
            self.application_reason2.config(state='disabled')
        self.application_subject.select_clear()

    def clear_all_selection(self, event):
        self.application_subject.select_clear()
        self.application_reason.select_clear()
        self.application_reason2.select_clear()
        self.timespan.select_clear()

    def choosed_subject(self, event):
        actual_reason = self.application_reason.get()
        self.get_reason()
        supposed_reason = self.application_reason['values']
        if actual_reason not in supposed_reason:
            self.application_reason.delete(0, 'end')

    def insert_application_data(self, staffmeeting_id):
        staff_meeting = StaffMeeting.get(StaffMeeting.id == staffmeeting_id)
        self.update_entry(self.application_subject, staff_meeting.subject)
        self.update_entry(self.name_of_applicant_n, staff_meeting.applicant_n)
        self.update_entry(self.name_of_applicant_g, staff_meeting.applicant_g)
        self.update_entry(self.zip_code, staff_meeting.applicant_zipcode)
        self.update_entry(self.city, staff_meeting.applicant_city)
        self.update_entry(self.address, staff_meeting.applicant_address)
        self.update_entry(self.timespan, staff_meeting.timespan)
        self.update_entry(self.timespan_ind, staff_meeting.timespan_ind)

        reason = staff_meeting.reason.split(',')
        if len(reason[1]) < 2:
            reason[1] = ''
        self.update_entry(self.application_reason, reason[0])
        self.update_entry(self.application_reason2, reason[1])

    @staticmethod
    def update_entry(entry, value):
        entry.delete(0, 'end')
        entry.insert(0, value)

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
