from tkinter import Tk
import unittest
from frontend.mainwindow import MainWindow


class testTest(unittest.TestCase):
    def setUp(self):
        self.instance = MainWindow(Tk())

    def test(self):
        '''Test if mainwindow and frames contains a name'''
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
