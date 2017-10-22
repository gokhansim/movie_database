# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 13:38:05 2017

@author: Gokhans
"""

from bs4 import BeautifulSoup
import requests
import re


def get_metascore(soup):
    """
    METACRITIC SCORE

    Returns a double.
    """

    score = soup.find_all('div', class_='metacriticScore')
    if (len(score) == 0):
        return 0
    else:
        return int(score[0].span.text.strip())


def get_language(soup):
    """
    LANGUAGE

    Returns a string.

    There might be more than one language involved in the movie.
    Example: 'http://www.imdb.com/title/tt0808417/'
    In this case, multiple languages are presented as comma separated.

    """

    lang = soup.find_all('h4', text=re.compile(".*Language.*"))
    if len(lang) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.text.strip() for x in lang[0].parent.find_all('a')])


def get_country(soup):
    """
    COUNTRY

    Returns a string. 

    There might be more than one country involved in the movie. 
    Example: 'http://www.imdb.com/title/tt0808417/'
    In this case, multiple countries are presented as comma separated.

    """

    country = soup.find_all('h4', text=re.compile(".*Country.*"))
    if len(country) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.text.strip() for x in country[0].parent.find_all('a')])


def get_wins(soup):
    """
    WINS

    Returns int. 
    Total number of award wins for the movie.

    """

    total_awards = soup.find_all(
        'div', class_='desc', text=re.compile(".*\d win.*"))
    if len(total_awards) == 0:
        return 0
    else:
        wins = re.search("\d+ win", total_awards[0].text.strip())
        if wins:
            return int(wins.group().split(' ')[0])
        else:
            return 0


def get_noms(soup):
    """
    NOMINATIONS

    Returns int.

    """

    total_awards = soup.find_all(
        'div', class_='desc', text=re.compile(".*\d nomination.*"))
    if len(total_awards) == 0:
        return 0
    else:
        noms = re.search("\d+ nomination", total_awards[0].text.strip())
        if noms:
            return int(noms.group().split(' ')[0])
        else:
            return 0


def get_writers(soup):
    """
    WRITERS

    Returns a string. 

    There might be more than one writer involved in the movie. 
    Example: 'http://www.imdb.com/title/tt0456149/'
    In this case, multiple writers are presented as comma separated.


    """

    writers = soup.find_all('h4', text=re.compile(".*Writer.*"))
    if len(writers) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.text.strip() for x in writers[0].parent.find_all(attrs={'itemprop': 'name'})])


def get_directors(url):
    """
    DIRECTORS

    Returns a string. 

    Even though this information is included in the CSV files for most movies,
    there are cases where the director is not credited. 
    Example: 'http://www.imdb.com/title/tt1590078/'

    This function is usually not utilized.
    """
    
    r = requests.get(url)
    r.raise_for_status()
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    
    directors = soup.find_all('h4', text=re.compile(".*Director.*"))
    if len(directors) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.text.strip() for x in directors[0].parent.find_all(attrs={'itemprop': 'name'})])


def get_stars(soup):
    """
    STARS 

    Returns a string.
    Main stars of the movie.

    If there are multiple stars, they are joined by commas and the result is returned as a string.
    """

    stars = soup.find_all('span', attrs={'itemprop': 'actors'})
    if len(stars) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.a.span.text.strip() for x in stars])


def get_color(soup):
    """
    COLOR

    Returns string.
    Color status of the movie. e.g. Technicolor, Black and White etc.

    """

    color = soup.find_all('h4', text=re.compile(".*Color.*"))
    if len(color) == 0:
        return 'Undefined'
    else:
        return color[0].parent.a.text.strip()


def get_aspect_ratio(soup):
    """
    ASPECT RATIO

    Returns string.
    Aspect ratio of the movie. e.g. 1.37 : 1

    """

    aspect_ratio = soup.find_all('h4', text=re.compile(".*Aspect Ratio.*"))
    if len(aspect_ratio) == 0:
        return 'Undefined'
    else:
        return aspect_ratio[0].next_sibling.strip()


def get_awards(soup):
    """
    AWARDS - OSCARS, GOLDEN GLOBES, CANNES

    Returns, in order,
    Oscar wins, Oscar nominations, Golden Globe wins, Golden Globe nominations,
    Cannes wins, Cannes nominations

    All return types are int.

    The award categories the movie won are not counted in the nominations.
    e.g. La La Land was nominated for 14 Oscars, and won 6 of them. 
    For La La Land, oscar_wins = 6, oscar_noms = 8.


    """

    oscar = soup.find_all(
        'span', attrs={'class': 'award_category'}, text=re.compile(".*Oscar.*"))
    if len(oscar) == 0:
        oscar_noms = 0
        oscar_wins = 0
    elif len(oscar) == 1:
        oscar = oscar[0]
        if oscar.parent.b.text.strip() == 'Won':
            oscar_wins = int(oscar.parent['rowspan'])
            oscar_noms = 0
        else:
            oscar_wins = 0
            oscar_noms = int(oscar.parent['rowspan'])
    else:
        oscar_wins = int(oscar[0].parent['rowspan'])
        oscar_noms = int(oscar[1].parent['rowspan'])

    globe = soup.find_all(
        'span', attrs={'class': 'award_category'}, text=re.compile(".*Golden Globe.*"))
    if len(globe) == 0:
        globe_noms = 0
        globe_wins = 0
    elif len(globe) == 1:
        globe = globe[0]
        if globe.parent.b.text.strip() == 'Won':
            globe_wins = int(globe.parent['rowspan'])
            globe_noms = 0
        else:
            globe_wins = 0
            globe_noms = int(globe.parent['rowspan'])
    else:
        globe_wins = int(globe[0].parent['rowspan'])
        globe_noms = int(globe[1].parent['rowspan'])

    cannes = soup.find_all(string=re.compile("Cannes Film Festival"))
    if len(cannes) == 0:
        cannes_noms = 0
        cannes_wins = 0
    else:
        try:
            cannes = cannes[0].parent.next_sibling.next_sibling
            cannes_wins = cannes.find_all(string=re.compile("Won"))
            if len(cannes_wins) == 0:
                cannes_wins = 0
            else:
                cannes_wins = len(cannes_wins)
            
            cannes_noms = cannes.find_all(string=re.compile("Nominated"))
            if len(cannes_noms) == 0:
                cannes_noms = 0
            else:
                cannes_noms = len(cannes_noms)
        except:
            cannes_wins = 0
            cannes_noms = 0

    return (oscar_wins, oscar_noms, globe_wins, globe_noms, cannes_wins, cannes_noms)


def get_all(url):

    r = requests.get(url)
    r.raise_for_status()
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    metascore = get_metascore(soup)
    country = get_country(soup)
    lang = get_language(soup)
    writers = get_writers(soup)
    stars = get_stars(soup)
    color = get_color(soup)
    aspect = get_aspect_ratio(soup)

    # getting awards page for wins, noms and awards
    r = requests.get(url + 'awards')
    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    wins = get_wins(soup)
    noms = get_noms(soup)
    o_wins, o_noms, g_wins, g_noms, c_wins, c_noms = get_awards(soup)
    return (metascore, wins, noms, country, lang, writers, stars, color, aspect,
            o_wins, o_noms, g_wins, g_noms, c_wins, c_noms)
