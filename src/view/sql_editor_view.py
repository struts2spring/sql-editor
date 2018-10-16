import logging
import wx
import os
from src.view.TreePanel import CreatingTreePanel
from src.view.constants import ID_openConnection, ID_newWorksheet, ID_newConnection, \
    ID_SQL_EXECUTION, ID_SQL_LOG, ID_UPDATE_CHECK, TITLE, VERSION
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
# from src.view.AutoCompleteTextCtrl import TextCtrlAutoComplete
from wx import aui, ID_PREFERENCES
from src.view.worksheet.WorksheetPanel import CreateWorksheetTabPanel
from src.view.SqlOutputPanel import SqlScriptOutputPanel
from src.view.history.HistoryListPanel import HistoryGrid
from src.view.connection.NewConnectionWizard import CreateNewConncetionWixard
import platform
import sys
from src.view.preference.OpalPreferences import OpalPreference
from src.view.AutoCompleteTextCtrl import TextCtrlAutoComplete

logger = logging.getLogger('extensive')


class DatabaseMainFrame(wx.Frame):

    def __init__(self, parent):
        logger.info("This is from Runner ")
        title = TITLE
        style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style)
        logger.info('1----------------------->' + os.getcwd())
        path = os.path.abspath(__file__)
        tail = None
        while tail != 'src':
            path = os.path.abspath(os.path.join(path, '..'))
            head, tail = os.path.split(path)
            
        imageLocation = os.path.join(path, "images")
        image = wx.Image(os.path.join(imageLocation, "Opal_database.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.Icon()
        icon.CopyFromBitmap(image)
        
        self.SetIcon(icon)
        self.SetMinSize(wx.Size(400, 300))
        self.createMenuBar()
        self.createStatusBar()
#         self.creatingTreeCtrl()
        
        try:
            self.createAuiManager()
        except Exception as e:
            logger.error(e, exc_info=True)
        self.bindingEvent()
        self._mgr.Update()  

    def creatingTreeCtrl(self):
        # Create a TreeCtrl
        treePanel = CreatingTreePanel(self)

        return treePanel
    #---------------------------------------------    
         
    def constructToolBar(self):
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
        logger.debug(path)
        path = os.path.abspath(os.path.join(path, "images"))
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize)
        tb1.SetToolBitmapSize(wx.Size(16, 16))
        tb1.AddTool(ID_newConnection, "New Connection", wx.Bitmap(os.path.join(path, "connect.png")),shortHelp='Create a new connection')
        tb1.AddSeparator()
        
        tb1.AddTool(ID_openConnection, "Open Connection", wx.Bitmap(os.path.join(path, "database_connect.png")),shortHelp='Open Connection')
        tb1.AddTool(ID_newWorksheet, "Script", wx.Bitmap(os.path.join(path, "script.png")),shortHelp='Open a new script worksheet')
        tb1.AddTool(wx.ID_PREFERENCES, "Preferences", wx.Bitmap(os.path.join(path, "preference.png")),shortHelp='Preference')
        
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
        
        return tb1

    def selectCallback(self, values):
        """ Simply function that receive the row values when the
            user select an item
        """
        logger.debug(values)
        
    def setDynamicChoices(self):
        ctrl = self._ctrl
        text = ctrl.GetValue().lower()
        current_choices = ctrl.GetChoices()
        choices = [choice for choice in self.dynamic_choices if self.match(text, choice)]
        if choices != current_choices:
            ctrl.SetChoices(choices)

    def match(self, text, choice):
        '''
        Demonstrate "smart" matching feature, by ignoring http:// and www. when doing
        matches.
        '''
        t = text.lower()
        c = choice.lower()
        if c.startswith(t): return True
        if c.startswith(r'http://'): c = c[7:]
        if c.startswith(t): return True
        if c.startswith('www.'): c = c[4:]
        return c.startswith(t)    

    def createAuiManager(self):
        logger.debug('createAuiManager')
        # tell FrameManager to manage this frame
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        # set up default notebook style
        self._notebook_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0      
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
        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))    
        self._perspectives = []
        
        # add a bunch of panes
#         self._mgr.AddPane(self.CreateSizeReportCtrl(), wx.aui.AuiPaneInfo().Name("test1").Caption("Pane Caption").Top().CloseButton(True).MaximizeButton(True))
                # add the toolbars to the manager

        self._mgr.AddPane(self.constructToolBar(), aui.AuiPaneInfo().
                          Name("tb1").Caption("Big Toolbar").
                          ToolbarPane().Top().CloseButton(True).
                          LeftDockable(False).RightDockable(False).Gripper(True))    
        
        self._mgr.AddPane(self.creatingTreeCtrl(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "folder_database.png"))).
                          Name("databaseNaviagor").Caption("Database Navigator").Dockable(True).Movable(True).MinSize(wx.Size(300, 100)).
                          Left().Layer(1).Position(1).CloseButton(False).MaximizeButton(True).MinimizeButton(True))
     
        self._mgr.AddPane(self.constructSqlPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "script.png"))).
                          Name("sqlExecution").Caption("SQL execution").LeftDockable(True).
                          Center().CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        
#         self._mgr.AddPane(self.constructSchemaViewerPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "script.png"))).
#                           Name("schemaViewer").Caption("Schema Viewer").LeftDockable(True).
#                           Center().CloseButton(True).MaximizeButton(True).MinimizeButton(True))      
#         self._mgr.AddPane(self.constructSchemaViewerPane(), aui.AuiPaneInfo().
#                           Name("test9").Caption("Min Size 200x100").
#                           BestSize(wx.Size(200, 100)).MinSize(wx.Size(200, 100)).
#                           Bottom().Layer(1).CloseButton(True).MaximizeButton(True))      
  
        self._mgr.AddPane(self.sqlScriptOutputPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "sql_script_recent.png"))).
                          Name("scriptOutput").Caption("Script Output").Dockable(True).Movable(True).LeftDockable(True).
                          Bottom().Layer(0).Row(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True).PinButton(visible=True).GripperTop())
            
        self._mgr.AddPane(self.constructHistoryPane(), aui.AuiPaneInfo().Icon(wx.Bitmap(os.path.join(path, "sql.png"))).
                          Name("sqlLog").Caption("SQL Log").Dockable(True).BestSize(wx.Size(200, 200)).
                          Bottom().Layer(0).Row(1).CloseButton(True).MaximizeButton(visible=True).MinimizeButton(visible=True))
            
        self._mgr.GetPane("tb1").Show()
        self.perspective_default = self._mgr.SavePerspective()
        perspective_all = self._mgr.SavePerspective()
        all_panes = self._mgr.GetAllPanes()
        # "commit" all changes made to FrameManager
        self._mgr.Update()        

    def constructHistoryPane(self):
        historyGrid = HistoryGrid(self)
        return historyGrid
    
#     def constructSchemaViewerPane(self):
#         svgViewer = SVGViewerPanel(self)
#         return svgViewer
    def sqlScriptOutputPane(self):
        sqlScriptOutputPanel = SqlScriptOutputPanel(self)
        return sqlScriptOutputPanel

    def constructSqlPane(self):
        worksheet = CreateWorksheetTabPanel(self)      
#         worksheet.addTab('Start Page')
        return worksheet
    
    def getCurrentCursorPosition(self):
        lineNo = 1
        column = 1
        return "Line " + str(lineNo) + " , Column " + str(column)
        
    def createStatusBar(self):
        logger.debug('creating status bar')
        self.statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
        self.statusbar.SetStatusText("Welcome to {}".format(TITLE), 1)
        
    def createMenuBar(self):
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
        
        logger.debug('creating menu bar')
                # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        fileOpenItem = wx.MenuItem(file_menu, wx.ID_OPEN, 'Open Database connection \tCtrl+O')
        openbmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16, 16))
        fileOpenItem.SetBitmap(openbmp)
        file_menu.Append(fileOpenItem)        
        
        qmi = wx.MenuItem(file_menu, wx.ID_EXIT, '&Quit \tCtrl+Q')
        bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, (16, 16))
        qmi.SetBitmap(bmp)
        file_menu.Append(qmi)
        
        edit_menu = wx.Menu()
        
        undoBmp = wx.MenuItem(file_menu, wx.ID_UNDO, "Undo \tCtrl+Z")
        undoBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, (16, 16)))
        
        redoBmp = wx.MenuItem(file_menu, wx.ID_REDO, "Redo \tShift+Ctrl+Z")
        redoBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, (16, 16)))
        
        cutBmp = wx.MenuItem(file_menu, wx.ID_CUT, "Cut \tCtrl+X")
        cutBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, (16, 16)))
        
        copyBmp = wx.MenuItem(file_menu, wx.ID_COPY, "Copy \tCtrl+C")
        copyBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, (16, 16)))
        
        pasteBmp = wx.MenuItem(file_menu, wx.ID_PASTE, "Paste \tCtrl+V")
        pasteBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (16, 16)))
        
        edit_menu.Append(undoBmp)
        edit_menu.Append(redoBmp)
        edit_menu.Append(cutBmp)
        edit_menu.Append(copyBmp)
        edit_menu.Append(pasteBmp)
        
#         edit_menu.Append(wx.ID_COPY, "Copy \tCtrl+C")
#         edit_menu.Append(wx.ID_PASTE, "Paste \tCtrl+V")
        
        window_menu = wx.Menu()
                
        preferenceBmp = wx.MenuItem(window_menu, wx.ID_PREFERENCES, "&Preferences")
        preferenceBmp.SetBitmap(wx.Bitmap(os.path.join(path, "preference.png")))
                
        window_menu.AppendSeparator()
        childViewMenu = wx.Menu()
        childViewMenu.Append(ID_SQL_EXECUTION, 'SQL Execution')
        childViewMenu.Append(ID_SQL_LOG, 'SQL Log')
        window_menu.Append(wx.ID_VIEW_LIST, "Show &View", childViewMenu)
        window_menu.Append(preferenceBmp)
        
        help_menu = wx.Menu()
        
        aboutBmp = wx.MenuItem(help_menu, wx.ID_HELP, "&About {}".format(TITLE))
        aboutBmp.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (16, 16)))
        updateCheckBmp = wx.MenuItem(help_menu, ID_UPDATE_CHECK, "Check for &Updates")
        updateCheckBmp.SetBitmap(wx.Bitmap(os.path.join(path, "object_refresh.png")))
        
        help_menu.Append(updateCheckBmp)
        help_menu.Append(aboutBmp)
        
        mb.Append(file_menu, "&File")
        mb.Append(edit_menu, "&Edit")
        mb.Append(window_menu, "&Window")
        mb.Append(help_menu, "&Help")
        self.SetMenuBar(mb)
        
    def bindingEvent(self):
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_HELP)
        
        self.Bind(wx.EVT_MENU, self.onOpenConnection, id=ID_openConnection)
        self.Bind(wx.EVT_MENU, self.onNewConnection, id=ID_newConnection)
        self.Bind(wx.EVT_MENU, self.onNewWorksheet, id=ID_newWorksheet)
        self.Bind(wx.EVT_MENU, self.onPreferences, id=ID_PREFERENCES)
        self.Bind(wx.EVT_MENU, self.onSqlLog, id=ID_SQL_LOG)
        self.Bind(wx.EVT_MENU, self.onSqlExecution, id=ID_SQL_EXECUTION)
    
    def OnClose(self, event):
#         self._mgr.UnInit()
#         del self._mgr
        self.Destroy()    
    
    def OnExit(self, event):
        self.Close() 
        
    def onOpenConnection(self, event):
        logger.debug('onOpenConnection')

    def onNewConnection(self, event):
        logger.debug('onNewConnection')
        CreateNewConncetionWixard().createWizard()
        databaseNavTab = self.GetTopLevelParent()._mgr.GetPane("databaseNaviagor")
        databaseNavTab.window.recreateTree()
        logger.debug("recreating database navigation tree.")

    def onNewWorksheet(self, event):
        logger.debug('onNewWorksheet')
#         all_panes = self._mgr.GetAllPanes()
        sqlExecutionTab = self.GetTopLevelParent()._mgr.GetPane("sqlExecution")
        sqlExecutionTab.window.addTab("Worksheet")
        
    def onPreferences(self, event):
        logger.debug('onPreferences')
        frame1 = OpalPreference(None, "Preferences")
        
    def onSqlLog(self, event):
        logger.debug('onSqlLog')
        sqlLogTab = self.GetTopLevelParent()._mgr.GetPane("sqlLog").Show()
        self.GetTopLevelParent()._mgr.Update()
        
    def onSqlExecution(self, event):
        logger.debug('onSqlExecution')
        sqlExecutionTab = self.GetTopLevelParent()._mgr.GetPane("sqlExecution").Show()
        self.GetTopLevelParent()._mgr.Update()
        
    def OnAbout(self, event):
        logger.debug('OnAbout')
        plate = platform.platform()
#         msg=u"\u00A9"
        msg = u"""{} 
Version : {} Release 
Build : 0.1 Release 
An advanced Database tool for developers, DBAs and analysts.
This product includes software developed by other open source projects.
\u00A9 BSD

Plateform: {} 
Python :{}""".format(TITLE, VERSION, plate, sys.version)
#         msg=msg.unicode('utf-8')
        dlg = wx.MessageDialog(self, msg, TITLE,
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
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


if __name__ == "__main__":
    app = wx.App()
    frame = DatabaseMainFrame(None)
    frame.Show()
    app.MainLoop()
