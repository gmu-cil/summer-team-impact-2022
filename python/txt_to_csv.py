import re
import csv
import os
import sys

persons = []
memoirs = []
count = 0

EXCEL_LIMIT = 32767 - 2000
# Folder Path
folder = sys.argv[1]
path = r'C:\Users\andan\OneDrive\Desktop\STIP\txt\{}'.format(folder)

ethnic_groups = [
    'Han', 'Zhuang', 'Hui', 'Man', 'Uygur', 'Miao', 'Yi', 'Tujia', 'Zang', 'Mongol',
    'Dong', 'Bouyei', 'Yao', 'Chosŏn', 'Hani', 'Li', 'Kazak', 'Dai', 'She', 'Lisu', 'Dongxiang', 'Gelao',
    'Lahu', 'Wa', 'Sui', 'Naxi', 'Qiang', 'Tu', 'Mulao', 'Xibe', 'Kirgiz', 'Jingpo', 'Daur', 'Salar', 'Blang',
    'Maonan', 'Tajik', 'Pumi', 'Achang', 'Nu', 'Ewenki', 'Gin', 'Jino', 'Deang', 'Bonan', 'Russ', 'Yugur',
    'Uzbek', 'Monba', 'Oroqen', 'Derung', 'Hezhen', 'Gaoshan', 'Lhoba', 'Tatar'
]


class Person:
    def __init__(self, person_id, first_name, last_name, full_name, gender, year_birth, year_death, year_rightist, birthplace, nationality, education, title, workplace, events, reference, description):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.gender = gender
        self.year_birth = year_birth
        self.year_death = year_death
        self.year_rightist = year_rightist
        self.birthplace = birthplace
        self.nationality = nationality
        self.education = education
        self.title = title
        self.workplace = workplace
        self.events = events
        self.reference = reference
        self.description = description


class Event:
    def __init__(self, event_id, person_id, start_year, end_year, event):
        self.event_id = event_id
        self.person_id = person_id
        self.start_year = start_year
        self.end_year = end_year
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
                            name_text = split[1]
                        else:
                            person.person_id = f"{folder}{count}"
                            name_text = sub

                        person.description = line
                        count += 1

                        # sth(1985... or sth(?-1985)
                        if (re.match('.*\s\([0-9]{4}|.*\s\(\?-[0-9]{4}', name_text)):
                            name_data = re.split('\s', name_text)
                            print(name_data)
                            if ('' in name_data):
                                name_data.remove('')

                            first_name = name_data[0]
                            last_name = ''
                            for i, val in enumerate(name_data):
                                if (i > 0 and i < len(name_data) - 1):
                                    last_name += val
                                    last_name += ' '
                            full_name = first_name + ' ' + last_name
                            years_s = name_data[len(name_data) - 1]
                            years = re.split('-', years_s)
                            print(years)
                            person.first_name = first_name
                            person.last_name = last_name
                            person.full_name = full_name
                            year_birth = years[0][1:]
                            year_death = years[1][:-1]

                            if (re.match(r'\d+', year_birth)):
                                person.year_birth = re.findall(
                                    r'\d+', year_birth)[0]
                            else:
                                person.year_birth = ''

                            if (re.match(r'\d+', year_death)):
                                person.year_death = re.findall(
                                    r'\d+', year_death)[0]
                            else:
                                person.year_death = ''

                        # pattern: sth(1985...
                        elif (re.match(r'[a-zA-Z]*\([0-9]{4}', name_text)):

                            name_data = re.split('(', name_text, 1)
                            names = name_data[0]
                            if (' ' in names):
                                names_text = re.split(' ', names, 1)
                                first_name = names_text[0]
                                last_name = names_text[1]
                            else:
                                first_name = names
                                last_name = ''
                            full_name = first_name + ' ' + last_name
                            person.first_name = first_name
                            person.last_name = last_name
                            person.full_name = full_name
                        # sth(?-1985)
                        elif (re.match('[a-zA-Z]*\(\?-[0-9]{4}', name_text)):
                            name_data = re.split('(', name_text, 1)
                            names = name_data[0]
                            if (' ' in names):
                                names_text = re.split(' ', names, 1)
                                first_name = names_text[0]
                                last_name = names_text[1]
                            else:
                                first_name = names
                                last_name = ''
                            full_name = first_name + ' ' + last_name
                            person.first_name = first_name
                            person.last_name = last_name
                            person.full_name = full_name
                            year_data = re.split('-', year_text)
                            year_birth = year_data[0][1:]
                            year_death = year_data[1][:-1]
                            person.year_birth = year_birth
                            person.year_death = year_death
                        # (1985-1986)
                        elif (re.match(".*\s([0-9]{4}-[0-9]{4})", name_text)):
                            name_data = re.split('\s', name_text, 1)
                            names = name_data[0]
                            if (' ' in names):
                                names_text = re.split(' ', names, 1)
                                first_name = names_text[0]
                                last_name = names_text[1]
                            else:
                                first_name = names
                                last_name = ''
                            full_name = first_name + ' ' + last_name
                            year_text = name_data[1]
                            year_data = re.split('-', year_text)
                            year_birth = year_data[0][1:]
                            year_death = year_data[1][:-1]
                            person.year_birth = year_birth
                            person.year_death = year_death
                        else:
                            name_data = re.split(' ', name_text, 1)
                            if (len(name_data) == 2):
                                first_name = name_data[0]
                                last_name = name_data[1]
                            elif (len(name_data) == 1):
                                first_name = name_data[0]
                                last_name = ''
                            full_name = first_name + ' ' + last_name
                            person.first_name = first_name
                            person.last_name = last_name
                            person.full_name = full_name

                    if (i > 0):
                        for group in ethnic_groups:
                            test = sub.strip().lower()
                            # "Han"
                            if (re.search('^{}$'.format(group), test, re.IGNORECASE)):
                                person.nationality = group
                            # "Han Nationality"
                            if (re.match('nationality', test, re.IGNORECASE)):
                                # account for [nationality] nationality or nationality [nationality]
                                nationality = re.split(' ', test)
                                nationality.remove('nationality')
                                person.nationality = nationality[0]
                            # "Han ethnic group"
                            if (re.match('ethnic', test, re.IGNORECASE)):
                                nationality = re.split(' ', test)
                                person.nationality = nationality[0]

                    if (re.match('male', sub, re.IGNORECASE)):
                        person.gender = 'male'

                    if (re.match('female', sub, re.IGNORECASE)):
                        person.gender = 'female'

                    if (re.match('education', sub, re.IGNORECASE)):
                        education_s = re.split(' ', sub)
                        print(education_s)
                        for sub_string in education_s:
                            sub_string = sub_string.strip().lower()
                            print(sub_string)
                        try:
                            education_s.remove('education')
                        except ValueError:
                            pass

                        education = ''
                        for sub_string in education_s:
                            education += sub_string
                            education += ' '
                        person.education = education

                    if (re.match('(\s|,)age(\s|,)', sub)):
                        age = re.split(' ', sub)
                        age.remove('age')
                        person.age = (int)(age)
                    if (re.match('\snative|born\s', sub)):
                        if (re.findall('\s(in|at)\s', sub)):
                            native = re.split('\sin|at\s', sub)
                            birthplace = native[1]
                        else:
                            native = re.split('\s', sub)
                            birthplace = native[1]

                        person.birthplace = birthplace

                    if (re.search('\s(in|of|at)\s', sub)):
                        # exclude the native/born string
                        if not (any(re.findall(r'native|born', sub))):
                            print(sub)

                            data = re.split('\sin|of|at\s', sub, 1)
                            title = data[0].strip()
                            workplace = data[1].strip()
                            person.title = title
                            person.workplace = workplace

                    if (re.search('(cadre|cadres)$', sub, re.IGNORECASE)):
                        data = re.split('\s', sub)
                        title = ''
                        workplace = ''
                        for index, sub_string in enumerate(data):
                            if (index != len(data) - 1):
                                workplace += sub_string
                                workplace += ' '
                            else:
                                title = 'cadre'
                        person.title = title
                        person.workplace = workplace

                    if (re.search('(teacher|teachers)$', sub, re.IGNORECASE)):
                        data = re.split('\s', sub)
                        title = ''
                        workplace = ''
                        for index, sub_string in enumerate(data):
                            if (index != len(data) - 1):
                                workplace += sub_string
                                workplace += ' '
                            else:
                                title = 'teacher'
                        person.title = title
                        person.workplace = workplace
            else:
                # person.reference
                if (re.match("^[-]+$", line)):
                    if person.reference:
                        # done = False
                        result = ''
                        counter = index + 1
                        memoir_part = 0
                        done = False

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
                            print(len(result))

                            if (len(result) < EXCEL_LIMIT):
                                memoir_another = Memoir('', '', '')
                                memoir_another.memoir_id = f'M{person.person_id}{memoir_counter}-{memoir_part}'
                                memoir_counter += 1
                                memoir_another.person_id = person.person_id
                                memoir_another.memoir = result
                                memoirs.append(memoir_another)

                # If not the end "--Excerpted" or "From"
                if not re.match('^(--|--Excerpted|Excerpted)', line):
                    # Enter an event line
                    event_o = Event('', '', '', '', '')
                    # extract the first sentence
                    sentence = line
                    sentence = sentence.strip()
                    event = ''
                    start_year = ''
                    end_year = ''
                    if (re.match('.*[0-9]{4}.*', sentence)):
                        # "In 1985..."
                        if (re.match("^In\s[0-9]{4}[\s|,|.]", sentence)):

                            subs = re.split('\s', sentence, 1)
                            year_text = subs[1]
                            data = re.split('\s|,|\.', year_text, 1)
                            start_year = data[0]
                            event = data[1]
                        elif (re.match("^In\s[0-9]{4}-[0-9]{4}[\s|,|.]", sentence)):
                            subs = re.split('\s', sentence, 1)
                            year_text = subs[1]
                            year_data = re.split('-', year_text, 1)
                            start_year = year_data[0]
                            other = re.split('\s|,|\.', year_data[1], 1)
                            end_year = other[0]
                            event = other[1]
                        elif (re.match("^On\s[0-9]{4}(\s|,|\.)", sentence)):
                            subs = re.split('\s', sentence, 1)
                            year_text = subs[1]
                            data = re.split('\s|,|\.', year_text, 1)
                            start_year = data[0]
                            event = data[1]
                        else:
                            # "1986,..."
                            if (re.match('^[0-9]{4}(\s|,|\.)', sentence)):
                                years = re.split('\s|,|\.', sentence, 1)
                                start_year = years[0]
                                event = years[1]

                            # "1986-1990, "
                            elif (re.match('^[0-9]{4}-[0-9]{4}(\s|,|\.)', sentence)):
                                years = re.split('-', sentence, 1)
                                start_year = years[0]
                                year_text = years[1]
                                data = re.split('\s|,|\.', year_text, 1)
                                end_year = data[0]
                                event = data[1]

                            elif (re.match('^[0-9]{4}-\?(\s|,|\.)', sentence)):
                                years = re.split('-', sentence, 1)
                                start_year = years[0]
                                year_text = years[1]
                                data = re.split('(\s|,|\.)', year_text, 1)
                                end_year = data[0]
                                event = data[1]

                    if ((re.search('\sthe.{1}right', event) or re.search('\sright.{1}wing', event))
                            and (re.search('\sbeaten\s', event) or re.search('\sclassified\s', event))):
                        if (int(start_year) < 1960 and int(start_year) > 1956):
                            person.year_rightist = start_year

                    if (re.match(r'\d+', start_year)):
                        event_o.start_year = re.findall(r'\d+', start_year)[0]
                    if (re.match(r'\d+', end_year)):
                        event_o.end_year = re.findall(r'\d+', end_year)[0]
                    else:
                        event_o.end_year = ''

                    event_o.event = event.strip()
                    event_o.event_id = f'E{person.person_id}{event_counter}'
                    event_o.person_id = person.person_id
                    events.append(event_o)
                    event_counter += 1
                else:
                    reference_text = line[2:]
                    person.events = events
                    person.reference = reference_text

        persons.append(person)


csv_target = r'C:\Users\andan\OneDrive\Desktop\STIP\updated_csv'


def write_to_csv(persons):
    global memoirs
    os.chdir(csv_target)
    person_fields = ['person_id', 'first_name', 'last_name', 'full_name', 'gender', 'year_of_birth', 'year_of_death',
                     'year_rightist', 'birthplace', 'nationality', 'education', 'title', 'workplace', 'reference', 'description']
    event_fields = ['event_id', 'person_id', 'start_year', 'end_year', 'event']
    memoir_fields = ['memoir_id', 'person_id', 'memoir']
    csv_file = persons[0].person_id[0]

    with open(f'{csv_file}_persons.csv', mode='w', encoding="utf-8", newline='') as csvfile:
        person_writer = csv.writer(csvfile)
        person_writer.writerow(person_fields)
        for person in persons:
            person_writer.writerow([
                person.person_id,
                person.first_name,
                person.last_name,
                person.full_name,
                person.gender,
                person.year_birth,
                person.year_death,
                person.year_rightist,
                person.birthplace,
                person.nationality,
                person.education,
                person.title,
                person.workplace,
                person.reference,
                person.description])

    with open(f'{csv_file}_events.csv', mode='w', encoding='utf-8', newline='') as csvfile:
        event_writer = csv.writer(csvfile)
        event_writer.writerow(event_fields)
        for person in persons:
            for event in person.events:
                if (event.event):
                    event_writer.writerow([
                        event.event_id,
                        event.person_id,
                        event.start_year,
                        event.end_year,
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

    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            # call read text file function
            read_text_file(file_path)

    # for memoir in memoirs:
    #     print(memoir.memoir_id)
    #     print(memoir.memoir)
    write_to_csv(persons)
