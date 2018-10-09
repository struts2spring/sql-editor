
import sqlite3 as lite
import os
import subprocess
import io
import logging

logger = logging.getLogger('extensive')



class SqlExecuterProcess():
    '''
    '''
    def __init__(self):
#         subprocess.call(cmd, shell=True)
        pass
    
    def executeCmd(self, command):
#         subprocess.call(cmd, shell=True)
#         process = subprocess.check_output(['echo $PWD','sqlite3','_opal.sqlite','.schema book'], stderr=subprocess.PIPE, shell=True)
        args = ["sqlite3", "db.sqlite", "CREATE TABLE my_table(my_column TEXT)"]
        process = subprocess.call(args)
        logger.debug(process)
#         while True:
#             line = process.stdout.readline()
#             if line != '':
#                 #the real code does filtering here
#                 print("test:", line.rstrip())
#             else:
#                 break
#         pro=process.communicate(command)
#         print(process.returncode)
#         print(pro)

class SQLExecuter1():
    '''
    '''
    def __init__(self, database=None):
        logger.debug("SQLExecuter1:%",os.getcwd())
        self.conn = lite.connect('_opal.sqlite')
        
    def sqlite_insert(self, table, rows):
        for row in rows:
            cols = ', '.join('"{}"'.format(col) for col in row.keys())
            vals = ', '.join(':{}'.format(col) for col in row.keys())
            sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
            self.conn.cursor().execute(sql, row)
        self.conn.commit()
    def sqlite_insert_or_update(self, table, rows):
        try:
            for row in rows:
                cols = ', '.join('"{}"'.format(col) for col in row.keys())
                vals = ', '.join(':{}'.format(col) for col in row.keys())
                sql = 'INSERT OR REPLACE INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
                self.conn.cursor().execute(sql, row)
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e
    
    
    def sqlite_select(self, table):
        
        returnRows = list()
        with self.conn:    
            
            cur = self.conn.cursor() 
            cur.execute("SELECT * FROM " + table)
        
            rows = cur.fetchall()
            
            for row in rows:
                returnRows.append(row)
        return returnRows
    
    def executeText(self, text=None):
        ''' This method takes input text to execute in database.
        returns output as dict
        '''
        sqlOutput = dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                rows = cur.execute(text).fetchall()
                logger.debug("cur.description: %s",cur.description) 
                for idx, item in enumerate(rows):
                    sqlOutput[idx] = item
        except Exception as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise e
        return sqlOutput
    
    
if __name__ == "__main__":
#     sqlExecuter = SQLExecuter(database='_opal.sqlite')
    sqlExecuterProcess = SqlExecuterProcess()
    command = """.tables """
    result = sqlExecuterProcess.executeCmd(command)
    logger.debug(result)
    
#     book_row = [
#                 {'id':'2',
#                  'book_name':'abc0'},
#                 {'id':'3', 'book_name':'abc1'}
#             ]
#     sqlExecuter.sqlite_insert_or_update('book', book_row)
#     print(sqlExecuter.sqlite_select('book'))
#     text="select * from book;"
#     sqlExecuter.executeText(text)

    pass
