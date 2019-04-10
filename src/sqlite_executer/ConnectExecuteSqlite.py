'''
Created on Feb 19, 2017

@author: vijay
'''
import sqlite3
import os
import re
from os.path import expanduser
import sys
from datetime import datetime

import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class SqlType():
    '''
    defining sql type for table, view, index, trigger
    '''

    def __init__(self, type=None, name=None, tbl_name=None, rootpage=None, sql=None):
        self.type = type
        self.name = name
        self.tbl_name = tbl_name
        self.rootpage = rootpage
        self.sql = sql
        self.columns = None

    def getCreateSql(self):
        
        columnText = ''
        for column in self.columns:
            primaryKeyText = ''
            if str(column.primaryKey) == "1":
                primaryKeyText = ' PRIMARY KEY'
            autoIncrementText = ''
            if str(column.autoIncrement) == "1":
                autoIncrementText = ' AUTOINCREMENT'
            nullableText = ''
            if str(column.nullable) == "1":
                nullableText = ' NOT NULL'
            uniqueText = ''
            if str(column.unique) == "1":
                uniqueText = ' UNIQUE'
            defultValueText = ''
            if column.defultValue and str(column.primaryKey) == "0" and str(column.autoIncrement) == "0":
                defultValueText = f'DEFAULT {column.defultValue}'
            columnText += f"\n`{column.name}` {column.dataType}{primaryKeyText}{nullableText}{autoIncrementText}{uniqueText}{defultValueText}," 
        columnText = columnText[:-1]
        sql = f'CREATE TABLE IF NOT EXISTS `{self.name}` ({columnText});'
        return sql

    def __repr__(self):
        return f'''SqlType(type={self.type}, name={self.name},tbl_name={self.tbl_name},rootpage={self.rootpage} 
                    ,sql={self.sql},columns={self.columns})'''

        
class Column():
    '''
    @param sequence: int 
    @param name: text
    @param dataType: text
    @param nullable: 0 or 1
    @param primaryKey: 0 or 1 for primary key
    '''

    def __init__(self, sequence, name, dataType, nullable, defultValue, primaryKey, unique=0, description=None, autoIncrement=0):
        self.sequence = sequence
        self.name = name
        self.dataType = dataType
        self.nullable = nullable
        self.defultValue = defultValue
        self.primaryKey = primaryKey
        self.unique = unique
        self.description = description
        self.autoIncrement = autoIncrement

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __repr__(self):
        return f'''Column(sequence={self.sequence}, name={self.name},dataType={self.dataType},nullable={self.nullable} 
                    ,defultValue={self.defultValue},primaryKey={self.primaryKey},unique={self.unique}, description={self.description},autoIncrement={self.autoIncrement})'''

        
class IndexInfo():
    '''
    @param  sequence: A sequence number assigned to each index for internal tracking purposes.
    @param name : The name of the index.
    @param unique: "1" if the index is UNIQUE and "0" if not
    @param origin: 
        "c" if the index was created by a CREATE INDEX statement, 
        "u" if the index was created by a UNIQUE constraint, or 
        "pk" if the index was created by a PRIMARY KEY constraint.
    @param partialIndex: "1" if the index is a partial index and "0" if not.

    '''

    def __init__(self, sequence, name, unique, origin, partialIndex):
        self.sequence = sequence
        self.name = name
        self.unique = unique
        self.origin = origin
        self.partialIndex = partialIndex


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
            sql = f'INSERT INTO "{table}" ({cols}) VALUES ({vals})'
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
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
                for row in rows:
                    returnRows.append(row)
        except Exception as e:
            logger.error(e, exc_info=True)
            
        return returnRows
    
    def getColumns(self, tableName=None):
        logger.debug(f'tableName: `{tableName}`')
        columns = list()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                rows = cur.execute(f"pragma table_info(`{tableName}`)").fetchall()
                for row in rows:
                    columns.append(Column(row[0], row[1], row[2], row[3], row[4], row[5]))
        except Exception as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise e
        return columns
    
    def getColumn(self, tableName=None):
        logger.debug('tableName: %s', tableName)
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                sql = f"SELECT name, sql FROM sqlite_master WHERE type='table' AND name = `{tableName}`;"
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
        This table is for internal use of editor.
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
        
        
        CREATE TABLE project_setting (id INTEGER PRIMARY KEY autoincrement,
        name TEXT , 
        description TEXT , 
        value TEXT );
        insert into project_setting values(1,'MAX_RECENT_WORKSPACES','maximum number of workspaces','10');
        insert into project_setting values(2,'SHOW_RECENT_WORKSPACES','RECENT_WORKSPACES','user.home/workspace');
        insert into project_setting values(3,'SHOW_RECENT_WORKSPACES','show recent workspace at startup','false');
        insert into project_setting values(4,'SHOW_WORKSPACE_SELECTION_DIALOG','show workspace selection dialog startup','false');
        insert into project_setting values(5,'default_workspace','show default workspace first startup','user.home/workspace');
       
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

    def getSqlObjects(self):
        '''
        return list of SqlType object
        '''
        sqlTypeObjectList = []
        try:
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            sqliteVersion = cur.fetchone()
            logger.debug(f"SQLite version: {sqliteVersion[0]}")
            
            sqliteTypes = cur.execute("select distinct type from sqlite_master;").fetchall()
            for sqliteType in sqliteTypes:
                query = f"""select * from sqlite_master where type='{sqliteType[0]}' \nAND name NOT LIKE 'sqlite_%' \nAND name != 'SAMPLE' ;
                """
                logger.debug(query)
                queryResult = cur.execute(query).fetchall()
                for typeObject in queryResult:
                    sqlType = SqlType(type=typeObject[0], name=typeObject[1], tbl_name=typeObject[2], rootpage=typeObject[3], sql=typeObject[4])
                    sqlTypeObjectList.append(sqlType)
                    logger.debug(typeObject)
                
        except sqlite3.Error as e:
            logger.error(e, exc_info=True)
        finally:
            pass
        return sqlTypeObjectList
    
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
            sqlScript = f"select db_file_path from conns where connection_name= '{connectionName}'"
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
        tableName = None
        try:
            manageSqliteDatabase = ManageSqliteDatabase(connectionName=connectionName, databaseAbsolutePath=self.getDbFilePath(connectionName))
            sqlText = "select tbl_name from sqlite_master order by tbl_name;"
            tbl_name_list = manageSqliteDatabase.executeSelectQuery(sqlText)
            logger.debug(tbl_name_list)
            
            tablePresent = False
            i = 1
            while not tablePresent:
                tableName = 'Table_{}'.format(i)
                if tuple([tableName]) in tbl_name_list:
                    logger.info(tableName + ' already present')
                    i += 1
                else:
                    tablePresent = True
             
        except Exception as e:
            logger.error(e, exc_info=True)
        
        return tableName
    
    def importingData(self, connectionName=None, sqlList=None):
        logger.info('importingData to {}'.format(connectionName))
        count = 0
        try:
            manageSqliteDatabase = ManageSqliteDatabase(connectionName=connectionName, databaseAbsolutePath=self.getDbFilePath(connectionName))
            for sql in sqlList:
                manageSqliteDatabase.executeText(sql)
                count += 1
        except Exception as e:
            count -= 1
            logger.error(e, exc_info=True)      
        importStatus = f"Total rows {count} / {len(sqlList) - 1} inserted."
        logger.info(f"Total rows {count} / {len(sqlList) - 1} inserted.")
        return importStatus


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
        sqlScript = '''
        CREATE TABLE  if not exists SAMPLE
          (
            id INTEGER primary key
        );
        CREATE VIEW SAMPLE_V AS SELECT ID FROM SAMPLE;
        '''
        cur = self.conn.cursor() 
        rows = cur.executescript(sqlScript).fetchall()
        logger.debug(cur.description)

    def getSqlObjects(self):
        '''
        @return list of SqlType object [ table, view, index, trigger] from the given sqlite database path
        '''
        sqlTypeObjectList = []
        try:
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            sqliteVersion = cur.fetchone()
            logger.debug(f"SQLite version: {sqliteVersion[0]}")
            
            sqliteTypes = cur.execute("select distinct type from sqlite_master;").fetchall()
            for sqliteType in sqliteTypes:
                query = f"""select * from sqlite_master where type='{sqliteType[0]}' 
                    AND name NOT LIKE 'sqlite_%' 
                    AND name != 'SAMPLE' ;
                """
                logger.debug(query)
                queryResult = cur.execute(query).fetchall()
                for typeObject in queryResult:
                    sqlType = SqlType(type=typeObject[0], name=typeObject[1], tbl_name=typeObject[2], rootpage=typeObject[3], sql=typeObject[4])
                    if sqlType.type == 'table':
                        sqlType.columns = self.getColumns(sqlType.name)
                    sqlTypeObjectList.append(sqlType)
                    logger.debug(typeObject)
                
        except sqlite3.Error as e:
            logger.error(e, exc_info=True)
        finally:
            if self.conn:
                self.conn.close()
        return sqlTypeObjectList

    def getObject(self):
        '''
        @return: Method returns all database object [ table, view, index] from the given sqlite database path
        '''
        con = None
        
        try:
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
            logger.debug("SQLite version: %s" % data)   
            cur.execute("select tbl_name from sqlite_master where type='table';")
            types = cur.execute("select distinct type from sqlite_master;").fetchall()
            databaseList = list()
            dbObjects = list()
            selection = None
            for sqliteType in types:
                tObjectArrayList = list()
                if sqliteType[0] == 'table':
                    selection = 'tbl_name'
                elif sqliteType[0] == 'index':
                    selection = 'name'
                elif sqliteType[0] == 'trigger':
                    selection = 'name'
                query = f"select {selection} from sqlite_master where type='{sqliteType[0]}' order by tbl_name AND name NOT LIKE 'sqlite_%' AND name!='SAMPLE' ;"
                logger.debug(query)
                tObjectList = cur.execute(query).fetchall()
                tableColumnList = list()
                for tObj in tObjectList:
                    if sqliteType[0] == 'table':
                        tableColumnsOrIndexesSql = "PRAGMA {}_info('{}');".format(sqliteType[0], tObj[0])
                        tableColumnsOrIndexesList = cur.execute(tableColumnsOrIndexesSql).fetchall()
                        tableColumnsOrIndexes = list()
                        for objChild in tableColumnsOrIndexesList:
                            tableColumnsOrIndexes.append(objChild)
                        tableColumnList.append({tObj[0]: tableColumnsOrIndexes})
                    if sqliteType[0] == 'index':
                        tableColumnsOrIndexesSql = "PRAGMA {}_info('{}');".format(sqliteType[0], tObj[0])
                        tableColumnsOrIndexesList = cur.execute(tableColumnsOrIndexesSql).fetchall()
                        tableColumnsOrIndexes = list()
                        for objChild in tableColumnsOrIndexesList:
                            tableColumnsOrIndexes.append(objChild[2])
                        tableColumnList.append({tObj[0]: tableColumnsOrIndexes})
                        
                    if sqliteType[0] == 'view':
                        tableColumnList.append({tObj[0]: []})
                        logger.debug('view')
                    if sqliteType[0] == 'trigger':
                        tableColumnList.append({tObj[0]: []})
                        logger.debug('trigger')
                dbObjects.append({sqliteType[0]: tableColumnList})
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
        @return script output as dict
        '''
        sqlOutput = dict()
        try:
            with self.conn:    
                cur = self.conn.cursor() 

                if text.count(';') > 1 :
                    cur.executescript(text)
                elif text.strip().lower().startswith(('update', 'drop', 'alter')):
                    cur.execute(text)
                else:
                    rows = cur.execute(text).fetchall()
                    if cur.description:
                        headerList = list()
                        for idx, desc in enumerate(cur.description):
                            headerList.append(desc[0])
                        sqlOutput[0] = tuple(headerList)
                        for idx, item in enumerate(rows):
                            items = []
                            for v in item:
                                if v is None:
                                    v = '-______-NULL'# this is to make a distinguish between Null
                                elif self.isBlob(v):
                                    v = '-______-BLOB'
                                    
                                items.append(v)
#                             item=['-______-Null' if v is None else v for v in item] 
                            sqlOutput[idx + 1] = items
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
            self.conn.rollback()
        return sqlOutput 
    
    def isBlob(self, text):
        blob = False
        try:
            if text != None and not isinstance(text, int) and not isinstance(text, str) and text.startswith(b'\x89'):
                blob = True
        except:
            logger.error('isBlob')
        return blob
    
    def executeSelectQuery(self, text=None):
        rows = None
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
            sql = f'INSERT INTO "{table}" ({cols}) VALUES ({vals});'
            
            self.conn.cursor().execute(sql, row)
        self.conn.commit()
        
    def sqlite_insert_or_update(self, table, rows):
        try:
            for row in rows:
                cols = ', '.join('"{}"'.format(col) for col in row.keys())
                vals = ', '.join(':{}'.format(col) for col in row.keys())
                sql = f'INSERT OR REPLACE INTO "{table}" ({cols}) VALUES ({vals});'
                self.conn.cursor().execute(sql, row)
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            logger.error(e, exc_info=True)
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e
    
    def sqlite_select(self, tableName=None):
        
        returnRows = list()
        if tableName:
            with self.conn:    
                cur = self.conn.cursor() 
                cur.execute(f"SELECT * FROM {tableName};")
                rows = cur.fetchall()
                for row in rows:
                    returnRows.append(row)
        return returnRows
    
    def getColumns(self, tableName=None):
        logger.debug(f'tableName: {tableName}')
        columns = list()
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                rows = cur.execute(f"pragma table_info('{tableName}');").fetchall()
                for row in rows:
                    columns.append(Column(row[0], row[1], row[2], row[3], row[4], row[5]))
        except Exception as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise e
        return columns   
    
    def getUpdateForTable(self, tableName=None):
        columns = self.getColumns(tableName)
        columnsNameText = ''
        whereClause = None
        for column in columns:
            if column.primaryKey:
                whereClauseValue = None
                if column.dataType.lower() in ('int', 'integer', 'numeric'):
                    whereClauseValue = 0
                else:
                    whereClauseValue = ''
                whereClause = f'\nWHERE `{column.name}`={whereClauseValue}'
            if column.dataType.lower() in ('int', 'integer', 'numeric'):
                columnsNameText += f', `{column.name}`=0'
#                 columnsValueList.append('0')
            else:
                columnsNameText += f", `{column.name}`=''"
        columnsNameText = columnsNameText[1:]
        sql = f'''UPDATE `{tableName}` \nSET {columnsNameText} {whereClause};'''
        return sql

    def getDeleteForTable(self, tableName=None):
        whereClause = None
        columns = self.getColumns(tableName)
        for column in columns:
            if column.primaryKey:
                whereClauseValue = None
                if column.dataType.lower() in ('int', 'integer', 'numeric'):
                    whereClauseValue = 0
                else:
                    whereClauseValue = ''
                whereClause = f'\nWHERE `{column.name}`={whereClauseValue}'
        sql = f'DELETE FROM `{tableName}` {whereClause};'
        return sql

    def getInsertForTable(self, tableName=None):
        columns = self.getColumns(tableName)
        columnsNameText = ",".join([f"`{column.name}`" for column in columns])
        columnsValueList = []
        for column in columns:
            if column.dataType.lower() in ('int', 'integer', 'numeric'):
                columnsValueList.append('0')
            else:
                columnsValueList.append("NULL")
        columnsValueText = ",".join(columnsValueList)
        insertSql = f'''INSERT OR REPLACE INTO `{tableName}` ({columnsNameText}) \nVALUES ({columnsValueText});'''
        return insertSql

    def getSelectForTable(self, tableName=None):
        columns = self.getColumns(tableName)
        columnsNameText = ", ".join([f"`{column.name}`" for column in columns])

        selectSql = f'''SELECT {columnsNameText} \nFROM `{tableName}`; '''
        return selectSql
    
    def getColumn(self, tableName=None):
        try:
            with self.conn:    
                cur = self.conn.cursor() 
                sql = f"SELECT name, sql FROM sqlite_master WHERE type='table' AND name = '{tableName}';"
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
#     tableName = SQLUtils().definingTableName(connectionName='picture')
#     print(tableName)
    
#########################################################################################
    sqlExecuter = SQLExecuter(database='_opal.sqlite')
    sqlExecuter.getSqlObjects()
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
#     connectionName="emp"
#     sqlExecuter=SQLExecuter()
#     databaseAbsolutePath=sqlExecuter.getDbFilePath(connectionName=connectionName)
#     db=ManageSqliteDatabase(connectionName=connectionName ,databaseAbsolutePath=databaseAbsolutePath)
#     result=db.sqlite_select(tableName="sqlite_master")
#     logger.debug(result)
