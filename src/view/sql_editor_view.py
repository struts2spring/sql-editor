import logging
import platform
import sys

import wx

from src.view.connection.NewConnectionWizard import CreateNewConncetionWixard
from src.view.constants import *

from src.view.openConnection.OpenExistingConnection import OpenExistingConnectionFrame
from src.view.preference.Preferences import OpalPreference
from src.view.util.FileOperationsUtil import FileOperations

from src.view.perspective import PerspectiveManager
from src.view.views.console.worksheet.WelcomePage import WelcomePanel
from src.view.other.OtherPanel import OtherViewTreePanel
    
logger = logging.getLogger('extensive')
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD


class DatabaseMainFrame(wx.Frame, PerspectiveManager):

    def __init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE , title=TITLE):
        logger.info("This is from Runner ")
        
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style)

        self.fileOperations = FileOperations()
        icon = wx.Icon()
        icon.CopyFromBitmap(self.fileOperations.getImageBitmap(imageName="eclipse16.png"))
        
        self.SetIcon(icon)
        self.SetMinSize(wx.Size(400, 300))
        self.createMenuBar()
        self.createStatusBar()
        
#         self.creatingTreeCtrl()
        
        try:
            PerspectiveManager.__init__(self)
        except Exception as e:
            logger.error(e, exc_info=True)
            
        self.bindingEvent()
        self._mgr.Update()  

    #---------------------------------------------    

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
    
#     def constructSchemaViewerPane(self):
#         svgViewer = SVGViewerPanel(self)
#         return svgViewer
    
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
        logger.debug('creating menu bar')
                # create menu
        mb = wx.MenuBar()

        menuItemList = [
            ("&File", [
                    [ID_openConnection, 'Open Database connection \tCtrl+O', None, None],
                    [wx.NewIdRef(), 'Recent Files', None, None],
                    [wx.NewIdRef(), 'Refresh \tF5', None, "refresh.png"],
                    [],
                    [wx.NewIdRef(), 'Close \tCtrl+W', None, None],
                    [wx.NewIdRef(), 'Close All \tCtrl+Shift+W', None, None],
                    [],
                    [wx.NewIdRef(), 'Save \tCtrl+S', None, None],
                    [wx.NewIdRef(), 'Save As...', None, None],
                    [wx.NewIdRef(), 'Save All \tCtrl+Shift+S', None, None],
                    [],
                    [wx.NewIdRef(), 'Recent Files', None, None],
                    [wx.NewIdRef(), 'Import', None, "import_prj.png"],
                    [wx.NewIdRef(), 'Export', None, "export.png"],
                    [],
                    [wx.NewIdRef(), 'Print', None, "print.png"],
                    [],
                    [ wx.ID_EXIT, '&Quit \tCtrl+Q', None, None],
                ]) ,
            ("&Edit", [
                    [ wx.ID_UNDO, "Undo \tCtrl+Z", None, "undo_edit.png"],
                    [ wx.ID_REDO, "Redo \tShift+Ctrl+Z", None, "redo_edit.png"],
                    [],
                    [ wx.ID_CUT, "Cut \tCtrl+X", None, "cut_edit.png"],
                    [ wx.ID_COPY, "Copy \tCtrl+C", None, "copy_edit.png"],
                    [ wx.ID_PASTE, "Paste \tCtrl+V", None, "paste_edit.png"],
                    [],
                    [ wx.NewIdRef(), "Delete", None, "delete_obj.png"],
                    [ wx.NewIdRef(), "Set encoding...", None, None],
                ]),
            ("&Search", [
                    [wx.NewIdRef(), 'Search \tCtrl+H', None, 'searchres.png'],
                    [ID_SEARCH_FILE, 'File', None, 'search_history.png']
                ]),
            ("&Navigate", [
                    [wx.NewIdRef(), 'Open Type', None, 'opentype.png'],
                    [wx.NewIdRef(), 'Open Task', None, 'open_task.png'],
                    [wx.NewIdRef(), 'Go to Line... \tCtrl+L', None, None]
                ]),
            ("&Project", [
                    [wx.NewIdRef(), 'Open Project', None, None],
                    [wx.NewIdRef(), 'Close Project', None, None],
                    [],
                    [wx.NewIdRef(), 'Build All \tCtrl+B', None, None],
                    [wx.NewIdRef(), 'Build Project', None, None],
                    [wx.NewIdRef(), 'Clean', None, None],
                    [wx.NewIdRef(), 'Build Automatically', None, None],
                    [],
                    [wx.NewIdRef(), 'Properties', None, None],
                ]),
            ("&Run", [
                    [wx.NewIdRef(), 'Run \tCtrl+F11', None, "runlast_co.png"],
                    [wx.NewIdRef(), 'Debug \tF11', None, "debuglast_co.png"],
                    [],
                    [wx.NewIdRef(), 'Run As', None, 'run_exc.png'],
                    
                ]),
            ("&Window", [
                    [ID_CREATE_NEW_WINDOW, 'New Window', None, None ],
                    [ID_APPEARANCE, 'Appearance', [
                                                [ID_HIDE_TOOLBAR, 'Hide Toolbar', "toolbar.png", None],
                                                [ID_HIDE_STATUSBAR, 'Hide Status Bar', None, None]
                                            ], None
                    ],
                    [],
                    [ID_SHOW_VIEW, "Show &View", [
                                                [ID_SHOW_VIEW_TOOLBAR, 'View Toolbar', "toolbar.png", None ],
                                                [ID_PERSPECTIVE_TOOLBAR, 'Perspective Toolbar', "toolbar.png", None ],
                                                [],
                                                [ID_SQL_EXECUTION, 'Center Pane', "script.png", None ],
                                                [ID_SQL_LOG, 'SQL Log', "sql.png" , None],
                                                [ID_CONSOLE_LOG, 'Console', "console_view.png", None ],
                                                [ID_DATABASE_NAVIGATOR, "Database Navigator", "folder_database.png", None ],
                                                [ID_FILE_EXPLORER, 'File Explorer', "file_explorer.png" , None],
                                                [ID_PROJECT_EXPLORER, 'Project Explorer', "resource_persp.png", None ],
                                                [ID_NAVIGATOR, 'Navigator', "filenav_nav.png", None ],
                                                [ID_TASKS, 'Tasks', "tasks_tsk.png", None ],
                                                [ID_TERMINAL, 'Terminal', 'terminal.png', None ],
                                                [ID_OUTLINE, 'Outline', "outline_co.png", None ],
                                                [ID_PYTHON_PACKAGE_EXPLORER, 'Python Package Explorer', "package_explorer.png", None ],  # TODO : need to set image icon
                                                [],
                                                [ID_OTHER_VIEW, 'Other', None, None ]
                                            ], None
                    ],
                    [ID_PROSPECTIVE_NAVIGATION, "Perspective", [
                                                [ wx.NewIdRef(), 'Open Perspective', "new_persp.png", [
                                                        [ wx.NewIdRef(), 'Python', "python_16x16.png", None],
                                                        [ wx.NewIdRef(), 'Java', "jperspective.png", None],
                                                        [ wx.NewIdRef(), 'Java EE', "javaee_perspective.png", None],
                                                        [ wx.NewIdRef(), 'Resources', "resource_persp.png", None],
                                                        [ wx.NewIdRef(), 'Git', "gitrepository.png", None],
                                                        [],
                                                        [wx.NewIdRef(), "Other", None],
                                                    ]],
                                                [ wx.NewIdRef(), 'SQL Log', "sql.png", None ],
                                                [ wx.NewIdRef(), 'Console', "console_view.png", None ]
                                            ], None
                    ],
                    [],
                    [ID_PREFERENCES, "&Preferences", None, "preference.png" ]
                ]),
            ("&Help", [
                    [ ID_WELCOME, "Welcome", None, "welcome16.png"],
                    [ ID_UPDATE_CHECK, "Check for &Updates", None, "iu_update_obj.png"],
                    [ wx.NewIdRef(), "Tip of the day", None, "smartmode_co.png"],
                    [ wx.NewIdRef(), "Tips and Tricks...", None, "tricks.png"],
                    [],
                    [ wx.NewIdRef(), "Install New Software...", None, "iu_obj.png"],  # TODO: need to set icon
                    [],
                    [ wx.ID_HELP, "&About {}".format(TITLE), None, None],
                    [ wx.NewIdRef(), "Contribute", None, "star.png"],
                ])
            ]
        
        for menuItem in menuItemList:
            topLevelMenu = wx.Menu()
            if menuItem[1]:
                for windowMenu in menuItem[1]:
                    if len(windowMenu) == 0:
                        topLevelMenu.AppendSeparator()
                    elif windowMenu[2]:
                        firstLevelMenu = wx.Menu()
                        try:
                            for showViewMenu in windowMenu[2]:
                                if len(showViewMenu) == 0:
                                    firstLevelMenu.AppendSeparator()
                                elif showViewMenu[3]:
                                    menuaItem = wx.MenuItem()
                                    secondLevelMenuItem = wx.Menu()
                                    for secondLevelMenu in showViewMenu[3]:
                                        if len(secondLevelMenu) == 0:
                                            secondLevelMenuItem.AppendSeparator()
                                        else:
                                            self.appendLeafToMenu(secondLevelMenu[0], attacheTo=secondLevelMenuItem, menuName=secondLevelMenu[1], imageName=secondLevelMenu[2])
                                    firstLevleMenuItem = firstLevelMenu.Append(-1, showViewMenu[1], secondLevelMenuItem)
                                    firstLevleMenuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=showViewMenu[2]))
                                else:
                                    self.appendLeafToMenu(showViewMenu[0], attacheTo=firstLevelMenu, menuName=showViewMenu[1], imageName=showViewMenu[2])
                                    
                            topLevelMenu.Append(windowMenu[0], windowMenu[1], firstLevelMenu)
                        except Exception as e:
                            logger.error(e, exc_info=True)
                    else:
                        firstLevelMenu = wx.MenuItem(topLevelMenu, windowMenu[0], windowMenu[1])
                        if windowMenu[3]:
                            firstLevelMenu.SetBitmap(self.fileOperations.getImageBitmap(imageName=windowMenu[3]))
                        topLevelMenu.Append(firstLevelMenu)
        
            mb.Append(topLevelMenu, menuItem[0])

        self.SetMenuBar(mb)
    
    def appendLeafToMenu(self, menuId, attacheTo=None, menuName=None, imageName=None):
        '''
        Append menuItem to menu
        '''
        try:
            menuItem = wx.MenuItem(attacheTo, menuId, menuName)
            if imageName:
                menuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=imageName))
            attacheTo.Append(menuItem)
        except Exception as e:
            logger.error(e, exc_info=True)
        return attacheTo
    
    def bindingEvent(self):
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_HELP)
        self.Bind(wx.EVT_MENU, self.OnWelcome, id=ID_WELCOME)
        
        self.Bind(wx.EVT_MENU, self.onOpenConnection, id=ID_openConnection)
        self.Bind(wx.EVT_MENU, self.onNewConnection, id=ID_newConnection)
        self.Bind(wx.EVT_MENU, self.onNewWorksheet, id=ID_newWorksheet)
        self.Bind(wx.EVT_MENU, self.onPreferences, ID_PREFERENCES)
        self.Bind(wx.EVT_MENU, self.onSqlLog, id=ID_SQL_LOG)
        self.Bind(wx.EVT_MENU, self.onConsole, id=ID_CONSOLE_LOG)
        self.Bind(wx.EVT_MENU, self.onDatabaseNavigator, id=ID_DATABASE_NAVIGATOR)
        self.Bind(wx.EVT_MENU, self.onFileExplorer, id=ID_FILE_EXPLORER)
        self.Bind(wx.EVT_MENU, self.onOtherView, id=ID_OTHER_VIEW)
        
        self.Bind(wx.EVT_MENU, self.onSqlExecution, id=ID_SQL_EXECUTION)
        self.Bind(wx.EVT_MENU, self.onShowViewToolbar, id=ID_SHOW_VIEW_TOOLBAR)
        self.Bind(wx.EVT_MENU, self.onPerspectiveToolbar, id=ID_PERSPECTIVE_TOOLBAR)
        self.Bind(wx.EVT_MENU, self.onHideToolbar, id=ID_HIDE_TOOLBAR)
        self.Bind(wx.EVT_MENU, self.onHideStatusbar, id=ID_HIDE_STATUSBAR)
    
    def OnClose(self, event):
#         self._mgr.UnInit()
#         del self._mgr
        self.Destroy()    
    
    def OnExit(self, event):
        self.Close() 
        
    def onOpenConnection(self, event):
        logger.debug('onOpenConnection')
        self.openFrame()
#         databasefile=page2.markFile.GetValue() 
#         connectionName=page2.connectionNameTextCtrl.GetValue()
#         self.createNewDatabase( connectionName=connectionName,databaseAbsolutePath=databasefile)

    def openFrame(self):
        dialog = OpenExistingConnectionFrame(None, 'Open Existing Connection')
        result = dialog.ShowModal()
        self.refreshDatabaseNaviagtionTree()
#         if  result==  wx.ID_OK:
#             logger.info('ok')
#         else:
#             logger.info('Cancel')
#         frame = OpenExistingConnectionFrame(None, 'Open Existing Connection')
#         frame.Show()
#         if frame ==None:
#             logger.info("OpenExistingConnectionFrame closed")

    def onNewConnection(self, event):
        logger.debug('onNewConnection')
        CreateNewConncetionWixard(self).createWizard()
        self.refreshDatabaseNaviagtionTree()

    def refreshDatabaseNaviagtionTree(self):
        databaseNavTab = self.GetTopLevelParent()._mgr.GetPane("databaseNaviagor")
        databaseNavTab.window.recreateTree()
        logger.debug("recreating database navigation tree.")
        
    def onNewWorksheet(self, event):
        logger.debug('onNewWorksheet')
#         all_panes = self._mgr.GetAllPanes()
        sqlExecutionTab = self.GetTopLevelParent()._mgr.GetPane("centerPane")
        sqlExecutionTab.window.addTab("Worksheet")
        
    def onPreferences(self, event):
        logger.debug('onPreferences')
        frame1 = OpalPreference(None, "Preferences", size=(600, 560))
        
    def onHideToolbar(self, event):
        logger.debug('onHideStatusbar')
        if self.GetTopLevelParent()._mgr.GetPane("viewToolbar").IsShown():
            for menuItem in event.GetEventObject().GetMenuItems():
                if menuItem.GetItemLabel() == 'Hide Toolbar':
                    menuItem.SetItemLabel('Show Toolbar')
                    menuItem.SetText('Show Toolbar')
            self.GetTopLevelParent()._mgr.GetPane("viewToolbar").Hide()
            self.GetTopLevelParent()._mgr.GetPane("perspectiveToolbar").Hide()
        else:
            for menuItem in event.GetEventObject().GetMenuItems():
                if menuItem.GetItemLabel() == 'Show Toolbar':
                    menuItem.SetItemLabel('Hide Toolbar')
                    menuItem.SetText('Hide Toolbar')
            sqlLogTab = self.GetTopLevelParent()._mgr.GetPane("viewToolbar").Show()
            sqlLogTab = self.GetTopLevelParent()._mgr.GetPane("perspectiveToolbar").Show()
        self.GetTopLevelParent()._mgr.Update()

    def onHideStatusbar(self, event):
        logger.debug('onHideStatusbar')
        frameSize = self.GetSize()
        if self.statusbar.IsShown():
            for menuItem in event.GetEventObject().GetMenuItems():
                if menuItem.GetItemLabel() == 'Hide Status Bar':
                    menuItem.SetItemLabel('Show Status Bar')
                    menuItem.SetText('Show Status Bar')
            self.statusbar.Hide()
        else:
            for menuItem in event.GetEventObject().GetMenuItems():
                if menuItem.GetItemLabel() == 'Show Status Bar':
                    menuItem.SetItemLabel('Hide Status Bar')
                    menuItem.SetText('Hide Status Bar')
            self.statusbar.Show()
        self.SetSize(frameSize)
        self._mgr.Update()

    def onShowViewToolbar(self, event):
        logger.debug('onShowViewToolbar')
        sqlLogTab = self.GetTopLevelParent()._mgr.GetPane("viewToolbar").Show()
        self.GetTopLevelParent()._mgr.Update()

    def onPerspectiveToolbar(self, event):
        logger.debug('onPerspectiveToolbar')
        sqlLogTab = self.GetTopLevelParent()._mgr.GetPane("perspectiveToolbar").Show()
        self.GetTopLevelParent()._mgr.Update()

    def onSqlLog(self, event):
        logger.debug('onSqlLog')
        self.addTab(tabName="sqlLog", tabDirection=3)

    def onDatabaseNavigator(self, event):
        logger.debug("onDatabaseNavigator")
        self.addTab(tabName="databaseNaviagor", tabDirection=4)    
            
    def onConsole(self, event):
        logger.debug('onConsole')
        self.addTab(tabName="consoleOutput", tabDirection=3)        

    def onOtherView(self, event):
        logger.debug('onOtherView')
        frame1 = OtherViewTreePanel(self, "Show View", size=(600, 560))

    def onFileExplorer(self, event):
        logger.debug('onFileExplorer')

        self.addTab(tabName="fileExplorer", tabDirection=4)
        
    def onSqlExecution(self, event):
        logger.debug('onSqlExecution')

        self.addTab(tabName="centerPane", tabDirection=5)
    
    def OnWelcome(self, event):
        logger.debug("OnWelcome")
        name = 'Start Page'
        self.addTab(tabName="onWelcome", tabDirection=5)
#         centerPaneTab.window.addTab(name)    

    def addTab(self, tabName='', tabDirection=5):
        self._mgr.SetAutoNotebookStyle(aui.AUI_NB_DEFAULT_STYLE | wx.BORDER_NONE)
#         worksheetPanel=WelcomePanel(self)
        targetTab = self.GetTopLevelParent()._mgr.GetPane(tabName).Show()
        targetTab.CaptionVisible(True)
        
        for pane in self._mgr.GetAllPanes():
            logger.debug(pane.dock_direction_get())
            if pane.dock_direction_get() == tabDirection:  # adding to center tab
                if not pane.HasNotebook():
                    self._mgr.CreateNotebookBase(self._mgr._panes, pane)
                targetTab.NotebookPage(pane.notebook_id)
                self._mgr.ActivatePane(targetTab.window)
                break
            else:
                self._mgr.AddPane(targetTab.window, targetTab)  
               
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


if __name__ == "__main__":
    app = wx.App()
    frame = DatabaseMainFrame(None)
    frame.Show()
    app.MainLoop()
