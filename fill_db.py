# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:50:37 2017

@author: Gokhans
"""

import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import time
import glob
import fill_functions as ff

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    try:
        cnx = mysql.connector.connect(user='root', password='',
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
        df = df.rename(index=str, columns={"Title type": "title_type"})
        df = df.dropna(subset=['IMDb Rating'])
        # the database will include movies only.
        # TV Series and Mini Series are omitted.
        df = df.query('title_type not in ["TV Series","Mini-Series"]')
        df['Directors'].fillna('Undefined', inplace=True)
        df['Runtime (mins)'].fillna(0, inplace=True)

        # iterating DF
        for index, row in df.iterrows():
            const = row['const']
            cursor.execute("SELECT const FROM `movie_all`"
                           "WHERE const='%s'" % row['const'])
            data = cursor.fetchall()
            if not data:
                i += 1
                url = row['URL']
                if row['Directors'] == 'Undefined':
                    row['Directors'] =  ff.get_directors(url)

                res = ff.get_all(url)
                command = ("INSERT INTO `movie_all` "
                               "VALUES ('%s', '%s', '%s', '%s', %f, %d, "
                               "%d, %d, '%s', '%s', %d, %d, %d, '%s', '%s', "
                               "'%s', '%s', '%s', '%s', %d, %d, %d, %d, %d, %d)" %
                               (row['Title'].replace("'", "''"), row['const'],
                                row['URL'], row['Directors'].replace(
                                   "'", "''"),
                                row['IMDb Rating'], row['Num. Votes'],
                                row['Runtime (mins)'], row['Year'],
                                row['Release Date (month/day/year)'], row['title_type'],
                                res[0], res[1], res[2], res[3].replace(
                                   "'", "''"), res[4],
                                res[5].replace(
                                   "'", "''"), res[6].replace("'", "''"),
                                res[7], res[8], res[9], res[10], res[11], res[12],
                                res[13], res[14]))
                try:
                    print('Adding a new movie')
                    cursor.execute(command)
                    print('Added to database: %s, %d' %
                          (row['Title'], int(row['Year'])))
                    cnx.commit()
                except:
                    print("Error occured, logging")
                    file = open("errorfile.txt","a")
                    file.write(command+"\n")
                    file.close()

            else:
                print('Movie already exists: %s, %d' %
                      (row['Title'], int(row['Year'])))
        end_time = time.time()
        print('Done with the CSV file %s in %d seconds' %
              (filename, end_time - start_time))
        print('New movies added: ', i)
        print('\n****************************************************\n')
