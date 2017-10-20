# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:50:37 2017

@author: Gokhans
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

df = pd.read_csv('WATCHLIST.csv')

url = df['URL'][0]

r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'lxml')
"""
METACRITIC SCORE
"""
def get_metascore(soup):
    score = soup.find_all('div',class_='metacriticScore')
    if (len(score) == 0):
        metascore = 0
    else:
        metascore = score[0].span.get_text()
    return metascore

"""
LANGUAGE

Returns a string.

There might be more than one language involved in the movie.
Example: 'http://www.imdb.com/title/tt0808417/'
In this case, multiple languages are presented as comma separated.

"""
def get_language(soup):
    lang = soup.find_all('h4',text=re.compile(".*Language.*"))
    if len(lang) == 0:
        lang = 'Undefined'
    else:
        lang= lang[0].parent.find_all('a')
        lang = [x.text for x in lang]
        lang = ', '.join(lang)
    return lang

"""
COUNTRY

Returns a string. 

There might be more than one country involved in the movie. 
Example: 'http://www.imdb.com/title/tt0808417/'
In this case, multiple countries are presented as comma separated.

"""
def get_country(soup):
    country = soup.find_all('h4',text=re.compile(".*Country.*"))
    if len(country) == 0:
        country = 'Undefined'
    else:
        country= country[0].parent.find_all('a') 
        country = [x.text for x in country]
        country = ', '.join(country)
    return country

"""
WINS

Returns int. 

"""
def get_wins(soup):        
    total_awards = soup.find_all(attrs={'itemprop':'awards'})
    if len(total_awards) == 0:
        return 0
    total_awards=  total_awards[0].text.strip()
    wins = re.compile(".*\swins")
    wins = wins.search(total_awards)
    if wins:
        wins = wins.group().split(' ')[0]
    else:
        wins = 0
    return wins

"""
NOMINATIONS

Returns int.

"""
def get_noms(soup):
    total_awards = soup.find_all(attrs={'itemprop':'awards'})
    if len(total_awards) == 0:
        return 0
    total_awards=  total_awards[0].text.strip()
    noms = re.compile("\d*\snominations")
    noms = noms.search(total_awards)
    if noms:
        noms = noms.group().split(' ')[0]
    else:
        noms = 0
    return noms

"""
WRITERS

Returns a string. 

There might be more than one writer involved in the movie. 
Example: 'http://www.imdb.com/title/tt0456149/'
In this case, multiple writers are presented as comma separated.


"""
def get_writers(soup):
    writers = soup.find_all('h4',text=re.compile(".*Writers.*"))[0]
    if len(writers) == 0:
        writers = 'Undefined'
    else:
        writers = ', '.join([x.text for x in writers.parent.find_all(attrs={'itemprop':'name'})])
    return writers

url = 'http://www.imdb.com/title/tt4048272/'

    
"""
AWARDS - OSCARS, GOLDEN GLOBES, CANNES
"""
def get_awards(url):
    r  = requests.get(url+'awards')
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    oscar = soup.find_all('span',attrs={'class':'award_category'},text=re.compile(".*Oscar.*"))
    if len(oscar) == 0:
        oscar_noms = 0
        oscar_wins = 0
    elif len(oscar) == 1:
        oscar = oscar[0]
        if oscar.parent.b.text.strip() == 'Won':
            oscar_wins = int(oscar.parent['rowspan'])
            oscar_noms = oscar_wins
        else:
            oscar_wins = 0
            oscar_noms = int(oscar.parent['rowspan'])
    else:
        oscar_wins = int(oscar[0].parent['rowspan'])
        oscar_noms = int(oscar[1].parent['rowspan']) + oscar_wins
            
    globe = soup.find_all('span',attrs={'class':'award_category'},text=re.compile(".*Golden Globe.*"))
    if len(globe) == 0:
        globe_noms = 0
        globe_wins = 0
    elif len(globe) == 1:
        globe = globe[0]
        if globe.parent.b.text.strip() == 'Won':
            globe_wins = int(globe.parent['rowspan'])
            globe_noms = globe_wins
        else:
            globe_wins = 0
            globe_noms = int(globe.parent['rowspan'])
    else:
        globe_wins = int(globe[0].parent['rowspan'])
        globe_noms = int(globe[1].parent['rowspan']) + globe_wins
    
    cannes = soup.find_all('h3',text=re.compile(".*Cannes.*"))
    if len(cannes) == 0:
        cannes_noms = 0
        cannes_wins = 0
        print('a')
    else:
        cannes = cannes[0].parent
        print(cannes)

get_awards(url)






        