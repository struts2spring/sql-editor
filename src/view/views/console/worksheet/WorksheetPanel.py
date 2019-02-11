'''
Created on 15-Dec-2016

@author: vijay
'''
import wx
import os

import wx.lib.agw.aui.auibook as aui

from src.view.constants import ID_RUN, ID_TEXTCTRL_AUTO_COMPLETE, ID_SQL_LOG
from wx import ID_SPELL_CHECK
from src.view.views.console.worksheet.EditorPanel import CreatingEditorPanel
from src.view.views.console.worksheet.ResultListPanel import CreateResultSheetTabPanel
from src.view.views.console.worksheet.WelcomePage import WelcomePanel
from src.view.views.console.worksheet.tableInfoPanel import CreatingTableInfoPanel

import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.views.database.explorer.databaseTree import DataSourceTreeNode, \
    DataSource
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
from src.view.AutoCompleteTextCtrl import TextCtrlAutoComplete
from wx.lib.pubsub import pub
from src.view.util.FileOperationsUtil import FileOperations

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

ID_executeScript = wx.NewIdRef()


class CreateWorksheetTabPanel(wx.Panel):

    def __init__(self, parent=None, *args, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.BORDER_NONE, **kw):
        wx.Panel.__init__(self, parent, id=-1, style=style)
        self.parent = parent
        path = os.path.abspath(__file__)
        tail = None
#         head, tail = os.path.split(path)
#         print('createAuiManager',head, tail )
        try:
            while tail != 'src':
                path = os.path.abspath(os.path.join(path, '..',))
                head, tail = os.path.split(path)
        except Exception as e:
            logger.error(e, exc_info=True)
        path = os.path.abspath(os.path.join(path, "images"))
        
        # Attributes
        self._nb = aui.AuiNotebook(self)
#         if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
#             imageLocation = os.path.join("..", "..", "images")
#         elif "view" == os.path.split(os.getcwd())[-1:][0]:
#             imageLocation = os.path.join("..", "images")
        imgList = wx.ImageList(16, 16)
        imgList.Add(wx.Bitmap(os.path.join(path, "sql_script.png")))
        
        self._nb.AssignImageList(imgList) 
        
        self.addTab()
#         self._nb.AddPage(worksheetPanel, "2", imageId=0)
        # Layout
        
        self.__DoLayout()

    def addTab(self, name='Start Page', worksheetPanel=None, dataSourceTreeNode=None):
        if name == 'Start Page':
            worksheetPanel = WelcomePanel(self._nb)
        elif name.startswith('tableInfo_'):
            name = name.replace('tableInfo_', '', 1)
            worksheetPanel = CreatingTableInfoPanel(self._nb, -1, style=wx.CLIP_CHILDREN | wx.BORDER_NONE, tableName=name)
        elif name.startswith('Worksheet'):
            worksheetPanel = CreatingWorksheetWithToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN | wx.BORDER_NONE , dataSourceTreeNode=dataSourceTreeNode)
#             worksheetPanel.worksheetPanel.editorPanel
            name = 'Worksheet ' + str(len(self.GetPages(type(worksheetPanel))))
        elif name.startswith('openFileLoad'):
            name = name.replace('openFileLoad', '', 1)
        self._nb.AddPage(worksheetPanel, name)
        self.SetCurrentPage(worksheetPanel)
        self.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN, self.onTabRightDown, self._nb)
        self.Bind(aui.EVT_AUINOTEBOOK_BG_DCLICK, self.onBgDoubleClick, self._nb)
#         self.Bind(aui.AUI_NB_CLOSE_BUTTON, handler, source, id, id2)

    def onBgDoubleClick(self, event):
        logger.debug('onBgDoubleClick')
        name = 'Worksheet '
        self.addTab(name)

    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        
    def SetCurrentPage(self, page):
        """
        Set the current page to the page given
        """
        n = self._nb.GetPageIndex(page)
        if n != -1:
            self._nb.SetSelection(n)
            return True
        return False    
    
    def GetCurrentPage(self):
        """
        Get the current active Page page
        """
        num = self._nb.GetSelection()
        if num == -1:
            page = None
        else:
            page = self._nb.GetPage(num)
        return page

    def GetPages(self, page_type):
        """
        Get all the Page pages of a particular type
        """
        npages = self._nb.GetPageCount()
        res = []
        for n in range(0, npages):
            page = self._nb.GetPage(n)
            if isinstance(page, page_type):
                res.append(page)
        return res        
    
    def onCloseTab(self, event=None, currentlySelectedPage=None):
        logger.debug("onCloseTab")
        logger.debug("currentlySelectedPage %s", currentlySelectedPage)
#         self._nb.RemovePage(currentlySelectedPage)
        if self._nb.DeletePage(currentlySelectedPage) :
            logger.info('page deleted')
        npages = self._nb.GetPageCount()
        logger.debug("npages {}".format(npages))

    def onCloseOthersTabs(self, event=None, currentlySelectedPage=None):
        logger.debug("onCloseOthersTab")
        logger.debug("currentlySelectedPage %s", currentlySelectedPage)
        npages = self._nb.GetPageCount()
        
        for n in range(currentlySelectedPage, npages):
            self._nb.DeletePage(currentlySelectedPage + 1)
        for n in range(0, currentlySelectedPage):
            self._nb.DeletePage(0)
        
    def onCloseLeftTabs(self, event=None, currentlySelectedPage=None):
        logger.debug("onCloseLeftTabs")
        logger.debug("currentlySelectedPage %s", currentlySelectedPage)
        for n in range(0, currentlySelectedPage):
            self._nb.DeletePage(0)
    
    def onCloseRightTabs(self, event=None, currentlySelectedPage=None):
        npages = self._nb.GetPageCount()
        
        for n in range(currentlySelectedPage, npages):
            self._nb.DeletePage(currentlySelectedPage + 1)
        logger.debug("onCloseRightTabs")
        logger.debug("currentlySelectedPage %s", currentlySelectedPage)
    
    def onCloseAllTabs(self, event):
        logger.debug("onCloseAllTabs")
#         npages = self._nb.DeleteAllPages()
        while self._nb.GetPageCount() != 0:
            self._nb.DeletePage(0)

#         GetPageCount()
#         for n in range(0, npages):
#             page = self._nb.GetPage(n)
#             page.
#     
    def onTabRightDown(self, evt=None):
        logger.debug('rightdown PopUp')
        currentlySelectedPage = self._nb.GetSelection()
        logger.debug("onTabRightDown: currentlySelectedPage %s", currentlySelectedPage)
        
        pos = self.ScreenToClient(wx.GetMousePosition())
        self.popupmenu = wx.Menu()
        popupList = [
            {'label':'Close', 'icon':wx.ART_CLOSE, "eventMethod": lambda event: self.onCloseTab(event, currentlySelectedPage)},
            {'label':'Close Others', 'icon':wx.ART_CLOSE, "eventMethod":lambda event: self.onCloseOthersTabs(event, currentlySelectedPage)},
            {'label':"Close Other tabs to the left", 'icon':wx.ART_CLOSE, "eventMethod":lambda event: self.onCloseLeftTabs(event, currentlySelectedPage)},
            {'label':'Close Other tabs to the right', 'icon':wx.ART_CLOSE, "eventMethod":lambda event: self.onCloseRightTabs(event, currentlySelectedPage)},
            {'label':'Close &All', 'icon':wx.ART_CLOSE, "eventMethod":self.onCloseAllTabs}
            ]
        for popupRow in popupList:
            itemId = wx.ID_ANY
            item = wx.MenuItem(self.popupmenu, itemId, popupRow['label'])
            item.SetBitmap(wx.ArtProvider.GetBitmap(popupRow['icon'], wx.ART_MENU, (16, 16)))
            self.popupmenu.Append(item)
            self.Bind(wx.EVT_MENU, popupRow['eventMethod'], item)
#             deleteMenuItem = wx.MenuItem(menu, wx.ID_DELETE, "Delete \t Delete")
#             delBmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
#             deleteMenuItem.SetBitmap(delBmp)
#             delMenu = menu.AppendItem(deleteMenuItem)
# #             self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
#             
#             
#             self.Bind(wx.EVT_MENU, self.onOpenSqlEditorTab, item3)
            
        self.PopupMenu(self.popupmenu, pos)
#         tab = event.GetEventObject()
#         num = tab.GetActivePage()
#         conpage = tab.GetWindowFromIdx(num)
#         menu = conpage.GetPageMenu()
#         date = DateControlPop(self, -1, pos = (30,30))
#         self.PopupMenu(menu)
#         menu.Destroy()
        
#         self.popmenu=None
#         if self.popmenu:
#             self.popmenu.Destroy()
#             self.popmenu = None
#         fileMenu = wx.Menu()   
#         imp = wx.Menu()
#         imp.Append(wx.ID_ANY, 'Import newsfeed list...') 
#         fileMenu.AppendMenu(wx.ID_ANY, 'I&mport', imp)
#         self.popmenu.Append(fileMenu)
#         self.PopupMenu(self.popmenu, event.GetPosition())


#         sizer.Fit(self)
class CreatingStartPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        worksheetToolbar = self.constructWorksheetToolBar()
        worksheetPanel = CreatingWorksheetPanel(self)
        self.bindingEvent()
        ####################################################################
        vBox.Add(worksheetToolbar , 0, wx.EXPAND | wx.ALL, 0)
        vBox.Add(worksheetPanel , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)   


class CreatingWorksheetWithToolbarPanel(wx.Panel):

    def __init__(self, parent, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        dataSourceTreeNode = kw['dataSourceTreeNode']
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.fileOperations = FileOperations()
        ####################################################################
        worksheetToolbar = self.constructWorksheetToolBar()
        self.worksheetPanel = CreatingWorksheetPanel(self)
        self.worksheetPanel.setResultData()
        self.bindingEvent()
        ####################################################################
        hBox11 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(worksheetToolbar, 1, wx.ALIGN_RIGHT, 0)
        hBox2.Add(self.createDropdownToolbar(dataSourceTreeNode=dataSourceTreeNode), 0, wx.ALIGN_LEFT , 0)
        hBox11.Add(hBox1 , 1, wx.ALIGN_RIGHT, 0)
        hBox11.Add(hBox2 , 0, wx.ALIGN_LEFT, 0)
        ####################################################################
        vBox.Add(hBox11 , 0, wx.EXPAND | wx.ALL, 0)
        vBox.Add(self.worksheetPanel , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
    
    def createDropdownToolbar(self, dataSourceTreeNode=None):
        tb2 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb2.SetToolBitmapSize(wx.Size(16, 16))
        self.dynamic_choices = list()
        sqlExecuter = SQLExecuter()
        dbList = sqlExecuter.getListDatabase()  
        for db in dbList:
            self.dynamic_choices.append(db[1])
           
        self._ctrl = TextCtrlAutoComplete(tb2, id=ID_TEXTCTRL_AUTO_COMPLETE, size=(250, 20), choices=self.dynamic_choices)
#         self._ctrl.SetSize((250, 15))
        self._ctrl.SetChoices(self.dynamic_choices)
        self._ctrl.SetEntryCallback(self.dynamic_choices)
#         self._ctrl.SetMatchFunction('_opal')
        if dataSourceTreeNode:
            self._ctrl.SetValue(dataSourceTreeNode.dataSource.connectionName)
        tb2.AddControl(self._ctrl)
        tb2.Realize() 
        return tb2
    
    def constructWorksheetToolBar(self):
        logger.debug("constructWorksheetToolBar")
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))

        tb1.AddTool(ID_RUN, "Run", self.fileOperations.getImageBitmap("webinar.png"), shortHelp="Run   (Ctrl+Enter)") 
        tb1.AddTool(ID_executeScript, "Run Script  F9", self.fileOperations.getImageBitmap("sql_script_exec.png"), shortHelp="Run Script  F9")
        tb1.AddSeparator()
        tb1.AddTool(ID_SPELL_CHECK, "Spelling check", self.fileOperations.getImageBitmap("abc.png"), shortHelp="Spelling check")
        
        tb1.AddTool(ID_SQL_LOG, "Sql history", self.fileOperations.getImageBitmap("sql.png"), shortHelp="Sql history")
        
        tb1.Realize()
        
        return tb1     
    
    def onSpellCheck(self, event):
        logger.debug('onSpellCheck')

    def onSqlLog(self, event):
        logger.debug('onSqlLog')
        pub.sendMessage('sqlLogView', event=event)      
        
    def bindingEvent(self):
        self.Bind(wx.EVT_MENU, self.executeSQL, id=ID_RUN)
        self.Bind(wx.EVT_MENU, self.onSpellCheck, id=ID_SPELL_CHECK)
        self.Bind(wx.EVT_MENU, self.onSqlLog, id=ID_SQL_LOG)

    def executeSQL(self, event):
        logger.debug('CreatingWorksheetWithToolbarPanel.executeSQL')
        self.GetTopLevelParent()
#         x=self.GetParent()
        creatingEditorPanel = self.GetChildren()[1].splitter.Children[0]
        creatingEditorPanel.sstc.executeSQL()
        resultPanel = self.GetChildren()[1].splitter.Children[1]
#         resultPanel.createDataViewCtrl(data=music,headerList=["Artist","Title","Genre"])
#         resultPanel.setModel(music)
#         resultPanel.Layout()

    
class CreatingWorksheetPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        
#         self._nb = wx.Notebook(self)
        
        ####################################################################
        self.data = dict()
#         worksheetToolbar = self.constructWorksheetToolBar()
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D)
#         splitter = MultiSplitterWindow(self, id=-1, style=wx.SP_LIVE_UPDATE)
        self.splitter = splitter
        self.editorPanel = CreatingEditorPanel(splitter)
#         self.resultPanel = ResultPanel(splitter, data=self.getData())
#         self.resultPanel = CreatingResultWithToolbarPanel(splitter)
        self.resultPanel = CreateResultSheetTabPanel(splitter)
#         self.resultPanel = CreatingResultWithToolbarPanel(splitter)
        splitter.SetMinimumPaneSize(20)
        splitter.SplitHorizontally(self.editorPanel, self.resultPanel)
#         splitter.AppendWindow(self.editorPanel)
#         splitter.AppendWindow(self.resultPanel)
#         splitter.SetOrientation(wx.VERTICAL)
#         splitter.SizeWindows()  
        
#         editorPanel = CreatingEditorPanel(self)
        ####################################################################
        vBox.Add(splitter , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(editorPanel , 1, wx.EXPAND | wx.ALL)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
    def SetOrientation(self, value):
        if value:
            self.splitter.SetOrientation(wx.VERTICAL)
        else:
            self.splitter.SetOrientation(wx.HORIZONTAL)
        self.splitter.SizeWindows()        
    
    def setResultData(self, data=None):
        if data:
            logger.debug('setResultData count: %s', len(data.keys()))
            self.data = data
#             self.data = music
            self.resultPanel.Layout()

    def getData(self):
        # Get the data from the ListCtrl sample to play with, converting it
        # from a dictionary to a list of lists, including the dictionary key
        # as the first element of each sublist.
#         self.data=music
        return self.data

    
    #---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    dataSource = DataSource(connectionName='employee_9_jan_2019', filePath=r'C:\Users\xbbntni\eclipse-workspace2\pyTrack\src\employee.sqlite')
    dataSourceTreeNode = DataSourceTreeNode(depth=0, dataSource=dataSource, nodeLabel=None, imageName=None, children=None)
    panel = CreateWorksheetTabPanel(frame)
    panel.addTab(name='Worksheet', dataSourceTreeNode=dataSourceTreeNode)
#     panel.addTab("123")
    frame.Show()
    app.MainLoop()
