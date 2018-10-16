'''
Created on 15-Dec-2016

@author: vijay
'''
import wx
from src.view.worksheet.EditorPanel import CreatingEditorPanel
from src.view.worksheet.ResultListPanel import CreateResultSheetTabPanel
import os

import wx.lib.agw.aui.auibook as aui

from src.view.constants import ID_RUN
from wx import ID_SPELL_CHECK
import logging
from src.view.worksheet.WelcomePage import WelcomePanel

logger = logging.getLogger('extensive')



ID_executeScript = wx.NewId()

class CreateWorksheetTabPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
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

    def addTab(self, name='Start Page'):
        if name == 'Start Page':
            worksheetPanel=WelcomePanel(self._nb)
        else:
            worksheetPanel = CreatingWorksheetWithToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN)
#             worksheetPanel.worksheetPanel.editorPanel
            name = 'Worksheet ' + str(len(self.GetPages(type(worksheetPanel))))
        self._nb.AddPage(worksheetPanel, name)
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
            self._nb.DeletePage(currentlySelectedPage+1)
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
            self._nb.DeletePage(currentlySelectedPage+1)
        logger.debug("onCloseRightTabs")
        logger.debug("currentlySelectedPage %s", currentlySelectedPage)
    
    def onCloseAllTabs(self, event):
        logger.debug("onCloseAllTabs")
        npages = self._nb.DeleteAllPages()
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
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        worksheetToolbar = self.constructWorksheetToolBar()
        self.worksheetPanel = CreatingWorksheetPanel(self)
        self.worksheetPanel.setResultData()
        self.bindingEvent()
        ####################################################################
        vBox.Add(worksheetToolbar , 0, wx.EXPAND | wx.ALL, 0)
        vBox.Add(self.worksheetPanel , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
        
    def constructWorksheetToolBar(self):
        logger.debug("constructWorksheetToolBar")
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
                
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))
#         playImage = None
#         if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
#             imageLocation = os.path.join("..", "..", "images")
# #             playImage=wx.Bitmap(os.path.join("..","..", "images", "play.png"))
#         elif "view" == os.path.split(os.getcwd())[-1:][0]:
#             imageLocation = os.path.join("..", "images")
#             playImage=wx.Bitmap(os.path.join("..", "images", "play.png"))
            
#         playImage=wx.Bitmap(os.path.join(imageLocation, "sql_exec.png"))
        tb1.AddTool(ID_RUN, "Run F5",wx.Bitmap(os.path.join(path, "triangle_green.png"))) 
        tb1.AddTool(ID_executeScript, "Run Script  F9", bitmap=wx.Bitmap(os.path.join(path, "sql_script_exec.png")))
        tb1.AddSeparator()
        tb1.AddTool(ID_SPELL_CHECK, "Spelling check", wx.Bitmap(os.path.join(path, "abc.png")))
        self.Bind(wx.EVT_MENU, self.executeSQL, id=ID_RUN)
#         tb1.AddLabelTool(id=ID_openConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
#         tb1.AddLabelTool(id=ID_newConnection, label="Open Connection", shortHelp="Open Connection", bitmap=wx.Bitmap(os.path.join("..", "images", "open.png")))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_WARNING))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()
        
        return tb1     
    
    def bindingEvent(self):
        self.Bind(wx.EVT_MENU, self.executeSQL, id=ID_RUN)
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
    panel = CreateWorksheetTabPanel(frame)
    panel.addTab()
    panel.addTab("123")
    frame.Show()
    app.MainLoop()
