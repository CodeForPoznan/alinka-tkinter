from tkinter.ttk import Button, Frame, Labelframe, Notebook, Treeview

from backend.database import StaffMeeting


class ListOfData(Labelframe):

    """Contains list of student in database"""

    def __init__(self, window, base, **kwargs):
        Labelframe.__init__(self, window, **kwargs)
        self.base = base
        self.notebook = Notebook(self)
        self.notebook.grid(row=0, column=0, padx=5, pady=5)

        self.student = Frame(self.notebook)
        self.student.grid(row=0, column=0)
        self.student_list = Treeview(
            self.student,
            height=24,
            columns=("name", "pesel"),
            displaycolumns="name"
        )
        self.student_list.heading('name', text="Nazwisko i imię", anchor='w')
        self.student_list.column('name', width=240)
        self.student_list['show'] = 'headings'
        self.student_list.grid(row=0, column=0)

        self.button = Button(
            self.student,
            text="Usuń",
            command=self.delete_from_student_list
        )
        self.button.grid(row=1, column=0)

        self.staff_meeting = Frame(self.notebook)
        self.staff_meeting.grid(row=0, column=0)
        self.table = Treeview(
            self.staff_meeting,
            height=24,
            columns=("name", "id", "student_id"),
            displaycolumns="name"
        )
        self.table.heading('name', text='Zespoły', anchor='w')
        self.table.column('name', width=235)
        self.table.column('#0', stretch=0, width=10)
        self.table.grid(row=0, column=0)
        self.delete_staffmeeting = Button(
            self.staff_meeting,
            text="Usuń wpis",
            command=self.delete_from_staffmeeting
        )
        self.delete_staffmeeting.grid(row=1, column=0)

        self.notebook.add(self.student, text="Dzieci")
        self.notebook.add(self.staff_meeting, text="Zespoły")

    def get_students(self):
        return self.base.get_dict_of_students()

    def get_pesel_from_name(self, name):
        students = self.get_students()
        for pesel in students:
            if students[pesel] == name:
                return pesel

    def fill_student_list(self):
        self.student_list.delete(*self.student_list.get_children())
        if not self.get_students():
            return

        for student, pesel in zip(
            self.get_students().values(),
            self.get_students().keys()
        ):
            self.student_list.insert("", 'end', values=(student, pesel))

    def delete_from_student_list(self):
        selected_item = self.student_list.selection()
        pesel = str(self.student_list.item(selected_item)['values'][1])
        if len(pesel) < 11:
            pesel = "0" + pesel
        self.base.delete_student(pesel)
        self.fill_student_list()
        self.fill_staffmeeting_list()

    def fill_staffmeeting_list(self):
        self.table.delete(*self.table.get_children())
        staff_meeting = StaffMeeting.select()
        meeting_in_table = {}  # {value: iid}
        for i in staff_meeting:
            if i.date not in meeting_in_table.keys():
                meeting_in_table[i.date] = self.table.insert(
                    "",
                    'end',
                    values=(i.date,)
                )
                actual_iid = self.table.insert(
                    meeting_in_table[i.date],
                    'end',
                    values=(self.base.get_student_name(i.student),)
                )
                self.table.set(actual_iid, column="id", value=i.id)
                self.table.set(
                    actual_iid,
                    column="student_id",
                    value=i.student
                )
            else:
                actual_iid = self.table.insert(
                    meeting_in_table[i.date],
                    'end',
                    values=(self.base.get_student_name(i.student),)
                )
                self.table.set(actual_iid, column="id", value=i[0])
                self.table.set(actual_iid, column="student_id", value=i[20])
        for idd in meeting_in_table.values():
            if not self.table.parent(idd):
                self.table.item(idd, open=True)

    def delete_from_staffmeeting(self):
        selected_item = self.table.selection()
        staffmeeting_id = self.table.item(selected_item)['values'][1]
        StaffMeeting.get(StaffMeeting.id == staffmeeting_id).delete_instance()
        self.fill_staffmeeting_list()
