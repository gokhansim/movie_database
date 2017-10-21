# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:50:37 2017

@author: Gokhans
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
from mysql.connector import errorcode
import time
import glob


def get_metascore(soup):
    
    """
    METACRITIC SCORE
    
    Returns a double.
    """
    
    score = soup.find_all('div',class_='metacriticScore')
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
    
    lang = soup.find_all('h4',text=re.compile(".*Language.*"))
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
    
    country = soup.find_all('h4',text=re.compile(".*Country.*"))
    if len(country) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.text.strip() for x in country[0].parent.find_all('a') ])


def get_wins(soup):  
    
    """
    WINS
    
    Returns int. 
    Total number of award wins for the movie.
    
    """     

    total_awards = soup.find_all('div',class_='desc', text=re.compile(".*\d win.*"))
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
    
    total_awards = soup.find_all('div',class_='desc', text=re.compile(".*\d nomination.*"))
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
    
    writers = soup.find_all('h4',text=re.compile(".*Writer.*"))
    if len(writers) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.text.strip() for x in writers[0].parent.find_all(attrs={'itemprop':'name'})])
    

def get_directors(soup):
    
    """
    DIRECTORS
    
    Returns a string. 
    
    Even though this information is included in the CSV files for most movies,
    there are cases where the director is not credited. 
    Example: 'http://www.imdb.com/title/tt1590078/'
    
    This function is usually not utilized.
    """
    
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    directors = soup.find_all('h4',text=re.compile(".*Director.*"))
    if len(directors) == 0:
        return 'Undefined'
    else:
        return ', '.join([x.text.strip() for x in directors[0].parent.find_all(attrs={'itemprop':'name'})])
    
    
def get_stars(soup):
        
    """
    STARS 
    
    Returns a string.
    Main stars of the movie.
    
    If there are multiple stars, they are joined by commas and the result is returned as a string.
    """

    stars = soup.find_all('span',attrs={'itemprop':'actors'})
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
    
    color = soup.find_all('h4',text=re.compile(".*Color.*"))
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
    
    aspect_ratio = soup.find_all('h4',text=re.compile(".*Aspect Ratio.*"))
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


    oscar = soup.find_all('span',attrs={'class':'award_category'},text=re.compile(".*Oscar.*"))
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
            
    globe = soup.find_all('span',attrs={'class':'award_category'},text=re.compile(".*Golden Globe.*"))
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
        cannes = cannes[0].parent.next_sibling.next_sibling
        cannes_wins = cannes.find_all(string=re.compile("Won"))
        if len(cannes_wins) == 0:
            cannes_wins = 0
        else:
            cannes_wins = int(cannes_wins[0].parent.parent['rowspan'])
        
        cannes_noms = cannes.find_all(string=re.compile("Nominated"))
        if len(cannes_noms) == 0:
            cannes_noms = 0
        else:
            cannes_noms = int(cannes_noms[0].parent.parent['rowspan'])
    return (oscar_wins,oscar_noms,globe_wins,globe_noms,cannes_wins, cannes_noms)



def get_all(url):
    
    
    r  = requests.get(url)
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
    r  = requests.get(url+'awards')
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    
    wins = get_wins(soup)
    noms = get_noms(soup)
    o_wins, o_noms, g_wins, g_noms, c_wins, c_noms = get_awards(soup)
    return (metascore, wins, noms, country, lang, writers, stars, color, aspect,
            o_wins, o_noms, g_wins, g_noms, c_wins, c_noms)
    
    
# =============================================================================
# MAIN
# =============================================================================
    
if __name__ == '__main__':
    try:
        cnx = mysql.connector.connect(user='USER',password='PASS',
                                    host='127.0.0.1',
                                    database='movies')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    cursor = cnx.cursor()
    
    filenames = glob.glob('./*.csv')
    
    for filename in filenames:
        i = 0
        start_time = time.time()
        df = pd.read_csv(filename)
        df=df.rename(index=str, columns={"Title type": "title_type"})
        df = df.dropna(subset=['IMDb Rating'])
        # the database will include movies only. 
        # TV Series and Mini Series are omitted.
        df=df.query('title_type not in ["TV Series","Mini-Series"]')
        df['Directors'].fillna('Undefined', inplace=True)
        df['Runtime (mins)'].fillna(0, inplace=True)
        # DB Connection
        
        
        # iterating DF
        for index, row in df.iterrows():
            const = row['const']
            cursor.execute("SELECT const FROM `movie_all`"
                           "WHERE const='%s'" % row['const'])
            data = cursor.fetchall()
            if not data:
                print('Adding a new movie')
                i += 1
                url = row['URL']
                if row['Directors'] == 'Undefined':
                    row['Directors'] = get_directors(url)
                
                res = get_all(url)
                
                #FOR DEBUGGING
#                print("INSERT INTO `movie_all` "
#                     "VALUES ('%s', '%s', '%s', '%s', %f, %d, "
#                     "%d, %d, '%s', '%s', %d, %d, %d, '%s', '%s', "
#                     "'%s', '%s', '%s', '%s', %d, %d, %d, %d, %d, %d)" % 
#                     (row['Title'].replace("'", "''"), row['const'], row['URL'],
#                      row['Directors'],
#                     float(row['IMDb Rating']), row['Num. Votes'], 
#                     row['Runtime (mins)'], row['Year'],
#                     row['Release Date (month/day/year)'], row['title_type'],
#                     res[0], res[1], res[2], res[3], res[4], res[5], res[6], 
#                     res[7], res[8], res[9], res[10], res[11], res[12], res[13],
#                     res[14]))
                                
                cursor.execute ("INSERT INTO `movie_all` "
                                "VALUES ('%s', '%s', '%s', '%s', %f, %d, "
                                "%d, %d, '%s', '%s', %d, %d, %d, '%s', '%s', "
                                "'%s', '%s', '%s', '%s', %d, %d, %d, %d, %d, %d)" % 
                                (row['Title'].replace("'", "''"), row['const'], 
                                row['URL'],row['Directors'].replace("'", "''"),
                                row['IMDb Rating'], row['Num. Votes'], 
                                row['Runtime (mins)'], row['Year'],
                                row['Release Date (month/day/year)'], row['title_type'],
                                res[0], res[1], res[2], res[3], res[4], 
                                res[5].replace("'", "''"), res[6].replace("'", "''"), 
                                res[7], res[8], res[9], res[10], res[11], res[12], 
                                res[13], res[14]))
                print('Added to database: %s, %d' % (row['Title'], row['Year']))
                cnx.commit()
            else:
                print('Movie already exists: %s, %d' % (row['Title'], row['Year']))
        end_time = time.time()
        print('Done with the CSV file %s in %d seconds' % (filename, end_time - start_time))
        print('New movies added: ', i)
        print('\n****************************************************\n')
    
    
    
    
    

        