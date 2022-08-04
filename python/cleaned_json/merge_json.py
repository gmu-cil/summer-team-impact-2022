import os
import json

target = '/Users/wprice/Documents/Translate/cleaned_json'
os.chdir(target)

targets = ['A', 'B', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
        'Q', 'R', 'S', 'T', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'X', 'Y', 'Z']

if __name__ == '__main__':
    jsonArray = []
    
    newJson = {}

    # with open('combined.json', 'r', encoding='utf-8') as input:
    #     newJson = json.load(input)

    for target in targets: 
        with open(f'{target}.json', 'r', encoding='utf-8') as input:
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