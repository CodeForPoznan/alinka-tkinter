from tkinter import Button, LabelFrame, Listbox
from tkinter.ttk import Entry, Label, Treeview

from backend.database import Staff, StaffMeeting


class StaffFrame(LabelFrame):

    """Contains data of staffmeeteng"""

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)
        self.staff_id = None
        self.all_staff = [i.name for i in Staff.select()]
        self.data_label = Label(self, text="Data zespołu")
        self.data_label.grid(row=0, column=0, padx=5, pady=1, sticky='e')
        self.data_entry = Entry(self, width=20)
        self.data_entry.grid(row=0, column=1, padx=5, pady=1, sticky='w')

        self.table = Treeview(self, columns=("name", "speciality"))
        self.table.heading('#1', text='imię i nazwisko')
        self.table.heading('#2', text='specjalizacja')
        self.table.column('#1', width=200)
        self.table.column('#2', width=200)

        self.table.grid(
            row=1,
            column=0,
            rowspan=1,
            columnspan=2,
            padx=5,
            pady=5
        )
        self.table['show'] = 'headings'
        self.table.bind('<<TreeviewSelect>>', self.on_treeview_selected)

        self.another_stuff_frame = LabelFrame(self, text="Inni specjaliści")
        self.another_stuff_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.another_staff = Listbox(
            self.another_stuff_frame,
            width=48,
            height=12
        )
        self.another_staff.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        self.another_staff.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.add_button = Button(
            self,
            text="Dodaj członka",
            command=self.add_member
        )
        self.add_button.grid(row=3, column=0, padx=5, pady=5)
        self.delete_button = Button(
            self,
            text="Usuń członka",
            command=self.remove_member
        )
        self.delete_button.grid(row=3, column=1, padx=5, pady=5)

    def get_staff_from_table(self):
        '''return list of member of staff_meeting from table
        eg. [[name, speciality],[name, speciality]]'''
        staff_meeting_list = []
        for child in self.table.get_children():
            staff_meeting_list.append(
                self.table.item(child)["values"]
            )
        return staff_meeting_list

    def insert_staff(self, staffmeeting_id=None):
        self.staff_id = staffmeeting_id

        if staffmeeting_id is None:
            self.tables_tidying()
            return

        staff_meeting = StaffMeeting.get(StaffMeeting.id == staffmeeting_id)
        self.data_entry.delete(0, 'end')
        self.data_entry.insert(0, staff_meeting.date)
        self.table.delete(*self.table.get_children())
        self.another_staff.delete(0, 'end')

        for i in range(1, 10):
            member = getattr(staff_meeting, 'member{}'.format(i))
            if member is not None:
                staff = Staff.get(id=member)
                self.table.insert('', 'end', values=(
                    staff.name,
                    staff.speciality
                ))
        self.tables_tidying()

    def on_listbox_select(self, event):
        '''Remove selection from table after clicking listbox.'''
        if self.table.selection():
            self.table.selection_remove(self.table.selection()[0])

    def on_treeview_selected(self, event):
        '''Remove selection from lisbox after clicking table'''
        self.another_staff.select_clear(0, 'end')

    def tables_tidying(self):
        '''Remove unused staff from table.'''
        self.another_staff.delete(0, 'end')
        used_staff = [x[0] for x in self.get_staff_from_table()]
        for member in Staff.select():
            if member.name not in used_staff:
                self.another_staff.insert('end', member.name)

    def add_member(self):
        '''Add member from listbox to table.'''
        if not self.another_staff.curselection():
            pass
        else:
            self.table.insert('', 'end', values=(
                self.another_staff.selection_get(),
                Staff.get(
                    Staff.name == self.another_staff.selection_get()
                ).speciality
            ))

            self.tables_tidying()

    def remove_member(self):
        '''Removes member from table to listbox.'''
        selected_item = self.table.selection()
        if selected_item:
            self.table.delete(selected_item)
        self.tables_tidying()

    def clear(self):
        self.table.delete(*self.table.get_children())
        self.tables_tidying()
