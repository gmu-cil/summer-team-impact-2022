import os
import json
import pandas as pd
import sys 

def status(row):
    if pd.isna(row['year_of_death']):
        return 'Unknown'
    else:
        return 'Dead'

def detailJob(row):
    if (pd.isna(row['title'])):
        return 0
    else:
        data = row['title'].split()
        return data[len(data) - 1]

# def translate_title(row):
#     translator = Translator()
#     if row['title']:
#         result = translator.translate(row['title'], src='en', dest='zh-cn').text
#         print(result)
#         return result
#     else:
#         return ''

def checkEmptyEventArray(row):
    data = json.loads(row['events'][0])
    if (pd.isna(data['event_id'])):
        return []
    else:
        return row['events']

def checkEmptyMemoirArray(row):
    data = json.loads(row['memoirs'][0])
    if (pd.isna(data['memoir_id'])):
        return []
    else:
        return row['memoirs']

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

csv_target = r'C:\Users\andan\OneDrive\Desktop\STIP\isolated'
json_target = r'C:\Users\andan\OneDrive\Desktop\STIP\updated_json'
folder = sys.argv[1]

if __name__ == '__main__':
    person_json = {}

    os.chdir(csv_target)
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    person_csv = pd.read_csv(f'{folder}_persons.csv')
    events_csv = pd.read_csv(f'{folder}_events.csv')
    memoirs_csv = pd.read_csv(f'{folder}_memoirs.csv')

    initial = person_csv.at[0, 'person_id'][0:1]
    person_csv.insert(loc=1, column='initial', value=[initial for _ in person_csv.index])

    merged_1 = events_csv.merge(person_csv, on='person_id', how='right')
    
    # Add contributor_id column
    merged_1.insert(loc=1, column='contributor_id', value=['pL8BFnZxdSeSWSIuyAkTBQZuNbf2' for _ in merged_1.index])
    
    # Add publish column
    merged_1.insert(loc=2, column='publish', value=['original' for _ in merged_1.index])

    # Add status column
    merged_1['status'] = merged_1.apply(lambda row: status(row), axis=1)

     # Add detail job column
    merged_1['detail_job'] = merged_1.apply(lambda row: detailJob(row), axis=1)

    # # Add title in Chinese
    # merged_1['chinese_title'] = merged_1.apply(lambda row: translate_title(row), axis=1)
    # merged_1['']

    # Swap first_name and last_name
    merged_1.rename(columns={
            'first_name': 'last_name', 
            'last_name': 'first_name',
            'title': 'detail_job',
            'nationality': 'ethnicity',
            'detail_job': 'job'
            }, inplace=True)

    merged_1['events'] = [Event(event_id, start_year, end_year, event).toJSON()
        for event_id, start_year, end_year, event 
        in zip(merged_1['event_id'], merged_1['start_year'], merged_1['end_year'], merged_1['event'])]

    dataframes_1 = merged_1.groupby(['person_id']).agg({
            'contributor_id': 'first',
            'publish': 'first',
            'status': 'first',
            'initial': 'first',
            'first_name': 'first',
            'last_name': 'first',
            'gender': 'first',
            'year_of_birth': 'first',
            'year_of_death': 'first',
            'year_rightist': 'first',
            'ethnicity': 'first',
            'birthplace': 'first',
            'education': 'first',
            'job': 'first',
            'detail_job': 'first',
            'workplace': 'first',
            'reference': 'first',
            'description': 'first',
            'events': lambda x: x.tolist()
            }).reset_index()

    # merged_1['status'] = merged_1.apply(lambda row: status(row), axis=1)
  
    print(dataframes_1.head(30))
    print(len(dataframes_1.index))
    print(dataframes_1.columns)

    merged_2 = dataframes_1.merge(memoirs_csv, on='person_id', how='left')
    
    merged_2['memoirs'] = [Memoir(memoir_id, memoir).toJSON()
        for memoir_id, memoir in zip(merged_2['memoir_id'], merged_2['memoir'])
    ]

    dataframes_2 = merged_2.groupby(['person_id']).agg({
            'contributor_id': 'first',
            'publish': 'first',
            'status': 'first',
            'initial': 'first',
            'first_name': 'first',
            'last_name': 'first',
            'gender': 'first',
            'year_of_birth': 'first',
            'year_of_death': 'first',
            'year_rightist': 'first',
            'ethnicity': 'first',
            'birthplace': 'first',
            'education': 'first',
            'job': 'first',
            'detail_job': 'first',
            'workplace': 'first',
            'reference': 'first',
            'description': 'first',
            'events': 'first',
            'memoirs': lambda x: x.tolist()
            }).reset_index()

    # clean empty arrays
    dataframes_2['events'] = dataframes_2.apply(lambda row: checkEmptyEventArray(row), axis=1)
    dataframes_2['memoirs'] = dataframes_2.apply(lambda row: checkEmptyMemoirArray(row), axis=1)

    # print(dataframes_2.head(30))
    # print(dataframes_2.columns)
    # print(len(dataframes_2.index))

    # print(dataframes_1.head(20))
    # output = json.loads(dataframes_1.at[0, 'events'][0])
    # print(output)

    person_json = dataframes_2.set_index('person_id').to_dict(orient='index')
    # for key, value in person_json['persons'].values():
    #     value['events'] = value['events'].decode('utf-8')

    jsonString = json.dumps(person_json, indent=4, ensure_ascii=False)
    jsonString = jsonString.replace(r'\"', r'"')
    jsonString = jsonString.replace(r'"{', r'{')
    jsonString = jsonString.replace(r'}"', r'}')
    jsonString = jsonString.replace('NaN', '0')
    jsonString = jsonString.replace('null', '0')
    jsonString = jsonString.replace(r'""', r'"')
    jsonString = jsonString.replace('\u201c', r"'")
    jsonString = jsonString.replace('\u201d', r"'")
    jsonString = jsonString.replace(r'\\"', r'\\')

    os.chdir(json_target)

    with open(f'{folder}_updated.json', 'w', encoding='utf-8') as f:
        f.write(jsonString)

    # for person in person_json:
    #     print(person)

    # for person in person_json:
    #     print(person)
    # with open('test.json', 'w', encoding='utf-8-sig') as jsonf:
    #     jsonString = json.dumps(person_json, indent=4)
    #     jsonf.write(jsonString)

    # with open('events_combined.csv', encoding='utf-8-sig') as csv_reader:
    #     reader = csv.DictReader(csv_reader)

    #     for row in reader:
    #         jsonArray.append(row)

    # with open('events_combined.json', 'w', encoding='utf-8-sig') as jsonf:
    #     jsonString = json.dumps(jsonArray, indent=4)
    #     jsonf.write(jsonString)

    # translator = Translator()
    # result = translator.translate("Department of Literature and Education", src='en', dest='zh-cn')
    # print(googletrans.LANGUAGES)
    # print(result)