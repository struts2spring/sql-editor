'''
Created on 02-Dec-2015

@author: vijay
'''
import os
import shutil
import sqlite3 as lite
import sys


class Util():
    def remove(self, path=None):
        if path and os.path.exists(path):
            shutil.rmtree(path)

    def insert(self):
        try:
            con = lite.connect('test.db')

            cur = con.cursor()

            cur.executescript("""
                DROP TABLE IF EXISTS Cars;
                CREATE TABLE Cars(Id INT, Name TEXT, Price INT);
                INSERT INTO Cars VALUES(1,'Audi',52642);
                INSERT INTO Cars VALUES(2,'Mercedes',57127);
                INSERT INTO Cars VALUES(3,'Skoda',9000);
                INSERT INTO Cars VALUES(4,'Volvo',29000);
                INSERT INTO Cars VALUES(5,'Bentley',350000);
                INSERT INTO Cars VALUES(6,'Citroen',21000);
                INSERT INTO Cars VALUES(7,'Hummer',41400);
                INSERT INTO Cars VALUES(8,'Volkswagen',21600);
                """)

            con.commit()
        except lite.Error as e:

            if con:
                con.rollback()

#             print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if con:
                con.close()

    def getData(self):
        con = lite.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Cars")

            rows = cur.fetchall()

#             for row in rows:
#                 print row
    
    def convert_bytes(self, bytes):
        bytes = float(bytes)
        if bytes >= 1099511627776:
            terabytes = bytes / 1099511627776
            size = '%.2fT' % terabytes
        elif bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2fG' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.2fM' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.2fK' % kilobytes
        else:
            size = '%.2fb' % bytes
        return size

if __name__ == '__main__':
    path = '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/3238'

    util = Util()
#     util.remove(path)
    util.getData()
    pass
