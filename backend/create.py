from docx import Document
import os

from .decision_create import *
from .styles import my_styles
from zipfile import ZipFile
from .change_xml import *



class Decision():
    def __init__(self, value):
        self.value = value
        self.document = my_styles(Document())
        
        
    def issue(self):
        if self.value["subject"] == "kształcenie specjalne":
            self.issue_special_education()
        elif self.value["subject"] == "indywidualne nauczanie":
            self.issue_individual()
        elif self.value["subject"] == "indywidualne roczne przygotowanie przedszkolne":
            self.issue_individual_preschool()
        elif self.value["subject"] == "wczesne wspomaganie rozwoju":
            self.issue_development_support()
        elif self.value["subject"] == "zajęcia rewalidacyjno-wychowawcze indywidualne":
            self.issue_profound()
        elif self.value["subject"] == "zajęcia rewalidacyjno-wychowawcze zespołowe":
            self.issue_profound()
    
    def issue_special_education(self):
        normal_right(
            self.document, 
            "Grodzisk Wielkopolski, {}".format(
                self.value["staff_meeting_date"]
                ),
            size=10,
            bold=False
            )
        add_line(
            self.document, 2
            )
        normal_center(
            self.document,
            "ORZECZENIE NR \n o potrzebie kształcenia specjalnego",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 8
            )
        normal_justify(
            self.document, 
            "Działając na podstawie art. 127 ust. 10 ustawy z dnia 14"
            "grudnia 2016 r. – Prawo oświatowe (Dz.U. z 2017 r. poz. "
            "59 i 949)",
            size=9
            )
        applicant(
            self.document, 
            self.value["applicant_n"]
            )
        staff(
            self.document,self.value 
            )
        add_line(
            self.document, 12
            )
        normal_center(
            self.document,
            "orzeka o potrzebie kształcenia specjalnego",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document, 
            self.value["name_n"], 
            "(imię i nazwisko)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["birth_date"] + "r., " + self.value["birth_place"],
            "data i  miejsce urodzenia dziecka lub ucznia"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["pesel"],
            "(numer PESEL dziecka lub ucznia, a w przypadku braku"
            " numeru PESEL – seria i numer dokumentu potwierdzającego"
            " jego tożsamość)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value["zip_code"],
                    " ",
                    self.value["city"],
                    ", ",
                    self.value["address"]
                    ]
                ),
            "(adres zamieszkania dziecka lub ucznia)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value['school_name'],
                    ", ",
                    self.value['school_sort'],
                    ", ",
                    self.value['school_city'],
                    ", ",
                    self.value['school_address'],
                    ", ",
                    self.value['profession'],
                    ", ",
                    self.value['class']
                    ]
                ),
            "(nazwa i adres przedszkola, innej formy wychowania"
            " przedszkolnego, szkoły lub ośrodka, o którym mowa w"
            " art. 2 pkt 7 ustawy z dnia 14 grudnia 2016 r. – Prawo"
            " oświatowe, a w przypadku ucznia – także oznaczenie"
            " oddziału w szkole oraz nazwa zawodu&)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                [
                    self.value["applicant_n"],
                    ", ",
                    self.value["applicant_zipcode"],
                    " ",
                    self.value['applicant_city'],
                    ", ",
                    self.value['applicant_address']
                ]
                ),
            "(imiona i nazwiska rodziców& oraz adres ich zamieszkania)"
            )
        add_line(
            self.document, 10
            )
        normal_center(
            self.document,
            "na okres&: {}".format(self.value['timespan']),
            bold=True
            )

        page_break(self.document)
        reason(
            self.document,
            self.value
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "Diagnoza",
            size=10,
            bold=True
            )
        normal_justify(
            self.document,
            "Zespół Orzekający przedstawia diagnozę funkcjonowania dziecka lub"
            " ucznia, z uwzględnieniem potencjału rozwojowego oraz mocnych "
            "stron i uzdolnień dziecka lub ucznia oraz występujących w "
            "środowisku nauczania i wychowania barier i ograniczeń "
            "utrudniających jego funkcjonowanie:",
            size=8
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "Zalecenia",
            size=10,
            bold=True
            )
        normal_left(
            self.document,
            "Zespół Orzekający zaleca:"
            )
        recommendations(
            self.document,
            self.value['recommendations']
            )
        normal_center(
            self.document,
            "Dodatkowe informacje",
            size=10,
            bold=True
            )
        normal_center(
            self.document,
            "(w zależności od potrzeb podaje się dodatkowe istotne informacje"
            " o dziecku lub uczniu, w szczególności o wspomagającej lub"
            " alternatywnej metodzie komunikacji (AAC), którą posługuje się"
            " dziecko lub uczeń)",
            size=8
            )
        add_line(self.document, 10)
        normal_justify(
            self.document,
            "W przypadku wydania nowego orzeczenia o potrzebie kształcenia"
            " specjalnego należy wskazać okoliczności, które Zespół Orzekający"
            " uznał za istotne dla rozstrzygnięcia, oraz wyjaśnić powody, na"
            " podstawie których stwierdzono potrzebę wydania nowego"
            " orzeczenia&:",
            size=10
            )
        add_line(self.document, 10)
        normal_left(
            self.document,
            "Orzeczenie uchyla&:",
            size=10,
            bold=True
            )
        normal_left(
            self.document,
            "1) orzeczenie nr ………… o potrzebie kształcenia specjalnego"
            " z dnia ………………… wydane przez ……………………………………………………………",
            size=10,
            bold=True
            )
        normal_bold(
            self.document,
            "2) orzeczenie nr ………….. o potrzebie zajęć rewalidacyjno-"
            "wychowawczych zespołowych/indywidualnych& z dnia"
            " …………………………… wydane przez  …………………………………"
            )
        add_line(self.document, 10)
        normal_bold(
            self.document,
            "Od niniejszego orzeczenia przysługuje odwołanie do Kuratora"
            " Oświaty w ................................................"
            " za pośrednictwem Zespołu Orzekającego, który wydał orzeczenie,"
            " w terminie 14 dni od dnia jego doręczenia."
            )

        add_line(self.document, 30)
        normal_right(
            self.document,
            "(podpis Przewodniczącego Zespołu Orzekającego)               ",
            size=8
            )
        insert_reciver(self.document, self.value)


    def issue_individual(self):
        normal_right(
            self.document, 
            "Grodzisk Wielkopolski, {}".format(
                self.value["staff_meeting_date"]
                ),
            size=10,
            bold=False
            )
        add_line(
            self.document, 2
            )
        normal_center(
            self.document,
            "ORZECZENIE NR \n o potrzebie indywidualnego nauczania",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 8
            )
        normal_justify(
            self.document, 
            "Działając na podstawie art. 127 ust. 10 ustawy z dnia 14 grudnia"
            " 2016 r. – Prawo oświatowe (Dz. U. z 2017 r. poz. 59 i 949)",
            size=9
            )
        applicant(
            self.document, 
            self.value["applicant_n"]
            )
        staff(
            self.document,self.value 
            )
        add_line(
            self.document, 12
            )
        normal_center(
            self.document,
            "orzeka o potrzebie indywidualnego nauczania",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document, 
            self.value["name_n"], 
            "(imię/imiona i nazwisko ucznia)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["birth_date"] + "r., " + self.value["birth_place"],
            "(data i miejsce urodzenia ucznia)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["pesel"],
            "(numer PESEL ucznia, a w przypadku braku numeru PESEL – seria i"
            " numer dokumentu potwierdzającego jego tożsamość)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value["zip_code"],
                    " ",
                    self.value["city"],
                    ", ",
                    self.value["address"]
                    ]
                ),
            "(adres zamieszkania ucznia)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value['school_name'],
                    ", ",
                    self.value['school_sort'],
                    ", ",
                    self.value['school_city'],
                    ", ",
                    self.value['school_address'],
                    ", ",
                    self.value['profession'],
                    ", ",
                    self.value['class']
                    ]
                ),
            "(nazwa i adres szkoły oraz oznaczenie oddziału w szkole, nazwa"
            " zawodu&)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                [
                    self.value["applicant_n"],
                    ", ",
                    self.value["applicant_zipcode"],
                    " ",
                    self.value['applicant_city'],
                    ", ",
                    self.value['applicant_address']
                ]
                ),
            "(imiona i nazwiska rodziców& oraz adres ich zamieszkania)"
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "na okres&: {}".format(self.value['timespan_ind']),
            bold=True
            )
        add_line(self.document, 10)
        reason_individual(
            self.document,
            self.value['reason'][0]
            )
        page_break(self.document)
        normal_center(
            self.document,
            "Diagnoza",
            size=10,
            bold=True
            )
        normal_justify(
            self.document,
            "Zespół Orzekający określa ograniczenia w funkcjonowaniu ucznia"
            " wynikające z przebiegu choroby lub procesu terapeutycznego:",
            size=8
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "Zalecenia",
            size=10,
            bold=True
            )
        normal_left(
            self.document,
            "Zespół Orzekający zaleca:"
            )
        recommendations(
            self.document,
            self.value['recommendations']
            )
        normal_center(
            self.document,
            "Dodatkowe informacje",
            size=10,
            bold=True
            )
        normal_center(
            self.document,
            "(w zależności od potrzeb podaje się dodatkowe istotne informacje"
            " o uczniu, w szczególności o wspomagającej lub alternatywnej"
            " metodzie komunikacji (AAC), którą posługuje się uczeń, a w"
            " przypadku ucznia szkoły prowadzącej kształcenie zawodowe – "
            "także możliwość dalszego kształcenia w zawodzie, w tym warunki"
            " realizacji praktycznej nauki zawodu)",
            size=8
            )
        add_line(self.document, 10)
        normal_justify(
            self.document,
            "W przypadku wydania nowego orzeczenia o potrzebie indywidualnego"
            " nauczania należy wskazać okoliczności, które Zespół Orzekający"
            " uznał za istotne dla rozstrzygnięcia, oraz wyjaśnić powody, na"
            " podstawie których stwierdzono potrzebę wydania nowego"
            " orzeczenia&:",
            size=10
            )
        add_line(self.document, 10)
        normal_bold(
            self.document,
            "Orzeczenie uchyla orzeczenie nr ...... o potrzebie"
            " indywidualnego nauczania z dnia .............."
            " wydane przez .....................&.\n\n"
            "Od niniejszego orzeczenia przysługuje odwołanie do Kuratora"
            " Oświaty w ........................za pośrednictwem Zespołu"
            " Orzekającego, który wydał orzeczenie, w terminie 14 dni od"
            " dnia jego doręczenia."
            )
        
        add_line(self.document, 10)

        normal_left(self.document, "\n\n\n")
        normal_right(
            self.document,
            "(podpis Przewodniczącego Zespołu Orzekającego)               ",
            size=8
            )
        insert_reciver(self.document, self.value)

    def issue_individual_preschool(self):
        normal_right(
            self.document, 
            "Grodzisk Wielkopolski, {}".format(
                self.value["staff_meeting_date"]
                ),
            size=10,
            bold=False
            )
        add_line(
            self.document, 2
            )
        normal_center(
            self.document,
            "ORZECZENIE NR \n o potrzebie indywidualnego obowiązkowego"
            " rocznego przygotowania przedszkolnego",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 8
            )
        normal_justify(
            self.document, 
            "Działając na podstawie art. 127 ust. 10 ustawy z dnia 14 grudnia"
            " 2016 r. – Prawo oświatowe (Dz. U. z 2017 r. poz. 59 i 949)",
            size=9
            )
        applicant(
            self.document, 
            self.value["applicant_n"]
            )
        staff(
            self.document,self.value 
            )
        add_line(
            self.document, 12
            )
        normal_center(
            self.document,
            "orzeka o potrzebie indywidualnego obowiązkowego rocznego"
            " przygotowania przedszkolnego",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document, 
            self.value["name_n"], 
            "(imię/imiona i nazwisko dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["birth_date"] + "r., " + self.value["birth_place"],
            "(data i miejsce urodzenia dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["pesel"],
            "(numer PESEL dziecka, a w przypadku braku numeru PESEL – seria"
            " i numer dokumentu potwierdzającego jego tożsamość)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value["zip_code"],
                    " ",
                    self.value["city"],
                    ", ",
                    self.value["address"]
                    ]
                ),
            "(adres zamieszkania dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value['school_name'],
                    ", ",
                    self.value['school_sort'],
                    ", ",
                    self.value['school_city'],
                    ", ",
                    self.value['school_address']
                    ]
                ),
            "(nazwa i adres przedszkola, szkoły podstawowej, w której"
            " zorganizowano oddział przedszkolny, lub innej formy wychowania"
            " przedszkolnego)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                [
                    self.value["applicant_n"],
                    ", ",
                    self.value["applicant_zipcode"],
                    " ",
                    self.value['applicant_city'],
                    ", ",
                    self.value['applicant_address']
                ]
                ),
            "(imiona i nazwiska rodziców& oraz adres ich zamieszkania)"
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "na okres&: {}".format(self.value['timespan_ind']),
            bold=True
            )
        add_line(self.document, 10)
        reason_individual_preschool(
            self.document,
            self.value['reason'][0]
            )
        page_break(self.document)
        normal_center(
            self.document,
            "Diagnoza",
            size=10,
            bold=True
            )
        normal_justify(
            self.document,
            "Zespół Orzekający określa ograniczenia w funkcjonowaniu dziecka"
            " wynikające z przebiegu choroby lub procesu terapeutycznego:",
            size=8
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "Zalecenia",
            size=10,
            bold=True
            )
        normal_left(
            self.document,
            "Zespół Orzekający zaleca:"
            )
        recommendations(
            self.document,
            self.value['recommendations']
            )
        normal_center(
            self.document,
            "Dodatkowe informacje",
            size=10,
            bold=True
            )
        normal_center(
            self.document,
            "(w zależności od potrzeb podaje się dodatkowe istotne informacje"
            " o dziecku, w szczególności o wspomagającej lub alternatywnej"
            " metodzie komunikacji (AAC), którą posługuje się dziecko)",
            size=8
            )
        add_line(self.document, 10)
        normal_justify(
            self.document,
            "W przypadku wydania nowego orzeczenia o potrzebie indywidualnego"
            " obowiązkowego rocznego przygotowania przedszkolnego należy"
            " wskazać okoliczności, które Zespół Orzekający uznał za istotne"
            " dla rozstrzygnięcia, oraz wyjaśnić powody, na podstawie których"
            " stwierdzono potrzebę wydania nowego orzeczenia&:",
            size=10
            )
        add_line(self.document, 10)
        normal_bold(
            self.document,
            "Orzeczenie uchyla orzeczenie nr ...... o potrzebie"
            " indywidualnego obowiązkowego rocznego przygotowania"
            " przedszkolnego z dnia .............................. wydane"
            " przez..................................................&.\n"
            "Od niniejszego orzeczenia przysługuje odwołanie do Kuratora"
            " Oświaty w ........................za pośrednictwem Zespołu"
            " Orzekającego, który wydał orzeczenie, w terminie 14 dni od"
            " dnia jego doręczenia."
            )
        
        normal_left(self.document, "\n\n\n")
        normal_right(
            self.document,
            "(podpis Przewodniczącego Zespołu Orzekającego)               ",
            size=8
            )
        insert_reciver(self.document, self.value)
    
    def issue_development_support(self):
        normal_right(
            self.document, 
            "Grodzisk Wielkopolski, {}".format(
                self.value["staff_meeting_date"]
                ),
            size=10,
            bold=False
            )
        add_line(
            self.document, 2
            )
        normal_center(
            self.document,
            "OPINIA NR \n o potrzebie wczesnego wspomagania rozwoju dziecka",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 8
            )
        normal_justify(
            self.document, 
            "Działając na podstawie art. 127 ust. 10 ustawy z dnia 14 grudnia"
            " 2016 r. – Prawo oświatowe (Dz. U. z 2017 r. poz. 59 i 949),",
            size=9
            )
        applicant(
            self.document, 
            self.value["applicant_n"]
            )
        staff(
            self.document,self.value 
            )
        add_line(
            self.document, 12
            )
        normal_center(
            self.document,
            "stwierdza potrzebę wczesnego wspomagania rozwoju dziecka",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document, 
            self.value["name_n"], 
            "(imię/imiona i nazwisko dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["birth_date"] + "r., " + self.value["birth_place"],
            "(data i miejsce urodzenia dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["pesel"],
            "(numer PESEL dziecka, a w przypadku braku numeru PESEL – seria"
            "i numer dokumentu potwierdzającego jego tożsamość)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value["zip_code"],
                    " ",
                    self.value["city"],
                    ", ",
                    self.value["address"]
                    ]
                ),
            "(adres zamieszkania dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                [
                    self.value["applicant_n"],
                    ", ",
                    self.value["applicant_zipcode"],
                    " ",
                    self.value['applicant_city'],
                    ", ",
                    self.value['applicant_address']
                ]
                ),
            "(imiona i nazwiska rodziców& oraz adres ich zamieszkania)"
            )
        add_line(
            self.document, 10
            )
        normal_center(
            self.document,
            "na okres&: {}".format(self.value['timespan']),
            bold=True
            )
        add_line(
            self.document, 10
            )
        normal_left(
            self.document,
            "ze względu na wykrytą niepełnosprawność.",
            )
        page_break(self.document)

        normal_center(
            self.document,
            "Diagnoza",
            size=10,
            bold=True
            )
        normal_justify(
            self.document,
            "Zespół Orzekający przedstawia diagnozę poziomu funkcjonowania"
            " dziecka, w tym informację o potencjale rozwojowym i mocnych"
            " stronach dziecka oraz występujących w środowisku barierach i"
            " ograniczeniach utrudniających jego funkcjonowanie:",
            size=8
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "Zalecenia",
            size=10,
            bold=True
            )
        normal_left(
            self.document,
            "Zespół Orzekający zaleca:"
            )
        recommendations(
            self.document,
            self.value['recommendations']
            )
        normal_center(
            self.document,
            "Dodatkowe informacje",
            size=10,
            bold=True
            )
        normal_center(
            self.document,
            "(w zależności od potrzeb podaje się dodatkowe istotne informacje"
            " o dziecku, w szczególności o wspomagającej lub alternatywnej"
            " metodzie komunikacji (AAC), którą posługuje się dziecko)",
            size=8
            )
        add_line(self.document, 10)
        normal_justify(
            self.document,
            "W przypadku wydania nowej opinii o potrzebie wczesnego wspomagania"
            " rozwoju dziecka należy wskazać okoliczności, które Zespół"
            " Orzekający uznał za istotne dla rozstrzygnięcia, oraz wyjaśnić"
            " powody, na podstawie których stwierdzono potrzebę wydania nowej"
            " opinii&:",
            size=10
            )
        add_line(self.document, 10)
        normal_left(
            self.document,
            "Opinia uchyla opinię nr ....o potrzebie wczesnego wspomagania"
            " rozwoju dziecka z dnia .......wydaną przez..........&:",
            size=10,
            bold=True
            )
        add_line(self.document, 10)
        normal_bold(
            self.document,
            "Od niniejszego orzeczenia przysługuje odwołanie do Kuratora"
            " Oświaty w ................."
            " za pośrednictwem Zespołu Orzekającego, który wydał orzeczenie,"
            " w terminie 14 dni od dnia jego doręczenia."
            )

        add_line(self.document, 30)
        normal_right(
            self.document,
            "(podpis Przewodniczącego Zespołu Orzekającego)               ",
            size=8
            )
        insert_reciver(self.document, self.value)

    def issue_profound(self):
        normal_right(
            self.document, 
            "Grodzisk Wielkopolski, {}".format(
                self.value["staff_meeting_date"]
                ),
            size=10,
            bold=False
            )
        add_line(
            self.document, 2
            )
        normal_center(
            self.document,
            "ORZECZENIE NR \n o potrzebie zajęć rewalidacyjno-wychowawczych",
            size=12,
            bold=True,
            )
        add_line(
            self.document, 8
            )
        normal_justify(
            self.document, 
            "Działając na podstawie art. 127 ust. 10 ustawy z dnia 14 grudnia"
            " 2016 r. – Prawo oświatowe (Dz. U. z 2017 r. poz. 59 i 949)",
            size=9
            )
        applicant(
            self.document, 
            self.value["applicant_n"]
            )
        staff(
            self.document,self.value 
            )
        add_line(
            self.document, 12
            )
        individual_group(
            self.document,
            self.value
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document, 
            self.value["name_n"], 
            "(imię/imiona i nazwisko dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["birth_date"] + "r., " + self.value["birth_place"],
            "(data i miejsce urodzenia dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            self.value["pesel"],
            "(numer PESEL dziecka, a w przypadku braku numeru PESEL – seria"
            " i numer dokumentu potwierdzającego jego tożsamość)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value["zip_code"],
                    " ",
                    self.value["city"],
                    ", ",
                    self.value["address"]
                    ]
                ),
            "(adres zamieszkania dziecka)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                    [
                    self.value['school_name'],
                    ", ",
                    self.value['school_sort'],
                    ", ",
                    self.value['school_city'],
                    ", ",
                    self.value['school_address']
                    ]
                ),
            "(nazwa i adres podmiotu organizującego zajęcia"
            " rewalidacyjno-wychowawcze&)"
            )
        add_line(
            self.document, 10
            )
        text_with_tag(
            self.document,
            "".join(
                [
                    self.value["applicant_n"],
                    ", ",
                    self.value["applicant_zipcode"],
                    " ",
                    self.value['applicant_city'],
                    ", ",
                    self.value['applicant_address']
                ]
                ),
            "(imiona i nazwiska rodziców& oraz adres ich zamieszkania)"
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "w okresie do dnia&: {}".format(self.value['timespan_ind']),
            bold=True
            )
        add_line(self.document, 10)
        normal_left(
            self.document,
            "ze względu na niepełnosprawność intelektualną w stopniu głębokim."
            )
        page_break(self.document)
        normal_center(
            self.document,
            "Diagnoza",
            size=10,
            bold=True
            )
        normal_justify(
            self.document,
            "Zespół Orzekający przedstawia diagnozę funkcjonowania dziecka,"
            " z uwzględnieniem potencjału rozwojowego, mocnych stron dziecka"
            " oraz występujących w środowisku nauczania i wychowania barier i"
            " ograniczeń utrudniających jego funkcjonowanie:",
            size=8
            )
        add_line(self.document, 10)
        normal_center(
            self.document,
            "Zalecenia",
            size=10,
            bold=True
            )
        normal_left(
            self.document,
            "Zespół Orzekający zaleca:"
            )
        recommendations(
            self.document,
            self.value['recommendations']
            )
        normal_center(
            self.document,
            "Dodatkowe informacje",
            size=10,
            bold=True
            )
        normal_center(
            self.document,
            "(w zależności od potrzeb podaje się dodatkowe istotne informacje"
            " o dziecku, w szczególności o wspomagającej lub alternatywnej"
            " metodzie komunikacji (AAC), którą posługuje się dziecko)",
            size=8
            )
        add_line(self.document, 10)
        normal_justify(
            self.document,
            "W przypadku wydania nowego orzeczenia o potrzebie zajęć"
            " rewalidacyjno-wychowawczych należy wskazać okoliczności, które"
            " Zespół Orzekający uznał za istotne dla rozstrzygnięcia, oraz"
            " wyjaśnić powody, na podstawie których stwierdzono potrzebę"
            " wydania nowego orzeczenia&:",
            size=10
            )
        add_line(self.document, 10)
        normal_bold(
            self.document,
            "Orzeczenie uchyla&:\n"
            "1) orzeczenie nr ...... o potrzebie zajęć"
            " rewalidacyjno-wychowawczych zespołowych/indywidualnych&"
            " z dnia ........wydane przez ........................\n"
            "2) orzeczenie nr ...... o potrzebie kształcenia specjalnego"
            " z dnia ........wydane przez ........................\n\n"
            "Od niniejszego orzeczenia przysługuje odwołanie do Kuratora"
            " Oświaty w ................"
            " za pośrednictwem Zespołu Orzekającego, który wydał orzeczenie,"
            " w terminie 14 dni od dnia jego doręczenia."
            )
        
        normal_left(self.document, "\n\n\n")
        normal_right(
            self.document,
            "(podpis Przewodniczącego Zespołu Orzekającego)               ",
            size=8
            )
        insert_reciver(self.document, self.value)

    def save(self):
        if not os.path.exists('./orzeczenia'):
            os.makedirs('./orzeczenia')
        self.document.save('tmp.docx')

    def insert_footnotes(self):
        zipedfile = ZipFile("tmp.docx", "r")
        zipedfile.extractall(path="new")
        insert_footnotes_xml1(self.value['footnotes'])
        document_xml_change1()
        change_content_xml()
        change_rels()
        save_changed_xml(
            "new",
            os.path.join(
                './orzeczenia',
                "{} - {} orzecz.docx".format(
                    self.value['name_n'],
                    self.value['staff_meeting_date']
                    )
                )
        )
        delete_xml_folder(path="new")
