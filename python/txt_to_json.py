import datetime
from datetime import datetime
import os
from turtle import right
import pandas as pd
import json


# the event class, contains start/end year of event and the event itself
class Event:
    def __init__(self, startYear, endYear, event):
        self.startYear = startYear
        self.endYear = endYear
        self.event = event

    #adds the object to json file in json format
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)

# memoir class, contains memoir title, author, and content
class Memoir:
    def __init__(self, memoirTitle, memoirAuthor, memoirContent):
        self.memoirTitle = memoirTitle
        self.memoirAuthor = memoirAuthor
        self.memoirContent = memoirContent

    #adds the object to json file in json format
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)


# translates gender in place from the *_persons.csv file (replace * with any letter, A_persons.csv )
def genderTranslation(row):
    if (row['gender'] == 'male'):
        return '男性'
    elif (row['gender'] == 'female'):
        return '女性'
    else:
        return '未知'

# gets the rightist year from the *_persons.csv (A_persons.csv, B_persons.csv, etc..)
def getRightistYear(row):
    if row['rightistYear']:
        return row['rightistYear']
    else:
        return ''

# translates status in place from the *_persons file (A_persons.csv, B_persons.csv, etc..)
def statusTranslation(row):
    if (row['status'] == 'Dead'):
        return '亡故'
    elif (row['status'] == 'Alive'):
        return '在世'
    else:
        return '未知'

# gets Chinese description
def getDescription(row):
    # change path as fit
    path = '/Users/wprice/Documents/Translate/final/C'
    os.chdir(path)
    text = ''
    for file in os.listdir(path):
        if row['fullName'] in file: #if the chinese name matches the file name
            with open(file, 'r', encoding="utf-8") as txt_file:
                line = txt_file.readline()
                description = line.split('，')  # split by Chinese comma
                if len(description) > 1: #detects if there is a description, not just a name
                    for i in range(1, len(description)):
                        text += description[i]
                    return text
                else:
                    return "未知" #unknown 


def getMemoir(row):
    path = '/Users/wprice/Documents/Translate/final/C'
    os.chdir(path)
    memoir = ''
    found = False
    memoirs = []
    content = ''
    for file in os.listdir(path):
        if row['fullName'] in file:  # matching Chinese name
            with open(file, 'r', encoding="utf-8") as txt_file:
                lines = txt_file.readlines()
                for line in lines:
                    memoir = Memoir('', '', '')
                    if '---' in line:  # when '---' is found, memoir is found
                        found = True
                    if found:
                        memoir.memoirAuthor = ''
                        memoir.memoirTitle = ''
                        if '----' not in line:
                            content += line
                memoir.memoirContent = content
                memoirs.append(memoir.toJson())
    return memoirs


def getEvents(row):
    path = '/Users/wprice/Documents/Translate/final/C'
    os.chdir(path)
    found = False
    events = []
    for file in os.listdir(path):
        if row['fullName'] in file:  # matching Chinese name
            with open(file, 'r', encoding="utf-8") as txt_file:
                index = 0
                lines = txt_file.readlines()
                for line in lines:
                    event = Event(0, 0, '')
                    if row['fullName'] in line or '——' in line:
                        continue
                    elif '19' in line:  # when '---' is found, memoir is found
                        found = True
                    elif '--' in line:
                        return events
                    else:
                        found = False
                    if found:
                        index += 1
                        event.startYear = line[:4]
                        event.endYear = 0
                        event.event = line[6:]

                        events.append(event.toJson())
    return events


def getReference(row):
    path = '/Users/wprice/Documents/Translate/final/C'
    os.chdir(path)

    found = False
    for file in os.listdir(path):
        if row['fullName'] in file:  # matching Chinese name
            with open(file, 'r', encoding="utf-8") as txt_file:
                lines = txt_file.readlines()
                for line in lines:
                    if '——' in line:
                        return line[2:]
    return '未知'


def getEthnicity(row):
    if row['description'] and len(row[21]) >= 2:
        if '族' in row['description'][1] and len(row['description'][1]) < 5:
            return row['description'][1]
        elif '族' in row['description'][0] and len(row['description'][0]) < 5:
            return row['description'][0]
        else:
            return '未知'
    else:
        return '未知'


def memiorAuthor(row):
    return ''


def memiorTitle(row):
    return ''


def eventEndingDate(row):
    return ''


def imageId(row):
    return ''


def job(row):
    return ''


def initial(row):
    return 'C'


def firstName(row):
    return ''


def lastName(row):
    return ''


def birthplace(row):
    return ''


def deathYear(row):
    return 0


def rightistYear(row):
    return ''


def birthPlace(row):
    return ''


def education(row):
    return ''


def detailJob(row):
    return ''


def workplace(row):
    return ''

def contributorId(row):
    return ''


def workplaceCombined(row):
    path = '/Users/wprice/Documents/Translate/final/C'
    os.chdir(path)
    text = ''
    for file in os.listdir(path):
        if row['fullName'] in file:
            with open(file, 'r', encoding="utf-8") as txt_file:
                line = txt_file.readline()
                description = line.split('，')  # split by Chinese comma
                if len(description) > 2:
                    for i in range(2, len(description)):
                        text += description[i]
                    return text
                else:
                    return "未知"


def source(row):
    return '原文'

def checkEmptyEventArray(row):
    
    if row['events'] == '':
        return []
    else:
        return row['events']
    
def checkEmptyMemoirsArray(row):
    
    if row['memoirs']:
        if '"memoirContent": ""' in row['memoirs'][0]:
            return []
        else:
            return row['memoirs']


if __name__ == '__main__':
    target = '/Users/wprice/Documents/Translate/final'
    os.chdir(target)

    df = pd.read_csv('C_persons.csv') #change the name of csv file as fit
    
    #goes into the *_persons.csv file, and read row by row
    
    # the 'gender' column will be filled with the return value of 'genderTranslation' function.
    # same logic applies for all other
    df['gender'] = df.apply(lambda row: genderTranslation(row), axis=1)
    df['status'] = df.apply(lambda row: statusTranslation(row), axis=1)
    df['memoirs'] = df.apply(lambda row: getMemoir(row), axis=1)
    df['memoirs'] = df.apply(lambda row: checkEmptyMemoirsArray(row), axis=1)
    df['events'] = df.apply(lambda row: getEvents(row), axis=1)
    df['events'] = df.apply(lambda row: checkEmptyEventArray(row), axis=1)
    df['reference'] = df.apply(lambda row: getReference(row), axis=1)
    df['ethnicity'] = df.apply(lambda row: getEthnicity(row), axis=1)
    df['imageId'] = df.apply(lambda row: imageId(row), axis=1)
    df['job'] = df.apply(lambda row: job(row), axis=1)
    df['initial'] = df.apply(lambda row: initial(row), axis=1)
    df['firstName'] = df.apply(lambda row: job(row), axis=1)
    df['lastName'] = df.apply(lambda row: job(row), axis=1)
    df['birthplace'] = df.apply(lambda row: birthplace(row), axis=1)
    df['deathYear'] = df.apply(lambda row: deathYear(row), axis=1)
    df['birthPlace'] = df.apply(lambda row: birthPlace(row), axis=1)
    df['education'] = df.apply(lambda row: education(row), axis=1)
    df['detailJob'] = df.apply(lambda row: detailJob(row), axis=1)
    df['workplace'] = df.apply(lambda row: workplace(row), axis=1)
    df['workplaceCombined'] = df.apply(lambda row: workplaceCombined(row), axis=1)
    df['source'] = df.apply(lambda row: source(row), axis=1)
    df['description'] = df.apply(lambda row: getDescription(row), axis=1)
    df.insert(loc=2, column='lastUpdatedAt', value=[str(datetime.now().replace(microsecond=0).isoformat()) for _ in df.index])
   
    # removes any columns that were extra/not needed
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.drop(['birthPlace'], axis=1)
    df = df.drop(['publish'], axis=1)
    df = df.drop(['contributorId'], axis=1)
    df['contributorId'] = df.apply(lambda row: contributorId(row), axis=1)
    person_json = df.set_index(
        'rightistId', drop=False).to_dict(orient='index')
    df['rightistYear'] = df.apply(lambda row: getRightistYear(row), axis=1)

    # puts the csv file into a json file, removes some speicla characters
    jsonString = json.dumps(person_json, indent=4, ensure_ascii=False)
    jsonString = jsonString.replace(r'\"', r'"')
    jsonString = jsonString.replace(r'"{', r'{')
    jsonString = jsonString.replace(r'}"', r'}')
    jsonString = jsonString.replace('NaN', '0')
    jsonString = jsonString.replace('null', '0')
    jsonString = jsonString.replace('\u201c', r"'")
    jsonString = jsonString.replace('\u201d', r"'")
    jsonString = jsonString.replace(r'\\"', r'\\')

    with open('output.json', mode='w', encoding='utf-8-sig') as f:
        f.write(jsonString)
