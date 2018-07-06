from tkinter import Button, Toplevel

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

from backend.database import DataBase
from backend.create import Decision
from backend.create_decree import Decree
from backend.create_protokol import Protokol
from frontend.frames.actualdata import StudentData
from frontend.frames.application import Application
from frontend.frames.staffframe import StaffFrame
from frontend.frames.studentdata import ListOfData


class MainWindow():
    def __init__(self, window):
        self.base = DataBase('database.db')
        # self.base.add_fake_data()
        self.window = window
        self.notebook = ListOfData(self.window, self.base, text="Baza danych")
        self.notebook.grid(row=0, column=0, rowspan=8, sticky='n', padx=5, pady=5)
        self.notebook.table.bind('<<TreeviewSelect>>', self.select_meeting)
        self.notebook.student_list.bind('<<TreeviewSelect>>', self.select_student)

        self.actual_student = StudentData(self.window, self.base, text="Dane dziecka")
        self.actual_student.grid(row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.applicationframe = Application(self.window, text="Wnioskodawcy")
        self.applicationframe.grid(row=1, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.staff_meeting_frame = StaffFrame(self.window, self.base, text="Zespół orzekający")
        self.staff_meeting_frame.grid(row=2, column=1, rowspan=6, sticky='w', padx=5, pady=5)
        self.add_to_base = Button(self.window, text="Zapisz", width=14, height=2, command=self.save_data)
        self.add_to_base.grid(row=2, column=2, sticky='w')
        self.clear_forms = Button(self.window, text="Wyczyść", width=14, height=2, command=self.clear)
        self.clear_forms.grid(row=3, column=2, sticky='w')
        self.create_decision = Button(self.window, text="Stwórz orzeczenie", width=14, height=2, command=self.issue_decision)
        self.create_decision.grid(row=4, column=2, sticky='w')
        self.create_protokol_button = Button(self.window, text="Stwórz zarządzenie", width=14, height=2, command=self.create_decree)
        self.create_protokol_button.grid(row=5, column=2, sticky='w')
        self.create_decree_button = Button(self.window, text="Stwórz protokół", width=14, height=2, command=self.create_protokol)
        self.create_decree_button.grid(row=6, column=2, sticky='w')
        self.close_button = Button(self.window, text="Zamknij", width=14, height=2, command=self.close)
        self.close_button.grid(row=7, column=2, sticky='w')
        self.staff_meeting_frame.insert_staff(self.base, staff={'team' : [], 'id' : ""})



        self.fake_data()
        self.notebook.fill_student_list()
        self.notebook.fill_staffmeeting_list()

    def save_data(self):
        '''
        Validate necessary content of actual_student() and
        applicationframe
        '''
        if self.validate_student_content():
            # braki w student content
            return 1
        '''
        Check if there is or isn't student pesel in student table
        and add or update student data accordingly

        '''
        if self.validate_staffmeeting_content():
            # braki w staff content
            return 1
        
        values = self.values()
        '''
        Update/Create student
        '''
        if not self.base.pesel_exists(values['pesel']):
            self.base.add_student_to_db(self.values())
        else:
            self.base.update_student(self.values())
        '''
        Update/create staffmeeting

        Staffmeeting is reconized as "the same" if its date,
        student and subject is the same

        '''
        if self.base.staffmeeting_exists(values):
            self.base.update_staffmeeting(values)
            # zaktualizowano staffmeeting
        else:
            self.base.add_staffmeeting(values)
            # dodano nowy staffmeeting
        self.notebook.fill_student_list()
        self.notebook.fill_staffmeeting_list()
    
    def clear(self):
        self.actual_student.clear()
        self.applicationframe.clear()
        self.staff_meeting_frame.clear()
        
    def issue_decision(self):
        if self.save_data():
            return
        create = Decision(self.values())
        create.issue()
        create.save()
        create.insert_footnotes()
    
    def create_decree(self):
        if self.save_data():
            return
        create = Decree(self.values())
        create.create()
        create.save()

    def create_protokol(self):
        if self.save_data():
            return
        create = Protokol(self.values())
        create.create()
        create.save()
    
    def close(self):
        self.window.destroy()
    
    def values(self):
        return dict(
            zip(
                [
                    "name_n",
                    "name_g",
                    "zip_code",
                    "city",
                    "address",
                    "pesel",
                    "birth_date",
                    "birth_place",
                    "casebook",
                    "subject",
                    "reason",
                    "applicant_n",
                    "applicant_g",
                    "applicant_zipcode",
                    "applicant_city",
                    "applicant_address",
                    "timespan",
                    "timespan_ind",
                    "staff_id",
                    "staff_meeting_date",
                    "staff",
                    "school_name",
                    "school_sort",
                    "school_address",
                    "school_city",
                    "class",
                    "profession",
                    "recommendations",
                    "footnotes"
                ],
                [
                    self.actual_student.name_of_student_n_entry.get(),
                    self.actual_student.name_of_student_g_entry.get(),
                    self.actual_student.zip_code_of_student_entry.get(),
                    self.actual_student.city_of_student_entry.get(),
                    self.actual_student.address_of_student_entry.get(),
                    self.actual_student.pesel_entry.get(),
                    self.actual_student.birth_date,
                    self.actual_student.birth_place_entry.get(),
                    self.actual_student.id_of_student_entry.get(),
                    self.applicationframe.application_subject.get(),
                    self.get_disability(
                        self.applicationframe.application_reason.get(),
                        self.applicationframe.application_reason2.get()
                        ),
                    self.applicationframe.name_of_applicant_n.get(),
                    self.applicationframe.name_of_applicant_g.get(),
                    self.applicationframe.zip_code.get(),
                    self.applicationframe.city.get(),
                    self.applicationframe.address.get(),
                    self.applicationframe.timespan.get(),
                    self.applicationframe.timespan_ind.get(),
                    self.staff_meeting_frame.staff_id,
                    self.staff_meeting_frame.data_entry.get(),
                    self.staff_list(),
                    self.base.get_school(self.actual_student.school.get())[1],
                    self.base.get_school(self.actual_student.school.get())[2],
                    self.base.get_school(self.actual_student.school.get())[3],
                    self.base.get_school(self.actual_student.school.get())[4],
                    self.actual_student.class_entry.get(),
                    self.actual_student.profession_entry.get(),
                    self.get_form_data(
                        self.applicationframe.application_subject.get()
                        )[0],
                    self.get_form_data(
                        self.applicationframe.application_subject.get()
                        )[1]
                ]
            )
        )

    def select_meeting(self, event):
        '''insert selected staffmeeting into form'''
        item = self.notebook.table.selection()
        parent = self.notebook.table.item(self.notebook.table.parent(item))['values']
        if parent:
            student_id = self.notebook.table.item(item)['values'][2]
            staff_id = self.notebook.table.item(item)['values'][1]
            staffmeeting_data = self.base.get_staffmeeting_data(staff_id)
            self.staff_meeting_frame.insert_staff(self.base, staffmeeting_data)
            self.actual_student.insert_actual_data(
                self.base.get_student_data(id=student_id)
                )
            self.applicationframe.insert_application_data(
                staffmeeting_data
                )
    
    def select_student(self, event):
        choosen = self.notebook.student_list.selection()
        student_pesel = str(self.notebook.student_list.item(choosen)['values'][1])
        if len(student_pesel) == 10:
            student_pesel = '0' + student_pesel
        elif len(student_pesel) == 9:
            student_pesel = '00' + student_pesel
        student_data = self.base.get_student_data(pesel=student_pesel)
        self.actual_student.insert_actual_data(student_data)
        
    def staff_list(self):
        staff_meeting_list = {'team': []}
        if (
            (not self.staff_meeting_frame.data_entry.get())
            or 
            (not self.staff_meeting_frame.table.get_children())
            ):
            # niewypełniony staff
            return staff_meeting_list
        '''Construct list of staff with specialization'''
        staff_meeting_list = {'team': []}
        for child in self.staff_meeting_frame.table.get_children():
            staff_meeting_list['team'].append(
                self.staff_meeting_frame.table.item(child)["values"]
                )
        
        '''Check sex of leader of the team'''
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
    
    def get_form_data(self, application_subject):
        if application_subject == "kształcenie specjalne":
            return [
                recommend_special_education,
                footnotes_special_education
                ]
        elif application_subject == "indywidualne roczne przygotowanie przedszkolne":
            return [
                recommend_individual_preschool,
                footnotes_individual_preschool
                ]
        elif application_subject == "indywidualne nauczanie":
            return [
                recommend_individual,
                footnotes_individual
                ]
        elif application_subject == "wczesne wspomaganie rozwoju":
            return [
                recommend_development_support,
                footnotes_development_support
                ]
        elif application_subject == "zajęcia rewalidacyjno-wychowawcze indywidualne":
            return [
                recommend_profound,
                footnotes_profound
                ]
        elif application_subject == "zajęcia rewalidacyjno-wychowawcze zespołowe":
            return [
                recommend_profound,
                footnotes_profound
                ]
        else:
            return [[],[]]
    
    
    def validate_student_content(self):
        if (
            self.actual_student.name_of_student_n_entry.get() and
            self.actual_student.pesel_entry.get() and
            self.actual_student.pesel_validation() and
            self.actual_student.class_entry.get() and
            self.actual_student.school.get() and
            self.applicationframe.application_subject.get() and
            self.applicationframe.application_reason.get() and
            (
                self.applicationframe.timespan.get() or
                self.applicationframe.timespan_ind.get()
            )
            ):
            return 0
        else:
            return 1    
    
    def validate_staffmeeting_content(self):
        if(
            self.staff_meeting_frame.data_entry.get() and
            self.staff_meeting_frame.table.get_children()
            ):
            return 0
        else:
            return 1

    def fake_data(self):
        self.actual_student.name_of_student_n_entry.insert('end', 'Jakub Rzeźniczak')
        self.actual_student.name_of_student_g_entry.insert('end', 'Jakuba Rzeźniczaka')
        self.actual_student.pesel_string.set("76020707430")
        self.actual_student.zip_code_of_student_entry.insert('end', '65-898')
        self.actual_student.city_of_student_entry.insert('end', 'Ugody')
        self.actual_student.birth_place_entry.insert('end', 'Trąbowo Dolne')
        self.actual_student.address_of_student_entry.insert('end', 'Zielona 29b/5')
        
        self.actual_student.school['values'] = self.base.select_school(self.base.sort_of_school()[1])
        self.actual_student.school.current(0)

        self.applicationframe.name_of_applicant_n.insert('end', 'Tomasz Rzeźniczak i Adelajda Kieł')
        self.applicationframe.name_of_applicant_g.insert('end', 'Tomasza Rzeźniczaka i Adelajdy Kieł')
        self.applicationframe.zip_code.insert('end', '65-898')
        self.applicationframe.city.insert('end', 'Ugody')
        self.applicationframe.address.insert('end', 'Zielona 29b/5')
        self.applicationframe.application_subject.current(0)
        # self.applicationframe.application_reason.current(0)
        self.applicationframe.timespan.current(1)
    