from bs4 import BeautifulSoup as bs
import requests
import lxml
import pandas as pd
import openpyxl
from collections import Counter
import json as js
import sklearn
import main

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

anime_6 = []
anime_6_25 = []
anime_6_5 = []
anime_6_75 = []
anime_7 = []
anime_7_25 = []
anime_7_5 = []
anime_7_75 = []
anime_8 = []
anime_8_25 = []
anime_8_5 = []
anime_8_75 = []
anime_9 = []
anime_9_25 = []

df3_dict = {
    '5.0' : [],
    '5.25' : [],
    '5.5' : [],
    '5.75' : [],
    '6.0' : [],
    '6.25' : [],
    '6.5' : [],
    '6.75' : [],
    '7.0' : [],
    '7.25' : [],
    '7.5' : [],
    '7.75' : [],
    '8.0' : [],
    '8.25' : [],
    '8.5' : [],
    '8.75' : [],
    '9.0' : [],
    '9.25' : []
    }

df3_columns = df3_dict.keys()
df3_columns = list(df3_columns)

def roundPlus(value):
    valueList = str(value).split('.')
    while len(valueList[1]) != 3:
        valueList[1] += '0'

    if int(valueList[1]) < 125:
        valueList[1] = '000'
    
    elif int(valueList[1]) == 250 or int(valueList[1]) == 500 or int(valueList[1]) == 750:
        pass

    elif int(valueList[1]) >= 125 and int(valueList[1]) < 250:
        valueList[1] = '250'
    elif int(valueList[1]) > 250 and int(valueList[1]) < 375:
        valueList[1] = '250'
    elif int(valueList[1]) >= 375 and int(valueList[1]) < 500:
        valueList[1] = '500'
    elif int(valueList[1]) > 500 and int(valueList[1]) < 625:
        valueList[1] = '500'
    elif int(valueList[1]) >= 625 and int(valueList[1]) < 750:
        valueList[1] = '750'
    elif int(valueList[1]) > 750 and int(valueList[1]) < 875:
        valueList[1] = '750'
    else:
        valueList[0] = int(valueList[0])+1
        valueList[1] = '000'
    
    return float(f'{valueList[0]}.{valueList[1]}')
    

def classifierForestGump(dataAnime=main.anime_df):
    ratings = list(dataAnime['rating'].values)
    titles = list(dataAnime['title'].values) 
    for rate in ratings:
        tmpColumns = list(df3_dict.keys())
        rateRounded = roundPlus(float(rate))
        df3_dict[str(rateRounded)].append(titles[ratings.index(rate)])
        tmpColumns.remove(str(rateRounded))
        for i in tmpColumns:
            df3_dict[i].append('.')

classifierForestGump()
df3 = pd.DataFrame(df3_dict)

print(df3)

df3.to_excel("ggg.xlsx")

