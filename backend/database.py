from collections import OrderedDict
import sqlite3

from .fixtures import staff, places


class DataBase():

    def __init__(self, dbase):
        self.conection = sqlite3.connect(dbase)
        self.cur = self.conection.cursor()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY,
            name_n TEXT,
            name_g TEXT,
            zip_code TEXT,
            city TEXT,
            address TEXT,
            pesel TEXT UNIQUE,
            birth_date TEXT,
            birth_place TEXT,
            casebook TEXT,
            school_name TEXT,
            school_sort TEXT,
            school_address TEXT,
            school_city TEXT,
            class TEXT,
            profession TEXT
            )'''
        )
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY,
            name TEXT,
            speciality TEXT
            )'''
        )
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
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS school (
            id INTEGER PRIMARY KEY,
            name TEXT,
            sort TEXT,
            address TEXT,
            zipcode TEXT
            )'''
        )
        self.conection.commit()

    def empty_database(self):
        '''Check if database is empty'''
        self.cur.execute('''SELECT * FROM staff''')
        return self.cur.fetchall()

    def add_fake_data(self):
        for i in staff:
            self.cur.execute('''INSERT INTO staff VALUES(NULL, ?, ?)''', i)
        for i in places:
            self.cur.execute(
                '''INSERT INTO school VALUES(NULL, ?, ?, ?, ?)''', i
            )

        self.conection.commit()

    def add_student_to_db(self, values):
        value = [
            values['name_n'],
            values['name_g'],
            values['zip_code'],
            values['city'],
            values['address'],
            values['pesel'],
            values['birth_date'],
            values['birth_place'],
            values['casebook'],
            values['school_name'],
            values['school_sort'],
            values['school_address'],
            values['school_city'],
            values['class'],
            values['profession']
        ]

        self.cur.execute(
            '''
            INSERT INTO student
            VALUES(
                NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )''', value
        )

        self.conection.commit()

    def get_student_data(self, pesel="", id=""):
        '''return dict of student data.'''
        student = {}
        if pesel:
            self.cur.execute(
                '''SELECT * FROM student WHERE pesel=?''', (pesel,)
            )
        else:
            self.cur.execute(
                '''SELECT * FROM student WHERE id=?''', (id,)
            )
        student_data = self.cur.fetchall()[0]
        student = dict(zip([
            'id', 'name_n', 'name_g', 'zip_code', 'city', 'address', 'pesel',
            'birth_date', 'birth_place', 'casebook', 'school_name',
            'school_sort', 'school_address', 'school_city', 'class',
            'profession'
        ], student_data))

        return student

    def update_student(self, values):
        value = [
            values['name_n'],
            values['name_g'],
            values['zip_code'],
            values['city'],
            values['address'],
            values['pesel'],
            values['birth_date'],
            values['birth_place'],
            values['casebook'],
            values['school_name'],
            values['school_sort'],
            values['school_address'],
            values['school_city'],
            values['class'],
            values['profession'],
            values['pesel']
        ]
        self.cur.execute(
            '''
            UPDATE student
            SET
                name_n=?,
                name_g=?,
                zip_code=?,
                city=?,
                address=?,
                pesel=?,
                birth_date=?,
                birth_place=?,
                casebook=?,
                school_name=?,
                school_sort=?,
                school_address=?,
                school_city=?,
                class=?,
                profession=?
            WHERE pesel=?
            ''', (value)
        )
        self.conection.commit()

    def delete_student(self, pesel):
        student_id = self.get_student_id(pesel)
        self.cur.execute(
            '''
            DELETE FROM student
            WHERE pesel=?
            ''', (pesel,)
        )
        self.cur.execute(
            '''
            DELETE FROM staffmeeting
            WHERE student=?
            ''', (student_id,)
        )
        self.conection.commit()

    def add_staffmeeting(self, values):
        '''
        Add new staffmeeting to database
        '''
        student_id = self.get_student_id(values['pesel'])
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
        student_id = self.get_student_id(values['pesel'])
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

    def select_school(self, sort):
        self.cur.execute(
            '''
            SELECT name
            FROM school
            WHERE sort=?
            ''', (sort,)
        )
        schools = []
        for i in self.cur.fetchall():
            schools.append(i[0])
        return schools

    def sort_of_school(self):
        self.cur.execute(
            '''
            SELECT sort
            FROM school'''
        )
        sort = []
        for i in self.cur.fetchall():
            sort.append(i[0])
        return sorted(set(sort))

    def staff_meeting_list(self):
        '''get tuple with id, date, ids of stuff, student'''
        self.cur.execute('''SELECT * FROM staffmeeting''')
        return self.cur.fetchall()

    def get_all_staff(self):
        self.cur.execute('''SELECT name, speciality FROM staff''')
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

    def who_is(self, id):
        '''select list contains name and speciality refering to
           given id of staff.'''
        self.cur.execute(
            '''
            SELECT
                name,
                speciality
            FROM staff
            WHERE id=?
            ''', (id,)
        )
        return list(self.cur.fetchall()[0])

    def what_speciality(self, name):
        '''return list containing name and speciality
           refering to given NAME.'''
        self.cur.execute(
            '''
            SELECT
                name,
                speciality
            FROM staff
            WHERE name=?
            ''', (name,)
        )
        return list(self.cur.fetchone())

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

        staff['team'] = [self.who_is(x) for x in who_meets]
        return staff

    def convert_staff_to_id(self, staff_data_list):
        '''convert staff_data_list from
        eg. [[name, speciality], [name, speciality]] to
            [1, 2, None....]
        it has to return exactly 9 id's'''
        id_list = []
        for i in staff_data_list:
            self.cur.execute('''
                SELECT id FROM staff WHERE name=?
                ''', (i[0],)
            )
            id_list.append(self.cur.fetchone()[0])
        for i in range(len(id_list), 9):
            id_list.append(None)

        return id_list

    def get_school(self, name):
        self.cur.execute('''
            SELECT * FROM school
            WHERE name=?
            ''', (name,)
        )
        return self.cur.fetchall()[0]

    def get_student_id(self, pesel):
        '''Get student id from student tab.'''
        self.cur.execute(
            '''
            SELECT id
            FROM student
            WHERE pesel=?
            ''', (pesel,)
        )
        return self.cur.fetchone()[0]

    def get_student_name(self, id):
        '''Return name of the student by his/her id'''
        self.cur.execute(
            '''
            SELECT name_n
            FROM student
            WHERE id=?
            ''', (id,)
        )
        student = self.cur.fetchone()[0]
        student_name = []
        splitted_name = student.split(" ")
        first_name = splitted_name[:-1]
        last_name = splitted_name[-1]
        student_name.append(last_name)
        student_name += first_name
        return " ".join(student_name)

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
            staffmeeting_data['team'].append(self.who_is(i))
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
        self.cur.execute(
            '''SELECT pesel, name_n FROM student'''
        )
        student_list = self.cur.fetchall()
        if student_list:
            for i in student_list:
                student_name = []
                splitted_name = i[1].split(" ")
                first_name = splitted_name[:-1]
                last_name = splitted_name[-1]
                student_name.append(last_name)
                student_name += first_name
                students[i[0]] = " ".join(student_name)
        return OrderedDict(sorted(students.items(), key=lambda t: t[1]))

    def pesel_exists(self, pesel):
        self.cur.execute(
            '''
            SELECT 1
            FROM student
            WHERE pesel=?
            ''', (pesel,)
        )
        return self.cur.fetchone()

    def staffmeeting_exists(self, values):
        student_id = self.get_student_id(values['pesel'])
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
