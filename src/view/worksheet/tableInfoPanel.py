import wx

import wx.lib.agw.aui.auibook as aui
import os
from src.view.constants import ID_RUN, ID_EXECUTE_SCRIPT, LOG_SETTINGS,\
    ID_ADD_ROW, ID_DUPLICATE_ROW, ID_DELETE_ROW, ID_SAVE_ROW, ID_REFRESH_ROW
from src.view.worksheet.ResultListPanel import ResultPanel
import logging.config
from src.view.util.FileOperationsUtil import FileOperations
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter, \
    ManageSqliteDatabase
from src.view.worksheet.ResultGrid import ResultDataGrid
from src.view.SqlOutputPanel import SqlConsoleOutputPanel
from src.view.util.parsingUtil import SqlParser
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
        logger.debug(kw)
        ####################################################################
#         self.topResultToolbar = self.constructTopResultToolBar()
        self.bottomResultToolbar = wx.StatusBar(self)
        resultPanel, toolbar = self.getPanelByTabName(tableName=kw['tableName'], tabName=kw['tabName'])
#         self.resultPanel = ResultPanel(self, data=None)
        self.bottomResultToolbar.SetStatusText("some text")
#         self.bottomResultToolbar = self.constructBottomResultToolBar()
#         self.resultPanel = ResultDataGrid(self, data=self.getData())
#         bottomResultToolbar = self.constructBottomResultToolBar()
        
        ####################################################################
        vBox.Add(toolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(self.resultPanel , 1, wx.EXPAND | wx.ALL, 0)
        vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        vBox.Add(self.bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
        
    def constructTopResultToolBar(self, tabName=None):
        
        fileOperations = FileOperations()
        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        
        tb1.SetToolBitmapSize(wx.Size(42, 42))

        if tabName=='Data':
            tb1.AddSimpleTool(ID_SAVE_ROW, "Save", fileOperations.getImageBitmap(imageName="save_to_database.png"), short_help_string='Save to database')
            tb1.AddSeparator()
            
            tb1.AddSimpleTool(ID_REFRESH_ROW, "Result refresh", fileOperations.getImageBitmap(imageName="resultset_refresh.png"), short_help_string='Refresh data')
            tb1.AddSimpleTool(ID_ADD_ROW, "Add a new row", fileOperations.getImageBitmap(imageName="row_add.png"), short_help_string='Add new row')
            tb1.AddSimpleTool(ID_DUPLICATE_ROW, "Duplicate current row", fileOperations.getImageBitmap(imageName="row_copy.png"), short_help_string='Duplicate current row')
            tb1.AddSimpleTool(ID_DELETE_ROW, "Delete current row", fileOperations.getImageBitmap(imageName="row_delete.png"), short_help_string='Delete current row')
            tb1.AddSeparator()
            
            
#         tb1.AddTool(ID_RUN, "Pin", fileOperations.getImageBitmap(imageName="pin2_green.png"))

        tb1.Realize()
        
        return tb1     

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
            selectedItemText, dbFilePath = self.findingConnectionName()
            db = ManageSqliteDatabase(connectionName=selectedItemText, databaseAbsolutePath=dbFilePath)
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
            if not tableData:
                tableData = {
                            0:("#", "Name", "Datatype", "PRIMARY KEY", "Nullable", "Unique", "Auto increment", "Default data", "Description")
                        }
            resultPanel = ResultDataGrid(self, data=None)
            sqlParser = SqlParser()
            tableData = sqlParser.getColumn(createSql=sqlData)
            resultPanel.addData(tableData)
        elif tabName == 'Indexes':
            resultPanel = ResultDataGrid(self, data=None)
            
            resultPanel.addData(indexData)
        elif tabName == 'Data':
            toolbar = self.constructTopResultToolBar(tabName=tabName)
            resultPanel = ResultDataGrid(self, data=None)
            data = None
            if tableName:
                data = db.executeText(text="SELECT * FROM '{}' LIMIT 20;".format(tableName))
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
    frame = CreatingTableInfoFrame(None, 'Open Existing Connection')
    frame.Show()
    app.MainLoop()
