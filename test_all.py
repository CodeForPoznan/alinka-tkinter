from tkinter import Tk
import unittest
from frontend.mainwindow import MainWindow
from frontend.values import sorts
from backend.database import School


class testTest(unittest.TestCase):
    def setUp(self):
        self.instance = MainWindow(Tk())

    def tearDown(self):
        self.instance.window.destroy()

    def test_Mainwindow_and_frames_contains_a_name(self):
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

    def test_School_class_contains_only_sort_of_sorts_list(self):
        query = School.select()
        list_of_sorts = [school.sort for school in query]
        for sort in list_of_sorts:
            self.assertIn(sort, sorts)
