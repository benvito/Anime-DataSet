from bs4 import BeautifulSoup as bs
import requests
import lxml
import pandas as pd
import openpyxl
from collections import Counter
import json as js
import sklearn
import random as rnd
import numpy as np

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

df3_dict_title = {
}

df3_columns = df3_dict.keys()
df3_columns = list(df3_columns)

def roundPlus(value): # 0.56
    global roundedSeries
    global rounded100k
    if type(value) == float:
        
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
    else:
        if value < 1000:
            roundedSeries = []
            i = 0
            step = 5
            while i < 500:
                if 0<=i<50:
                    roundedSeries.append(i + 5)
                    i+=step
                elif i >= 50:
                    roundedSeries.append(i + 50)
                    step = 50
                    i+=step
            if value <= 50:
                value = value/5
                value = round(value) * 5
            else:
                value = value/50
                value = round(value) * 50
            return value
        else:
            step = 100000
            value /= step
            rounded100k = []
            for i in range(35):
                if i == 0:
                    rounded100k.append(step)
                else:
                    rounded100k.append(rounded100k[i-1] + step)
            return round(value) * step
            

def string_DF(target, dataAnime):
    global sourceAll
    titles = list(dataAnime['title'].values)
    sourceAll = []
    sources = list(dataAnime[target].values)
    for i in sources:
        for j in i:
            sourceAll.append(j)
    sourceAll = list(set(sources))
    
    for index in range(len(titles)):
        df3_dict_title[titles[index]] = []
        sources_anime = sources[index]
        for source_column in sourceAll:
            if sources_anime == source_column:
                df3_dict_title[titles[index]].append(1)
            else:
                df3_dict_title[titles[index]].append(0)

    df_string = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=sourceAll)
    return df_string

def studios_DF(dataAnime):
    titles = list(dataAnime['title'].values)
    studiosAll = []
    studios = list(dataAnime['studio'].values)
    for i in studios:
        if type(i) == list:
            for k in i:
                studiosAll.append(k)
        else: 
            studiosAll.append(i)
    studiosAll = list(set(studiosAll))

    for index in range(len(titles)):
        df3_dict_title[titles[index]] = []
        studio_anime = studios[index]
        typeList = False
        for studio_column in studiosAll:
            if type(studio_anime) == list:
                if studio_anime[0] == studio_column:
                    df3_dict_title[titles[index]].append(1)
                elif studio_anime[1] == studio_column:
                    df3_dict_title[titles[index]].append(1)
                else:
                    df3_dict_title[titles[index]].append(0)
            else:
                if studio_anime == studio_column:
                    df3_dict_title[titles[index]].append(1)
                else:
                    df3_dict_title[titles[index]].append(0)
        
    df_studio = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=studiosAll)
    return df_studio


def genres_DF(dataAnime):
    global genresAll
    
    titles = list(dataAnime['title'].values)
    genresAll = []
    genres = list(dataAnime['genre'].values)
    for i in genres:
        for j in i:
            genresAll.append(j)
    genresAll = list(set(genresAll)) #[a, b, c, d] список всех жанров без повторов

    for index in range(len(titles)):
        df3_dict_title[titles[index]] = []
        genres_anime = genres[index]
        for genre in genres_anime:
            for genre_column in genresAll:
                if genre == genre_column:
                    df3_dict_title[titles[index]].append(1)
                else:
                    df3_dict_title[titles[index]].append(0)
            break
        df3 = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=genresAll)
        for i in range(len(df3_dict_title[titles[index]])):
            #print(genres_anime)
            for genre in genres_anime: 
                #print(genre, df3.columns[i])      
                if genre == df3.columns[i]:
                    #print("Match!")
                    df3_dict_title[titles[index]][i] = 1
                    break
                else:
                    df3_dict_title[titles[index]][i] = 0
    df_genres = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=genresAll)
    return df_genres
    
def classifierForestGump(dataAnime:pd.DataFrame, titles_df:str, target_value:str, nameTable=f'binary_df_{rnd.randint(100, 500)}'):
    #числоа(rate, votes, views) 
    titles = list(dataAnime[titles_df].values)
    target = list(dataAnime[target_value].values)
    if target_value == 'series':
        for i in target:
            if i == 'Unknown':
                target[target.index(i)] = 0
            else:
                target[target.index(i)] = int(target[target.index(i)])
    if type(target[0]) == np.float64 or type(target[0]) == np.int64 or type(target[0]) == float or type(target[0]) == int:
        for index in range(len(titles)):
            if type(target[0]) == np.float64 or type(target[0]) == float: 
                xRounded = roundPlus(float(target[index]))
                tmpColumns = list(df3_dict.keys())

            elif type(target[0]) == np.int64 or type(target[0]) == int:
                xRounded = roundPlus(int(target[index])) 
                if len(str(target[0])) > 4:
                    tmpColumns = rounded100k
                elif len(str(target[0])) <= 4:
                    tmpColumns = roundedSeries

            df3_dict_title[titles[index]] = []

            for roundedX in tmpColumns:
                if type(xRounded) == float:
                    if xRounded == float(roundedX):
                        df3_dict_title[titles[index]].append(1) 
                    else:
                        df3_dict_title[titles[index]].append(0)  

                if type(xRounded) == int:
                    if xRounded == int(roundedX):                
                        df3_dict_title[titles[index]].append(1) 
                    else:                   
                        df3_dict_title[titles[index]].append(0)
        
        if target_value == 'rating':
            df3 = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=list(df3_dict.keys()))
        elif target_value == 'views':
            df3 = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=rounded100k)
        elif target_value == 'votes':
            df3 = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=rounded100k)
        elif target_value == 'minutes':
            df3 = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=roundedSeries)
        elif target_value == 'series':
            df3 = pd.DataFrame.from_dict(df3_dict_title, 'index', columns=roundedSeries)
            
        df3.to_excel(f"{nameTable}.xlsx")
    if type(target[0]) == list:
        df_genres = genres_DF(dataAnime=dataAnime)
        df_genres.to_excel(f"{nameTable}.xlsx")
    elif type(target[0]) == str and target_value != 'studio':
        df_str = string_DF(dataAnime=dataAnime,target=target_value)
        df_str.to_excel(f"{nameTable}.xlsx")
    elif target_value == 'studio':
        df_studio = studios_DF(dataAnime=dataAnime)
        df_studio.to_excel(f"{nameTable}.xlsx")