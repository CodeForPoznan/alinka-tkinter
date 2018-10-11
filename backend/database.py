from collections import OrderedDict
from os.path import abspath, dirname, isfile, join

from peewee import IntegerField, Model, SqliteDatabase, TextField

from backend.fixtures import staff, places


DB_PATH = join(dirname(dirname(abspath(__file__))), 'database.db')
DB = SqliteDatabase(DB_PATH)


class Staff(Model):

    class Meta:
        database = DB

    name = TextField()
    speciality = TextField()


class School(Model):

    class Meta:
        database = DB

    name = TextField()
    sort = TextField()
    address = TextField()
    zipcode = TextField()


class Student(Model):

    class Meta:
        database = DB

    name_n = TextField()
    name_g = TextField()
    zip_code = TextField()
    city = TextField()
    address = TextField()
    pesel = TextField(unique=True)
    birth_date = TextField()
    birth_place = TextField()
    casebook = TextField()
    school_name = TextField()
    school_sort = TextField()
    school_address = TextField()
    school_city = TextField()
    class_ = TextField(column_name='class')
    profession = TextField()


class StaffMeeting(Model):

    class Meta:
        database = DB

    date = TextField()
    member1 = IntegerField()
    member2 = IntegerField()
    member3 = IntegerField()
    member4 = IntegerField()
    member5 = IntegerField()
    member6 = IntegerField()
    member7 = IntegerField()
    member8 = IntegerField()
    member9 = IntegerField()
    subject = TextField()
    reason = TextField()
    applicant_n = TextField()
    applicant_g = TextField()
    applicant_zipcode = TextField()
    applicant_city = TextField()
    applicant_address = TextField()
    timespan = TextField()
    timespan_ind = TextField()
    student = IntegerField()


class DataBase:

    def __init__(self):
        if not isfile(DB_PATH):
            DB.connect()
            DB.create_tables([School, Staff, StaffMeeting, Student])
            self.add_fake_data()

    def add_fake_data(self):
        for i in staff:
            Staff(**i).save()
        for i in places:
            School(**i).save()

    def delete_student(self, pesel):
        student = Student.get(Student.pesel == pesel)
        StaffMeeting.delete().where(StaffMeeting.student == student.id)
        student.delete_instance()

    def convert_staff_to_id(self, staff_data_list):
        '''convert staff_data_list from
        eg. [[name, speciality], [name, speciality]] to
            [1, 2, None....]
        it has to return exactly 9 id's'''
        id_list = []

        for i in staff_data_list:
            id_list.append(Staff.get(Staff.name == i[0]).id)

        for i in range(len(id_list), 9):
            id_list.append(None)

        return id_list

    def get_student_name(self, id):
        '''Return name of the student by his/her id'''
        student = Student.get(id=id).name_n
        splitted_name = student.split(" ")
        first_names = splitted_name[:-1]
        last_name = splitted_name[-1]
        return " ".join([last_name] + first_names)

    def get_staffmeeting_data(self, staffmeeting_id):
        '''
        return dict of staffmeeting data
        '''
        staff_meeting = StaffMeeting.get(StaffMeeting.id == staffmeeting_id)
        staffmeeting_data = {
            'id': staff_meeting.id,
            'date': staff_meeting.date,
            'member1': staff_meeting.member1,
            'member2': staff_meeting.member2,
            'member3': staff_meeting.member3,
            'member4': staff_meeting.member4,
            'member5': staff_meeting.member5,
            'member6': staff_meeting.member6,
            'member7': staff_meeting.member7,
            'member8': staff_meeting.member8,
            'member9': staff_meeting.member9,
            'subject': staff_meeting.subject,
            'reason': staff_meeting.reason,
            'applicant_n': staff_meeting.applicant_n,
            'applicant_g': staff_meeting.applicant_g,
            'applicant_zipcode': staff_meeting.applicant_zipcode,
            'applicant_city': staff_meeting.applicant_city,
            'applicant_address': staff_meeting.applicant_address,
            'timespan': staff_meeting.timespan,
            'timespan_ind': staff_meeting.timespan_ind,
            'student': staff_meeting.student
        }
        # convert member id to his name and speciality
        staffmeeting_data['team'] = []
        staff = [
            staffmeeting_data['member{}'.format(x)]
            for x in range(1, 10)
            if staffmeeting_data['member{}'.format(x)] is not None
        ]

        for i in staff:
            staffmeeting_data['team'].append(Staff.get(id=i).name)
        reason = staffmeeting_data['reason'].split(',')
        if len(reason[1]) < 2:
            reason[1] = ''
        staffmeeting_data['reason'] = reason[0]
        staffmeeting_data['reason2'] = reason[1]
        return staffmeeting_data

    def get_dict_of_students(self):
        '''return dict of student containing
        {pesel: name}'''
        students = {}
        student_list = Student.select()

        for i in student_list:
            splitted_name = i.name_n.split(" ")
            first_names = splitted_name[:-1]
            last_name = splitted_name[-1]
            students[i.pesel] = " ".join([last_name] + first_names)
        return OrderedDict(sorted(students.items(), key=lambda t: t[1]))
