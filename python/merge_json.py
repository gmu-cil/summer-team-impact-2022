import os
import json

target = r'C:\Users\andan\OneDrive\Desktop\STIP\valid'
os.chdir(target)

src_folder = 'combined'
target_folder = 'C'
targets = ['A', 'B', 'C', 'D', 'E', 'F']

if __name__ == '__main__':
    jsonArray = []
    
    newJson = {}

    with open('combined.json', 'r', encoding='utf-8') as input:
        newJson = json.load(input)

    for target in targets: 
        with open(f'{target}_valid.json', 'r', encoding='utf-8') as input:
            jsonArray.append(json.load(input))

    # with open(f'{src_folder}.json', 'r', encoding='utf-8') as input:
    #     old_json = json.load(input)

    # with open(f'{target_folder}.json', 'r', encoding='utf-8') as input:
    #     add_json = json.load(input)
    for j in jsonArray:
        newJson = newJson | j
    
    # new_json = old_json | add_json

    # string dump of the merged dict
    jsonString_merged = json.dumps(newJson, indent=4)

    with open(f'combined.json', 'w', encoding='utf-8') as f:
        print(jsonString_merged)
        f.write(jsonString_merged)