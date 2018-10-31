import wx

import wx.lib.agw.aui.auibook as aui
import os
from src.view.constants import ID_RUN, ID_EXECUTE_SCRIPT, LOG_SETTINGS
from src.view.worksheet.ResultListPanel import ResultPanel
import logging.config
from src.view.util.FileOperationsUtil import FileOperations

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
        self.parent = parent
        
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
        name='Columns '
        
        # add following list of tabs
        listOfTabs=['Columns', 'Indexes', 'Data', 'References', 'Triggers', 'SQL', 'ER diagram']
        for tabName in listOfTabs:
            tableInfoPanel = CreatingTableInfoToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN)
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
    def onTabRightDown(self,event):
        logger.info('onTabRightDown')
        
    def onBgDoubleClick(self,event):
        logger.info('onBgDoubleClick')
        
    def onCloseClick(self,event):
        logger.info('onCloseClick')
        self.GetCurrentPage()        
        
class CreatingTableInfoToolbarPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.data=list()
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        self.topResultToolbar = self.constructTopResultToolBar()
        self.bottomResultToolbar=wx.StatusBar(self)
        self.resultPanel = ResultPanel(self, data=None)
        self.bottomResultToolbar.SetStatusText("some text")
#         self.bottomResultToolbar = self.constructBottomResultToolBar()
#         self.resultPanel = ResultDataGrid(self, data=self.getData())
#         bottomResultToolbar = self.constructBottomResultToolBar()
        
        ####################################################################
        vBox.Add(self.topResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(self.resultPanel , 1, wx.EXPAND | wx.ALL, 0)
        vBox.Add(self.resultPanel , 1, wx.EXPAND | wx.ALL)
        vBox.Add(self.bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
        
    def constructTopResultToolBar(self):
        
        fileOperations=FileOperations()
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))

        tb1.AddTool(ID_RUN, "Pin", fileOperations.getImageBitmap(imageName="pin2_green.png"))
        tb1.AddTool(ID_EXECUTE_SCRIPT, "Result refresh",  fileOperations.getImageBitmap(imageName="resultset_refresh.png"))
        tb1.AddSeparator()

        tb1.Realize()
        
        return tb1     
if __name__ == '__main__':
    
    app = wx.App(False)
    frame = CreatingTableInfoFrame(None, 'Open Existing Connection')
    frame.Show()
    app.MainLoop()
