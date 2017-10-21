# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:32:34 2017

@author: Gokhans
"""

import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user='USER', password='PASS',
                                  host='127.0.0.1',
                                  database='movies')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

TABLES = {}
TABLES['movie_all'] = (
    "CREATE TABLE `movie_all` ("
    "  `title` varchar(200) NOT NULL,"
    "  `const` varchar(100) NOT NULL,"
    "  `url` varchar(100) NOT NULL,"
    "  `directors` varchar(300) NOT NULL,"
    "  `IMDB Rating` numeric(2,1) NOT NULL,"
    "  `num_votes` int,"
    "  `runtime` int,"
    "  `year` numeric(4,0),"
    "  `release_date` datetime,"
    "  `title_type` varchar(100),"
    "  `metascore` int,"
    "  `wins` int,"
    "  `noms` int,"
    "  `country` varchar(300),"
    "  `language` varchar(200),"
    "  `writers` varchar(300),"
    "  `stars` varchar(300),"
    "  `color` varchar(40),"
    "  `aspect_ratio` varchar(15),"
    "  `oscar_wins` int,"
    "  `oscar_noms` int,"
    "  `globe_wins` int,"
    "  `globe_noms` int,"
    "  `cannes_wins` int,"
    "  `cannes_noms` int,"
    "  PRIMARY KEY (`const`)"
    ") ENGINE=InnoDB")


cursor = cnx.cursor()
for name, ex in TABLES.items():
    print("Creating table {}".format(name), end='')
    cursor.execute(ex)
