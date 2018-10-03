from tkinter import Button, Toplevel
from tkinter.ttk import Treeview


class SettingsWindow(Toplevel):
    def __init__(self, window, base, **kwargs):
        super().__init__(window, base, **kwargs)
        self.base = base

