import os
from docx import Document

from .decision_create import (
    add_line,
    application_reason,
    application_subject,
    normal_center,
    normal_justify,
    normal_left,
    staff_decree
)
from .styles import my_styles


class Decree():
    def __init__(self, values):
        self.values = values
        self.document = my_styles(Document())
    
    def create(self):
        normal_center(
            self.document,
            "Zarządzenie Nr {}/{}\n".format("alfa", "beta"),
            size=14,
            bold=True
            )
        normal_center(
            self.document,
            "Dyrektora Poradni Psychologiczno - Pedagogicznej w Grodzisku"
            " Wlkp. z dnia {} r.\n".format(self.values['staff_meeting_date']),
            size=11,
            bold=True
            )
        normal_center(
            self.document,
            "w sprawie powołania Zespołu Orzekającego\n",
            size=11,
            bold=False
            )
        normal_justify(
            self.document,
            "Działając na podstawie §4.1 rozporządzenia Ministra Edukacji"
            " Narodowej z dnia 7 września 2017 r. w sprawie orzeczeń i opinii"
            " wydawanych przez zespoły orzekające działające w publicznych"
            " poradniach psychologiczno - pedagogicznych (Dz.U. z 2017 r.,"
            " poz. 1743)\n",
            size = 11
            )
        normal_center(
            self.document,
            "powołuję następujący skład Zespołu Orzekającego Poradni"
            " Psychologiczno - Pedagogicznej w Grodzisku Wlkp. dla"
            " rozpatrzenia sprawy:\n",
            size=11,
            bold=True
            )
        normal_left(
            self.document,
            "imię i nazwisko: {}\n"
            "na wniosek: {}\n"
            "data urodzenia: {} r.\n"
            "nr karty indywidualnej: {}\n".format(
                self.values['name_n'],
                self.values['applicant_g'],
                self.values['birth_date'],
                self.values['casebook']
                ),
            size=11
            )
        normal_left(
            self.document,
            "wniosek o wydanie {} z uwagi na {}\n".format(
                application_subject(self.values),
                application_reason(self.values['reason'])
                ),
            size=11
            )
        staff_decree(self.document, self.values)

    def save(self):
        if not os.path.exists('./orzeczenia'):
            os.makedirs('./orzeczenia')
        self.document.save(
            os.path.join(
                './orzeczenia',
                "{} - {} zarz.docx".format(
                    self.values['name_n'],
                    self.values['staff_meeting_date']
                    )
                )
            ) 
