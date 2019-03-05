import sys
from os.path import abspath, dirname, isfile, join
from tkinter import Tk

from peewee import SqliteDatabase

from backend.fixtures import staff, places
from backend.models import database_proxy, School, Staff, StaffMeeting, Student
from frontend.mainwindow import MainWindow

if getattr(sys, 'frozen', False):
    __file__ = sys.executable

DB_PATH = join(dirname(abspath(__file__)), 'alinka.sqlite')
DB = SqliteDatabase(DB_PATH)
database_proxy.initialize(DB)

if not isfile(DB_PATH):
    database_proxy.connect()
    database_proxy.create_tables([School, Staff, StaffMeeting, Student])

    for i in staff:
        Staff(**i).save()
    for i in places:
        School(**i).save()


window = Tk()
app = MainWindow(window)
window.mainloop()
