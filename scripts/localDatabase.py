import sqlite3
import os

# global db of project
localdbFile = 'cache.db'


def create_connection(): # Use as a template for other DB functions
    try:
        con = sqlite3.connect('database' + os.sep + localdbFile)
        cur = con.cursor()

        # Here goes code that interacts with DB

    except sqlite3.Error as e:
        print(e)
    finally:
        if con:
            con.close()


def addValue(key, valueList):  # addValue('Flowers', 'Yellow', 'White', 'Green', 'Purple', 'Orange', 'Red')
    try:
        con = sqlite3.connect('database' + os.sep + localdbFile)
        cur = con.cursor()

        sql = """INSERT INTO photos(key, c, c1, c2, c3, c4, c5)
        VALUES(?, ?, ?, ?, ?, ?, ?)"""
        t = (str(key), str(valueList[0]), str(valueList[1]), str(valueList[2]), str(valueList[3]), str(valueList[4]), str(valueList[5]))
        cur.execute(sql, t)
        con.commit()

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()


def deleteValue(uniqueKey):  # delete the whole row based on the uniqueKey inputed
    try:
        con = sqlite3.connect('database' + os.sep + localdbFile)
        cur = con.cursor()

        g = uniqueKey
        sql = """DELETE FROM photos WHERE key = ?"""
        cur.execute(sql, (g, ))
        con.commit()
        return (cur.rowcount, 'row deleted')

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()


def showValues():  # prints all data form the table photos
    try:
        con = sqlite3.connect('database' + os.sep + localdbFile)
        cur = con.cursor()

        # Code that runs on connection
        res = cur.execute("SELECT * FROM photos")
        print("\n", res.fetchall())

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()


# NOT WORKING
def searchValue(uniqueKey):  # based on the uniqueKey inputed return all the colors in a list for easier processing 
    try:
        con = sqlite3.connect('database' + os.sep + localdbFile)
        cur = con.cursor()

        x = input("Enter the row that you would like to individually open based off of 'key' and 'c'': ")
        y = x.split(' ')
        sql = """SELECT * FROM photos WHERE key = ? AND c = ?"""
        res = cur.execute(sql, (y, ))
        con.commit()
        print("\n", res.fetchall())

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()
