# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:32:34 2017

@author: Gokhans
"""

import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user='USERNAME',password='PASSWORD',
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
TABLES['movies'] = (
    "CREATE TABLE `movies` ("
    "  `title` varchar(200) NOT NULL,"
    "  `const` varchar(100),"
    "  `url` varchar(100) NOT NULL,"
    "  `directors` varchar(300) NOT NULL,"
    "  `IMDB Rating` numeric(2,1) NOT NULL,"
    "  `runtime` int,"
    "  `year` numeric(4,0),"
    "  `release_date` datetime," 
    "  `type` varchar(100),"
    "  `month` varchar(20),"
    "  `num_votes` int,"
    "  PRIMARY KEY (`const`)"
    ") ENGINE=InnoDB")


cursor = cnx.cursor()
for name, ex in TABLES.items(): 
    print("Creating table {} ".format(name), end='')
    cursor.execute(ex)