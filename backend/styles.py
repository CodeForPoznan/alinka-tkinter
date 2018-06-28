# pylint: disable=E1101, E0611

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt


def my_styles(document):
    '''
    Header - center, 12pt, bold
    
    style for

    Zespół orzekajacy przy poradni...
    Orzeka o....
    '''
    Header_my = document.styles.add_style(
        'Header_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Header_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(12)
    font.bold = True
    justification = Header_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.CENTER

    '''
    Small_my - justificated, 10pt
    '''

    Small_my = document.styles.add_style(
        'Small_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Small_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(10)
    font.bold = False
    justification = Small_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    '''
    Text_my - centered, 10pt, bold

    style for

    Name, adress, itd
    '''
    Text_my = document.styles.add_style(
        'Text_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Text_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(10)
    font.bold = True
    justification = Text_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    '''
    Tag_my - centered, 8pt, bold

    style for

    Name, adress, itd
    '''
    Tag_my = document.styles.add_style(
        'Tag_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Tag_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(7)
    font.bold = False
    justification = Tag_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.CENTER

    '''
    Normal_center_my
    '''
    Normal_center_my = document.styles.add_style(
        'Normal_center_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Normal_center_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(10)
    font.bold = False
    justification = Normal_center_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.CENTER

    '''
    Normal_right_my
    '''
    Normal_right_my = document.styles.add_style(
        'Normal_right_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Normal_right_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(10)
    font.bold = False
    justification = Normal_right_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    '''
    Normal_left_my
    '''
    Normal_left_my = document.styles.add_style(
        'Normal_left_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Normal_left_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(10)
    font.bold = False
    justification = Normal_left_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.LEFT

    '''
    Normal_justify_my
    '''
    Normal_justify_my = document.styles.add_style(
        'Normal_justify_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Normal_justify_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(10)
    font.bold = False
    justification = Normal_justify_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    '''
    Przypisdolny
    '''

    Przypisdolny = document.styles.add_style(
        'Przypisdolny', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Przypisdolny.font
    font.name = 'TimesNewRoman'
    font.size = Pt(7)
    font.bold = False
    justification = Przypisdolny.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.LEFT

    '''
    Normal_bold_my
    '''

    Normal_bold_my = document.styles.add_style(
        'Normal_bold_my', WD_STYLE_TYPE.PARAGRAPH
        )
    font = Normal_bold_my.font
    font.name = 'TimesNewRoman'
    font.size = Pt(10)
    font.bold = True
    justification = Normal_bold_my.paragraph_format
    justification.alignment = WD_ALIGN_PARAGRAPH.LEFT
   
    return document
