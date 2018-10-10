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

    def add_student_to_db(self, values):
        Student(
            name_n=values['name_n'],
            name_g=values['name_g'],
            zip_code=values['zip_code'],
            city=values['city'],
            address=values['address'],
            pesel=values['pesel'],
            birth_date=values['birth_date'],
            birth_place=values['birth_place'],
            casebook=values['casebook'],
            school_name=values['school_name'],
            school_sort=values['school_sort'],
            school_address=values['school_address'],
            school_city=values['school_city'],
            class_=values['class'],
            profession=values['profession']
        ).save()

    def update_student(self, values):
        student = Student.get(Student.pesel == values['pesel'])
        student.name_n = values['name_n']
        student.name_g = values['name_g']
        student.zip_code = values['zip_code']
        student.city = values['city']
        student.address = values['address']
        student.birth_date = values['birth_date']
        student.birth_place = values['birth_place']
        student.casebook = values['casebook']
        student.school_name = values['school_name']
        student.school_sort = values['school_sort']
        student.school_address = values['school_address']
        student.school_city = values['school_city']
        student.class_ = values['class']
        student.profession = values['profession']
        student.save()

    def delete_student(self, pesel):
        student = Student.get(Student.pesel == pesel)
        StaffMeeting.delete().where(StaffMeeting.student == student.id)
        student.delete_instance()

    def add_staffmeeting(self, values):
        """Add new staffmeeting to database."""
        staff_meeting = StaffMeeting(
            date=values['staff_meeting_date'],
            subject=values['subject'],
            reason=values['reason'][1] + ", " + values['reason'][2],
            applicant_n=values['applicant_n'],
            applicant_g=values['applicant_g'],
            applicant_zipcode=values['applicant_zipcode'],
            applicant_city=values['applicant_city'],
            applicant_address=values['applicant_address'],
            timespan=values['timespan'],
            timespan_ind=values['timespan_ind'],
            student=Student.get(Student.pesel == values['pesel']).id
        )

        team = values['staff']['team']
        for i, member in enumerate(self.convert_staff_to_id(team), 1):
            setattr(staff_meeting, 'member{}'.format(i), member)

        staff_meeting.save()

    def update_staffmeeting(self, values):
        staff_meeting = StaffMeeting.get(
            StaffMeeting.date == values['staff_meeting_date'],
            StaffMeeting.subject == values['subject'],
            StaffMeeting.student == Student.get(
                Student.pesel == values['pesel']
            ).id
        )

        staff_meeting.applicant_n = values['applicant_n']
        staff_meeting.applicant_g = values['applicant_g']
        staff_meeting.applicant_zipcode = values['applicant_zipcode']
        staff_meeting.applicant_city = values['applicant_city']
        staff_meeting.applicant_address = values['applicant_address']
        staff_meeting.reason = (
            values['reason'][1] + ", " + values['reason'][2]
        )
        staff_meeting.timespan = values['timespan'],
        staff_meeting.timespan_ind = values['timespan_ind']

        team = values['staff']['team']
        for i, member in enumerate(self.convert_staff_to_id(team), 1):
            setattr(staff_meeting, 'member{}'.format(i), member)

        staff_meeting.save()

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

    def staffmeeting_exists(self, values):
        try:
            StaffMeeting.get(
                StaffMeeting.date == values['staff_meeting_date'],
                StaffMeeting.subject == values['subject'],
                StaffMeeting.student == Student.get(
                    Student.pesel == values['pesel']
                ).id
            )
        except StaffMeeting.DoesNotExist:
            return False
        else:
            return True
