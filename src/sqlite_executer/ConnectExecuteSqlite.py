'''
Created on Feb 19, 2017

@author: vijay
'''
import sqlite3
import os
import re
from os.path import expanduser
import sys
import logging
from datetime import date, datetime
from sqlalchemy.sql.expression import false

logger = logging.getLogger('extensive')


class SQLExecuter():
    '''
    '''

    def __init__(self, database='_opal.sqlite'):
        logger.debug(self.__class__.__name__)
        home = expanduser("~")
        databasePath = os.path.join(home, database)
        logger.debug('databasePath: %s', databasePath)
        self.conn = sqlite3.connect(databasePath)
#         self.createOpalTables()
        
    def sqlite_insert(self, table, rows):
        '''
        @param table: table name 
        @param rows: list of row dictionary of column values
        '''
        for row in rows:
            cols = ', '.join('"{}"'.format(col) for col in row.keys())
            vals = ', '.join(':{}'.format(col) for col in row.keys())
            sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
            try:
                with self.conn:    
                    cur = self.conn.cursor() 
                    cur.execute(sql, row)
            except Exception as e:
                logger.error(e, exc_info=True)
#         self.conn.commit()
#         pass
        
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
            logger.error(e, exc_info=True)
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e
    
    def sqlite_select(self, table):
        
        returnRows = list()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                cur.execute("SELECT * FROM " + table)
                rows = cur.fetchall()
                for row in rows:
                    returnRows.append(row)
        except Exception as e:
            logger.error(e, exc_info=True)
            
        return returnRows
    
    def getColumn(self, tableName=None):
        logger.debug('tableName: %s', tableName)
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                sql = "SELECT name, sql FROM sqlite_master WHERE type='table' AND name = '" + tableName + "';"
                rows = cur.execute(sql).fetchall()
                tableCreateStmt = rows[0][1]
                match = re.findall(r'[^[]*\[([^]]*)\]', tableCreateStmt)
                columns = set(match)
                if columns:
                    logger.debug(columns)
#                 tableCreateStmt.replace(/^[^\(]+\(([^\)]+)\)/g, '$1').split(',')
#                 logger.debug(rows)
#                 for idx, item in enumerate(rows):
#                     logger.debug(item)
        except Exception as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise e
    
    def executeText(self, text=None):
        ''' This method takes input text to execute in database.
        returns output as dict
        '''
        logger.debug('text: %s', text)
        error = 'success'
        sqlOutput = dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
#                 logger.debug('before')
                if text.strip().lower().startswith('update'):
                    cur.execute(text)
                else:
                    rows = cur.execute(text).fetchall()
#                     logger.debug(rows)
                    logger.debug(cur.description) 
    #                 logger.debug(rows)
                    if cur.description:
                        headerList = list()
                        for idx, desc in enumerate(cur.description):
        #                     logger.debug(idx, desc)
                            headerList.append(desc[0])
                        sqlOutput[0] = tuple(headerList)
                        for idx, item in enumerate(rows):
                            sqlOutput[idx + 1] = item
        except Exception as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
        logger.debug('len(sqlOutput) : %s', len(sqlOutput))
        return sqlOutput
    
    def createOpalTables(self):
        '''
        '''
        err = 'success'
        sqlScript = '''
        drop table if exists dbms;
        drop table if exists conns;
        CREATE TABLE  if not exists conns
          (
            id INTEGER PRIMARY KEY,
            connection_name TEXT UNIQUE,
            db_file_path TEXT,
            dbms_id integer not null,
            user_name TEXT,
            password TEXT,
            host TEXT,
            port INTEGER,
            sid TEXT,
            service_name TEXT,
            created_time REAL DEFAULT (datetime('now', 'localtime')),
            foreign key (dbms_id) references dbms(id)
          );
          
        create table if not exists dbms
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dbms_name text UNIQUE,
            vendor text,
            jdbc_driver TEXT,
            driver_path TEXT,
            created_time REAL DEFAULT (datetime('now', 'localtime'))
            
        );
        CREATE TABLE if not exists sql_log
          (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            sql TEXT,
            connection_name TEXT,
            created_time [timestamp] DEFAULT (datetime('now', 'localtime')),
            executed INTEGER,
            duration INTEGER
          );
          

          
        insert into dbms (dbms_name, vendor) values (  'SQLite','SQLite');
        insert into dbms (dbms_name, vendor) values (  'Oracle','Oracle');
        insert into dbms (dbms_name, vendor, jdbc_driver,driver_path) values (  'H2','H2','org.h2.Driver','/lib');
        insert into dbms (dbms_name, vendor, jdbc_driver,driver_path) values (  'HSQLDB','HSQLDB','org.hsqldb.jdbc.JDBCDriver','/lib');
        
       
        '''
        try:
            with self.conn:    
                cur = self.conn.cursor()    
#                 logger.debug('before')
                rows = cur.executescript(sqlScript).fetchall()
                logger.debug(cur.description) 

        except Exception as e:
            logger.error(e, exc_info=True)
            err = e
            self.conn.rollback()
        finally:
            self.conn.commit()
#             raise e
        return err

    def addNewConnectionRow(self, dbFilePath=None, connectionName=None):
        '''
        addNewConnectionRow adding a new row of connection
        '''
        row = dict()
        row['connection_name'] = connectionName
        row['db_file_path'] = dbFilePath
        row['dbms_id'] = 1
        rowList = list()
        rowList.append(row)
        self.sqlite_insert('conns', rowList)
#         "insert into conns (connection_name, db_file_path, dbms_id) values (  'database_sqlite_2','/docs/github/OpalDatabaseVisualizer-v1/src/sqlite_executer/_opal_2.sqlite', 1);"

    def removeConnctionRow(self, connectionName=None):
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                sqlQuery = "DELETE FROM conns WHERE connection_name=?"
                cur.execute(sqlQuery, (connectionName,))
        except Exception as e:
            logger.error(e, exc_info=True)

    def getObject(self):
    
        con = None
        
        try:
#             self.connection = sqlite3.connect('_opal.sqlite')
            
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            
            data = cur.fetchone()
            
            logger.debug("SQLite version: %s" % data)   
            cur.execute("select tbl_name from sqlite_master where type='table';")
            types = cur.execute("select distinct type from sqlite_master;").fetchall()
            databaseList = list()
            dbObjects = list()
#             logger.debug types
            for t in types:
#                 logger.debug t[0], type(t)
                tObjectArrayList = list()
                query = "select tbl_name from sqlite_master where type='{}' order by tbl_name;".format(t[0])
                logger.debug(query)
                tObjectList = cur.execute(query).fetchall()
                tableColumnList = list()
                for tObj in tObjectList:
                    if t[0] == 'table' or t[0] == 'index':
                        tableColumnsOrIndexesSql = "PRAGMA {}_info('{}');".format(t[0], tObj[0])
                        logger.debug(tableColumnsOrIndexesSql)
                        tableColumnsOrIndexesList = cur.execute(tableColumnsOrIndexesSql).fetchall()
#                         logger.debug objChildList
                        tableColumnsOrIndexes = list()
                        for objChild in tableColumnsOrIndexesList:
                            tableColumnsOrIndexes.append(objChild)
#                             logger.debug objChild
                        tableColumnList.append([tObj[0], tableColumnsOrIndexes])
                    if t[0] == 'view':
                        tableColumnList.append([tObj[0], []])
                        logger.debug('view')
                        
#                     if t[0] == 'index':
#                         tablesHavingIndexesSql = "PRAGMA " + t[0] + "_info(%s);" % tObj[0]
#                         tablesHavingIndexesList = cur.execute(tablesHavingIndexesSql).fetchall()
#                         logger.debug tablesHavingIndexesSql
#                         for tableHavingIndexes in tablesHavingIndexesList:
#                             tableIndexesSql = "PRAGMA " + t[0] + "_list(%s);" % tObj[0]
# #                         logger.debug objChildList
#                         tableColumnsOrIndexes = list()
#                         for objChild in tableColumnsOrIndexesList:
#                             tableColumnsOrIndexes.append(objChild)
                        
#                         logger.debug tableColumnList
#                 tObjectArrayList.append(tableColumnList)
#                 logger.debug tObjectArrayList
                dbObjects.append((t[0], tableColumnList))
            logger.debug(dbObjects)
#                 dbObjects.append(tObjectArrayList)
#             logger.debug dbObjects
#             logger.debug cur.fetchallDict()
#             for row in cur.execute("select tbl_name from sqlite_master where type='table';"):
#                 logger.debug row                
            
#             data = cur.fetchone()
        except sqlite3.Error as e:
            logger.error(e, exc_info=True)
        finally:
            pass
#             if self.conn:
#                 self.conn.close()
        databaseList.append('_opal')
        databaseList.append(dbObjects)
        return databaseList
    
    def getListDatabase(self):
        '''
        This method will return list of database available to connect.
        assumption , conns and sql_log table will available.
        
        '''
#         self.createOpalTables()
        dbList = self.sqlite_select("conns")
        return dbList

    def getContectedObject(self, connectionName, databaseAbsolutePath):
        dbObjects = ManageSqliteDatabase(connectionName=connectionName , databaseAbsolutePath=databaseAbsolutePath).getObject()
        return dbObjects
    
    def getDbFilePath(self, connectionName=None):
        dbFilePath = None
        if connectionName:
            sqlScript = "select db_file_path from conns where connection_name= '{}'".format(connectionName)
            cur = self.conn.cursor()   
            rows = cur.execute(sqlScript).fetchone()
            if rows:
                dbFilePath = rows[0]
        return dbFilePath


class SQLUtils():

    def __init__(self):
        pass

    def updateSqlLog(self, sqlText, duration, connectionName=None):
        logger.debug('updateSqlLog : %s', sqlText)
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        table = 'sql_log'
        rows = [{'id':None, 'sql':str(sqlText), 'connection_name':connectionName, 'created_time':datetime.now(), 'executed':'1', 'duration':duration}]
        sqlExecuter.sqlite_insert(table, rows)
        
    def refreshSqlLogUi(self):
        logger.debug('refreshSqlLogUi')
        historyGrid = self.GetTopLevelParent()._mgr.GetPane("sqlLog").window
        sqlText = 'select * from sql_log order by created_time desc;'
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        sqlOutput = sqlExecuter.executeText(sqlText)
        historyGrid.addData(data=sqlOutput)
    
    def getDbFilePath(self, connectionName):
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        return  sqlExecuter.getDbFilePath(connectionName)
    
    def definingTableName(self, connectionName=None):
        '''
        This is to define new table name .
        '''
        
#         while
        tableName=None
        try:
            manageSqliteDatabase = ManageSqliteDatabase(connectionName=connectionName, databaseAbsolutePath=self.getDbFilePath(connectionName))
            sqlText = "select tbl_name from sqlite_master order by tbl_name;"
            tbl_name_list = manageSqliteDatabase.executeSelectQuery(sqlText)
            logger.debug(tbl_name_list)
            
            tablePresent=False
            i=1
            while not tablePresent:
                tableName='Table {}'.format(i)
                if tuple([tableName]) in tbl_name_list:
                    logger.info(tableName+' already present')
                    i +=1
                else:
                    tablePresent=True
             
        except Exception as e:
            logger.error(e, exc_info=True)
        
        return tableName
    
class ManageSqliteDatabase():

    def __init__(self, connectionName=None, databaseAbsolutePath=None):
        '''
        @param param: connection_name
        @param param: databaseAbsolutePath
        '''
#         databaseAbsolutePath=os.path.abspath(databaseAbsolutePath)
#         databasePath=os.path.abspath(databaseAbsolutePath)
#         databaseAbsolutePath=os.path.normpath(databaseAbsolutePath)
        pathDir = os.path.dirname(databaseAbsolutePath)
        head, tail = os.path.split(databaseAbsolutePath)
        os.chdir(pathDir)
        self.conn = sqlite3.connect(tail)
        self.connectionName = connectionName
 
    def createTable(self):
        sql = '''
        CREATE TABLE  if not exists ABC
          (
            id INTEGER PRIMARY KEY
        );
        '''
        cur = self.conn.cursor() 
        cur.execute(sql)
        
    def getObject(self):
        '''
        Method returns all database object [ table, view, index] from the given sqlite database path
        '''
    
        con = None
        
        try:
#             self.connection = sqlite3.connect('_opal.sqlite')
            
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            
            data = cur.fetchone()
            
            logger.debug("SQLite version: %s" % data)   
            cur.execute("select tbl_name from sqlite_master where type='table';")
            types = cur.execute("select distinct type from sqlite_master;").fetchall()
            databaseList = list()
            dbObjects = list()
#             logger.debug types
            for t in types:
#                 logger.debug t[0], type(t)
                tObjectArrayList = list()
                query = "select tbl_name from sqlite_master where type='{}' order by tbl_name;".format(t[0])
                logger.debug(query)
                tObjectList = cur.execute(query).fetchall()
                tableColumnList = list()
                for tObj in tObjectList:
                    if t[0] == 'table' or t[0] == 'index':
#                         tableColumnsOrIndexesSql = "PRAGMA " + t[0] + "_info(%s);" % tObj[0]
                        tableColumnsOrIndexesSql = "PRAGMA {}_info('{}');".format(t[0], tObj[0])
                        
#                         logger.debug(tableColumnsOrIndexesSql)
                        tableColumnsOrIndexesList = cur.execute(tableColumnsOrIndexesSql).fetchall()
#                         logger.debug objChildList
                        tableColumnsOrIndexes = list()
                        for objChild in tableColumnsOrIndexesList:
                            tableColumnsOrIndexes.append(objChild)
#                             print objChild
                        tableColumnList.append({tObj[0]: tableColumnsOrIndexes})
                    if t[0] == 'view':
                        tableColumnList.append({tObj[0]: []})
                        logger.debug('view')

                dbObjects.append({t[0]: tableColumnList})
#             logger.debug(dbObjects)

        except sqlite3.Error as e:
            logger.error(e, exc_info=True)
            sys.exit(1)
            
        finally:
            
            if self.conn:
                self.conn.close()
        databaseList.append(self.connectionName)
        databaseList.append(dbObjects)
        return databaseList        

    def executeText(self, text=None):
        ''' This method takes input text to execute in database.
        returns output as dict
        '''
        sqlOutput = dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
#                 logger.debug('before')
                listOfSqls = text.strip().lower().split(';')
                if len(listOfSqls) > 1 and not text.strip().lower().startswith('select'):
                    cur.executescript(text)
                elif text.strip().lower().startswith('update'):
                    cur.execute(text)
                else:
                    rows = cur.execute(text).fetchall()
#                     logger.debug(rows)
#                     logger.debug(cur.description) 
    #                 logger.debug(rows)
                    if cur.description:
                        headerList = list()
                        for idx, desc in enumerate(cur.description):
        #                     logger.debug(idx, desc)
                            headerList.append(desc[0])
                        sqlOutput[0] = tuple(headerList)
                        for idx, item in enumerate(rows):
                            sqlOutput[idx + 1] = item
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
            self.conn.rollback()
#             raise e
#         logger.debug(sqlOutput)
        return sqlOutput
    
    def executeSelectQuery(self, text=None):
        rows=None
        with self.conn:    
                cur = self.conn.cursor() 
                rows = cur.execute(text).fetchall()
        return rows
    
    def sqlite_insert(self, table, rows):
        '''
        @param table: table name 
        @param rows: list of row dictionary of column values
        '''
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
            logger.error(e, exc_info=True)
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e
    
    def sqlite_select(self, table):
        
        returnRows = list()
        with self.conn:    
            
            cur = self.conn.cursor() 
#             logger.debug('before')
            cur.execute("SELECT * FROM {}".format(table))
        
            rows = cur.fetchall()
            
            for row in rows:
                returnRows.append(row)
        return returnRows
    
    def getColumn(self, tableName=None):
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                sql = "SELECT name, sql FROM sqlite_master WHERE type='table' AND name = '" + tableName + "';"
                rows = cur.execute(sql).fetchall()
                tableCreateStmt = rows[0][1]
                match = re.findall(r'[^[]*\[([^]]*)\]', tableCreateStmt)
                columns = set(match)
#                 if columns:
#                     logger.debug(columns)
#                 tableCreateStmt.replace(/^[^\(]+\(([^\)]+)\)/g, '$1').split(',')
#                 logger.debug(rows)
#                 for idx, item in enumerate(rows):
#                     logger.debug(item)
        except Exception as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise e    

    
if __name__ == "__main__":
    logger.debug('hi')
    tableName=SQLUtils().definingTableName(connectionName='picture')
    print(tableName)
    
#########################################################################################
#     sqlExecuter = SQLExecuter(database='_opal.sqlite')
#     sqlExecuter = SQLExecuter(database='_opal.sqlite')
# #     sqlExecuter.getDbFilePath('database_sqlite_1')
#     sqlExecuter.addNewConnectionRow(dbFilePath=r"c:\soft\4.sqlite", connectionName='4')
#     obj=sqlExecuter.getObject()
#     if len(obj[1])==0:
#         sqlExecuter.createOpalTables()
#     logger.debug(len(obj[1]))
#     result=sqlExecuter.executeText("select * from conns")
#     logger.debug(result)
#     obj=sqlExecuter.getObject()
#     logger.debug(obj)
#     tableName = 'albums'
#     sqlExecuter.getColumn(tableName)
#     sql = "SELECT * FROM albums "
#     result = sqlExecuter.executeText(text=sql)
#     logger.debug(result)

##########################################################################################
#     dbList = sqlExecuter.getListDatabase()
#     for db in dbList:
#         if db[3] == 1:
#             dbObjects = ManageSqliteDatabase(connectionName=db[1] ,databaseAbsolutePath=db[2]).getObject()
#             logger.debug(dbObjects)
##########################################################################################
            
#     logger.debug(dbList)
#     ManageSqliteDatabase(connectionName="1", databaseAbsolutePath=r"_opal_1.sqlite")
