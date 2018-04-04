from tkinter import Button
from tkinter.ttk import Button


from frontend.settings_window import SettingsWindow
from frontend.frames.studentlist import StudentList
from frontend.frames.actualdata import StudentData
from frontend.frames.staffmeetinglist import StaffMeetingList
from frontend.frames.application import Application



class MainWindow():
    def __init__(self, window):
        self.window = window

        self.studentframe = StudentList(self.window, text="Lista dzieci")
        self.studentframe.grid(row=2, column=0, rowspan=2)
        self.staffframe = StaffMeetingList(self.window, text="Lista zespołów")
        self.staffframe.grid(row=0, column=0, rowspan=2)
        self.settings = Button(self.window, text="Ustawienia", command=self.settingz)
        self.settings.grid(row=0, column=3)
        self.actual_student = StudentData(self.window, text="Dane dziecka")
        self.actual_student.grid(row=0, column=1)
        self.applicationframe = Application(self.window, text="Wnioskodawcy")
        self.applicationframe.grid(row=1, column=1)
        self.add_to_base = Button(self.window, text="Dodaj do bazy")
        self.add_to_base.grid(row=3, column=1)
        self.create_documents = Button(self.window, text="Twórz dokumenty")
        self.create_documents.grid(row=3, column=3)
    
    def settingz(self):
        win = SettingsWindow()
