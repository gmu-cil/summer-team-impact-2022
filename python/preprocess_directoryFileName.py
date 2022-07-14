import os
import re
import aspose.words as aw
import win32com.client as win32
from win32com.client import constants
from pathlib import Path
from translate import Translator
import pypinyin


def translate_file_name(filename):
    """
    This method convert English name to Chinese name
    """

    result = pypinyin.lazy_pinyin(filename, style=pypinyin.Style.NORMAL)
    print(result)
    # if result:
    result[0] = result[0].capitalize()+"_"

    return "".join(result)+"_"+filename


def convert_doc_docx():
    """
    This method converts doc file to docx file, 
    and rename the file directory into English name with Chinese name
    """
    #directory = r"C:\Users\yulez\Documents\STIP"
    #directory = r"C:\Users\yulez\Documents\STIP\data\translated-files"
    new_directory = r"C:\Users\yulez\Documents\STIP\data\output"
    directory = r"C:\Users\yulez\Documents\STIP\data\New folder"
    extension = ".docx"
    for root, subdirectories, files in os.walk(directory):
        table = {}

        for file in files:

            try:

                old_path = os.path.join(root, file)

                p = Path(old_path)
                name_without_extension = p.stem
                extension = p.suffix

                chinese_name = ""
                for n in re.findall(r'[\u25A1-\u9fff]+', file):
                    chinese_name += n

                translated_filename = translate_file_name(chinese_name)

                p.rename(Path(p.parent, translated_filename + extension))
                table[translated_filename] = 0

            except FileExistsError:
                print(translated_filename)

                table[translated_filename] += 1
                new_file = translated_filename + \
                    str(table[translated_filename]) + extension
                print(new_file)
                p.rename(Path(p.parent, new_file))
