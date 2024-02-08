import sqlite3
from sqlite3 import Error
con = sqlite3.connect("Cache.db")

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

def addValue(key, c, c1, c2, c3, c4, c5):
    sql = """INSERT INTO photos(key, c, c1, c2, c3, c4, c5) 
    VALUES(?, ?, ?, ?, ?, ?, ?)"""
    t = (key, c, c1, c2, c3, c4, c5)
    cur.execute(sql, t)
    con.commit()
    
def deleteValue():
    g = input("Enter the row that you would like to delete based off of 'key': ")
    
    sql = """DELETE FROM photos WHERE key = ?"""
    
    cur.execute(sql, (g, ))
    con.commit()
    
    return (cur.rowcount, 'row deleted')

def showValue():
    res = cur.execute("SELECT * FROM photos")
    print("\n", res.fetchall())

def searchValue():
    x = input("Enter the row that you would like to individually open based off of 'key' and 'c'': ")
    y = x.split(' ')
    sql = """SELECT * FROM photos WHERE key = ? AND c = ?"""
    res = cur.execute(sql, (y, ))
    con.commit()
    print("\n",res.fetchall())
    
addValue('Flowers', 'Yellow', 'White', 'Green', 'Purple', 'Orange', 'Red')    
deleteValue()
showValue()
searchValue()