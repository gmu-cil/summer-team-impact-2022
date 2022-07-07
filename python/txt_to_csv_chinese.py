from googletrans import Translator, constants
from pprint import pprint
import openpyxl
import pandas as pd

import re
import csv
import os
import sys

persons = []
memoirs = []
count = 0
csv_file = 0

EXCEL_LIMIT = 32767 - 2000
# Folder Path
# folder = sys.argv[1]
# path = r'C:\Users\andan\OneDrive\Desktop\STIP\txt\{}'.format(folder)
csv_file_path = r'C:\Users\yulez\Documents\STIP\data\refined_csv\refined_csv\A_persons.csv'
dest_path = r'C:\Users\yulez\Documents\STIP\data'

chinese_ethnic_groups = [
    '汉族', '壮族', '回族', '满族', '维吾尔族', '苗族', '彝族', '土家族', '藏族', '蒙古族',
    '侗族', '布依族', '瑶族', '白族', '朝鲜族', '哈尼族', '黎族', '哈萨克族', '傣族', '畲族', '傈僳族', '东乡族', '仡佬族',
    '拉祜族', '佤族', '水族', '纳西族', '羌族', '土族', '仫佬族', '锡伯族', '柯尔克孜族', '景颇族', '达斡尔族', '撒拉族', '布朗族',
    '毛南族', '塔吉克族', '普米族', '阿昌族', '怒族', '鄂温克族', '京族', '基诺族', '德昂族', '保安族', '俄罗斯族', '裕固族',
    '乌孜别克族', '门巴族', '鄂伦春族', '独龙族', '赫哲族', '高山族', '珞巴族', '塔塔尔族'
]


def translateColToChinese(english_col_name, chinese_col_name):
    # init the Google API translator
    translator = Translator()
    deep_copy = csv_file.copy()

    deep_copy[chinese_col_name] = deep_copy[english_col_name].apply(
        lambda x: translator.translate(x, dest='zh-cn').text)

    deep_copy.to_csv(dest_path+"chinese_csv_file.csv")


if __name__ == "__main__":

    # handle missing data: filled-in values is Unknown
    csv_file = pd.read_csv(csv_file_path).fillna(value="Unknown")

    # translate english gender to chinese gender
    translateColToChinese("gender", "chinese_gender")
