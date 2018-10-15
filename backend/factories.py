import datetime
import string
from random import randint

from factory import base
from factory import Faker
from factory import fuzzy

from backend.models import School, Staff, StaffMeeting, Student
from frontend.values import reasons, timespan


def school_name():
    return 'Szkoła Podstawowa nr {} w {}'.format(
        randint(1, 99),
        Faker("city", locale="pl_PL").generate({})
    )


class PeeweeFactory(base.Factory):

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        obj = model_class(*args, **kwargs)
        obj.save()
        return obj


class SchoolFactory(PeeweeFactory):

    class Meta:
        model = School

    name = fuzzy.FuzzyAttribute(school_name)
    sort = fuzzy.FuzzyChoice([
        'inne',
        'liceum ogólnokształcące',
        'przedszkole',
        'zasadnicza szkoła zawodowa',
        'szkoła podstawowa',
        'technikum',

    ])
    address = Faker("street_address", locale="pl_PL")
    zipcode = Faker("postcode", locale="pl_PL")


class StaffFactory(PeeweeFactory):

    class Meta:
        model = Staff

    name = Faker("name", locale="pl_PL")
    speciality = fuzzy.FuzzyChoice([
        'psycholog',
        'surdopedagog',
        'logopeda',
        'pedagog',
        'tyflopedagog',
        'neurosocjopsycholog',
        'lekarz pediatra',
    ])


class StudentFactory(PeeweeFactory):

    class Meta:
        model = Student

    name_n = Faker("name", locale="pl_PL")
    name_g = Faker("name", locale="pl_PL")
    zip_code = Faker("postcode", locale="pl_PL")
    city = Faker("city", locale="pl_PL")
    address = Faker("street_address", locale="pl_PL")
    pesel = fuzzy.FuzzyText(length=11, chars=string.digits)
    birth_date = fuzzy.FuzzyDate(start_date=datetime.date(2000, 1, 1))
    birth_place = Faker("city", locale="pl_PL")
    casebook = fuzzy.FuzzyText(length=8, chars=string.ascii_uppercase)
    school_name = fuzzy.FuzzyAttribute(school_name)
    school_sort = fuzzy.FuzzyChoice([
        'inne',
        'liceum ogólnokształcące',
        'przedszkole',
        'zasadnicza szkoła zawodowa',
        'szkoła podstawowa',
        'technikum',

    ])
    school_address = Faker("street_address", locale="pl_PL")
    school_city = Faker("city", locale="pl_PL")
    class_ = fuzzy.FuzzyAttribute(lambda: str(randint(1, 8)))
    profession = Faker("job", locale="pl_PL")


class StaffMeetingFactory(PeeweeFactory):

    class Meta:
        model = StaffMeeting

    date = fuzzy.FuzzyDate(start_date=datetime.date(2018, 1, 1))
    member1 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member2 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member3 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member4 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member5 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member6 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member7 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member8 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    member9 = fuzzy.FuzzyAttribute(lambda: StaffFactory().id)
    subject = fuzzy.FuzzyChoice([
        'kształcenie specjalne',
        'indywidualne nauczanie',
        'indywidualne roczne przygotowanie przedszkolne',
        'wczesne wspomaganie rozwoju',
        'zajęcia rewalidacyjno-wychowawcze indywidualne',
        'zajęcia rewalidacyjno-wychowawcze zespołowe',
    ])
    reason = fuzzy.FuzzyChoice(reasons)
    applicant_n = Faker("name", locale="pl_PL")
    applicant_g = Faker("name", locale="pl_PL")
    applicant_zipcode = Faker("postcode", locale="pl_PL")
    applicant_city = Faker("city", locale="pl_PL")
    applicant_address = Faker("street_address", locale="pl_PL")
    timespan = fuzzy.FuzzyChoice(timespan)
    timespan_ind = ''
    student = fuzzy.FuzzyAttribute(lambda: StudentFactory().id)
