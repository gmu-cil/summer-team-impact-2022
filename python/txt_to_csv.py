import re
import csv
import os
import sys

persons = []
count = 0

# Folder Path
folder = sys.argv[1]
path = r'C:\Users\andan\OneDrive\Desktop\STIP\txt\{}'.format(folder)

ethnic_groups = [
    'Han', 'Zhuang', 'Hui', 'Man', 'Uygur', 'Miao', 'Yi', 'Tujia', 'Zang', 'Mongol',
    'Dong', 'Bouyei', 'Yao', 'Chosŏn', 'Hani', 'Li', 'Kazak', 'Dai', 'She', 'Lisu', 'Dongxiang', 'Gelao',
    'Lahu', 'Wa','Sui', 'Naxi','Qiang','Tu','Mulao','Xibe','Kirgiz','Jingpo','Daur','Salar','Blang',
    'Maonan', 'Tajik', 'Pumi', 'Achang', 'Nu', 'Ewenki', 'Gin', 'Jino', 'Deang', 'Bonan', 'Russ', 'Yugur',
    'Uzbek', 'Monba', 'Oroqen', 'Derung', 'Hezhen', 'Gaoshan', 'Lhoba', 'Tatar'
]

class Person:
    def __init__(self, person_id, first_name, last_name, full_name, gender, year_birth, year_death, birthplace, nationality, education, title, workplace, events, reference, description):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name 
        self.full_name = full_name
        self.gender = gender
        self.year_birth = year_birth
        self.year_death = year_death
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

def map(textfile):
    global count
    with open(textfile, mode='r', encoding="utf-8") as f:
        lines = []
        events = []
        event_counter = 0
        person = Person('', '', '', '', '', '', '', '', '', '', '', '', [], '', '')
        lines = f.readlines()
        lines = [value for value in lines if value != '\n']
        done = False
        for index, line in enumerate(lines):
            if (done):
                break

            if (index == 0):
                subs = re.split(',', line)
                print(line)
                for i, sub in enumerate(subs):
                    sub = sub.strip()
                    if (i == 0):
                        #name
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
                            person.year_birth = years[0][1:]
                            person.year_death = years[1][:-1]  
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
                        # check the next string for province
                        # if ('Province' in subs[i + 1]):
                        #     birthplace += ', '
                        #     birthplace += subs[i + 1]
                        
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
                        if (re.match("^In\s[0-9]{4}(\s|,|.)", sentence)):
                            subs = re.split('\s', sentence, 1)
                            year_text = subs[1]
                            data = re.split('\s|,|\.', year_text, 1)
                            start_year = data[0]
                            event = data[1]
                        
                            
                        elif (re.match("^On\s[0-9]{4}(\s|,|\.)", sentence)):
                            print(event)
                            subs = re.split('\s', sentence, 1)
                            year_text = subs[1]
                            data = re.split('\s|,|\.', year_text, 1)
                            start_year = data[0]
                            event = data[1]
                        else:
                            print(sentence)
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
                    
                    event_o.start_year = start_year
                    event_o.end_year = end_year
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
                    done = True
                    

csv_target = r'C:\Users\andan\OneDrive\Desktop\STIP\csv'

def write_to_csv(persons):
    os.chdir(csv_target)
    person_fields = ['person_id', 'first_name', 'last_name', 'full_name', 'gender', 'year_of_birth', 'year_of_death', 'birthplace', 'nationality', 'education', 'title', 'workplace', 'reference', 'description']
    event_fields = ['event_id', 'person_id', 'start_year', 'end_year', 'event']
    csv_file = persons[0].person_id[0]

    with open(f'{csv_file}_persons.csv', mode='w', encoding="utf-8", newline='') as csvfile:
        person_writer = csv.writer(csvfile)
        person_writer.writerow(person_fields)
        for person in persons:
            person_writer.writerow([person.person_id, person.first_name, person.last_name, person.full_name, person.gender, person.year_birth, person.year_death, person.birthplace, person.nationality, person.education, person.title, person.workplace, person.reference, person.description])
        

    with open(f'{csv_file}_events.csv', mode='w', encoding='utf-8', newline='') as csvfile:
        event_writer = csv.writer(csvfile)
        event_writer.writerow(event_fields)
        for person in persons:
            for event in person.events:
                if (event.event):
                    event_writer.writerow([event.event_id, event.person_id, event.start_year, event.end_year, event.event])


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
    
    write_to_csv(persons)