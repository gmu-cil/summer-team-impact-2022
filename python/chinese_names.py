import csv
import os
from googletrans import Translator
import pandas as pd
import re
import json

# data folder
target = r'C:\Users\yulez\Documents\STIP\data\A'
source = r'C:\Users\yulez\Documents\STIP\data\result'
# folder contains uncleaned csv (by running txt_to_csv)
# next = r'C:\Users\andan\OneDrive\Desktop\STIP\other'
# folder contains cleaned csv
# other = r'C:\Users\andan\OneDrive\Desktop\STIP\refined_csv'
EXCEL_LIMIT = 32767 - 2000

# csv_file_path = r'C:\Users\yulez\Documents\STIP\data\refined_csv\refined_csv\A_persons.csv'
dest_path = r'C:\Users\yulez\Documents\STIP\data'

# init the Google API translator
translator = Translator()


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
person_fields = ['person_id', 'first_name', 'last_name', 'full_name', 'gender', 'year_of_birth', 'year_of_death',
                 'year_rightist', 'birthplace', 'nationality', 'education', 'title', 'workplace', 'reference', 'description']
event_fields = ['event_id', 'person_id', 'start_year', 'end_year', 'event']
memoir_fields = ['memoir_id', 'person_id', 'memoir']


ethnic_groups_mapping = dict(zip(ethnic_groups, chinese_ethnic_groups))


os.chdir(source)


def cleanName(row):
    return row['last_name'].split()[0].title()


class Event:
    def __init__(self, event_id, start_year, end_year, event):
        self.event_id = event_id
        self.start_year = start_year
        self.end_year = end_year
        self.event = event

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)


class Memoir:
    def __init__(self, memoir_id, memoir):
        self.memoir_id = memoir_id
        self.memoir = memoir

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)


def get_chinese_description(row):
    for file in os.listdir():
        if (file.endswith('.txt')):
            if row['chineseName'] in file:
                with open(file, 'r', encoding='utf-8') as input:
                    lines = input.readlines()
                    for index, line in enumerate(lines):
                        if (index == 0):
                            return line


def get_chinese_reference(row):
    for file in os.listdir():
        if (file.endswith('.txt')):
            if row['chineseName'] in file:
                with open(file, 'r', encoding='utf-8') as input:
                    lines = input.readlines()
                    for index, line in enumerate(lines):
                        line = line.replace('\u2014', '-')
                        if (index != 0):
                            if re.match('^(--)+', line):
                                return line


def get_chinese_events(row):
    for file in os.listdir():
        if (file.endswith('.txt')):
            if row['chineseName'] in file:
                with open(file, 'r', encoding='utf-8') as input:
                    events = []
                    lines = input.readlines()
                    count = 0
                    for index, line in enumerate(lines):
                        line = line.replace('\u2014', '-')
                        line = line.replace('\uff0c', ',')
                        if (index > 0):
                            if not re.match('^(——|——摘自|摘自)', line):

                                if re.match('^[0-9]{4}', line):
                                    # print(row['chineseName'])
                                    # print(line)
                                    event_o = Event('', '', '', '')
                                    data = re.split(',', line, 1)
                                    if (len(data) == 2):
                                        start_year = data[0][:-1]
                                        event = data[1]
                                        rightistId = row['rightistId']
                                        event_o.event_id = f'E{rightistId}{count}'
                                        event_o.start_year = start_year
                                        event_o.event = event
                                        jsonString = event_o.toJSON()
                                        events.append(jsonString)
                                    else:
                                        events.append(event_o.toJSON())

                                    count += 1
                    return events


def get_chinese_memoirs(row):

    for file in os.listdir():
        if (file.endswith('.txt')):
            if row['chineseName'] in file:
                with open(file, 'r', encoding='utf-8') as input:
                    memoirs = []
                    memoir_counter = 0
                    lines = input.readlines()
                    for index, line in enumerate(lines):
                        if index > 1:
                            # extract memoir
                            if (re.match("^[-]+$", line)):
                                # store memoir
                                if row['chinese_reference']:
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
                                        memoir_another = Memoir('', '')
                                        rightistId = row['rightistId']
                                        memoir_another.memoir_id = f'M{rightistId}{memoir_counter}'
                                        memoir_counter += 1
                                        memoir_another.memoir = result
                                        jsonString = memoir_another.toJSON()
                                        memoirs.append(jsonString)

                                    while (len(result) > EXCEL_LIMIT):

                                        memoir_o = Memoir('', '')
                                        rightistId = row['rightistId']
                                        memoir_another.memoir_id = f'M{rightistId}{memoir_counter}'

                                        base = result[:-
                                                      (len(result) - EXCEL_LIMIT)]
                                        memoir_o.memoir = base

                                        jsonString = memoir_another.toJSON()
                                        memoirs.append(jsonString)

                                        memoir_part += 1
                                        result = result[-(len(result) -
                                                          EXCEL_LIMIT):]

                                        if (len(result) < EXCEL_LIMIT):
                                            memoir_another = Memoir('', '')
                                            rightistId = row['rightistId']
                                            memoir_another.memoir_id = f'M{rightistId}{memoir_counter}'

                                            memoir_counter += 1
                                            memoir_another.memoir = result
                                            jsonString = memoir_another.toJSON()
                                            memoirs.append(jsonString)

                    return memoirs


def chineseEthnicity(csvFile, english_col_name, chinese_col_name):
    """
    this method maps english ethnicity to its relative chinese ethnicity, 
    and append the new 'chinese ethnicity column' into pandas.
    """

    csvFile[chinese_col_name] = csvFile[english_col_name].apply(
        lambda x: ethnic_groups_mapping[x])


def translateColToChinese(csvFile, english_col_name, chinese_col_name):
    """
    translate english col to chinese col from "current" CSV file. 
    A new CVS file with the new chinese translated col is added in the new file.  
    In this project, 'gender' is used here.
    """

    csvFile[chinese_col_name] = csvFile[english_col_name].apply(
        lambda x: translator.translate(x, dest='zh-cn').text)


# def chineseJob():


if __name__ == '__main__':
    ids = []
    names = []
    descriptions = []
    counter = 0
    index = 0

    os.chdir(source)
    merged = pd.read_csv('A_persons.csv').fillna(value="Unknown")
    os.chdir(target)
    merged['chinese_description'] = merged.apply(
        lambda row: get_chinese_description(row), axis=1)
    merged['chinese_reference'] = merged.apply(
        lambda row: get_chinese_reference(row), axis=1)
    merged['chinese_events'] = merged.apply(
        lambda row: get_chinese_events(row), axis=1)
    merged['chinese_memoirs'] = merged.apply(
        lambda row: get_chinese_memoirs(row), axis=1)

    translateColToChinese(merged, "gender", "chinese_gender")
    chineseEthnicity(merged, "ethnicity", "chinese_ethnicity")

    print(merged.head(50))
    print(merged.columns)
    # create a new CSV file
    merged.to_csv(dest_path + "\chinese_csv_file.csv", encoding='utf-8-sig')
