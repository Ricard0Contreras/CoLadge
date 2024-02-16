import sqlite3
import os
from sqlite3 import Error

con = sqlite3.connect('..' + os.sep + 'database' + os.sep + 'cache.db')

cur = con.cursor()


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def addValue(key, c, c1, c2, c3, c4, c5):  # addValue('Flowers', 'Yellow', 'White', 'Green', 'Purple', 'Orange', 'Red')
    sql = """INSERT INTO photos(key, c, c1, c2, c3, c4, c5)
    VALUES(?, ?, ?, ?, ?, ?, ?)"""
    t = (key, c, c1, c2, c3, c4, c5)
    cur.execute(sql, t)
    con.commit()


def deleteValue(uniqueKey):  # delete the whole row based on the uniqueKey inputed
    g = uniqueKey
    sql = """DELETE FROM photos WHERE key = ?"""
    cur.execute(sql, (g, ))
    con.commit()
    return (cur.rowcount, 'row deleted')


def showValues():  # prints all data form the table photos
    res = cur.execute("SELECT * FROM photos")
    print("\n", res.fetchall())


def searchValue(uniqueKey):  # based on the uniqueKey inputed return all the colors in a list for easier processing 
    x = input("Enter the row that you would like to individually open based off of 'key' and 'c'': ")
    y = x.split(' ')
    sql = """SELECT * FROM photos WHERE key = ? AND c = ?"""
    res = cur.execute(sql, (y, ))
    con.commit()
    print("\n", res.fetchall())
