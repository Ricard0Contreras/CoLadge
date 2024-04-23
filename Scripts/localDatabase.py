import sqlite3
import os

# global db of program
localdbFile = 'cache.db'


def create_connection(): # Use as a template for other DB functions
    try:
        con = sqlite3.connect('Database' + os.sep + localdbFile)
        cur = con.cursor()

        # Here goes code that interacts with DB

    except sqlite3.Error as e:
        print(e)
    finally:
        if con:
            con.close()


def addValue(key, valueColor):  # addValue('Flowers', 'Yellow', 'White', 'Green')
    try:
        con = sqlite3.connect('Database' + os.sep + localdbFile)
        cur = con.cursor()

        sql = """INSERT INTO photos(key, c)
        VALUES(?, ?)"""
        t = (str(key), str(valueColor))
        cur.execute(sql, t)
        con.commit()

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()


def deleteValue(uniqueKey):  # delete the whole row based on the uniqueKey inputed
    try:
        con = sqlite3.connect('Database' + os.sep + localdbFile)
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
        con = sqlite3.connect('Database' + os.sep + localdbFile)
        cur = con.cursor()

        # Code that runs on connection
        res = cur.execute("SELECT * FROM photos")
        print("\n", res.fetchall())

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()


def returnColors(uniqueKey):  # based on the uniqueKey inputed return all the colors in a list for easier processing 
    try:
        con = sqlite3.connect('Database' + os.sep + localdbFile)
        cur = con.cursor()

        cur.execute("""SELECT c FROM photos WHERE key = ?""", [uniqueKey])
        result = [*cur.fetchone()]
        
        #tempList = str(tempList.split(','))
        listColor = []
        listColor = str(result).split(',')

        for n in range(len(listColor)):
            listColor[n] = str(listColor[n]).replace("[", "")
            listColor[n] = str(listColor[n]).replace("(", "")
            listColor[n] = str(listColor[n]).replace("'", "")
            listColor[n] = str(listColor[n]).replace('"', "")
            listColor[n] = str(listColor[n]).replace("]", "")
            listColor[n] = str(listColor[n]).replace(")", "")
            listColor[n] = listColor[n].strip()

        return listColor

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()


def keyInDB(uniqueKey):
    try:
        con = sqlite3.connect('Database' + os.sep + localdbFile)
        cur = con.cursor()

        cur.execute("""SELECT key FROM photos WHERE key = ?""", [uniqueKey])
        result = cur.fetchone()
        if str(result) == 'None':
            return False
        else:
            return True

    except sqlite3.Error as e:
        print(e)

    finally:
        if con:
            con.close()
