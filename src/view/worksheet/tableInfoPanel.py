import wx

import wx.lib.agw.aui.auibook as aui
import os
from src.view.constants import ID_RUN, ID_EXECUTE_SCRIPT, LOG_SETTINGS
from src.view.worksheet.ResultListPanel import ResultPanel
import logging.config
from src.view.util.FileOperationsUtil import FileOperations
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter, \
    ManageSqliteDatabase
from src.view.worksheet.ResultGrid import ResultDataGrid
from src.view.SqlOutputPanel import SqlScriptOutputPanel
from src.view.util.parsingUtil import SqlParser

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
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(500, 200),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.SetMinSize((400, 100))
        sizer = wx.BoxSizer(wx.VERTICAL)        
        self.title = title
        # self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        
        self.creatingTableInfoPanel = CreatingTableInfoPanel(self)
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
        self.tableName = 'Unknown'
        self.parent = parent
        if kw and 'tableName' in kw.keys():
            self.tableName = kw['tableName']
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
            tableInfoPanel = CreatingTableInfoToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN, tableName=self.tableName, tabName=tabName)
            self._nb.AddPage(tableInfoPanel, tabName)      
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
        self.tabName = kw['tabName']
        self.data = list()
        vBox = wx.BoxSizer(wx.VERTICAL)
        print(kw)
        ####################################################################
        self.topResultToolbar = self.constructTopResultToolBar()
        self.bottomResultToolbar = wx.StatusBar(self)
        resultPanel = self.getPanelByTabName(tableName=kw['tableName'], tabName=kw['tabName'])
#         self.resultPanel = ResultPanel(self, data=None)
        self.bottomResultToolbar.SetStatusText("some text")
#         self.bottomResultToolbar = self.constructBottomResultToolBar()
#         self.resultPanel = ResultDataGrid(self, data=self.getData())
#         bottomResultToolbar = self.constructBottomResultToolBar()
        
        ####################################################################
        vBox.Add(self.topResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(self.resultPanel , 1, wx.EXPAND | wx.ALL, 0)
        vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        vBox.Add(self.bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
        
    def constructTopResultToolBar(self):
        
        fileOperations = FileOperations()
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))

        tb1.AddTool(ID_RUN, "Pin", fileOperations.getImageBitmap(imageName="pin2_green.png"))
        tb1.AddTool(ID_EXECUTE_SCRIPT, "Result refresh", fileOperations.getImageBitmap(imageName="resultset_refresh.png"))
        tb1.AddSeparator()

        tb1.Realize()
        
        return tb1     

    def getPanelByTabName(self, tableName=None, tabName=None):
        resultPanel = wx.Panel()
        tableData = None
        sampleData = None
        indexData = None
        referencesData = None
        triggersData = None
        try:
            selectedItemText, dbFilePath = self.findingConnectionName()
            db = ManageSqliteDatabase(connectionName=selectedItemText, databaseAbsolutePath=dbFilePath)
            result = db.sqlite_select(tableName="sqlite_master")
            for row in result:
                # selection of table and table name
                if row[0] == 'table' and row[1] == tableName:
                    tableData = {
                        0:("Position #", "Name", "Datatype", "Nullable", "Auto increment", "Default data"),
                        1:(1, None, None, None, None, None, None,)
                    }
                    indexData = None
                    sqlData = row[4]
        except Exception as e:
            logger.error(e, exc_info=True)
            
        if tabName == 'Columns':
            if not tableData:
                tableData = {
                            0:("Position #", "Name", "Datatype", "Nullable", "Auto increment", "Default data"),
                            1:(1, None, None, None, None, None, None,)
                        }
            resultPanel = ResultDataGrid(self, data=None)
            sqlParser = SqlParser()
            tableData = sqlParser.getColumn(createSql=sqlData)
            resultPanel.addData(tableData)
        elif tabName == 'Indexes':
            resultPanel = ResultDataGrid(self, data=None)
            resultPanel.addData(indexData)
        elif tabName == 'Data':
            resultPanel = ResultDataGrid(self, data=None)
            resultPanel.addData(sampleData)
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
            resultPanel = SqlScriptOutputPanel(self, data=None)
            try:
                resultPanel.text.SetText(sqlData)
            except Exception as e:
                logger.error(e, exc_info=True)
                
        elif tabName == 'ER diagram':
            resultPanel = wx.Panel()
        
        return resultPanel

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
    frame = CreatingTableInfoFrame(None, 'Open Existing Connection')
    frame.Show()
    app.MainLoop()
