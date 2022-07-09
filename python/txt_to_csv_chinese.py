import re
import sys
import os
import csv
from googletrans import Translator, constants
from pprint import pprint
import pandas as pd

persons = []
memoirs = []
count = 0

EXCEL_LIMIT = 32767 - 2000
# Folder Path
folder = "A"
# print(folder)
path = r'C:\Users\yulez\Documents\STIP\data\{}'.format(folder)


csv_file = 0
deep_copy = 0

EXCEL_LIMIT = 32767 - 2000
# Folder Path
# folder = sys.argv[1]
# path = r'C:\Users\andan\OneDrive\Desktop\STIP\txt\{}'.format(folder)
csv_file_path = r'C:\Users\yulez\Documents\STIP\data\refined_csv\refined_csv\A_persons.csv'
dest_path = r'C:\Users\yulez\Documents\STIP\data'

chinese_ethnic_groups = [
    '汉族', '壮族', '回族', '满族', '维吾尔族', '苗族', '彝族', '土家族', '藏族', '蒙古族',
    '侗族', '布依族', '瑶族', '白族', '朝鲜族', '哈尼族', '黎族', '哈萨克族', '傣族', '畲族', '傈僳族', '东乡族', '仡佬族',
    '拉祜族', '佤族', '水族', '纳西族', '羌族', '土族', '仫佬族', '锡伯族', '柯尔克孜族', '景颇族', '达斡尔族', '撒拉族', '布朗族',
    '毛南族', '塔吉克族', '普米族', '阿昌族', '怒族', '鄂温克族', '京族', '基诺族', '德昂族', '保安族', '俄罗斯族', '裕固族',
    '乌孜别克族', '门巴族', '鄂伦春族', '独龙族', '赫哲族', '高山族', '珞巴族', '塔塔尔族', '未知'
]
ethnic_groups = [
    'Han', 'Zhuang', 'Hui', 'Man', 'Uygur', 'Miao', 'Yi', 'Tujia', 'Zang', 'Mongol',
    'Dong', 'Bouyei', 'Yao', 'Bai', 'Chosŏn', 'Hani', 'Li', 'Kazak', 'Dai', 'She', 'Lisu', 'Dongxiang', 'Gelao',
    'Lahu', 'Wa', 'Sui', 'Naxi', 'Qiang', 'Tu', 'Mulao', 'Xibe', 'Kirgiz', 'Jingpo', 'Daur', 'Salar', 'Blang',
    'Maonan', 'Tajik', 'Pumi', 'Achang', 'Nu', 'Ewenki', 'Gin', 'Jino', 'Deang', 'Bonan', 'Russ', 'Yugur',
    'Uzbek', 'Monba', 'Oroqen', 'Derung', 'Hezhen', 'Gaoshan', 'Lhoba', 'Tatar', 'Unknown'
]


ethnic_groups_mapping = dict(zip(ethnic_groups, chinese_ethnic_groups))


def chineseEthnicity(english_col_name, chinese_col_name):
    """
    this method maps english ethnicity to its relative chinese ethnicity, 
    and append the new 'chinese ethnicity column' into pandas.
    """

    deep_copy[chinese_col_name] = deep_copy[english_col_name].apply(
        lambda x: ethnic_groups_mapping[x])


def translateColToChinese(english_col_name, chinese_col_name):
    """
    translate english col to chinese col from "current" CSV file. 
    A new CVS file with the new chinese translated col is added in the new file.  
    In this project, 'gender' is used here.
    """

    deep_copy[chinese_col_name] = deep_copy[english_col_name].apply(
        lambda x: translator.translate(x, dest='zh-cn').text)


def event():
    return 0


class Person:
    def __init__(self, person_id, first_name, last_name, full_name, gender, year_birth, year_death, year_rightist, birthplace, nationality, education, title, workplace, events, reference, description):
        self.person_id = person_id
        # self.first_name = first_name
        # self.last_name = last_name
        # self.full_name = full_name
        # self.gender = gender
        # self.year_birth = year_birth
        # self.year_death = year_death
        # self.year_rightist = year_rightist
        # self.birthplace = birthplace
        # self.nationality = nationality
        # self.education = education
        # self.title = title
        # self.workplace = workplace
        self.events = events
        self.reference = reference
        #self.description = description


class Event:
    def __init__(self, event_id, person_id, start_year, end_year, event):
        self.event_id = event_id
        self.person_id = person_id
        self.event = event


class Memoir:
    def __init__(self, memoir_id, person_id, memoir):
        self.memoir_id = memoir_id
        self.person_id = person_id
        self.memoir = memoir


def map(textfile):

    global count
    global memoirs
    with open(textfile, mode='r', encoding="utf-8") as f:

        lines = []
        events = []
        event_counter = 0
        memoir_counter = 0
        person = Person('', '', '', '', '', '', '', '',
                        '', '', '', '', '', [], '', '')
        lines = f.readlines()
        lines = [value for value in lines if value != '\n']

        for index, line in enumerate(lines):

            if (index == 0):
                subs = re.split(',', line)
                for i, sub in enumerate(subs):
                    sub = sub.strip()
                    if (i == 0):
                        # name
                        name_text = ''

                        if re.match('^[A-Z]{1}\s', sub):
                            split = re.split(' ', sub, 1)
                            person.person_id = f"{split[0]}{count}"
                            # name_text = split[1]
                        else:
                            person.person_id = f"{folder}{count}"
                            # name_text = sub

                        # person.description = line
                        count += 1

            else:
                # extract memoir
                if (re.match("^[-]+$", line)):

                    # store memoir
                    if person.reference:
                        print("---find memoir", line)
                        # done = False
                        result = ''
                        counter = index + 1
                        memoir_part = 0
                        done = False

                        # pass "reference section" until "memoir" -- check with string pattern "-------"
                        while not done and counter < len(lines):
                            target = lines[counter]

                            if not re.match("^[-]+", target):
                                result += target
                            else:
                                done = True
                            counter += 1

                        if (len(result) < EXCEL_LIMIT):
                            memoir_another = Memoir('', '', '')
                            memoir_another.memoir_id = f'M{person.person_id}{memoir_counter}'
                            memoir_counter += 1
                            memoir_another.person_id = person.person_id
                            memoir_another.memoir = result

                            memoirs.append(memoir_another)

                        while (len(result) > EXCEL_LIMIT):

                            memoir_o = Memoir('', '', '')

                            memoir_o.memoir_id = f'M{person.person_id}{memoir_counter}-{memoir_part}'
                            memoir_o.person_id = person.person_id
                            base = result[:-(len(result) - EXCEL_LIMIT)]
                            memoir_o.memoir = base
                            memoirs.append(memoir_o)
                            memoir_part += 1
                            result = result[-(len(result) - EXCEL_LIMIT):]

                            if (len(result) < EXCEL_LIMIT):
                                memoir_another = Memoir('', '', '')
                                memoir_another.memoir_id = f'M{person.person_id}{memoir_counter}-{memoir_part}'
                                memoir_counter += 1
                                memoir_another.person_id = person.person_id
                                memoir_another.memoir = result
                                memoirs.append(memoir_another)

                # extract events: If not the end "--摘自" or "摘自"
                if not re.match('^(——|——摘自|摘自)', line):

                    # Enter an event line
                    event_o = Event('', '', '', '', '')
                    # extract the first sentence
                    sentence = line
                    sentence = sentence.strip()
                    event = ''

                    if (re.match('.*[0-9]{4}。*', sentence)):

                        # "In YYYY..."
                        if (re.match("^[0-9]{4}年[\s|，|。]", sentence) or
                            re.match("^[0-9]{4}-[0-9]{4}年[\s|，|。]", sentence) or
                            re.match("^[0-9]{4}年(\s|，|\。)", sentence) or
                            re.match('^[0-9]{4}(\s|，|\。)', sentence) or
                            re.match('^[0-9]{4}-[0-9]{4}(\s|，|\。)', sentence) or
                                re.match('^[0-9]{4}-\?(\s|，|\。)', sentence)):

                            event = sentence

                    event_o.event = event.strip()

                    event_o.event_id = f'E{person.person_id}{event_counter}'
                    event_o.person_id = person.person_id
                    events.append(event_o)
                    event_counter += 1

                # extract 摘要 and attach event attributes to person.
                else:

                    reference_text = line[2:]

                    person.events = events
                    person.reference = reference_text
        print("-----------end with one person document--------------")
        persons.append(person)


csv_target = r'C:\Users\yulez\Documents\STIP\data\CSVFiles'


def write_to_csv(persons):
    global memoirs
    os.chdir(csv_target)
    person_fields = ['person_id', 'reference']
    event_fields = ['event_id', 'person_id', 'event']
    memoir_fields = ['memoir_id', 'person_id', 'memoir']
    csv_file = persons[0].person_id[0]

    with open(f'{csv_file}_persons.csv', mode='w', encoding="utf-8", newline='') as csvfile:
        person_writer = csv.writer(csvfile)
        person_writer.writerow(person_fields)
        for person in persons:
            person_writer.writerow([
                person.person_id,
                person.reference])

    with open(f'{csv_file}_events.csv', mode='w', encoding='utf-8', newline='') as csvfile:
        event_writer = csv.writer(csvfile)
        event_writer.writerow(event_fields)
        for person in persons:
            for event in person.events:

                if (event.event):
                    event_writer.writerow([
                        event.event_id,
                        event.person_id,
                        event.event])

    with open(f'{csv_file}_memoirs.csv', mode='w', encoding='utf-8', newline='') as csvfile:
        memoir_writer = csv.writer(csvfile)
        memoir_writer.writerow(memoir_fields)
        for memoir in memoirs:
            memoir_writer.writerow([
                memoir.memoir_id,
                memoir.person_id,
                memoir.memoir])


# Change the directory
os.chdir(path)
# Read text File


def read_text_file(file_path):
    map(file_path)


if __name__ == "__main__":
    # init the Google API translator
    translator = Translator()
    # # handle missing data: filled-in values is Unknown
    # csv_file = pd.read_csv(csv_file_path).fillna(value="Unknown")
    # # create an copy of csv file.
    # deep_copy = csv_file.copy()

    # translateColToChinese("gender", "chinese_gender")
    # chineseEthnicity("nationality", "chinese_ethnicity")

    # # create a new CSV file
    # deep_copy.to_csv(dest_path+"chinese_csv_file.csv")

    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            # call read text file function
            read_text_file(file_path)

    # for memoir in memoirs:
    #     memoir.memoir_id
    #     memoir.memoir

    write_to_csv(persons)
