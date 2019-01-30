from peewee import ForeignKeyField, IntegerField, Model, Proxy, TextField


database_proxy = Proxy()


class Staff(Model):

    class Meta:
        database = database_proxy

    name = TextField()
    speciality = TextField()


class School(Model):

    class Meta:
        database = database_proxy

    name = TextField()
    sort = TextField()
    address = TextField()
    zipcode = TextField()


class Student(Model):

    class Meta:
        database = database_proxy

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

    @property
    def reverse_name(self):
        """Return reversed name of the student."""
        splitted_name = self.name_n.split(" ")
        first_names = splitted_name[:-1]
        last_name = splitted_name[-1]
        return " ".join([last_name] + first_names)


class StaffMeeting(Model):

    class Meta:
        database = database_proxy

    date = TextField()
    member1 = IntegerField(default=None, null=True)
    member2 = IntegerField(default=None, null=True)
    member3 = IntegerField(default=None, null=True)
    member4 = IntegerField(default=None, null=True)
    member5 = IntegerField(default=None, null=True)
    member6 = IntegerField(default=None, null=True)
    member7 = IntegerField(default=None, null=True)
    member8 = IntegerField(default=None, null=True)
    member9 = IntegerField(default=None, null=True)
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
