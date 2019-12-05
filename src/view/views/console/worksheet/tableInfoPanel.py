import wx

import logging.config
from src.view.constants import  LOG_SETTINGS, ID_ADD_ROW, ID_DUPLICATE_ROW, ID_DELETE_ROW, ID_SAVE_ROW, ID_REFRESH_ROW
from src.view.util.FileOperationsUtil import FileOperations
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter, ManageSqliteDatabase
from src.view.util.parsingUtil import SqlParser
from src.view.views.console.worksheet.ResultGrid import ResultDataGrid
from src.view.views.console.SqlOutputPanel import SqlConsoleOutputPanel
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
'''
Create tabs with 
Columns, Indexes, Data, References, Triggers, SQL, ER diagram

Columns Tab:
    should have tablualted data with columns
    Position #, Name, Datatype, Nullable,Auto increment, Default data, 
Indexes Tab:
    Index Name, Table, Index Type, Ascending, Unique, Qualifier, Cardinality, Index Description
Data Tab:
    Table data with 20 row.

References Tab:
    Name , Owner, Ref Table, Type, Ref Object, On Delete, On Update, Deferability
ER diagram Tab:
    
Triggers Tab:
    Name, Table, Description
SQL Tab:
    sql stamt 
    create table
    create index
    

'''


class CreatingTableInfoFrame(wx.Frame):
    
    def __init__(self, parent, title, **kw):
        wx.Frame.__init__(self, parent, -1, title, size=(500, 200),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.SetMinSize((400, 100))
        sizer = wx.BoxSizer(wx.VERTICAL)        
        self.title = title
        # self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        
        self.creatingTableInfoPanel = CreatingTableInfoPanel(self, kw)
        ####################################################################
        
        sizer.Add(self.creatingTableInfoPanel, 1, wx.EXPAND)
        # sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        
        self.SetSizer(sizer)
        self.Center()
#         self.createStatusBar()
        self.Show(True)

    def OnCloseFrame(self, event):
        self.Destroy()  


class CreatingTableInfoPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.tableName = None
        self.parent = parent
        self.dataSourceTreeNode = None
        if kw and 'tableName' in kw.keys():
            self.tableName = kw['tableName']
            self.dataSourceTreeNode = kw['dataSourceTreeNode']
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        # Attributes
        self._nb = aui.AuiNotebook(self)
        self.addTab()
        ####################################################################
        self.__DoLayout()

#         # vBox.Add(worksheetToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         # vBox.Add(self.worksheetPanel , 1, wx.EXPAND | wx.ALL, 0)
# #         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
#         sizer = wx.BoxSizer(wx.VERTICAL)
# #         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
#         self.SetSizer(sizer)  
    def addTab(self, name='Start Page'):
#             worksheetPanel.worksheetPanel.editorPanel
#         name = 'Columns '
        
        # add following list of tabs
        listOfTabs = ['Columns', 'Indexes', 'Data', 'References', 'Triggers', 'SQL', 'ER diagram']
        for tabName in listOfTabs:
            tableInfoPanel = CreatingTableInfoToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN, tableName=self.tableName, tabName=tabName, dataSourceTreeNode=self.dataSourceTreeNode)
            try:
                self._nb.AddPage(tableInfoPanel, tabName)  
            except Exception as e:
                logger.error(e)    
            self.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN, self.onTabRightDown, self._nb)
            self.Bind(aui.EVT_AUINOTEBOOK_BG_DCLICK, self.onBgDoubleClick, self._nb)  
            self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onCloseClick, self._nb)          

    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()

    def onTabRightDown(self, event):
        logger.info('onTabRightDown')
        
    def onBgDoubleClick(self, event):
        logger.info('onBgDoubleClick')
        
    def onCloseClick(self, event):
        logger.info('onCloseClick')
        self.GetCurrentPage()        

        
class CreatingTableInfoToolbarPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.fileOperations = FileOperations()
        self.tabName = kw['tabName']
        self.dataSourceTreeNode = kw['dataSourceTreeNode']
        self.data = list()
        self.sqlList = dict()
        vBox = wx.BoxSizer(wx.VERTICAL)
        logger.debug(kw)
        ####################################################################
        # adding new rows to the list on click of add button
#         self.newRows={}
        ####################################################################
#         self.topResultToolbar = self.constructTopResultToolBar()
        self.bottomResultToolbar = wx.StatusBar(self)
        self.resultPanel, self.toolbar = self.getPanelByTabName(tableName=kw['tableName'], tabName=kw['tabName'])
#         self.resultPanel = ResultPanel(self, data=None)
        self.bottomResultToolbar.SetStatusText("some text")
#         self.bottomResultToolbar = self.constructBottomResultToolBar()
#         self.resultPanel = ResultDataGrid(self, data=self.getData())
#         bottomResultToolbar = self.constructBottomResultToolBar()
        
        ####################################################################
        vBox.Add(self.toolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(self.resultPanel , 1, wx.EXPAND | wx.ALL, 0)
        vBox.Add(self.resultPanel , 1, wx.EXPAND | wx.ALL)
        vBox.Add(self.bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
        
    def constructTopResultToolBar(self, tabName=None):
        
        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        
        tb1.SetToolBitmapSize(wx.Size(42, 42))

        if tabName == 'Data':
            tools = [
                (ID_SAVE_ROW, "Save", "save_to_database.png", 'Save (Ctrl+S)', self.onSave),
                (),
                (ID_REFRESH_ROW, "Result refresh", "resultset_refresh.png", 'Result refresh \tF5', self.onRefresh),
                (ID_ADD_ROW, "Add a new row", "row_add.png", 'Add a new row', self.onAddRow),
                (ID_DUPLICATE_ROW, "Duplicate selected row", "row_copy.png", 'Duplicate selected row', self.onDuplicateRow),
                (ID_DELETE_ROW, "Delete selected row", "row_delete.png", 'Delete selected row', self.onDeleteRow),
                ]
            for tool in tools:
                if len(tool) == 0:
                    tb1.AddSeparator()
                else:
                    logger.debug(tool)
                    toolItem = tb1.AddSimpleTool(tool[0], tool[1], self.fileOperations.getImageBitmap(imageName=tool[2]), short_help_string=tool[3])
                    if tool[4]:
                        self.Bind(wx.EVT_MENU, tool[4], id=tool[0])
#             tb1.AddSimpleTool(ID_SAVE_ROW, "Save", fileOperations.getImageBitmap(imageName="save_to_database.png"), short_help_string='Save to database')
#             tb1.AddSeparator()
#             
#             tb1.AddSimpleTool(ID_REFRESH_ROW, "Result refresh", fileOperations.getImageBitmap(imageName="resultset_refresh.png"), short_help_string='Refresh data')
#             tb1.AddSimpleTool(ID_ADD_ROW, "Add a new row", fileOperations.getImageBitmap(imageName="row_add.png"), short_help_string='Add new row')
#             tb1.AddSimpleTool(ID_DUPLICATE_ROW, "Duplicate current row", fileOperations.getImageBitmap(imageName="row_copy.png"), short_help_string='Duplicate current row')
#             tb1.AddSimpleTool(ID_DELETE_ROW, "Delete current row", fileOperations.getImageBitmap(imageName="row_delete.png"), short_help_string='Delete current row')
#             tb1.AddSeparator()
            
#         tb1.AddTool(ID_RUN, "Pin", fileOperations.getImageBitmap(imageName="pin2_green.png"))

        tb1.Realize()
        
        return tb1     

    def onSave(self, event):
        logger.debug('onSave')
        
        # finding rows to be updated
        originalData = self.resultPanel.getData()
        for row in range(self.resultPanel.GetNumberRows()):
            rowMatch = True
            rowPresent = False
            for col in range(self.resultPanel.GetNumberCols()):
                newVal = self.resultPanel.GetCellValue(row, col)
                if row + 1 in originalData:
                    rowPresent = True
                    originalValue = originalData[row + 1][col]
                    if '-______-NULL' == originalValue:
                        originalValue = originalValue.replace('-______-', '')
                    if str(originalValue) != newVal:
                        rowMatch = False
                        break
                else:
                    rowPresent = False
            if rowPresent and not rowMatch:
                newData = [self.resultPanel.GetCellValue(row, col) for col in range(self.resultPanel.GetNumberCols())]
                columnClauseForUpdate = self.getColumnClauseForUpdate(newData=newData)
                whereClause = self.getWhereClause(originalData[row + 1])
                sql = f"UPDATE '{self.dataSourceTreeNode.nodeLabel}' SET {columnClauseForUpdate} WHERE {whereClause} ;"
                self.sqlList[row] = {
                                    'sql':sql,
                                    'dml':'UPDATE',
                                    'tableName':self.dataSourceTreeNode.nodeLabel,
                                    'columns':self.dataSourceTreeNode.sqlType.columns,
                                    'newValues':newData,
                                    'oldValues':originalData[row + 1]
                                    }
            elif not rowPresent:
                newData = [self.resultPanel.GetCellValue(row, col) for col in range(self.resultPanel.GetNumberCols())]
                self.sqlList.get(row)['values']=newData
        db = ManageSqliteDatabase(connectionName=self.dataSourceTreeNode.dataSource.connectionName, databaseAbsolutePath=self.dataSourceTreeNode.dataSource.filePath)
        for row, sqlListRow in self.sqlList.items():
            sql = self.getSql(sqlListRow).get('sql')
            db.executeText(sql)
        self.sqlList = dict()
# #         sqlText = self.generateSql()
#         db = ManageSqliteDatabase(connectionName=self.dataSourceTreeNode.dataSource.connectionName, databaseAbsolutePath=self.dataSourceTreeNode.dataSource.filePath)
# #         db.executeText(sqlText)
#         
#         originalData = self.resultPanel.getData()
#         originalDataSet = set()
#         for k, v in originalData.items():
#             if k > 0:
#                 originalDataSet.add(tuple([str(x) for x in v]))
#         
#         newData = set()
#         
#         for row in range(self.resultPanel.GetNumberRows()):
#             newRow = []
#             for col in range(self.resultPanel.GetNumberCols()):
#                 val = self.resultPanel.GetCellValue(row, col)
#                 if self.resultPanel.GetCellTextColour(row, col) == wx.LIGHT_GREY and val in ('NULL', 'BLOB'):
#                     newRow.append(f'-______-{val}')
#                 else:
#                     newRow.append(self.resultPanel.GetCellValue(row, col))
#             newData.add(tuple(newRow))
#         
#         sql = self.generateSql(oldDataSet=originalDataSet, newDataSet=newData)
#         print(sql)

    def onRefresh(self, event):
        logger.debug('onRefresh')
        self.sqlList = dict()
        db = ManageSqliteDatabase(connectionName=self.dataSourceTreeNode.dataSource.connectionName, databaseAbsolutePath=self.dataSourceTreeNode.dataSource.filePath)
#         result = db.sqlite_select(tableName="sqlite_master")
        data = None
        tableName = self.GetParent().GetParent().tableName
        if tableName:
            data = db.executeText(text=f"SELECT * FROM '{tableName}' LIMIT 500;")
        if data:
            logger.debug('setResultData count: %s', len(data.keys()))
        self.resultPanel.addData(data)
        self.resultPanel.Layout()

    def onAddRow(self, event):
        logger.debug('onAddRow')
        logger.debug(self.resultPanel.GetNumberRows())
#         self.newRows[self.resultPanel.GetNumberRows()+1]=list()
#         data=self.resultPanel.getData()
        columnsName = [column.name for column in self.dataSourceTreeNode.sqlType.columns]
        values = 'null,' * len(columnsName)
        values = values[:-1]
        valuesList = values[:-1].split(',')
        columns = "`,`".join(columnsName)
        sql = f'''INSERT INTO '{self.dataSourceTreeNode.nodeLabel}' (`{columns}`) VALUES ({values});'''
#         self.sqlList[self.resultPanel.GetNumberRows()] = sql
        self.sqlList[self.resultPanel.GetNumberRows()] = {
                                    'sql':sql,
                                    'dml':'INSERT',
                                    'tableName':self.dataSourceTreeNode.nodeLabel,
                                    'columns':columns,
                                    'values':valuesList
                                    }
        self.resultPanel.AppendRows(numRows=1, updateLabels=True)
        
        # TODO : a logic for save insert, update , delete has to go here
    def onDuplicateRow(self, event):
        logger.debug('onDuplicateRow')

    def onDeleteRow(self, event):
        seletedRows = list(self.resultPanel.GetSelectedRows())
        logger.debug(f'onDeleteRow: {seletedRows}')
        seletedRows.sort(reverse=True)
        originalData = self.resultPanel.getData()
        for selectedRow in seletedRows:
            if selectedRow in self.sqlList:
                del self.sqlList[selectedRow]
            elif selectedRow in originalData:
                columnsName = [column.name for column in self.dataSourceTreeNode.sqlType.columns]
                columns = "`,`".join(columnsName)
                data = originalData[selectedRow + 1]
                whereClause = self.getWhereClause(data)
                sql = f"""DELETE FROM '{self.dataSourceTreeNode.nodeLabel}' WHERE {whereClause} ;"""
#                 self.sqlList[selectedRow] = sql
                self.sqlList[selectedRow] = {
                                    'sql':sql,
                                    'dml':'DELETE',
                                    'tableName':self.dataSourceTreeNode.nodeLabel,
                                    'columns':columns,
                                    'values':data
                                    }
#             self.newRows.append(list())
#             if selectedRow+1 in self.newRows: 
#                 del self.newRows[selectedRow+1]
            self.resultPanel.DeleteRows(pos=selectedRow, numRows=1, updateLabels=True)

#         self.resultPanel.DeleteRows(pos=0, numRows=numRows, updateLabels=True)
#         self.resultPanel.dele  
    def getSql(self, sqlListRow): 
        sql=None
        columnsName = [column.name for column in self.dataSourceTreeNode.sqlType.columns]
        columns = "`,`".join(columnsName)
        if sqlListRow.get('dml') == 'DELETE':
            whereClause = self.getWhereClause(sqlListRow.get('values'))
            sql = f"""DELETE FROM '{sqlListRow.get('tableName')}' WHERE {whereClause} ;"""
        elif sqlListRow.get('dml') == 'INSERT':
#             columns = "`,`".join(sqlListRow.get('columns'))
            values="','".join(sqlListRow.get('values'))
            sql = f'''INSERT INTO '{sqlListRow.get('tableName')}' (`{sqlListRow.get('columns')}`) VALUES ('{values}');'''
        elif sqlListRow.get('dml') == 'UPDATE':
            columnClauseForUpdate = self.getColumnClauseForUpdate(newData=sqlListRow.get('newValues'))
            whereClause = self.getWhereClause(sqlListRow.get('oldValues'))
            sql = f"UPDATE '{self.dataSourceTreeNode.nodeLabel}' SET {columnClauseForUpdate} WHERE {whereClause} ;"
        sqlListRow['sql']=sql
        return sqlListRow   
        
    def getColumnClauseForUpdate(self, newData=None):
        columnClauseForUpdate = []
        for idx, column in enumerate(self.dataSourceTreeNode.sqlType.columns):
            dataStr = newData[idx]
            if '-______-NULL' == dataStr:
                dataStr = dataStr.replace('-______-', '')
            if column.primaryKey != 1:
                columnClauseForUpdate.append(f" `{column.name}` = {dataStr}")
        columnClauseForUpdateStr = ",".join(columnClauseForUpdate)     
        
        return columnClauseForUpdateStr

    def getWhereClause(self, data):
        whereClasue = []
        for idx, column in enumerate(self.dataSourceTreeNode.sqlType.columns):
            dataStr = data[idx]
            if '-______-NULL' == dataStr:
                dataStr = dataStr.replace('-______-', '')
                whereClasue.append(f" `{column.name}` is {dataStr}")
            else:
                whereClasue.append(f" `{column.name}`={dataStr}")
        whereClasueStr = " AND".join(whereClasue)
        return whereClasueStr

    def generateSql(self, oldDataSet=None, newDataSet=None):
        logger.debug('generateSql')
        intersect = oldDataSet.intersection(newDataSet)
        insertSqlData = newDataSet - oldDataSet
        oldPKSet = set(self.getPrimaryKeyValue(oldDataSet))
        newPKSet = set(self.getPrimaryKeyValue(newDataSet))
        insertPKSet = set(self.getPrimaryKeyValue(insertSqlData))
        updatePKSet = oldPKSet.intersection(insertPKSet)
        columnsName = [column.name for column in self.dataSourceTreeNode.sqlType.columns]
        columns = "','".join(columnsName)
        updateSqlDataSet = set()
        valuesList = list()
        for insertSqlDataRow in insertSqlData:
            if insertSqlDataRow[0] in updatePKSet:
                updateSqlDataSet.add(insertSqlDataRow)
            else:
                valuesList.append("','".join(insertSqlDataRow))
        sqlList = list()
        for values in valuesList: 
            sqlList.append(f'''INSERT INTO '{self.dataSourceTreeNode.nodeLabel}' ('{columns}') VALUES ('{values}');''')
        return '\n'.join(sqlList)

    def getPrimaryKeyValue(self, oldDataSet):
        return [str(oldData[0]) for oldData in oldDataSet]

    def getPanelByTabName(self, tableName=None, tabName=None):
        toolbar = self.constructTopResultToolBar()
        resultPanel = wx.Panel()
        tableData = None
        sampleData = None
        indexData = None
        referencesData = None
        triggersData = None
        sqlData = None
        db = None
        try:
#             selectedItemText, dbFilePath = self.findingConnectionName()
            db = ManageSqliteDatabase(connectionName=self.dataSourceTreeNode.dataSource.connectionName, databaseAbsolutePath=self.dataSourceTreeNode.dataSource.filePath)
            result = db.sqlite_select(tableName="sqlite_master")
            for row in result:
                # selection of table and table name
                if row[0] == 'table' and row[1] == tableName:
                    tableData = {
                        0:("#", "Name", "Datatype", "PRIMARY KEY", "Nullable", "Unique", "Auto increment", "Default data", "Description")
                    }
                    indexData = None
                    sqlData = row[4]
        except Exception as e:
            logger.error(e, exc_info=True)
            
        if tabName == 'Columns':
            resultPanel = ResultDataGrid(self, data=None)
            if tableName:
                rows = db.executeText(f"pragma table_info('{tableName}');")
                if rows:
                    rows[-1] = ['INTEGER', 'VARCHAR', 'VARCHAR', 'BOOLEAN', 'VARCHAR', 'BOOLEAN' ]
                resultPanel.addData(rows)
        elif tabName == 'Indexes':
            resultPanel = ResultDataGrid(self, data=None)
            
            resultPanel.addData(indexData)
        elif tabName == 'Data':
            toolbar = self.constructTopResultToolBar(tabName=tabName)
            resultPanel = ResultDataGrid(self, data=None)
            data = None
            if tableName:
                data = db.executeText(text=f"SELECT * FROM `{tableName}` LIMIT 500;")
            if data:
                logger.debug('setResultData count: %s', len(data.keys()))
#                 self.bottomResultToolbar.SetStatusText("Count: {}".format(str(len(data.keys()))))
                resultPanel.addData(data)
                resultPanel.Layout()
        elif tabName == 'References':
            resultPanel = ResultDataGrid(self, data=None)
            resultPanel.addData(referencesData)
        elif tabName == 'Triggers':
            resultPanel = ResultDataGrid(self, data=None)
            resultPanel.addData(triggersData)
        elif tabName == 'Triggers':
            resultPanel = ResultDataGrid(self, data=None)
            resultPanel.addData(triggersData)
        elif tabName == 'SQL':
            resultPanel = SqlConsoleOutputPanel(self, data=None)
            try:
                resultPanel.text.SetText(sqlData)
            except Exception as e:
                logger.error(e, exc_info=True)
                
        elif tabName == 'ER diagram':
            resultPanel = wx.Panel()
        
        return resultPanel, toolbar

    def findingConnectionName(self):
        '''
        This method defines connection name based on selected connection in the tree.
        @return: (connectionName, databaseAbsolutePath)
        '''
        ##################################################################################
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        textCtrl = self.GetTopLevelParent()._ctrl
        connectionName = textCtrl.GetValue()
        databaseAbsolutePath = sqlExecuter.getDbFilePath(connectionName)
        logger.debug("databaseAbsolutePath: %s", databaseAbsolutePath)
        
        ##################################################################################        
        return connectionName, databaseAbsolutePath


if __name__ == '__main__':
    
    app = wx.App(False)
    sqlExecuter = SQLExecuter(database='_opal.sqlite')
    frame = CreatingTableInfoFrame(None, 'Open Existing Connection', dataSourceTreeNode=None)
    frame.Show()
    app.MainLoop()
