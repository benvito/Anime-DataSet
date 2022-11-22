from bs4 import BeautifulSoup as bs
import requests
import lxml
import pandas as pd
import openpyxl
from collections import Counter
import json as js

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

data_first_table = '500anime_1.json'
data_second_table = '500anime_2.json'

def parse50(page):
    url = 'https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(page)
    req = requests.get(url)
    s = bs(req.text, "lxml")
    titles = s.find_all('div', class_="di-ib clearfix")
    for item in titles:
        animeGenreTmp = []
        print(item.text)
        anime_titles.append(item.text)
        link = item.find("a")
        linkUrl = link.get("href")
        print('url:',linkUrl)
        anime_links.append(linkUrl)
        reqAnime = requests.get(linkUrl)
        soupAnime = bs(reqAnime.text, "lxml")

        rate = soupAnime.find('div', class_= 'fl-l score')
        rate = rate.text
        anime_rate.append(float(rate))
        print('rate:',rate)

        genre = soupAnime.find_all('span', itemprop='genre')
        for genreAnime in genre:
            animeGenreTmp.append(genreAnime.text)

        try:
            type = soupAnime.find(class_='dark_text',text='Type:').find_next_sibling()
            type = type.text
            print('type:',type)
            anime_type.append(type)
        except:
            type = soupAnime.find(class_='dark_text', text='Type:').next_element.next_element
            type = type.text.strip()
            print('type:', type)
            anime_type.append(type)

        votes = soupAnime.find(itemprop='ratingCount')
        print('votes:',int(votes.text))
        anime_votes.append(int(votes.text))

        views = soupAnime.find(class_='numbers members').find('strong')
        views = views.text.replace(',', '')
        print('views:',int(views))
        anime_views.append(int(views))

        if type != 'TV':
            year = soupAnime.find(class_='dark_text', text='Aired:').next_element.next_element
            year = year.text
            year = int(''.join(filter(str.isdigit, year)))
            year = str(year)[-4:]
            year = int(year)
        else:
            year = soupAnime.find(class_='dark_text', text='Premiered:').find_next_sibling()
            year = year.text
            year = int(''.join(filter(str.isdigit, year)))
        print('year:', year)
        anime_year.append(year)

        minutes = soupAnime.find(class_='dark_text', text='Duration:').next_element.next_element
        if type == 'TV':
            minutes = minutes.text
            minutes = int(''.join(filter(str.isdigit, minutes)))
        else:
            minutes = minutes.text
            minutes = int(''.join(filter(str.isdigit, minutes)))
            minutes = str(minutes)
            if len(minutes) > 1:
                minutes = int(minutes[0]) * 60 + int(minutes[1:])
            else:
                minutes = int(minutes[0]) * 60
        print('minutes:', minutes)
        anime_minutes.append(minutes)

        series = soupAnime.find(class_='dark_text', text='Episodes:').next_element.next_element
        series = series.text.strip()
        print('series:',series)
        anime_series.append(series)

        source = soupAnime.find(class_='dark_text', text='Source:').next_element.next_element
        source = source.text.strip()
        print('source:',source)
        anime_source.append(source)

        studio = soupAnime.find(class_='dark_text', text='Studios:').find_next_sibling()
        studio2 = soupAnime.find(class_='dark_text', text='Studios:').find_next_sibling().find_next_sibling()
        if studio2 is None:
            print('studio:', studio.text)
            anime_studio.append(studio.text)
        else:
            print('studio:', studio.text,', ',studio2.text)
            anime_studio.append([studio.text, studio2.text])

        anime_genre.append(animeGenreTmp)
        print('genre:', animeGenreTmp)
        print('__________________________________________')

try:
    with open(data_first_table,'r', encoding='utf8') as json_file:
        data = js.load(json_file)

        anime_titles, anime_genre, anime_type, anime_rate, anime_votes, anime_views, anime_year, anime_minutes, \
        anime_series, anime_source, anime_studio, anime_links, = data['data500']['anime_titles'], data['data500']['anime_genre']\
            , data['data500']['anime_type'], data['data500']['anime_rate'], data['data500']['anime_votes'], data['data500']['anime_views']\
            , data['data500']['anime_year'], data['data500']['anime_minutes'], data['data500']['anime_series'], data['data500']['anime_source']\
            , data['data500']['anime_studio'], data['data500']['anime_links']
except:
    anime_titles, anime_genre, anime_type, anime_rate, anime_votes, anime_views, anime_year, anime_minutes,\
    anime_series, anime_source, anime_studio, anime_links, = [], [], [], [], [], [], [], [], [], [], [], []

    page = 0
    limit = int(input('Сколько аниме желаете проанализировать?(кратное 50) >>> '))
    limit = (page//50) * 50

    while page < limit:
        print('-------------------------------')
        print('page: ', (page / 50) + 1, ' / ', 500 / 50)
        print('-------------------------------')
        parse50(page)
        page += 50
        data = {
            'data500' : {
                'anime_titles' : anime_titles,
                'anime_genre' : anime_genre,
                'anime_type' : anime_type,
                'anime_rate' : anime_rate,
                'anime_votes' : anime_votes,
                'anime_views' : anime_views,
                'anime_year' : anime_year,
                'anime_minutes' : anime_minutes,
                'anime_series' : anime_series,
                'anime_source' : anime_source,
                'anime_studio' : anime_studio,
                'anime_links' : anime_links,
            }
        }
        with open(data_first_table, 'w', encoding='utf8') as json_file:
            js.dump(data, json_file)

anime_dict = {
    'title' : anime_titles,
    'genre' : anime_genre,
    'type' : anime_type,
    'rating' : anime_rate,
    'votes' : anime_votes,
    'views' : anime_views,
    'year' : anime_year,
    'minutes' : anime_minutes,
    'series' : anime_series,
    'source' : anime_source,
    'studio' : anime_studio
}

anime_df = pd.DataFrame(anime_dict)

anime_df.to_excel("DF_anime_1(rename).xlsx")
print(anime_df)

# df2

def df2_builder():

    last_year_rating = sum(anime_rate) / len(anime_rate)

    for year in set(anime_year):
        print('---------',year,'---------')
        year_df = anime_df[anime_df['year'] == year]
        year_column.append(year)

        # average rating
        ratings_year = list(map(float, year_df['rating'].values))
        average_rating_year = round(sum(ratings_year) / len(ratings_year), 2)
        average_rating.append(average_rating_year)
        print(average_rating_year)

        # coef of improve
        coef_improve_year = round((average_rating_year - last_year_rating) / average_rating_year, 4)
        coef_improve.append(coef_improve_year)
        print(coef_improve_year)

        # best rating
        best_rating_year = max(ratings_year)
        best_rating.append(best_rating_year)

        # best anime
        best_anime_year = year_df[year_df['rating'] == best_rating_year]['title'].values[0]
        best_anime.append(best_anime_year)
        print(best_rating_year, best_anime_year)

        # worst rating
        worst_rating_year = min(ratings_year)
        worst_rating.append(worst_rating_year)

        # worst anime
        worst_anime_year = year_df[year_df['rating'] == worst_rating_year]['title'].values[0]
        worst_anime.append(worst_anime_year)
        print(worst_rating_year, worst_anime_year)

        # most popular genre
        animGenreTmp = []
        for anim in year_df['genre'].values:
            for Genre in anim:
                animGenreTmp.append(Genre)
        counterGenres = Counter(animGenreTmp)
        popular_genre_year = ''
        maxCntr = 0
        for Genre in counterGenres:
            if counterGenres[Genre] > maxCntr:
                maxCntr = counterGenres[Genre]
        for Genre in counterGenres:
            if counterGenres[Genre] == maxCntr:
                popular_genre_year = Genre
        for Genre in counterGenres:
            if Genre == popular_genre_year:
                print(popular_genre_year)
                popular_genre.append(popular_genre_year)

        # max num of series
        # the longest anime
        try:
            num_series_year = map(int, list(year_df['series'].values))
            max_num_of_series_year = max(num_series_year)
            max_num_of_series.append(max_num_of_series_year)

            longest_anime_year = year_df[year_df['series'] == str(max_num_of_series_year)]['title'].values[0]
            longest_anime.append(longest_anime_year)
            print(longest_anime_year, max_num_of_series_year)
        except:
            max_num_of_series_year = 'Unknown'
            max_num_of_series.append(max_num_of_series_year)

            longest_anime_year = year_df[year_df['series'] == max_num_of_series_year]['title'].values[0]
            longest_anime.append(longest_anime_year)
            print(longest_anime_year, max_num_of_series_year)

        # most productive studio
        animStudioTmp = []
        for studio in year_df['studio'].values:
            if type(studio) is list:
                for studio2 in studio:
                    animStudioTmp.append(studio2)
            else:
                animStudioTmp.append(studio)
        counterStudios = Counter(animStudioTmp)
        prod_studio_year = ''
        maxCntr = 0
        for Studio in counterStudios:
            if counterStudios[Studio] > maxCntr:
                maxCntr = counterStudios[Studio]
        for Studio in counterStudios:
            if counterStudios[Studio] == maxCntr:
                prod_studio_year = Studio
        for Studio in counterStudios:
            if Studio == prod_studio_year:
                print(prod_studio_year)
                productive_studio.append(prod_studio_year)

        # most popular anime
        max_views = max(list(year_df['views'].values))
        popular_anime_year = year_df[year_df['views'] == max_views]['title'].values[0]
        popular_anime.append(popular_anime_year)
        print(popular_anime_year)

        # num of anime
        num_anime_year = len(list(year_df['title'].values))
        num_anime.append(num_anime_year)
        print(num_anime_year)

        last_year_rating = average_rating_year

try:
    with open(data_second_table, 'r', encoding='utf8') as json_file:
        data2 = js.load(json_file)

    year_column, average_rating, coef_improve, best_anime, best_rating, worst_anime, worst_rating, popular_genre, \
    longest_anime, max_num_of_series, productive_studio, popular_anime, num_anime =\
        data2['data500']['year_column'], data2['data500']['average_rating'], data2['data500']['coef_improve'], \
        data2['data500']['best_anime'], data2['data500']['best_rating'], data2['data500']['worst_anime'], \
        data2['data500']['worst_rating'], data2['data500']['popular_genre'], data2['data500']['longest_anime'], \
        data2['data500']['max_num_of_series'], data2['data500']['productive_studio'], data2['data500']['popular_anime'], \
        data2['data500']['num_anime']
except:
    year_column, average_rating, coef_improve, best_anime, best_rating, worst_anime, worst_rating, popular_genre, \
    longest_anime, max_num_of_series, productive_studio, popular_anime, num_anime = [], [], [], [], [], [], [], [], [], [], [], [], []
    df2_builder()
    data2 = {
        'data500' : {
            'year_column': year_column,
            'average_rating': average_rating,
            'coef_improve': coef_improve,
            'best_anime': best_anime,
            'best_rating': best_rating,
            'worst_anime': worst_anime,
            'worst_rating': worst_rating,
            'popular_genre': popular_genre,
            'longest_anime': longest_anime,
            'max_num_of_series': max_num_of_series,
            'productive_studio': productive_studio,
            'popular_anime': popular_anime,
            'num_anime': num_anime,
        }
    }

    with open(data_second_table, 'w', encoding='utf8') as json_file:
        js.dump(data2, json_file)

anime_year_dict = {
    'year' : year_column,
    'average rating' : average_rating,
    'coef of improve' : coef_improve,
    'best anime' : best_anime,
    'best rating' : best_rating,
    'worst anime' : worst_anime,
    'worst rating' : worst_rating,
    'most popular genre' : popular_genre,
    'the longest anime' : longest_anime,
    'max num of series' : max_num_of_series,
    'most productive studio' : productive_studio,
    'most popular anime' : popular_anime,
    'num of anime' : num_anime,
}

anime_df_year = pd.DataFrame(anime_year_dict)
anime_df_year.to_excel("Ds_Anime_2(rename).xlsx")

print(anime_df_year)
