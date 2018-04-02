from frontend.frames.studentlist import StudentList
from frontend.frames.actualdata import StudentData
from frontend.frames.staffmeetinglist import StaffMeetingList
from frontend.frames.application import Application


class MainWindow():
    def __init__(self, window):
        self.window = window

        self.studentframe = StudentList(self.window, text="Lista dzieci")
        self.studentframe.grid(row=0, column=0, rowspan=2)
        self.staffframe = StaffMeetingList(self.window, text="Lista zespołów")
        self.staffframe.grid(row=2, column=0)
        self.actual_student = StudentData(self.window, text="Dane dziecka")
        self.actual_student.grid(row=0, column=1)
        self.applicationframe = Application(self.window, text="Wnioskodawcy")
        self.applicationframe.grid(row=1, column=1)
