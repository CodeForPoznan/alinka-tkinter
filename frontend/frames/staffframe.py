from tkinter import Button, Entry, Label, LabelFrame, Listbox, DISABLED, ACTIVE
from tkinter.ttk import Entry, Label, Treeview


class StaffFrame(LabelFrame):
    """Contains data of staffmeeteng"""
    def __init__(self, window, base, **kwargs):
        LabelFrame.__init__(self, window, **kwargs)
        self.base = base
        self.staff_id = None
        self.all_staff = [x[0] for x in self.base.get_all_staff()]
        self.data_label = Label(self, text="Data zespołu")
        self.data_label.grid(row=0, column=0, padx=5, pady=1, sticky='e')
        self.data_entry = Entry(self, width=20)
        self.data_entry.grid(row=0, column=1, padx=5, pady=1, sticky='w')

        self.table = Treeview(self, columns=("name", "speciality"))
        self.table.heading('#1', text='imię i nazwisko')
        self.table.heading('#2', text='specjalizacja')
        self.table.column('#1', width = 200)
        self.table.column('#2', width = 200)

        self.table.grid(row=1,column=0, rowspan=1, columnspan=2, padx=5, pady=5)
        self.table['show'] = 'headings'
        self.table.bind('<<TreeviewSelect>>', self.on_treeview_selected)

        self.another_stuff_frame = LabelFrame(self, text="Inni specjaliści")
        self.another_stuff_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        self.another_staff = Listbox(self.another_stuff_frame, width=48, height=12)
        self.another_staff.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        self.another_staff.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.add_button = Button(self, text="Dodaj członka", command=self.add_member)
        self.add_button.grid(row=3, column=0, padx=5, pady=5)
        self.delete_button = Button(self, text="Usuń członka", command=self.remove_member)
        self.delete_button.grid(row=3, column=1, padx=5, pady=5)
    
    def get_all_staff(self):
        return [x[0] for x in self.base.get_all_staff()]
    
    def get_staff_from_table(self):
        '''return list of member of staff_meeting from table
        eg. [[name, speciality],[name, speciality]]'''
        staff_meeting_list = []
        for child in self.table.get_children():
            staff_meeting_list.append(
                self.table.item(child)["values"]
                )
        return staff_meeting_list
    
    def insert_staff(self, base, staff):
        self.base = base
        self.staff=staff
        self.staff_id = staff['id']
        if not self.staff_id:
            self.tables_tidying()
            return
        self.data_entry.delete(0, 'end')
        self.data_entry.insert(0, staff['date'])
        self.table.delete(*self.table.get_children())
        self.another_staff.delete(0, 'end')
        for i in staff['team']:
            self.table.insert('', 'end', values=(i[0], i[1]))
        self.tables_tidying()

    def on_listbox_select(self, event):
        if not isinstance(self.table.selection(), str):
            self.table.selection_remove(self.table.selection()[0])

    def on_treeview_selected(self, event):
        self.another_staff.select_clear(0, 'end')
    
    def tables_tidying(self):
        self.another_staff.delete(0, 'end')
        used_staff = [x[0] for x in self.get_staff_from_table()]
        for member in self.get_all_staff():
            if member not in used_staff:
                self.another_staff.insert('end', member)

    def add_member(self):
        if not self.another_staff.curselection():
            pass
        else:
            self.table.insert(
            '',
            'end',
            values=(
                self.another_staff.selection_get(),
                self.base.what_speciality(
                    self.another_staff.selection_get()
                    )[1]
                )
            )

            self.tables_tidying()
        
    def remove_member(self):
        selected_item = self.table.selection()
        if selected_item:
            self.table.delete(selected_item)
        self.tables_tidying()

    def clear(self):
        self.table.delete(*self.table.get_children())
        self.tables_tidying()


