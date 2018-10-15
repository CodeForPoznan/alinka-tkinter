from tkinter import Tk

from backend.factories import SchoolFactory
from frontend.mainwindow import MainWindow
from tests import MockedDatabaseTestCase


class MainWindowTestCase(MockedDatabaseTestCase):

    def setUp(self):
        super().setUp()

        # this line need to be run until we have something like that in code:
        # frontend/mainwindow.py
        # School.sort == sorted(
        #     i.sort for i in School.select().distinct()
        # )[1]
        SchoolFactory.create_batch(20)

        self.instance = MainWindow(Tk())

    def test_mainwindow_and_frames_contains_a_name(self):
        self.assertEqual(self.instance.notebook['text'], "Baza danych")
        self.assertEqual(self.instance.actual_student['text'], "Dane dziecka")
        self.assertEqual(
            self.instance.applicationframe['text'],
            "Wnioskodawcy"
        )
        self.assertEqual(
            self.instance.staff_meeting_frame['text'],
            "Zespół orzekający"
        )
