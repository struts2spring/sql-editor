import logging.config
import wx

from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
from src.view.AutoCompleteTextCtrl import TextCtrlAutoComplete
from src.view.TreePanel import CreatingTreePanel
from src.view.constants import LOG_SETTINGS, ID_newConnection, ID_openConnection, \
    ID_newWorksheet, ID_SAVE, ID_SAVE_ALL, ID_NEW, ID_TERMINAL

from wx.lib.agw.aui.aui_constants import actionDragFloatingPane, AUI_DOCK_NONE
from src.view.views.file.explorer.FileBrowserPanel import FileBrowser
from src.view.views.console.SqlOutputPanel import SqlConsoleOutputPanel
from src.view.views.console.worksheet.WorksheetPanel import CreateWorksheetTabPanel, \
    CreatingWorksheetWithToolbarPanel
from src.view.views.sql.history.HistoryListPanel import HistoryGrid
from src.view.views.console.worksheet.WelcomePage import WelcomePanel
from wx.lib.agw.aui.framemanager import NonePaneInfo
from src.view.util.FileOperationsUtil import FileOperations
from wx.lib.platebtn import PlateButton, PB_STYLE_DEFAULT, PB_STYLE_DROPARROW

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD
############################################################


class MyAuiManager(aui.AuiManager):
    
    def addTabByWindow(self, window=None , imageName="script.png", captionName=None, tabDirection=5):
        '''
        This method always create a new tab for the window.
        tabDirection=5 is the center 
        '''
        self.SetAutoNotebookStyle(aui.AUI_NB_DEFAULT_STYLE | wx.BORDER_NONE)
        for pane in self.GetAllPanes():
            logger.debug(pane.dock_direction_get())
            auiPanInfo = aui.AuiPaneInfo().Icon(FileOperations().getImageBitmap(imageName=imageName)).\
                Name(captionName).Caption(captionName).LeftDockable(True).Direction(wx.TOP).\
                Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True).CaptionVisible(visible=True)
            if pane.dock_direction_get() == tabDirection:  # adding to center tab
                targetTab = pane
                if not pane.HasNotebook():
                    self.CreateNotebookBase(self._panes, pane)
#                 targetTab.NotebookPage(pane.notebook_id)
                    self.AddPane(window, auiPanInfo, target=targetTab)
#                 self._mgr._notebooks
#                 self._mgr.ActivatePane(targetTab.window)
                else:
                    self.AddPane(window, auiPanInfo, target=targetTab)
                break
        self.Update()

    def OnTabBeginDrag(self, event):
        """
        Handles the ``EVT_AUINOTEBOOK_BEGIN_DRAG`` event.

        :param `event`: a :class:`~wx.lib.agw.aui.auibook.AuiNotebookEvent` event to be processed.
        """

        if self._masterManager:
            self._masterManager.OnTabBeginDrag(event)

        else:
            paneInfo = self.PaneFromTabEvent(event)

            if paneInfo.IsOk():

                # It's one of ours!
                self._action = actionDragFloatingPane
                mouse = wx.GetMousePosition()

                # set initial float position - may have to think about this
                # offset a bit more later ...
                self._action_offset = wx.Point(20, 10)
                self._toolbar_action_offset = wx.Point(20, 10)

                paneInfo.floating_pos = mouse - self._action_offset
                paneInfo.dock_pos = AUI_DOCK_NONE
                paneInfo.notebook_id = -1

                tab = event.GetEventObject()

                try:
                    if tab.HasCapture():
                        
                        tab.ReleaseMouse()
                except:
                    pass

                # float the window
                if paneInfo.IsMaximized():
                    self.RestorePane(paneInfo)
                paneInfo.Float()

                # The call to Update may result in
                # the notebook that generated this
                # event being deleted, so we have
                # to do the call asynchronously.
                wx.CallAfter(self.Update)

                self._action_window = paneInfo.window

                self._frame.CaptureMouse()
                event.SetDispatched(True)

            else:

                # not our window
                event.Skip()

    def GetPaneByHavingName(self, name):
        """
        This version of :meth:`GetPane` looks up a pane based on a 'pane name'.

        :param string `name`: the pane name.

        :see: :meth:`GetPane`
        """

        for p in self._panes:
            if p.name in name:
                return p

        return NonePaneInfo


class PerspectiveManager(object):
    """Creates a perspective manager for the given aui managed window.
    It supports saving and loading of on disk perspectives as created by
    calling SavePerspective from the AuiManager. Mixin class for a wx.Frame.

    """

    def __init__(self, base=None):
        """Initializes the perspective manager. The auimgr parameter is
        a reference to the windows AuiManager instance, base is the base
        path to where perspectives should be loaded from and saved to.
        @param base: path to configuration cache

        """
        super(PerspectiveManager, self).__init__()

        self.createAuiManager()
        
    def createAuiManager(self):
        logger.debug('createAuiManager')
        # tell FrameManager to manage this frame
        self._mgr = MyAuiManager()
        self._mgr.SetManagedWindow(self)
        # set up default notebook style
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | wx.BORDER_NONE
        self._notebook_theme = 1      
        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))    
        self._perspectives = []
        
        # add a bunch of panes
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("test1").Caption("Pane Caption").Top().CloseButton(True).MaximizeButton(True))
                # add the toolbars to the manager
        
#         topToolBar = wx.BoxSizer(wx.HORIZONTAL)
#         topToolBar.Add(self.constructToolBar(),1,wx.ALIGN_LEFT,4) # note the 2nd param 'proportion' is 1
#         #topToolBar.AddStretchSpacer()
#         topToolBar.Add(self.constructToolBar(),0,wx.ALIGN_RIGHT,4)
        
        self._mgr.AddPane(self.constructViewToolBar(), aui.AuiPaneInfo().
                          Name("viewToolbar").Caption("View Toolbar").
                          ToolbarPane().Top().Row(1).Position(1).CloseButton(True).
                          LeftDockable(False).RightDockable(False).Gripper(True))    
        self._mgr.AddPane(self.constructPerspectiveToolBar(), aui.AuiPaneInfo().
                          Name("perspectiveToolbar").Caption("Perspective Toolbar").
                          ToolbarPane().Top().Row(1).Position(2).CloseButton(True).
                          LeftDockable(False).RightDockable(False).Gripper(True))    
        
        self._mgr.AddPane(self.creatingFileExplorer(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="file_explorer.png")).BestSize(500, -1).
                          Name("fileExplorer").Caption("File Explorer").Dockable(True).Movable(True).MinSize(500, -1).Resizable(True).
                          Left().Layer(1).Position(2).CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        
        self._mgr.AddPane(self.creatingTreeCtrl(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="folder_database.png")).BestSize(500, -1).
                          Name("databaseNaviagor").Caption("Database Navigator").Dockable(True).Movable(True).MinSize(500, -1).
                          Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).MinimizeButton(True), target=self._mgr.GetPane("fileExplorer"))
        
        self._mgr.AddPane(WelcomePanel(self), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="welcome16.png")).BestSize(500, -1).
                          Name("onWelcome").Caption("Welcome").Dockable(True).Movable(True).MinSize(500, -1).CaptionVisible(visible=True).Direction(wx.TOP).
                          Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True))  
        self._mgr.AddPane(self.constructCenterPane(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="script.png")).
                          Name("centerPane").Caption("Center Pane").LeftDockable(True).Direction(wx.TOP).
                          Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True).CaptionVisible(visible=True), target=self._mgr.GetPane("onWelcome"))
        self._mgr.AddPane(self.getWorksheet(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="script.png")).
                          Name("Worksheet-0").Caption("Worksheet-0").LeftDockable(True).Direction(wx.TOP).
                          Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True).CaptionVisible(visible=True), target=self._mgr.GetPane("onWelcome"))
        
#         self._mgr.AddPane(self.constructSchemaViewerPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "script.png"))).
#                           Name("schemaViewer").Caption("Schema Viewer").LeftDockable(True).
#                           Center().CloseButton(True).MaximizeButton(True).MinimizeButton(True))      
#         self._mgr.AddPane(self.constructSchemaViewerPane(), aui.AuiPaneInfo().
#                           Name("test9").Caption("Min Size 200x100").
#                           BestSize(wx.Size(200, 100)).MinSize(wx.Size(200, 100)).
#                           Bottom().Layer(1).CloseButton(True).MaximizeButton(True))      
  
        self._mgr.AddPane(self.sqlConsoleOutputPane(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="console_view.png")).
                          Name("consoleOutput").Caption("Console").Dockable(True).Movable(True).LeftDockable(True).BestSize(wx.Size(500, 400)).MinSize(wx.Size(500, 400)).
                          Bottom().Layer(0).Row(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True).PinButton(visible=True).GripperTop())
            
        self._mgr.AddPane(self.constructHistoryPane(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="sql.png")).
                          Name("sqlLog").Caption("SQL Log").Dockable(True).BestSize(wx.Size(500, 400)).MinSize(wx.Size(500, 400)).
                          Bottom().Layer(0).Row(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True), target=self._mgr.GetPane("consoleOutput"))
        
        self._mgr.GetPane("onWelcome").Show()
        
        self._mgr.GetPane("viewToolbar").Show()
        self._mgr.GetPane("perspectiveToolbar").Show()
        self.perspective_default = self._mgr.SavePerspective()
        perspective_all = self._mgr.SavePerspective()
        self.setStyleToPanes()
        all_panes = self._mgr.GetAllPanes()
        # "commit" all changes made to FrameManager
        self._mgr.Update()  
        
        # some more event
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, self.OnAllowNotebookDnD)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)

        self.Bind(aui.EVT_AUI_PANE_FLOATING, self.OnFloatDock)
        self.Bind(aui.EVT_AUI_PANE_FLOATED, self.OnFloatDock)
        self.Bind(aui.EVT_AUI_PANE_DOCKING, self.OnFloatDock)
        self.Bind(aui.EVT_AUI_PANE_DOCKED, self.OnFloatDock)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        
#######################################################################################    

    def OnPaneClose(self, event):
        logger.debug("OnPaneClose")
#         if event.pane.name == "test10":

#         msg = "Are you sure you want to "
#         if event.GetEventType() == aui.wxEVT_AUI_PANE_MINIMIZE:
#             msg += "minimize "
#         else:
#             msg += "close/hide "
# 
#         res = wx.MessageBox(msg + "this pane?", "AUI", wx.YES_NO, self)
#         if res != wx.YES:
#             event.Veto()

    def OnAllowNotebookDnD(self, event):

        # for the purpose of this test application, explicitly
        # allow all noteboko drag and drop events
        event.Allow()

    def OnNotebookPageClose(self, event):
        logger.debug("OnNotebookPageClose")
        ctrl = event.GetEventObject()

#         if isinstance(ctrl.GetPage(event.GetSelection()), wx.html.HtmlWindow):
# 
#             res = wx.MessageBox("Are you sure you want to close/hide this notebook page?",
#                                 "AUI", wx.YES_NO, self)
#             if res != wx.YES:
#                 event.Veto()
    def OnFloatDock(self, event):

        paneLabel = event.pane.caption
        etype = event.GetEventType()

        strs = "Pane %s " % paneLabel
        if etype == aui.wxEVT_AUI_PANE_FLOATING:
            strs += "is about to be floated"

            if event.pane.name == "test8" and self._veto_tree:
                event.Veto()
                strs += "... Event vetoed by user selection!"
                logger.debug(strs)
                return

        elif etype == aui.wxEVT_AUI_PANE_FLOATED:
            strs += "has been floated"
        elif etype == aui.wxEVT_AUI_PANE_DOCKING:
            strs += "is about to be docked"

            if event.pane.name == "test11" and self._veto_text:
                event.Veto()
                strs += "... Event vetoed by user selection!"
                logger.debug(strs)
                return

        elif etype == aui.wxEVT_AUI_PANE_DOCKED:
            strs += "has been docked"

        logger.debug(strs)

    def __del__(self):

        self.timer.Stop()

    def OnClose(self, event):

        self.timer.Stop()
        self._mgr.UnInit()
        event.Skip()

    def TimerHandler(self, event):

        try:
            self.gauge.Pulse()
        except:
            self.timer.Stop()

#######################################################################################    
    def setStyleToPanes(self):
        all_panes = self._mgr.GetAllPanes()

        for pane in all_panes:

            if isinstance(pane.window, aui.AuiNotebook):
                nb = pane.window       
                nb.SetAGWWindowStyleFlag(self._notebook_style) 
                nb.SetArtProvider(aui.ChromeTabArt())
                nb.Refresh()
                nb.Update()

    def constructPerspectiveToolBar(self):
        tb1 = aui.AuiToolBar(self, -1, agwStyle=aui.AUI_TB_DEFAULT_STYLE | wx.NO_BORDER)
        tb1.AddSimpleTool(ID_NEW, "Open Perspective", self.fileOperations.getImageBitmap(imageName='new_persp.png'), short_help_string='Open Perspective')
        tb1.AddSeparator()
        tb1.AddSimpleTool(ID_NEW, "Java", self.fileOperations.getImageBitmap(imageName='jperspective.png'), short_help_string='Java')
        tb1.AddSimpleTool(ID_NEW, "Java EE", self.fileOperations.getImageBitmap(imageName='javaee_perspective.png'), short_help_string='Java EE')
        tb1.AddSimpleTool(ID_NEW, "Debug", self.fileOperations.getImageBitmap(imageName='debug_persp.png'), short_help_string='Debug')
        tb1.AddSimpleTool(ID_NEW, "Python", self.fileOperations.getImageBitmap(imageName='python_perspective.png'), short_help_string='Python')
        tb1.AddSimpleTool(ID_NEW, "Git", self.fileOperations.getImageBitmap(imageName='gitrepository.png'), short_help_string='Git')
        return tb1

    def constructViewToolBar(self):
        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, agwStyle=aui.AUI_TB_DEFAULT_STYLE | wx.NO_BORDER)
        
#         tb1.SetToolBitmapSize(wx.Size(42, 42))
#         tb1.AddSimpleTool(tool_id=ID_newConnection, label="New Connection", bitmap=wx.Bitmap(self.fileOperations.getImageBitmap(imageName="connect.png")), short_help_string='Create a new connection')
#         tb1.AddSeparator()
        
#         :TODO:FIXnew_con
#         tb4_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        tb4_bmp1 = self.fileOperations.getImageBitmap(imageName='new_con.png')
        tb1.AddSimpleTool(ID_NEW, "Item 1", tb4_bmp1, short_help_string='New')
        tb1.SetToolDropDown(ID_NEW, True)
        tb1.AddSeparator()
        
        tools = [
            (ID_SAVE, "Save (Ctrl+S)", "save.png", 'Save (Ctrl+S)'),
            (ID_SAVE_ALL, "Save All (Ctrl+Shift+S)", "saveall_edit.png", 'Save All (Ctrl+Shift+S)'),
            (),
            (ID_TERMINAL, "Open a Terminal", "linux_terminal.png", "Open a Terminal (Ctrl+Shift+Alt+T)"),
            (),
            (ID_newConnection, "New Connection", "connect.png", "New Connection"),
            (ID_openConnection, "Open Connection", "database_connect.png", 'Open Connection'),
            (ID_newWorksheet, "Script", "script.png", 'Open a new script worksheet'),
            (wx.ID_PREFERENCES, "Preferences", "preference.png", 'Preference'),
            ]
        for tool in tools:
            if len(tool) == 0:
                tb1.AddSeparator()
            else:
                tb1.AddSimpleTool(tool[0], tool[1], self.fileOperations.getImageBitmap(imageName=tool[2]), short_help_string=tool[3])
            
#         tb1.AddSimpleTool(ID_openConnection, "Open Connection", wx.Bitmap(self.fileOperations.getImageBitmap(imageName="database_connect.png")), short_help_string='Open Connection')
#         tb1.AddSimpleTool(ID_newWorksheet, "Script", wx.Bitmap(self.fileOperations.getImageBitmap(imageName="script.png")), short_help_string='Open a new script worksheet')
#         tb1.AddSimpleTool(wx.ID_PREFERENCES, "Preferences", wx.Bitmap(self.fileOperations.getImageBitmap(imageName="preference.png")), short_help_string='Preference')
#         tb1.DoGetBestSize()
        ###################################################################################################
        args = {}
        if True:
            args["colNames"] = ("col1", "col2")
            args["multiChoices"] = [ ("Zoey", "WOW"), ("Alpha", "wxPython"),
                                    ("Ceda", "Is"), ("Beta", "fantastic"),
                                    ("zoebob", "!!")]
            args["colFetch"] = 1
        else:
            args["choices"] = ["123", "cs", "cds", "Bob", "Marley", "Alpha"]
        args["selectCallback"] = self.selectCallback   
        self.dynamic_choices = list()
        sqlExecuter = SQLExecuter()
        dbList = sqlExecuter.getListDatabase()  
        for db in dbList:
            self.dynamic_choices.append(db[1])
           
#         self.dynamic_choices = [
#                 'aardvark', 'abandon', 'acorn', 'acute', 'adore',
#                 'aegis', 'ascertain', 'asteroid',
#                 'beautiful', 'bold', 'classic',
#                 'daring', 'dazzling', 'debonair', 'definitive',
#                 'effective', 'elegant',
#                 'http://python.org', 'http://www.google.com',
#                 'fabulous', 'fantastic', 'friendly', 'forgiving', 'feature',
#                 'sage', 'scarlet', 'scenic', 'seaside', 'showpiece', 'spiffy',
#                 'www.wxPython.org', 'www.osafoundation.org'
#                 ]

        self._ctrl = TextCtrlAutoComplete(tb1, **args)
        self._ctrl.SetSize((250, 25))
        self._ctrl.SetChoices(self.dynamic_choices)
        self._ctrl.SetEntryCallback(self.setDynamicChoices)
        self._ctrl.SetMatchFunction(self.match)
        tb1.AddControl(self._ctrl) 

        ###################################################################################################
#         tb1.AddControl( self.choice ) 
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
#         tb1.AddLabelTool(103, "Test"t1 = wx.TextCtrl(self, -1, "Test it out and see", size=(125, -1)), wx.ArtProvider_GetBitmap(wx.ART_WARNING))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        tb1.Realize()
        self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.onNewDropDown, id=ID_NEW)
        return tb1
        
    def onNewDropDown(self, event):

        if event.IsDropDownClicked():

            tb = event.GetEventObject()
            tb.SetToolSticky(event.GetId(), True)

            # create the popup menu
            # menuPopup = wx.Menu()
            menuPopup = self.createMenuByPerspective(perspectiveName='java')
            # bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))

            # javaProjectMenu =  wx.MenuItem(menuPopup, 10001, "Java Project")
            # javaProjectMenu.SetBitmap(bmp)
            # menuPopup.Append(javaProjectMenu)

            # project =  wx.MenuItem(menuPopup, 10002, "Project...")
            # project.SetBitmap(bmp)
            # menuPopup.Append(project)

            # javaPackage =  wx.MenuItem(menuPopup, 10003, "Package")
            # javaPackage.SetBitmap(bmp)
            # menuPopup.Append(javaPackage)

            # javaClass =  wx.MenuItem(menuPopup, 10004, "Class")
            # javaClass.SetBitmap(bmp)
            # menuPopup.Append(javaClass)

            # line up our menu with the button
            rect = tb.GetToolRect(event.GetId())
            pt = tb.ClientToScreen(rect.GetBottomLeft())
            pt = self.ScreenToClient(pt)

            self.PopupMenu(menuPopup, pt)

            # make sure the button is "un-stuck"
            tb.SetToolSticky(event.GetId(), False)    

    def createMenuByPerspective(self, perspectiveName='java'):
        menuItemList = {"java": [
                [10001, 'Java Project', None, None],
                [10002, 'Project...', "project.png", None],
                [],
                [10003, 'Package', None, None],
                [10004, 'Class', 'class_obj.png', None],
                [10005, 'Interface', 'int_obj.png', None],
                [10006, 'Enum', 'enum_obj.png', None],
                [10007, 'Annotation', 'annotation_obj.png', None],
                [10008, 'Source Folder', None, None],
                [10009, 'Java Working Set', None, None],
                [10010, 'Folder', None, None],
                [10011, 'File', None, None],

                ],
            "Python": [
                [20001, 'Python Project', None, None],
                [20002, 'Project...', "project.png", None],
                [],
                [20003, 'Source Folder', "packagefolder_obj.png", None],
                [20004, 'Python Project', "package_obj.png", None],
                [20005, 'Python Module', "project.png", None],
                [20006, 'Folder', "project.png", None],
                [20007, 'File', "file_obj.png", None],
                [],
                [20008, 'Other', "project.png", None],
                ],
            "Resource": [[30001, 'Database Project', None, None], ],
            "Debug": [[30001, 'Database Project', None, None], ],
            "database": [
                [30001, 'Database Project', None, None],
                [30001, 'Database Connection', None, None],
                [30001, 'ER Diagram', None, None],
                ]
            }
            
        menuPopup = wx.Menu()
        bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))
        for menuItemName in menuItemList[perspectiveName]:
            if len(menuItemName) > 1:
                menuItem = wx.MenuItem(menuPopup, menuItemName[0], menuItemName[1])
                if menuItemName[2]:
                    menuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=menuItemName[2]))
                menuPopup.Append(menuItem)
            else:
                menuPopup.AppendSeparator()
        return menuPopup

    def creatingFileExplorer(self):
        
        fileBrowserPanel = FileBrowser(self, size=(500, 300))
        return fileBrowserPanel
    
    def creatingTreeCtrl(self):
        # Create a TreeCtrl
        treePanel = CreatingTreePanel(self)

        return treePanel
    
    def getWorksheet(self):
        worksheetPanel = CreatingWorksheetWithToolbarPanel(self, -1, style=wx.CLIP_CHILDREN | wx.BORDER_NONE)
        return worksheetPanel
    
    def constructCenterPane(self):
        worksheet = CreateWorksheetTabPanel(self)      
#         worksheet.addTab('Start Page')
        return worksheet
    
    def sqlConsoleOutputPane(self):
        sqlConsoleOutputPanel = SqlConsoleOutputPanel(self)
        return sqlConsoleOutputPanel
    
    def constructHistoryPane(self):
        historyGrid = HistoryGrid(self)
        return historyGrid
    
    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition,
                              wx.Size(width, height), self._mgr)
        return ctrl
        
        
class SizeReportCtrl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, mgr=None):

        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER)

        self._mgr = mgr

#         self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnPaint(self, event):

        dc = wx.PaintDC(self)

        size = self.GetClientSize()
        s = ("Size: %d x %d") % (size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height = height + 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2))

        if self._mgr:

            pi = self._mgr.GetPane(self)

            s = ("Layer: %d") % pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 1))

            s = ("Dock: %d Row: %d") % (pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 2))

            s = ("Position: %d") % pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 3))

            s = ("Proportion: %d") % pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 4))

    def OnEraseBackground(self, event):
        # intentionally empty
        pass

    def OnSize(self, event):
        self.Refresh()
        event.Skip()
