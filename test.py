from tkinter import Tk
import unittest

from frontend.mainwindow import MainWindow

class testTest(unittest.TestCase):
    def test(self):
        instance = MainWindow(Tk())
        self.assertEqual(instance.notebook['text'], "Baza danych")

unittest.main()