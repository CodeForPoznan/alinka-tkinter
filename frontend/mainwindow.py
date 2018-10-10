from tkinter import Toplevel

from .values import (
    footnotes_development_support,
    footnotes_individual,
    footnotes_individual_preschool,
    footnotes_profound,
    footnotes_special_education,
    recommend_development_support,
    recommend_individual,
    recommend_individual_preschool,
    recommend_profound,
    recommend_special_education
)

from backend.database import DataBase, School, Student
from backend.create import Decision
from backend.create_decree import Decree
from backend.create_protokol import Protokol
from frontend.frames.actualdata import StudentData
from frontend.frames.buttons import ButtonFrame
from frontend.frames.application import Application
from frontend.frames.settings import SettingsWindow
from frontend.frames.staffframe import StaffFrame
from frontend.frames.studentdata import ListOfData


class MainWindow():

    def __init__(self, window):
        self.base = DataBase()
        self.window = window
        self.notebook = ListOfData(self.window, self.base, text="Baza danych")
        self.notebook.grid(row=0, column=0, rowspan=8, sticky='n', padx=5)
        self.notebook.table.bind('<<TreeviewSelect>>', self.select_meeting)
        self.notebook.student_list.bind(
            '<<TreeviewSelect>>',
            self.select_student
        )

        self.actual_student = StudentData(
            self.window,
            self.base,
            text="Dane dziecka"
        )
        self.actual_student.grid(
            row=0,
            column=1,
            sticky='wn',
            padx=5
        )
        self.applicationframe = Application(self.window, text="Wnioskodawcy")
        self.applicationframe.grid(
            row=1,
            column=1,
            sticky='w',
            padx=5
        )
        self.applicationframe.same.bind('<Button-1>', self.copy_address)
        self.staff_meeting_frame = StaffFrame(
            self.window,
            self.base,
            text="Zespół orzekający"
        )
        self.staff_meeting_frame.grid(
            row=0,
            column=2,
            rowspan=2,
            sticky='w',
            padx=5
        )

        self.staff_meeting_frame.insert_staff(
            self.base,
            staff={'team': [], 'id': ""}
        )

        self.button_frame = ButtonFrame(self.window, self.base)
        self.button_frame.grid(row=2, column=1, columnspan=2)

        self.button_frame.settings_button.bind('<Button-1>', self.settings)
        self.button_frame.save_button.bind('<Button-1>', self.save_data_event)
        self.button_frame.clear_button.bind('<Button-1>', self.clear)
        self.button_frame.create_decision_button.bind(
            '<Button-1>',
            self.issue_decision
        )
        self.button_frame.create_decree_button.bind(
            '<Button-1>',
            self.create_decree
        )
        self.button_frame.create_protokol_button.bind(
            '<Button-1>',
            self.create_protokol
        )
        self.button_frame.close_button.bind('<Button-1>', self.close)
        self.fake_data()
        self.notebook.fill_student_list()
        self.notebook.fill_staffmeeting_list()

    def save_data_event(self, event):
        self.save_data()

    def save_data(self):
        '''
        Validate necessary content of:
         actual_student, applicationframe, staffmeeting_frame
        '''
        valid_student_cont = self.validate_student_content()
        valid_staff_cont = self.validate_staffmeeting_content()
        if (valid_staff_cont or valid_student_cont):
            return 1

        values = self.values()

        # Update/Create student
        try:
            Student.get(Student.pesel == values['pesel'])
        except Student.DoesNotExist:
            self.base.add_student_to_db(self.values())
        else:
            self.base.update_student(self.values())

        # Update/create staffmeeting
        # Staffmeeting is reconized as "the same" if its date,
        # student and subject is the same
        if self.base.staffmeeting_exists(values):
            self.base.update_staffmeeting(values)
            # zaktualizowano staffmeeting
        else:
            self.base.add_staffmeeting(values)
            # dodano nowy staffmeeting
        self.notebook.fill_student_list()
        self.notebook.fill_staffmeeting_list()

    def clear(self, event):
        self.actual_student.clear()
        self.applicationframe.clear()
        self.staff_meeting_frame.clear()

    def issue_decision(self, event):
        if self.save_data():
            return
        create = Decision(self.values())
        create.issue()
        create.save()
        create.insert_footnotes()

    def create_decree(self, event):
        if self.save_data():
            return
        create = Decree(self.values())
        create.create()
        create.save()

    def create_protokol(self, event):
        if self.save_data():
            return
        create = Protokol(self.values())
        create.create()
        create.save()

    def close(self, event):
        self.window.destroy()

    def values(self):
        school = School.get(School.name == self.actual_student.school.get())
        return {
            'name_n': self.actual_student.name_of_student_n_entry.get(),
            'name_g': self.actual_student.name_of_student_g_entry.get(),
            'zip_code': self.actual_student.zip_code_of_student_entry.get(),
            'city': self.actual_student.city_of_student_entry.get(),
            'address': self.actual_student.address_of_student_entry.get(),
            'pesel': self.actual_student.pesel_entry.get(),
            'birth_date': self.actual_student.birth_date,
            'birth_place': self.actual_student.birth_place_entry.get(),
            'casebook': self.actual_student.id_of_student_entry.get(),
            'subject': self.applicationframe.application_subject.get(),
            'reason': self.get_disability(
                self.applicationframe.application_reason.get(),
                self.applicationframe.application_reason2.get()
            ),
            'applicant_n': self.applicationframe.name_of_applicant_n.get(),
            'applicant_g': self.applicationframe.name_of_applicant_g.get(),
            'applicant_zipcode': self.applicationframe.zip_code.get(),
            'applicant_city': self.applicationframe.city.get(),
            'applicant_address': self.applicationframe.address.get(),
            'timespan': self.applicationframe.timespan.get(),
            'timespan_ind': self.applicationframe.timespan_ind.get(),
            'staff_id': self.staff_meeting_frame.staff_id,
            'staff_meeting_date': self.staff_meeting_frame.data_entry.get(),
            'staff': self.staff_list(),
            'school_name': school.name,
            'school_sort': school.sort,
            'school_address': school.address,
            'school_city': school.zipcode,
            'class': self.actual_student.class_entry.get(),
            'profession': self.actual_student.profession_entry.get(),
            'recommendations': self.get_form_data(
                self.applicationframe.application_subject.get()
            )[0],
            'footnotes': self.get_form_data(
                self.applicationframe.application_subject.get()
            )[1]
        }

    def select_meeting(self, event):
        '''insert selected staffmeeting into form'''
        item = self.notebook.table.selection()
        parent = self.notebook.table.item(
            self.notebook.table.parent(item)
        )['values']
        if parent:
            student_id = self.notebook.table.item(item)['values'][2]
            staff_id = self.notebook.table.item(item)['values'][1]
            staffmeeting_data = self.base.get_staffmeeting_data(staff_id)
            self.staff_meeting_frame.insert_staff(
                self.base,
                staffmeeting_data
            )
            self.actual_student.insert_actual_data(
                Student.get(Student.id_ == student_id)
            )
            self.applicationframe.insert_application_data(
                staffmeeting_data
            )
            self.applicationframe.get_reason()

    def select_student(self, event):
        choosen = self.notebook.student_list.selection()
        student_pesel = str(
            self.notebook.student_list.item(choosen)['values'][1]
        )
        if len(student_pesel) == 10:
            student_pesel = '0' + student_pesel
        elif len(student_pesel) == 9:
            student_pesel = '00' + student_pesel
        student_data = Student.get(Student.pesel == student_pesel)
        self.actual_student.insert_actual_data(student_data)

    def copy_address(self, event):
        for i in [
                self.applicationframe.city,
                self.applicationframe.zip_code,
                self.applicationframe.address
        ]:
            i.delete(0, 'end')
        for x, y in zip([
            self.applicationframe.city,
            self.applicationframe.zip_code,
            self.applicationframe.address
        ], [
            self.actual_student.city_of_student_entry,
            self.actual_student.zip_code_of_student_entry,
            self.actual_student.address_of_student_entry
        ]):
            x.insert('end', y.get())

    def staff_list(self):
        staff_meeting_list = {'team': []}
        if (
            (not self.staff_meeting_frame.data_entry.get()) or
            (not self.staff_meeting_frame.table.get_children())
        ):
            # niewypełniony staff
            return staff_meeting_list

        # Construct list of staff with specialization
        staff_meeting_list = {'team': []}
        for child in self.staff_meeting_frame.table.get_children():
            staff_meeting_list['team'].append(
                self.staff_meeting_frame.table.item(child)["values"]
            )

        # Check sex of leader of the team
        if staff_meeting_list['team'][0][0].split(' ')[1][-1] == 'a':
            staff_meeting_list['team'][0][1] = "przewodnicząca zespołu"
        else:
            staff_meeting_list['team'][0][1] = "przewodniczący zespołu"
        return staff_meeting_list

    def get_disability(self, disability1, disability2):
        if len(disability2) < 3:
            disability2 = ""
        if disability1 != "" and disability2 == "":
            return [disability1, disability1, ""]
        if disability1 != "" and disability2 != "":
            return ["sprzężona", disability1, disability2]

    def get_form_data(self, subject):
        if subject == "kształcenie specjalne":
            return [
                recommend_special_education,
                footnotes_special_education
            ]
        if subject == "indywidualne roczne przygotowanie przedszkolne":
            return [
                recommend_individual_preschool,
                footnotes_individual_preschool
            ]
        if subject == "indywidualne nauczanie":
            return [
                recommend_individual,
                footnotes_individual
            ]
        if subject == "wczesne wspomaganie rozwoju":
            return [
                recommend_development_support,
                footnotes_development_support
            ]
        if subject == "zajęcia rewalidacyjno-wychowawcze indywidualne":
            return [
                recommend_profound,
                footnotes_profound
            ]
        if subject == "zajęcia rewalidacyjno-wychowawcze zespołowe":
            return [
                recommend_profound,
                footnotes_profound
            ]
        return [[], []]

    def validate_student_content(self):
        returned_value = 0
        for i, j in zip([
            self.actual_student.name_of_student_n_entry,
            self.actual_student.name_of_student_g_entry,
            self.actual_student.id_of_student_entry,
            self.actual_student.birth_place_entry,
            self.actual_student.school,
            self.applicationframe.application_subject,
            self.applicationframe.application_reason
        ], [
            self.actual_student.name_of_student_n_lab,
            self.actual_student.name_of_student_g_lab,
            self.actual_student.id_of_student,
            self.actual_student.birth_place_lab,
            self.actual_student.school_lab,
            self.applicationframe.application_subject_lab,
            self.applicationframe.application_reason_lab
        ]):
            if not i.get():
                j.config(fg='red')
                returned_value = 1
            else:
                j.config(fg='black')

        if self.actual_student.pesel_validation():
            returned_value = 1

        if self.applicationframe.application_subject.get() == \
                "kształcenie specjalne":
            if not self.applicationframe.timespan.get():
                self.applicationframe.timespan_lab.config(fg='red')
                returned_value = 1
            else:
                self.applicationframe.timespan_lab.config(fg='black')
        elif self.applicationframe.application_subject.get() in [
            "indywidualne roczne przygotowanie przedszkolne",
            "indywidualne nauczanie"
        ]:
            if not self.applicationframe.timespan_ind.get():
                self.applicationframe.timespan_lab.config(fg='red')
                returned_value = 1

        return returned_value

    def validate_staffmeeting_content(self):
        if (
            self.staff_meeting_frame.data_entry.get() and
            self.staff_meeting_frame.table.get_children()
        ):
            self.staff_meeting_frame.config(fg='black')
            return 0
        else:
            self.staff_meeting_frame.config(fg='red')
            return 1

    def settings(self, event):
        '''Toplevel window for setup'''
        new_window = Toplevel()
        new_window.title("Ustawienia")
        self.settings_window = SettingsWindow(new_window, self.base)

    def fake_data(self):
        self.actual_student.name_of_student_n_entry.insert(
            'end',
            'Jakub Rzeźniczak'
        )
        self.actual_student.name_of_student_g_entry.insert(
            'end',
            'Jakuba Rzeźniczaka'
        )
        self.actual_student.pesel_string.set("76020707430")
        self.actual_student.zip_code_of_student_entry.insert('end', '65-898')
        self.actual_student.city_of_student_entry.insert('end', 'Ugody')
        self.actual_student.birth_place_entry.insert('end', 'Trąbowo Dolne')
        self.actual_student.address_of_student_entry.insert(
            'end',
            'Zielona 29b/5'
        )
        self.actual_student.school['values'] = [
            i.name for i in School.select().where(
                School.sort == sorted(
                    i.sort for i in School.select().distinct()
                )[1]
            )
        ]
        self.actual_student.school.current(0)
        self.applicationframe.name_of_applicant_n.insert(
            'end',
            'Tomasz Rzeźniczak i Adelajda Kieł'
        )
        self.applicationframe.name_of_applicant_g.insert(
            'end',
            'Tomasza Rzeźniczaka i Adelajdy Kieł'
        )
        self.applicationframe.zip_code.insert('end', '65-898')
        self.applicationframe.city.insert('end', 'Ugody')
        self.applicationframe.address.insert('end', 'Zielona 29b/5')
        self.applicationframe.application_subject.current(0)
        self.applicationframe.timespan.current(1)
