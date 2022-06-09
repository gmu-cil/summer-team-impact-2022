import os
import shutil
import docx2txt
import re
import sys

# Folder Path
folder = sys.argv[1]
source_folder = r'C:\Users\andan\OneDrive\Desktop\STIP\data\{}'.format(folder)
txt_folder = r'C:\Users\andan\OneDrive\Desktop\STIP\txt'
destination_folder = r'C:\Users\andan\OneDrive\Desktop\STIP\txt\{}'.format(folder)
# Change the directory
os.chdir(source_folder)

def docx_to_txt(file_path):
    print(file_path)
    text = docx2txt.process(file_path)
    with open(f'{file_path}.txt', "w", encoding="utf-8") as text_file:
        text_file.write(text)

if __name__ == '__main__':
    for file in os.listdir():
        if (file.endswith('.docx')):    
            file_path = f"{os.getcwd()}\{file}"
            # make sure file is not empty
            if (os.path.getsize(file_path) > 0):
                # call read text file function
                docx_to_txt(file_path)
        
    if not os.path.isdir(destination_folder):
        os.chdir(txt_folder)
        os.mkdir(folder)
    
    os.chdir(source_folder)
    for file in os.listdir():
        if file.endswith('.txt'):
            source_path = f"{os.getcwd()}\{file}"
            destination_path = f"{destination_folder}\{file}"
            shutil.move(source_path, destination_path) 

        # if not os.path.isfile(os.path.join(source, file)):
        #     os.chdir(f'{source}\{file}')
        #     # convert docx to txt
        #     for sub_file in os.listdir():
        #         if sub_file.endswith(".docx"):
        #             file_path = f"{os.getcwd()}\{sub_file}"
        #             # call read text file function
        #             docx_to_txt(file_path)
            
        #     # move txt files to destination folder
        #     for sub_file in os.listdir():
        #         if sub_file.endswith('.txt'):
        #             source_path = f"{os.getcwd()}\{sub_file}"
        #             destination_path = f"{destination}\{sub_file}"
        #             shutil.move(source_path, destination_path) 
        
    # correct mismatched names
    os.chdir(destination_folder)
    for target in os.listdir():
        # Check whether file is in text format or not
        if target.endswith(".txt"):
            file_path = f'{os.getcwd()}\{target}'
            file_name = re.split('_', target)
            print(target)
            correct_name = file_name[0] + ' ' + file_name[1]
            incorrect_name = ''
            # call read text file function
            with open(file_path, mode='r', encoding='utf-8') as f:
                filedata = f.read()
                
            with open(file_path, mode='r', encoding='utf-8') as f:
                lines = f.readlines()
                first_line = lines[0]
                names = re.split(',', first_line, 1)
                name_text = names[0]
                # "A Andu..."
                if (re.match('[A-Z]{1}\s.*', name_text)):
                    name = re.split('\s', name_text)
                    # "A Andu Ald (1952-..."
                    if (re.match('^\(', name[len(name)-1])):
                        for index, sub_string in enumerate(name):
                            if (index > 0 and index < len(name) - 1):
                                incorrect_name += sub_string
                                incorrect_name += ' '
                    else:
                        incorrect_name = name[1]
                else:
                    if (re.match('\(', name_text)):
                        name = re.split('\s', name_text)
                        for index, sub_string in enumerate(name):
                            if (index != name[len(name) - 1]):
                                incorrect_name += sub_string
                                incorrect_name += ' '
            
            correct_name = correct_name.strip()
            incorrect_name = incorrect_name.strip()

            filedata = filedata.replace(incorrect_name, correct_name)
            filedata = filedata.replace('\u2014', '-')
            filedata = filedata.replace('\uff0c', ',')
            filedata = filedata.replace('==', '-')
            filedata = filedata.replace(' - ', '-')
            filedata = filedata.replace(' -', '-')
            filedata = filedata.replace('- ', '-')
            filedata = filedata.replace(') ', '), ')
            filedata = filedata.replace(' )', ')')
            filedata = re.sub('\([0-9]{4}\)', '\([0-9]{4}-\)', filedata)
            

            with open(file_path, mode='w', encoding='utf-8') as f:
                f.write(filedata)   
   
             

