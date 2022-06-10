import re
import csv
import os
import docx2txt

persons = []

class Person:
    def __init__(self, person_id, first_name, last_name, full_name, gender, year_birth, year_death, birthplace, nationality, education, title, workplace, events, reference):
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

class Event:
    def __init__(self, event_id, person_id, start_year, end_year, event):
        self.event_id = event_id
        self.person_id = person_id
        self.start_year = start_year
        self.end_year = end_year
        self.event = event

def map(textfile):
    print(textfile)
    with open(textfile, mode='r', encoding="utf-8") as f:
        count = 0
        lines = []
        events = []
        person = Person('', '', '', '', '', 0, 0, '', '', '', '', '', [], '')
        lines = f.readlines()
        lines = [value for value in lines if value != '\n']
    for index, line in enumerate(lines):
        line = line.replace('\u2014', '-')
        if (index == 0):
            subs = re.split(', ', line)
            for i, sub in enumerate(subs):
                if (i == 0):
                    #name
                    split = re.split(' ', sub, 1)

                    person.id = f"{split[0]}{count}"
                    count += 1

                    name_text = split[1]
                    # name_data = re.split(' ', name_text)

                    # if ('' in name_data):
                    #     name_data.remove('')

                    # print(name_data)
                    print(name_text)
                    if (re.search('.*[0-9]{4}', name_text)):
                        name_data = re.split(' ', name_text)
                        
                        if ('' in name_data):
                            name_data.remove('')

                        first_name = name_data[0]
                        last_name = ''
                        for i, val in enumerate(name_data):
                            if (i > 0 & i < len(name_data)):
                                last_name += val
                        full_name = first_name + last_name
                        print(name_data)
                        years_s = name_data[len(name_data) - 1]
                        years = re.split('-', years_s)

                        person.first_name = first_name
                        person.last_name = last_name
                        person.full_name = full_name
                        person.year_birth = years[0][1:]
                        person.year_death = years[1][:-1]  

                    else:
                        name_data = re.split(' ', name_text, 1)
                        if (len(name_data) == 2):
                            person.first_name = name_data[0]
                            person.last_name = name_data[1]
                        elif (len(name_data) == 1):
                            person.first_name = name_data[0]

                    # # [name] [name] [year]
                    # if (len(name_data) == 3):
                    #     first_name = name_data[0]
                    #     last_name = name_data[1]
                    #     full_name = ''.join([name_data[0], ' ', name_data[1]])

                    #     person.first_name = first_name
                    #     person.last_name = last_name
                    #     person.full_name = full_name

                    #     years = re.split('-', name_data[2])
                    #     person.year_birth = years[0][1:]
                    #     person.year_death = years[1][:-1]
                    # # [name] [name] or [name] [year]
                    # elif (len(name_data) == 2):
                    #     if not re.search('[0-9]{4}', name_data[1]):
                    #         full_name = ''.join([name_data[0], ' ', name_data[1]])
                    #         person.full_name = full_name
                    #     else:
                    #         full_name = name_data[0]
                    #         years = re.split('-', name_data[1])
                    #         print(name_data)
                    #         person.full_name = full_name
                    #         person.year_birth = years[0][1:]
                    #         person.year_death = years[1][:-1]        
                    # else:
                    #     full_name = name_data[0]
                    #     person.full_name = full_name

                if ('male' in sub):
                    person.gender = 'male'
                
                if ('female' in sub):
                    person.gender = 'female'

                if ('nationality' in sub):
                    # account for [nationality] nationality or nationality [nationality]
                    nationality = re.split(' ', sub)
                    nationality.remove('nationality')
                    person.nationality = nationality[0]

                if ('education' in sub):
                    education = re.split(' ', sub)
                    education.remove('education')
                    person.education = education[0]

                if any(re.findall(r'native|born', sub)):
                    birthplace = ''
                    native = re.split(' ', sub)
                    birthplace += native[len(native) - 1]
                    # check the next string for province
                    if ('Province' in subs[i + 1]):
                        birthplace += ', '
                        birthplace += subs[i + 1]
                    
                    person.birthplace = birthplace

                if (re.search(r'[a-zA-Z]+ in|of|at [a-zA-Z]+', sub)):
                    # exclude the native/born string
                    if not (any(re.findall(r'native|born', sub))):
                        data = re.split(r'in|of|at', sub, 1)
                        title = data[0].strip()
                        workplace = data[1].strip()
                        person.title = title
                        person.workplace = workplace
        else:
            # If not the end "--Excerpted" or "From"
            if not line.startswith(('--', 'From')):
                # Enter an event line
                event = Event(0, 0, 0, 0, ' ')
                if (re.search('In [0-9]{4}', line, re.IGNORECASE)):
                    subs = re.split('In ', line, 1, re.IGNORECASE)
                    # account for "In 1985, sth" or "In 1985. sth"
                    if not subs[0]:
                        data = re.split(' ', subs[1], 1)
                        year = (int)(data[0][:-1])
                        event.start_year = year
                        event.event = data[1]
                    # account for "sth in 1985."
                    else:
                        event = subs[0].strip()
                        data = re.split(' ', subs[1], 1)
                        year = (int)(data[0][:-1])
                        event.start_year = year
                        event.event = event

                # # remove "In" from "In 1985"
                # if (line.startswith('In')):
                #     line = re.split(' ', line, 1)[1]

                # print(line)
                # event = Event(0, 0, 0, 0, ' ')
           
                # if (re.search(r'[0-9]{4}, ', line)):
                #     subs = re.split(', ', line, 1)
                #     print(subs)
                #     year_text = subs[0]
                #     event_text = subs[1]
                #     if (re.search('[0-9]{4}-[0-9]{4}', year_text)):
                #         years = re.split('-', year_text)
                #         event.start_year = years[0]
                #         event.end_year = years[1]
                #     elif (re.search('[0-9]{4}', year_text)):
                #         event.start_year = (int)(year_text)
                #     event.event_id = f'E{person.person_id}'
                #     event.person_id = person.person_id
                #     event.event = event_text
                #     events.append(event)
                # elif (re.search(r'[0-9]{4}. ', line)):
                #     subs = re.split('. ', line, 1)
                #     year_text = subs[0]
                #     event_text = subs[1]

                #     if (re.search('[0-9]{4}-[0-9]{4}', year_text)):
                #         years = re.split('-', year_text)
                #         event.start_year = years[0]
                #         event.end_year = years[1]
                #     elif (re.search('[0-9]{4}', year_text)):
                #         event.start_year = (int)(year_text)

                #     event.event_id = f'E{person.person_id}'
                #     event.person_id = person.person_id
                #     event.event = event_text
                #     events.append(event)

                # elif (re.search(r'[0-9]{4}', line)):
                #     subs = re.split(' ', line, 1)
                #     year_text = subs[0]
                #     event_text = subs[1]

                #     if (re.search('[0-9]{4}-[0-9]{4}', year_text)):
                #         years = re.split('-', year_text)
                #         event.start_year = years[0]
                #         event.end_year = years[1]
                #     elif (re.search('[0-9]{4}', year_text)):
                #         event.start_year = (int)(year_text)

                #     event.event_id = f'E{person.person_id}'
                #     event.person_id = person.person_id
                #     event.event = event_text
                #     events.append(event)
                # else:
                #     continue
            else:
                # one long dash = 3 chars
                reference_text = line[6:]
                person.reference = reference_text
                return
        
        # elif (index == len(lines) - 1):
        #     # one long dash = 3 chars
        #     reference_text = line[6:]
        #     person.reference = reference_text
        # else:
        #     print(line)
        #     event = Event(0, ' ')
        #     line = line.strip()
        #     subs = re.split(', ', line, 1)
        #     year_text = subs[0]
        #     event_text = subs[1]
        #     year = re.split(' ', year_text)
        #     event.year = year
        #     event.event = event_text
        #     events.append(event)

    person.events = events
    persons.append(person)

def write_to_csv(persons):
    person_fields = ['person_id', 'first_name', 'last_name', 'full_name', 'gender', 'year of birth', 'year of death', 'birthplace', 'nationality', 'education', 'title', 'workplace', 'reference']
    event_fields = ['event_id', 'person_id', 'year', 'event']

    with open('persons.csv', mode='w', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(person_fields)
        for person in persons:
            writer.writerow([person.id, person.first_name, person.last_name, person.full_name, person.gender, person.year_birth, person.year_death, person.birthplace, person.nationality, person.education, person.title, person.workplace, person.reference])
            with open('events.csv', mode='w', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(event_fields)
                for event in person.events:
                    writer.writerow([person.id, event.year, event.event])

# Folder Path
path = r'C:\Users\andan\OneDrive\Desktop\STIP\B'
# Change the directory
os.chdir(path)
# Read text File
def read_text_file(file_path):
        map(file_path)
# iterate through all files

def docx_to_txt(file_path):
    text = docx2txt.process(file_path)

    with open(f'{file_path}.txt', "w", encoding="utf-8") as text_file:
        text_file.write(text)

if __name__ == "__main__":
    for file in os.listdir():
        if file.endswith(".docx"):
            file_name = re.split('.', file)
            file_path = f"{path}\{file}"
            # call read text file function
            docx_to_txt(file_path)

    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            # call read text file function
            read_text_file(file_path)
       
    write_to_csv(persons)