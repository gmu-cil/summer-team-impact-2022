import pandas as pd
import glob
import os

source_folder = r'C:\Users\andan\OneDrive\Desktop\STIP\isolated'
os.chdir(source_folder)
extension = 'csv'

def map_persons_csv():
    files = [i for i in glob.glob('*_persons.{}'.format(extension))]
    combined = pd.concat([pd.read_csv(f) for f in files])
    combined.to_csv("persons_combined.csv", index=False, encoding='utf-8-sig')

def map_events_csv():
    files = [i for i in glob.glob('*_events.{}'.format(extension))]
    combined = pd.concat([pd.read_csv(f) for f in files])
    combined.to_csv("events_combined.csv", index=False, encoding='utf-8-sig')

def map_memoirs_csv():
    files = [i for i in glob.glob('*_memoirs.{}'.format(extension))]
    combined = pd.concat([pd.read_csv(f) for f in files])
    combined.to_csv("memoirs_combined.csv", index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    map_persons_csv()
    map_events_csv()
    map_memoirs_csv()