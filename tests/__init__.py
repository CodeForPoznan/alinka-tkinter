import unittest

from peewee import SqliteDatabase

from backend.models import database_proxy, School, Staff, StaffMeeting, Student


MODELS = [School, Staff, StaffMeeting, Student]


class MockedDatabaseTestCase(unittest.TestCase):

    def setUp(self):
        test_db = SqliteDatabase(':memory:')
        database_proxy.initialize(test_db)
        database_proxy.connect()
        database_proxy.create_tables(MODELS)

    def tearDown(self):
        database_proxy.drop_tables(MODELS)
        database_proxy.close()
