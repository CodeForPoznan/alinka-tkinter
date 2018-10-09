import sqlite3
from collections import OrderedDict
from os.path import abspath, dirname, isfile, join

from peewee import Model, SqliteDatabase, TextField

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


class DataBase:

    def __init__(self):
        self.empty_database = not isfile(DB_PATH)
        self.conection = sqlite3.connect(DB_PATH)
        self.cur = self.conection.cursor()

        if self.empty_database:
            DB.connect()
            DB.create_tables([School, Staff, Student])

            self.cur.execute(
                '''CREATE TABLE IF NOT EXISTS staffmeeting (
                id INTEGER PRIMARY KEY,
                date TEXT,
                member1 INTEGER,
                member2 INTEGER,
                member3 INTEGER,
                member4 INTEGER,
                member5 INTEGER,
                member6 INTEGER,
                member7 INTEGER,
                member8 INTEGER,
                member9 INTEGER,
                subject TEXT,
                reason TEXT,
                applicant_n TEXT,
                applicant_g TEXT,
                applicant_zipcode TEXT,
                applicant_city TEXT,
                applicant_address TEXT,
                timespan TEXT,
                timespan_ind TEXT,
                student INTEGER
                )'''
            )

            self.add_fake_data()
            self.conection.commit()

    def add_fake_data(self):
        for i in staff:
            Staff(**i).save()
        for i in places:
            School(**i).save()

        self.conection.commit()

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

    def get_student_data(self, pesel="", id=""):
        '''return dict of student data.'''
        if pesel:
            student = Student.get(Student.pesel == pesel)
        else:
            student = Student.get(Student.id == id)

        return {
            'id': student.id,
            'name_n': student.name_n,
            'name_g': student.name_g,
            'zip_code': student.zip_code,
            'city': student.city,
            'address': student.address,
            'pesel': student.pesel,
            'birth_date': student.birth_date,
            'birth_place': student.birth_place,
            'casebook': student.casebook,
            'school_name': student.school_name,
            'school_sort': student.school_sort,
            'school_address': student.school_address,
            'school_city': student.school_city,
            'class': student.class_,
            'profession': student.profession,
        }

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
        self.cur.execute(
            '''
            DELETE FROM staffmeeting
            WHERE student=?
            ''', (student.id,)
        )
        self.conection.commit()
        student.delete_instance()

    def add_staffmeeting(self, values):
        '''
        Add new staffmeeting to database
        '''
        student_id = Student.get(Student.pesel == values['pesel']).id
        staff = [
            values['staff_meeting_date']
        ] + self.convert_staff_to_id(values['staff']['team'])
        for i in [
            values['subject'],
            values['reason'][1] + ", " + values['reason'][2],
            values['applicant_n'],
            values['applicant_g'],
            values['applicant_zipcode'],
            values['applicant_city'],
            values['applicant_address'],
            values['timespan'],
            values['timespan_ind'],
            student_id
        ]:
            staff.append(i)

        self.cur.execute(
            '''INSERT INTO staffmeeting VALUES(
            NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', staff
        )
        self.conection.commit()

    def update_staffmeeting(self, values):
        student_id = Student.get(Student.pesel == values['pesel']).id
        staff = self.convert_staff_to_id(values['staff']['team'])
        for i in [
            values['applicant_n'],
            values['applicant_g'],
            values['applicant_zipcode'],
            values['applicant_city'],
            values['applicant_address'],
            values['reason'][1] + ", " + values['reason'][2],
            values['timespan'],
            values['timespan_ind'],
            values['staff_meeting_date'],
            values['subject'],
            student_id
        ]:
            staff.append(i)

        self.cur.execute(
            '''
            UPDATE staffmeeting
            SET
                member1=?,
                member2=?,
                member3=?,
                member4=?,
                member5=?,
                member6=?,
                member7=?,
                member8=?,
                member9=?,
                applicant_n=?,
                applicant_g=?,
                applicant_zipcode=?,
                applicant_city=?,
                applicant_address=?,
                reason=?,
                timespan=?,
                timespan_ind=?
            WHERE
                date=? AND subject=? AND student=?
            ''', staff
        )
        self.conection.commit()

    def delete_from_staffmeeting(self, staffmeeting_id):
        self.cur.execute(
            '''
            DELETE FROM staffmeeting
            WHERE id=?''', (staffmeeting_id,)
        )
        self.conection.commit()

    def staff_meeting_list(self):
        '''get tuple with id, date, ids of stuff, student'''
        self.cur.execute('''SELECT * FROM staffmeeting''')
        return self.cur.fetchall()

    def select_meeting(self, id):
        '''select meeting from list of staffmeetings'''

        self.cur.execute('''
            SELECT *
            FROM staffmeeting
            WHERE id=?
            ''', (id,)
        )
        return self.cur.fetchall()[0]

    def look_for_staffmeeting(self, date, student_id):
        '''return id of staffmeeting'''
        self.cur.execute('''
            SELECT id
            FROM staffmeeting
            WHERE date=? AND student=?
            ''', (date, student_id)
        )
        a = self.cur.fetchone()
        return a[0]

    def convert_to_staff(self, id):
        '''convert id of staffmeeting into dict
        with important keys:
        ['date'] - containing staff meeting date
        ['team'] - containing staff meeting team data,
           eg. [[name, speciality], [name, speciality]].
        '''
        staff_data = list(self.select_meeting(id))
        staff = {}
        staff['date'] = staff_data[1]
        who_meets = [x for x in staff_data[2:-1] if x is not None]

        staff['team'] = [Staff.get(id=x).name for x in who_meets]
        return staff

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
        self.cur.execute(
            '''
            SELECT *
            FROM staffmeeting
            WHERE id=?
            ''', (staffmeeting_id,)
        )
        staffmeeting_data = dict(
            zip([
                'id',
                'date',
                'member1',
                'member2',
                'member3',
                'member4',
                'member5',
                'member6',
                'member7',
                'member8',
                'member9',
                'subject',
                'reason',
                'applicant_n',
                'applicant_g',
                'applicant_zipcode',
                'applicant_city',
                'applicant_address',
                'timespan',
                'timespan_ind',
                'student'
            ], self.cur.fetchall()[0])
        )
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
        student_id = Student.get(Student.pesel == values['pesel']).id
        subject = values['subject']
        date = values['staff_meeting_date']
        self.cur.execute(
            '''
            SELECT 1
            FROM staffmeeting
            WHERE date=? AND subject=? AND student=?
            ''', (date, subject, student_id)
        )
        if self.cur.fetchone():
            return 1
        else:
            return 0
