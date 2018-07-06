
import os
import shutil
from zipfile import ZipFile
from backend.data_xml import *


        
def insert_footnotes_xml1(footnotes_list):
    with open('new/word/footnotes.xml', 'w', encoding='UTF-8') as xml_to_save:
        footnotes_xml = footnote_base
        index = 2
        for i in footnotes_list:
            footnotes_xml += '''<w:footnote w:id="{}"><w:p><w:pPr>\
            <w:pStyle w:val="Przypisdolny"/></w:pPr><w:r><w:rPr>\
            <w:sz w:val="14"/></w:rPr><w:footnoteRef/>\
            <w:t>)</w:t></w:r><w:r><w:rPr><w:sz w:val="14"/></w:rPr>\
            <w:t xml:space="preserve"> {}</w:t></w:r></w:p>\
            </w:footnote>'''.format(index, i)
            index += 1
        footnotes_xml += "</w:footnotes>"
        xml_to_save.write(footnotes_xml)
        xml_to_save.close()

def document_xml_change1():
    with open('new/word/document.xml', 'r') as document_xml_to_change:
        document = document_xml_to_change.read()
        amper_occurance = document.count('&amp;')
        for occurance in range(0, amper_occurance):
            document = document.replace(
                '&amp;',
                '''</w:t></w:r><w:r><w:footnoteReference w:id="{0}"/>\
                <w:t>{1}</w:t></w:r><w:r><w:t>'''.format(
                    occurance + 2,
                    occurance + 1
                    ),
                1
                )
        document_xml_to_change.close()
    os.remove('new/word/document.xml')
    with open('new/word/document.xml', 'w') as document_xml_to_save:
        document_xml_to_save.write(document)
        document_xml_to_save.close()
            

def change_content_xml():
    with open('new/[Content_Types].xml', 'r') as content:
        document = content.read()
        first_part = document[:-8]
        last_part = document[-8:]
        full_content = first_part+content_types+last_part
        content.close()
    os.remove('new/[Content_Types].xml')
    with open('new/[Content_Types].xml', 'w') as new_content:
        new_content.write(full_content)
        new_content.close()

def change_rels():
    os.remove("new/word/_rels/document.xml.rels")
    with open("new/word/_rels/document.xml.rels", "w") as new_rels:
        new_rels.write(rels)
        new_rels.close()

    
def save_changed_xml(path, name):
    os.remove("tmp.docx")
    zipedfile = ZipFile(name, 'w')
    list_of_files=[]
    for i in os.walk(path):
        for x in i[2]:
            new_path = os.path.join(i[0],x)
            list_of_files.append(new_path)
    prefix_to_remove = os.path.commonprefix(list_of_files)

    for i in os.walk(path):
        for x in i[2]:        
            arcname_ = os.path.join(i[0],x).replace(prefix_to_remove,"")
            zipedfile.write("{}/{}".format(i[0], x), arcname=arcname_)
    zipedfile.close()

def delete_xml_folder(path):
    shutil.rmtree("new")


