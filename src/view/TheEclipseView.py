import platform
import sys

import wx
from src.view.views.calibre.filter.BookExplorer import BookExplorerPanel
from src.view.views.calibre.BookBrowser import BookBrowserPanel
from src.view.connection.NewConnectionWizard import CreateNewConncetionWixard
from src.view.constants import *

from src.view.openConnection.OpenExistingConnection import OpenExistingConnectionFrame
from src.view.preference.Preferences import OpalPreference
from src.view.util.FileOperationsUtil import FileOperations

from src.view.perspective import PerspectiveManager
from src.view.views.console.worksheet.WelcomePage import WelcomePanel
from src.view.other.OtherView import OtherViewTreePanel, OtherViewTreeFrame
from src.view.other.OtherPerspecitve import OtherPerspectiveTreeFrame
from src.view.views.database.explorer.DataSourceExplorer import DataSourcePanel
from src.view.other.Resources import ResourceFrame

import logging.config
# from src.view.TreePanel import CreatingTreePanel
from src.view.views.python.explorer.PythonExplorer import PythonExplorerPanel
from src.view.views.sql.history.HistoryListPanel import HistoryGrid
from src.view.views.file.explorer import FileBrowserPanel
from src.view.views.file.explorer.FileBrowserPanel import FileBrowser
from wx import py
from src.view.views.console.SqlOutputPanel import SqlConsoleOutputPanel
from src.view.views.java.explorer.JavaExplorer import CreatingJavaExplorerPanel
from src.view.views.project.explorer.ProjectExplorer import CreatingProjectExplorerPanel
from src.view.search.SearchFrame import SearchPanelsFrame
from src.view.views.file.MainStcPanel import MainStc
from src.view.views.console.worksheet.ResultGrid import ResultDataGrid
from src.view.other.NewFile import NewFileFrame
from src.view.other.imported.project.ImportProject import ImportProjectFrame

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD
from wx.lib.pubsub import pub


class EclipseMainFrame(wx.Frame, PerspectiveManager):

    def __init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE , title=TITLE):
        super(EclipseMainFrame, self).__init__()
        logger.info("This is from Runner ")

        pub.subscribe(self.onNewWorksheet, 'onNewWorksheet')
        pub.subscribe(self.onViewClick, 'sqlLogView')
        pub.subscribe(self.addFileToHistory, 'addFileToHistory')
#         self.startWebHelp()
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style)

        self.fileOperations = FileOperations()
        icon = wx.Icon()
        icon.CopyFromBitmap(self.fileOperations.getImageBitmap(imageName="eclipse16.png"))

        self.SetIcon(icon)
        self.SetMinSize(wx.Size(100, 100))
        self.createMenuBar()
        self.createStatusBar()

#         self.creatingTreeCtrl()

        try:
            self.perspective = PerspectiveManager.__init__(self)
            self.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN, self.onTabRightup1, self.perspective)
        except Exception as e:
            logger.error(e, exc_info=True)

        self.bindingEvent()
        self._mgr.Update()

#         wx.CallLater(13, self.startWebHelp)
    #---------------------------------------------
    def updateTitle(self, title=None):
        logger.debug(f'updateTitle: {title}')
        self.SetTitle(f'{TITLE}-{title}')

    def onTabRightup1(self, event):
        logger.debug('rightdown PopUp')
        _mgr = self._mgr
        currentlySelectedPage = event.GetSelection()
        logger.debug("onTabRightDown: currentlySelectedPage %s", currentlySelectedPage)
        pageInfo = event.GetEventObject().GetPageInfo(currentlySelectedPage)

        def onCloseTab(event=None, pageInfo=None):
            logger.debug("onCloseTab")
            logger.debug("currentlySelectedPage %s", pageInfo)
            self._mgr.ClosePane(self._mgr.GetPaneByWidget(pageInfo.window))
#             self._mgr.Update()
            # TODO:  need to work

        def onCloseOthersTabs(event=None, pageInfo=None):
            logger.debug("onCloseOthersTabs")
            logger.debug("currentlySelectedPage %s", currentlySelectedPage)
            for pane in _mgr.GetAllPanes():
                selectedPane = _mgr.GetPaneByWidget(pageInfo.window)
                if selectedPane.dock_direction == pane.dock_direction and selectedPane.window.GetId() != pane.window.GetId():
                    _mgr.ClosePane(pane)
            _mgr.Update()
            # TODO:  need to work

        def onCloseLeftTabs(event=None, pageInfo=None):
            logger.debug("onCloseLeftTabs")
            logger.debug("currentlySelectedPage %s", currentlySelectedPage)
            for pane in _mgr.GetAllPanes():
                selectedPane = _mgr.GetPaneByWidget(pageInfo.window)
                if selectedPane.dock_direction == pane.dock_direction and selectedPane.dock_pos > pane.dock_pos:
                    _mgr.ClosePane(pane)
            _mgr.Update()
            # TODO:  need to work

        def onCloseRightTabs(event=None, pageInfo=None):
            logger.debug("onCloseRightTabs")
            logger.debug("currentlySelectedPage %s", currentlySelectedPage)
            for pane in _mgr.GetAllPanes():
                selectedPane = _mgr.GetPaneByWidget(pageInfo.window)
                if selectedPane.dock_direction == pane.dock_direction and selectedPane.dock_pos < pane.dock_pos:
                    _mgr.ClosePane(pane)
            _mgr.Update()
            # TODO:  need to work

        def onCloseAllTabs(event=None, pageInfo=None):
            logger.debug("onCloseAllTabs")
            logger.debug("currentlySelectedPage %s", currentlySelectedPage)
            for pane in _mgr.GetAllPanes():
                selectedPane = _mgr.GetPaneByWidget(pageInfo.window)
                if selectedPane.dock_direction == pane.dock_direction:
                    _mgr.ClosePane(pane)
            _mgr.Update()

        pos = self.ScreenToClient(wx.GetMousePosition())
        self.popupmenu = wx.Menu()
        popupList = [
            {'label':'Close', 'icon':self.fileOperations.getImageBitmap(imageName="close.png"), "eventMethod": lambda event: onCloseTab(event, pageInfo)},
            {'label':'Close Others', 'icon':self.fileOperations.getImageBitmap(imageName="close.png"), "eventMethod":lambda event: onCloseOthersTabs(event, pageInfo)},
            {'label':"Close Other tabs to the left", 'icon':self.fileOperations.getImageBitmap(imageName="close.png"), "eventMethod":lambda event: onCloseLeftTabs(event, pageInfo)},
            {'label':'Close Other tabs to the right', 'icon':self.fileOperations.getImageBitmap(imageName="close.png"), "eventMethod":lambda event: onCloseRightTabs(event, pageInfo)},
            {'label':'Close &All', 'icon':self.fileOperations.getImageBitmap(imageName="close.png"), "eventMethod":lambda event: onCloseAllTabs(event, pageInfo)}

            ]

            # TODO:  need to work
        for popupRow in popupList:
            itemId = wx.ID_ANY
            item = wx.MenuItem(self.popupmenu, itemId, popupRow['label'])
            item.SetBitmap(popupRow['icon'])
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

    def startWebHelp(self):
        '''
        This method start web server for eclipse help .
        http://localhost:5000/
        '''
        try:
            process = wx.Process(self)
            process.Redirect()
            dirPath = os.path.dirname(os.path.realpath(__file__))
            filePath = os.path.join(dirPath, '..', 'web', 'HelpWeb.py')
            logger.debug(dirPath)
            cmd = f'python -u {filePath}'
            pid = wx.Execute(cmd, wx.EXEC_ASYNC, process)
            logger.debug(f'executing: {cmd} pid: {pid}')
        except Exception as e:
            logger.error(e)

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
        # id, name, None, imageName, methodName, enable, perspecitveNameList
        menuItemList = [
            ["&File", [
                    [wx.ID_NEW, 'New \tAlt+Shift+N', None, None, False, ['Python', 'database']],
                    
                    [ID_OPEN_FILE, 'Open File... ', None, None, False, ['Python']],
                    [ID_OPEN_PROJECT_FROM_FILE_SYSTEM, 'Open Project From File System...', None, 'importdir_wiz.png', False, ['Python']],
#                     [ID_openConnection, 'Open Database connection \tCtrl+O', None, None, False, ['database']],
                    [wx.ID_REFRESH, 'Refresh \tF5', None, "refresh.png", False, ['Python']],
                    [],
                    [ID_CLOSE, 'Close \tCtrl+W', None, None, False, ['Python']],
                    [ID_CLOSE_ALL, 'Close All \tCtrl+Shift+W', None, None, False, ['Python']],
                    [],
                    [ID_SAVE, 'Save \tCtrl+S', None, "save.png", True, ['Python']],
                    [ID_SAVE_AS, 'Save As...', None, "saveas_edit.png", False, ['Python']],
                    [ID_SAVE_ALL, 'Save All \tCtrl+Shift+S', None, "saveall_edit.png", False, ['Python']],
                    [],
                    [ID_RECENT_FILES, 'Recent Files', [
                                                [wx.ID_CLEAR, 'Clear History', None, None],
                                            ], None, False, ['Python']],
                    [ID_IMPORT, 'Import', None, "import_prj.png", False, ['Python']],
                    [ID_EXPORT, 'Export', None, "export.png", False, ['Python']],
                    [],
                    [wx.ID_PRINT, 'Print', None, "print.png", False, ['Python']],
                    [ID_PROJECT_PROPERTIES, 'Properties', None, "project_properties.png", False, ['Python']],
                    [ID_SWITCH_WORKSPACE, 'Switch Workspace', None, "workspace_switcher.png", False, ['Python']],
                    [ID_RESTART, 'Restart', None, "restart.png", False, ['Python']],
                    [],
                    [ wx.ID_EXIT, '&Quit \tCtrl+Q', None, None, False, ['Python']],
                ]] ,
            ["&Edit", [
                    [ wx.ID_UNDO, "Undo \tCtrl+Z", None, "undo_edit.png"],
                    [ wx.ID_REDO, "Redo \tShift+Ctrl+Z", None, "redo_edit.png"],
                    [],
                    [ wx.ID_SELECTALL, "Select All \tCtrl+A", None, "double-tick-16.png"],
                    [ wx.ID_CUT, "Cut \tCtrl+X", None, "cut_edit.png"],
                    [ wx.ID_COPY, "Copy \tCtrl+C", None, "copy_edit.png"],
                    [ wx.ID_PASTE, "Paste \tCtrl+V", None, "paste_edit.png"],
                    [],
                    [ wx.ID_DELETE, "Delete", None, "delete_obj.png"],
                    [ wx.NewIdRef(), "Set encoding...", None, None],
                ]],
            ["&Search", [
                    [ID_SEARCH_MENU, 'Search \tCtrl+H', None, 'searchres.png'],
                    [ID_SEARCH_FILE, 'File...', None, 'search_history.png']
                ]],
            ["&Navigate", [
                    [ID_OPEN_TYPE, 'Open Type', None, 'opentype.png'],
                    [ID_OPEN_TASK, 'Open Task', None, 'open_task.png'],
                    [ID_GOTO_LINE, 'Go to Line... \tCtrl+L', None, None]
                ]],
            ["&Project", [
                    [ID_OPEN_PROJECT, 'Open Project', None, None],
                    [ID_CLOSE_PROJECT, 'Close Project', None, None],
                    [],
                    [ID_BUILD_ALL, 'Build All \tCtrl+B', None, "build_exec.png"],
                    [ID_BUILD_PROJECT, 'Build Project', None, None],
                    [ID_CLEAN, 'Clean', None, None],
                    [ID_BUILD_AUTO, 'Build Automatically', None, None],
                    [],
                    [ID_PROJECT_PROPERTIES, 'Properties', None, None],
                ]],
            ["&Run", [
                    [ID_RUN, 'Run \tCtrl+F11', None, "runlast_co.png"],
                    [ID_DEBUG, 'Debug \tF11', None, "debuglast_co.png"],
                    [],
                    [ID_RUN_HISTORY, 'Run history', None, None],
                    [ID_RUN_AS, 'Run As', None, 'run_exc.png'],
                    [ID_RUN_CONFIG, 'Run Configurations...', None, None],
                    [],
                    [ID_DEBUG_HISTORY, 'Debug history', None, None],
                    [ID_DEBUG_AS, 'Debug As', None, 'run_exc.png'],
                    [ID_DEBUG_CONFIG, 'Debug Configurations...', None, None],

                ]],
            ["&Window", [
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
#                                                 [ID_SQL_EXECUTION, 'Center Pane', "script.png", None ],
                                                [ID_SQL_LOG, 'SQL Log', "sql.png" , None],
                                                [ID_CONSOLE_LOG, 'Console', "console_view.png", None ],
                                                [ID_DATABASE_NAVIGATOR, "Database Navigator", "folder_database.png", None ],
                                                [ID_FILE_EXPLORER, 'File Explorer', "file_explorer.png" , None],
                                                [ID_PROJECT_EXPLORER, 'Project Explorer', "resource_persp.png", None ],
                                                [ID_NAVIGATOR, 'Navigator', "filenav_nav.png", None ],
                                                [ID_TASKS, 'Tasks', "tasks_tsk.png", None ],
                                                [ID_TERMINAL, 'Terminal', 'terminal.png', None ],
                                                [ID_PYTHON_SHELL, 'Python Shell', 'shell.png', None ],
                                                [ID_OUTLINE, 'Outline', "outline_co.png", None ],
                                                [ID_VARIABLE, 'Variables', "variable_view.png", None ],
                                                [ID_BREAKPOINTS, 'Breakpoints', "breakpoint_view.png", None ],
                                                [ID_EXPRESSIONS, 'Expressions', "watchlist_view.png", None ],
                                                [ID_PYTHON_PACKAGE_EXPLORER, 'Python Package Explorer', "package_explorer.png", None ],  # TODO : need to set image icon
                                                [ID_JAVA_PACKAGE_EXPLORER, 'Java Package Explorer', "package_explorer.png", None ],  # TODO : need to set image icon
                                                [],
                                                [ID_OTHER_VIEW, 'Other', None, None ]
                                            ], None
                    ],
                    [ID_PROSPECTIVE_NAVIGATION, "Perspective", [
                                                [ ID_OPEN_PERSPECTIVE, 'Open Perspective', "new_persp.png", [
                                                        [ ID_PYTHON_PERSPECTIVE, 'Python', "python_perspective.png", None],
                                                        [ ID_JAVA_PERSPECTIVE, 'Java', "jperspective.png", None],
                                                        [ ID_JAVA_EE_PERSPECTIVE, 'Java EE', "javaee_perspective.png", None],
                                                        [ ID_RESOURCE_PERSPECTIVE, 'Resources', "resource_persp.png", None],
                                                        [ ID_GIT_PERSPECTIVE, 'Git', "gitrepository.png", None],
                                                        [ ID_DEBUG_PERSPECTIVE, 'Debug', "debug_persp.png", None],
                                                        [],
                                                        [ID_OTHER_PERSPECTIVE, "Other", None],
                                                    ]],
                                                [ wx.NewIdRef(), 'Customize Perspective...', None, None ],
                                                [ wx.NewIdRef(), 'Save Perspective As...', None, None ],
                                                [ wx.NewIdRef(), 'Reset Perspective...', None, None ],
                                                [ wx.NewIdRef(), 'Close Perspective...', None, None ],
                                                [ wx.NewIdRef(), 'Close All Perspective...', None, None ],
                                            ], None
                    ],
                    [],
                    [ID_PREFERENCES, "&Preferences", None, "preference.png" ]
                ]],
            ["&Help", [
                    [ ID_WELCOME, "Welcome", None, "welcome16.png"],
                    [],
                    [ wx.NewIdRef(), "Help Contents", None, "smartmode_co.png"],
                    [ wx.NewIdRef(), "Search", None, "help_search.png"],
                    [],
                    [ wx.NewIdRef(), "Show active key bindings \tShift+Ctrl+L", None, "keyboard.png"],
                    [ wx.NewIdRef(), "Tip of the day", None, "smartmode_co.png"],
                    [ wx.NewIdRef(), "Tips and Tricks...", None, "tricks.png"],
                    [ wx.NewIdRef(), "Report Bug or Enhancement ...", None, "report_bug.png"],
                    [ wx.NewIdRef(), "Cheat sheets ...", None, "cheet_sheet.png"],
                    [],
                    [ ID_UPDATE_CHECK, "Check for &Updates", None, "iu_update_obj.png"],
                    [ wx.NewIdRef(), "Install New Software...", None, "iu_obj.png"],  # TODO: need to set icon
                    [ wx.NewIdRef(), "Eclipse Marketplace", None, "marketplace16.png"],  # TODO: need to set icon
                    [],
                    [ wx.ID_ABOUT, "&About {}".format(TITLE), None, None],
                    [ wx.NewIdRef(), "Contribute", None, "star.png"],
                ]]
            ]

#         mb = self.createMenu(menuItemList=menuItemList)

#         if self.selectedPerspectiveName == 'python':
#             logger.debug(self.selectedPerspectiveName)
#             [ID_openConnection, 'Open Database connection \tCtrl+O', None, None, False, ['database']],

#         def creatingMenu(menuItemList):
#             logger.debug('Adding Menu')
#             menubar = wx.MenuBar()
#             for menuItem in menuItemList:
#                 topLevelMenu = wx.Menu()
#                 menubar.Append(topLevelMenu, menuItem[0])
#             return menubar
# 
#         creatingMenu(menuItemList)
                
        for menuItem in menuItemList:
            topLevelMenu = wx.Menu()
            if menuItem[1]:
                for windowMenu in menuItem[1]:
                    if len(windowMenu) == 0:
                        topLevelMenu.AppendSeparator()
                        
                    elif windowMenu[2] and windowMenu[0] != wx.ID_NEW:
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
                                            
                                            if secondLevelMenu[0] == wx.ID_CLEAR:
                                                print('got')
                                    firstLevleMenuItem = firstLevelMenu.Append(-1, showViewMenu[1], secondLevelMenuItem)
                                    firstLevleMenuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=showViewMenu[2]))
                                else:
                                    self.appendLeafToMenu(showViewMenu[0], attacheTo=firstLevelMenu, menuName=showViewMenu[1], imageName=showViewMenu[2])
                                    if showViewMenu[0] == wx.ID_CLEAR:
                                        print('got-----------------------')
                                        self.filehistory = wx.FileHistory()
                                        self.filehistory.UseMenu(firstLevelMenu)

                            topLevelMenu.Append(windowMenu[0], windowMenu[1], firstLevelMenu)
                        except Exception as e:
                            logger.error(e, exc_info=True)
                    elif windowMenu[0] == wx.ID_NEW:
                        logger.debug('new menu')
                        firstLevelMenu = wx.Menu()
                        
#                         secondLevelMenuItem = wx.Menu()
                        self.appendLeafToMenu(wx.NewIdRef(), attacheTo=firstLevelMenu, menuName='Project...', imageName=None)
                        self.appendLeafToMenu(wx.NewIdRef(), attacheTo=firstLevelMenu, menuName='Example...', imageName=None)
                        self.appendLeafToMenu(wx.NewIdRef(), attacheTo=firstLevelMenu, menuName='Other...', imageName=None)
#                         firstLevleMenuItem = firstLevelMenu.Append(-1, 'asdfzxc', secondLevelMenuItem)
#                         firstLevelMenu.Append(menuItem)
                        
#                         firstLevelMenu.Append(-1, 'asdfasd', secondLevelMenuItem)
#                         firstLevelMenu.Append(wx.NewIdRef(), 'asdasdff', secondLevelMenuItem)
#                         topLevelMenu.Append(firstLevelMenu)
                        topLevelMenu.Append(windowMenu[0], windowMenu[1], firstLevelMenu)
                        
                    else:
                        firstLevelMenu = wx.MenuItem(topLevelMenu, windowMenu[0], windowMenu[1])
                        if windowMenu[3]:
                            firstLevelMenu.SetBitmap(self.fileOperations.getImageBitmap(imageName=windowMenu[3]))
                        topLevelMenu.Append(firstLevelMenu)
                        self.Bind(wx.EVT_MENU, lambda e:self.onRightClickMenu(e), id=windowMenu[0])
            mb.Append(topLevelMenu, menuItem[0])

        self.disableInitial(menuBar=mb)
        self.SetMenuBar(mb)

#         self.addFileToHistory(r'C:\Users\xbbntni\Downloads\1.txt')
#         self.addFileToHistory(r'C:\Users\xbbntni\Downloads\India-Technology-NPS-New-Subscriber.pdf')
#         self.addFileToHistory(r'C:\Users\xbbntni\Downloads\India-Technology-NPS-Exiting.pdf')

    def addFileToHistory(self, path):
        self.filehistory.AddFileToHistory(path)

    def disableInitial(self, menuBar=None):
        itemIdList = [
#             ID_SAVE,
            ID_SAVE_ALL, wx.ID_UNDO, wx.ID_REDO, wx.ID_CUT, wx.ID_COPY, wx.ID_PASTE]
        for itemId in itemIdList:
            it = menuBar.FindItemById(itemId)
            it.Enable(False)
            
#         logger.debug(self.selectedPerspectiveName)
        # default perspective python
        selectedPerspectiveName = 'python'
        baseList = menuItemList[selectedPerspectiveName]
        menuItemListx = {
                selectedPerspectiveName: baseList
                }
        menuPopup = self.createMenuByPerspective(menuItemList=menuItemListx, perspectiveName=selectedPerspectiveName)
#         item = menuBar.FindItemById(wx.ID_NEW).SetSubMenu(menuPopup)
        self.appendSubMenu(menuBar=menuBar)

#         item = menuBar.FindItemById(wx.ID_NEW).GetSubMenu()
#         menuItem = wx.MenuItem(item, wx.NewIdRef(), "asdf")
#         item.Append(menuItem)
        
#         item.AppendItem(menuItem)
#         self.appendLeafToMenu(wx.NewIdRef(), attacheTo=item, menuName='Project1...', imageName=None)
#         item.Append(menuItem)
        
#     def createMenu(self, menuBar=wx.MenuBar(), menu=wx.Menu(), menuItemList=list()) :
#         '''
#         return mb: wx.MenuBar
#         '''
#         for menuItem in menuItemList:
#             menuItem = wx.MenuItem(menu, -1, 'asdf')
# #             if imageName:
# #                 menuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=imageName))
#             menu.Append(menuItem[0], windowMenu[1], firstLevelMenu)
#             self.createMenu(menuBar, menuItem)
#
#         return menuBar
    def appendSubMenu(self, menuBar=None, selectedPerspectiveName='python'):
        item = menuBar.FindItemById(wx.ID_NEW).GetSubMenu()
        
        # removing all menu 
        for menu in item.GetMenuItems():
            item.Remove(menu.Id)
        
        baseList = menuItemList[selectedPerspectiveName]
        for baseMenuItem in baseList:
            if len(baseMenuItem) > 1:
                menuItem = wx.MenuItem(item, baseMenuItem[0], baseMenuItem[1])
                if baseMenuItem[2]:
                    menuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=baseMenuItem[2]))
                item.Append(menuItem)
                self.Bind(wx.EVT_MENU, lambda e:self.onRightClickMenu(e), id=baseMenuItem[0])
            else:
                item.AppendSeparator()
        
    def appendLeafToMenu(self, menuId, attacheTo=None, menuName=None, imageName=None):
        '''
        Append menuItem to menu
        '''
        try:
            menuItem = wx.MenuItem(attacheTo, menuId, menuName)
            if imageName:
                menuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=imageName))
            attacheTo.Append(menuItem)
            self.Bind(wx.EVT_MENU, lambda e:self.onRightClickMenu(e), id=menuId)
        except Exception as e:
            logger.error(e, exc_info=True)
        return attacheTo

    def onRightClickMenu(self, event):
        logger.debug(f'onRightClickMenu:{event.Id}')
        if event.Id == ID_NEW_FILE:
            logger.debug('ID_NEW_FILE')
            self.newFileFlow(title='New File', file=None)
        if event.Id == ID_NEW_FOLDER:
            logger.debug('ID_NEW_FOLDER')
            self.newFileFlow(title='New Folder', file=None)
        if event.Id == ID_IMPORT:
            logger.debug('ID_IMPORT')
            self.importFlow(title='Import Project', file=None)
        if event.Id == wx.ID_SELECTALL:
            logger.debug('wx.ID_SELECTALL')
#             self.newFileFlow(title='New Folder', file=None)
  
    def importFlow(self, title=None, file=None):
        logger.debug('importFlow')
        importProjectFrame = ImportProjectFrame(self, title, selectedPath=file)
        importProjectFrame.CenterOnScreen()
        importProjectFrame.Show()
    
    def newFileFlow(self, title=None, file=None):
        newFileframe = NewFileFrame(self, title, selectedPath=file)
        newFileframe.CenterOnScreen()
        newFileframe.Show()

    def bindingEvent(self):

        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnWelcome, id=ID_WELCOME)

        self.Bind(wx.EVT_MENU, self.onUndo, id=ID_UNDO)
        self.Bind(wx.EVT_MENU, self.onRedo, id=ID_REDO)
        self.Bind(wx.EVT_MENU, self.onCopy, id=ID_COPY)
        self.Bind(wx.EVT_MENU, self.onPaste, id=ID_PASTE)
        self.Bind(wx.EVT_MENU, self.onCut, id=ID_CUT)
        self.Bind(wx.EVT_MENU, self.onFormatFile, id=ID_FORMAT_FILE)
#         self.Bind(wx.EVT_MENU, lambda evt, temp=wx.WXK_DOWN: self.onDuplicateLine(evt, temp), id=ID_DUPLICATE_LINE)
        self.Bind(wx.EVT_MENU, self.onDuplicateLine, id=ID_DUPLICATE_LINE)
        self.Bind(wx.EVT_MENU, self.onSave, id=ID_SAVE)
        self.Bind(wx.EVT_MENU, self.onSaveAll, id=ID_SAVE_ALL)
        self.Bind(wx.EVT_MENU, self.onSaveAs, id=ID_SAVE_AS)
#         self.Bind(wx.EVT_MENU, self.onNew, id=ID_NEW)

        self.Bind(wx.EVT_MENU, self.onOpenConnection, id=ID_openConnection)
        self.Bind(wx.EVT_MENU, self.onNewConnection, id=ID_newConnection)
        self.Bind(wx.EVT_MENU, lambda e: self.onNewWorksheet(e), id=ID_newWorksheet)
        self.Bind(wx.EVT_MENU, self.onPreferences, ID_PREFERENCES)
        self.Bind(wx.EVT_MENU, self.onFileSearch, ID_SEARCH_FILE)
        self.Bind(wx.EVT_MENU, self.onOpenResource, ID_RESOURCE)
        self.Bind(wx.EVT_MENU, self.onOpenType, ID_OPEN_TYPE)

        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_OUTLINE)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_SQL_LOG)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_VARIABLE)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_BREAKPOINTS)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_EXPRESSIONS)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_TERMINAL)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_PYTHON_SHELL)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_TASKS)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_PROJECT_EXPLORER)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_NAVIGATOR)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_JAVA_PACKAGE_EXPLORER)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_PYTHON_PACKAGE_EXPLORER)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_FILE_EXPLORER)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_DATABASE_NAVIGATOR)
        self.Bind(wx.EVT_MENU, self.onViewClick, id=ID_CONSOLE_LOG)

        self.Bind(wx.EVT_MENU, self.onOtherView, id=ID_OTHER_VIEW)
        self.Bind(wx.EVT_MENU, self.onOtherPerspecitve, id=ID_OTHER_PERSPECTIVE)

        self.Bind(wx.EVT_MENU, self.onSqlExecution, id=ID_SQL_EXECUTION)
        self.Bind(wx.EVT_MENU, self.onShowViewToolbar, id=ID_SHOW_VIEW_TOOLBAR)
        self.Bind(wx.EVT_MENU, self.onPerspectiveToolbar, id=ID_PERSPECTIVE_TOOLBAR)
        self.Bind(wx.EVT_MENU, self.onHideToolbar, id=ID_HIDE_TOOLBAR)
        self.Bind(wx.EVT_MENU, self.onHideStatusbar, id=ID_HIDE_STATUSBAR)
        self.Bind(wx.EVT_MENU, self.Cleanup, id=wx.ID_CLEAR)
        self.Bind(
            wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9
            )
#         self.accel_tbl = wx.AcceleratorTable([
#             (wx.ACCEL_CTRL, ord('H'), ID_SEARCH_FILE),
#             (wx.ACCEL_CTRL, ord('S'), ID_SAVE),
# #                                       (wx.ACCEL_CTRL, ord('V'), wx.ID_PASTE),
# #                                       (wx.ACCEL_ALT, ord('X'), wx.ID_PASTE),
# #                                       (wx.ACCEL_SHIFT | wx.ACCEL_ALT, ord('Y'), wx.ID_PASTE)
#                                      ])
#         self.SetAcceleratorTable(self.accel_tbl)

    def Cleanup(self, *args):
        logger.debug('Cleanup')
        for i in range(self.filehistory.GetCount() + 1):
            try:
                logger.debug(f'removing : {i}')
                self.filehistory.RemoveFileFromHistory(i)
            except:
                pass
        # A little extra cleanup is required for the FileHistory control
#         del self.filehistory

    def OnFileHistory(self, evt):
        # get the file based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.filehistory.GetHistoryFile(fileNum)
        logger.debug(f"You selected {path}")

        # add it back to the history so it will be moved up the list
        self.filehistory.AddFileToHistory(path)

    def enableButtons(self, buttonIds=[], enable=True):
        viewToolbar = self.GetTopLevelParent()._mgr.GetPane("viewToolbar")
        for buttonId in buttonIds:
            tool = viewToolbar.window.FindTool(buttonId)
            if enable:
                tool.state = aui.AUI_BUTTON_STATE_NORMAL
            else:
                tool.state = aui.AUI_BUTTON_STATE_DISABLED

        self._mgr.Update()

    def OnClose(self, event):
#         self._mgr.UnInit()
#         del self._mgr
        self.Destroy()

    def OnExit(self, event):
        self.Close()

    def onNew(self, event):
        logger.debug('onNew')

    def onSave(self, event):
        logger.debug('onSave1')
        # disabling button
        window = self.GetTopLevelParent().FindFocus()
        if isinstance(window, MainStc):
            logger.debug('MainStc window')
            window.SaveFile()
        elif isinstance(window, ResultDataGrid):
            logger.debug('window:ResultDataGrid')
        self.enableButtons(buttonIds=[ID_SAVE], enable=False)
        # changing title : removing start mark

    def onSaveAll(self, event):
        logger.debug('onSaveAll1')
        self.enableButtons(buttonIds=[ID_SAVE, ID_SAVE_ALL], enable=False)

    def onSaveAs(self, event):
        """Save File Using a new/different name
        @param event: wx.MenuEvent

        """
        logger.debug('onSaveAs')
        window = self.GetTopLevelParent().FindFocus()
        if isinstance(window, MainStc):
            logger.debug('MainStc window')
            window.SaveFile()
        #     def OnSaveAs(self, evt, title=u'', page=None):
#         if page:
#             ctrl = page
#         else:
#             ctrl = self.nb.GetCurrentCtrl()
#
#         if title == u'':
#             title = os.path.split(ctrl.GetFileName())[1]
#
#         sdir = ctrl.GetFileName()
#         if sdir is None or not len(sdir):
#             sdir = self._last_save
#
#         dlg = wx.FileDialog(self, _("Choose a Save Location"),
#                             os.path.dirname(sdir),
#                             title.lstrip(u"*"),
#                             u''.join(syntax.GenFileFilters()),
#                             wx.SAVE | wx.OVERWRITE_PROMPT)
#
#         if ebmlib.LockCall(self._mlock, dlg.ShowModal) == wx.ID_OK:
#             path = dlg.GetPath()
#             dlg.Destroy()
#
#             result = ctrl.SaveFile(path)
#             fname = ebmlib.GetFileName(ctrl.GetFileName())
#             if not result:
#                 err = ctrl.GetDocument().GetLastError()
#                 ed_mdlg.SaveErrorDlg(self, fname, err)
#                 ctrl.GetDocument().ResetAll()
#                 self.PushStatusText(_("ERROR: Failed to save %s") % fname, SB_INFO)
#             else:
#                 self._last_save = path
#                 self.PushStatusText(_("Saved File As: %s") % fname, SB_INFO)
#                 self.SetTitle("%s - file://%s" % (fname, ctrl.GetFileName()))
#                 self.nb.SetPageText(self.nb.GetSelection(), fname)
#                 self.nb.GetCurrentCtrl().FindLexer()
#                 self.nb.UpdatePageImage()
#                 self.AddFileToHistory(ctrl.GetFileName())
#         else:
#             dlg.Destroy()

    def onUndo(self, event):
        logger.debug('onUndo')
        self._mgr.GetManagedWindow().FindFocus().Undo()

    def onRedo(self, event):
        logger.debug('onRedo')
        self._mgr.GetManagedWindow().FindFocus().Redo()

    def onCopy(self, event):
        logger.debug('onCopy')
        self._mgr.GetManagedWindow().FindFocus().Copy()

#         currentlySelectedPage = event.GetSelection()
#         logger.debug("onTabRightDown: currentlySelectedPage %s", currentlySelectedPage)
#         pageInfo = event.GetEventObject().GetPageInfo(currentlySelectedPage)
#         logger.debug(pageInfo)

    def onPaste(self, event):
        logger.debug('onPaste')
        self._mgr.GetManagedWindow().FindFocus().Paste()

    def onCut(self, event):
        logger.debug('onCut')
        self._mgr.GetManagedWindow().FindFocus().Cut()

    def onFormatFile(self, event):
        logger.debug('onFormatFile')

    def onDuplicateLine(self, event):
        logger.debug('onDuplicateLine')
        self._mgr.GetManagedWindow().FindFocus().LineDuplicate()

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
#         databaseNavTab.window.recreateTree()
        logger.debug("recreating database navigation tree.")

    def onNewWorksheet(self, event, dataSourceTreeNode=None):
        logger.debug('onNewWorksheet')
#         all_panes = self._mgr.GetAllPanes()
        count = 0
        for pane in self._mgr.GetAllPanes():
            if "Worksheet-" in pane.name:
                countStr = pane.name.replace("Worksheet-", '')
                count = int(countStr)
                count += 1
        self._mgr.addTabByWindow(self.getWorksheet(dataSourceTreeNode), imageName="script.png", captionName="Worksheet-{}".format(count), tabDirection=5)

#         sqlExecutionTab = self.GetTopLevelParent()._mgr.GetPane("centerPane")
#         sqlExecutionTab.window.addTab("Worksheet")

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

    def onFileSearch(self, event):
        logger.debug('onFileSearch')
        frame = SearchPanelsFrame(None, size=(800, 400))
        frame.CenterOnScreen()

    def onOpenType(self, event):
        logger.debug('onOpenType')

    def onOpenResource(self, event):
        logger.debug('onOpenResource')
        frame = ResourceFrame(self, 'Open Resource', size=(800, 400))
        frame.CenterOnScreen()

    def onViewClick(self, event):
        logger.debug('onViewClick')
        if event.Id == ID_OUTLINE:
            self.openPanel(name="outlineView", imageName="outline_co.png", captionName="Outline", tabDirection=2)
        elif event.Id == ID_SQL_LOG:
            self.openPanel(name="sqlLogView", imageName="sql.png", captionName="SQL Log", tabDirection=3)
        elif event.Id == ID_VARIABLE:
            self.openPanel(name="variablesView", imageName="variable_view.png", captionName="Variables", tabDirection=2)
        elif event.Id == ID_BREAKPOINTS:
            self.openPanel(name="breakpointsView", imageName="breakpoint_view.png", captionName="Breakpoints", tabDirection=2)
        elif event.Id == ID_EXPRESSIONS:
            self.openPanel(name="expressionsView", imageName="watchlist_view.png", captionName="Expressions", tabDirection=2)
        elif event.Id == ID_TERMINAL:
            self.openPanel(name="terminalView", imageName="terminal.png", captionName="Terminal", tabDirection=3)
        elif event.Id == ID_PYTHON_SHELL:
            self.openPanel(name="pythonShellView", imageName="shell.png", captionName="Python Shell", tabDirection=3)
        elif event.Id == ID_TASKS:
            self.openPanel(name="tasksView", imageName="tasks_tsk.png", captionName="Tasks", tabDirection=3)
        elif event.Id == ID_PROJECT_EXPLORER:
            self.openPanel(name="projectExplorerView", imageName="resource_persp.png", captionName="Project Explorer", tabDirection=4)
        elif event.Id == ID_NAVIGATOR:
            self.openPanel(name="navigatorView", imageName="filenav_nav.png", captionName="Navigator", tabDirection=4)
        elif event.Id == ID_JAVA_PACKAGE_EXPLORER:
            self.openPanel(name="javaPackageExplorer", imageName="package_explorer.png", captionName="Java Package Explorer", tabDirection=4)
        elif event.Id == ID_PYTHON_PACKAGE_EXPLORER:
            self.openPanel(name="pythonPackageExplorer", imageName="package_explorer.png", captionName="Python Package Explorer", tabDirection=4)
        elif event.Id == ID_FILE_EXPLORER:
            self.openPanel(name="javaPackageExplorer", imageName="package_explorer.png", captionName="Java Package Explorer", tabDirection=4)
        elif event.Id == ID_DATABASE_NAVIGATOR:
            self.openPanel(name="databaseNaviagor", imageName="folder_database.png", captionName="Database Navigator", tabDirection=4)
        elif event.Id == ID_CONSOLE_LOG:
            self.openPanel(name="consoleOutput", imageName="console_view.png", captionName="Console", tabDirection=3)

    def onConsole(self, event):
        logger.debug('onConsole')
        self.openPanel(name="consoleOutput", imageName="console_view.png", captionName="Console", tabDirection=3)
#         self.addTab(tabName="consoleOutput", tabDirection=3)

    def openPanel(self, name="consoleOutput", imageName="console_view.png", captionName="Console", tabDirection=3):
#         name="consoleOutput"
        pane = self._mgr.GetPane(name)
        if pane.window == None:
            panel = wx.Panel(self)
            if name == "consoleOutput":
                panel = SqlConsoleOutputPanel(self)
            elif name == "databaseNaviagor":
                panel = DataSourcePanel(self)
            elif name == "pythonPackageExplorer":
                panel = PythonExplorerPanel(self)
            elif name == "projectExplorerView":
                panel = CreatingProjectExplorerPanel(self)
            elif name == "javaPackageExplorer":
                panel = CreatingJavaExplorerPanel(self)
            elif name == "pythonShellView":
                intro = f'{py.version.VERSION}'
                panel = py.shell.Shell(self, -1, introText=intro)
            elif name == "terminalView":
                panel = PythonExplorerPanel(self)
            elif name == "navigatorView":
                panel = PythonExplorerPanel(self)
            elif name == "tasksView":
                panel = PythonExplorerPanel(self)
            elif name == "fileExplorer":
                panel = FileBrowser(self, size=(500, 300))
            elif name == "sqlLogView":
                panel = HistoryGrid(self)
            elif name == "outlineView":
                panel = PythonExplorerPanel(self)
            elif name == "variablesView":
                panel = PythonExplorerPanel(self)
            elif name == "breakpointsView":
                panel = PythonExplorerPanel(self)
            elif name == "expressionsView":
                panel = PythonExplorerPanel(self)
            elif name == "bookExplorer":
                panel = BookExplorerPanel(self)
            elif name == "bookBrowser":
                panel = BookBrowserPanel(self)

            self._mgr.addTabByWindow(panel, imageName=imageName, name=name , captionName=captionName, tabDirection=tabDirection)
        elif not self._mgr.GetPaneByName(name).IsShown():
            panel = self._mgr.GetPaneByName(name).window
            if panel:
                panel.Show()
            pane.dock_direction = tabDirection
            pane.Show(True)
        self._mgr.Update()

    def onOtherView(self, event):
        logger.debug('onOtherView')
        frame = OtherViewTreeFrame(self, "Show View")
        frame.Show()

    def onOtherPerspecitve(self, event):
        logger.debug('onOtherPerspecitve')
        frame = OtherPerspectiveTreeFrame(self, "Open Pespective")
        frame.Show()

    def onFileExplorer(self, event):
        logger.debug('onFileExplorer')
        self.openPanel(name="fileExplorer", imageName="file_explorer.png", captionName="File Explorer", tabDirection=4)
#         fileBrowserPanel = FileBrowser(self, size=(500, 300))
#         self._mgr.addTabByWindow(fileBrowserPanel, imageName="file_explorer.png", name='fileExplorer' , captionName="File Explorer", tabDirection=4)

    def onSqlExecution(self, event):
        logger.debug('onSqlExecution')

        self.addTab(tabName="centerPane", tabDirection=5)

    def OnWelcome(self, event):
        logger.debug("OnWelcome")
        name = 'Start Page'
        self.addTab(tabName="onWelcome", tabDirection=5)
#         centerPaneTab.window.addTab(name)

    def addTabByWindo1(self, window=None , imageName="script.png", captionName=None, tabDirection=5):
        '''
        This method always create a new tab for the window.
        tabDirection=5 is the center
        '''
        self._mgr.SetAutoNotebookStyle(aui.AUI_NB_DEFAULT_STYLE | wx.BORDER_NONE)
        for pane in self._mgr.GetAllPanes():
            logger.debug(pane.dock_direction_get())
            auiPanInfo = aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName=imageName)).\
                Name(captionName).Caption(captionName).LeftDockable(True).Direction(wx.TOP).\
                Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True).CaptionVisible(visible=True)
            if pane.dock_direction_get() == tabDirection:  # adding to center tab
                targetTab = pane
                if not pane.HasNotebook():
                    self._mgr.CreateNotebookBase(self._mgr._panes, pane)
#                 targetTab.NotebookPage(pane.notebook_id)
                    self._mgr.AddPane(window, auiPanInfo, target=targetTab)
#                 self._mgr._notebooks
#                 self._mgr.ActivatePane(targetTab.window)
                else:
                    self._mgr.AddPane(window, auiPanInfo, target=targetTab)
                break
        self.GetTopLevelParent()._mgr.Update()

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
        msg = f"""{TITLE}

Version : {VERSION} Release
Build : 0.1 Release

An advanced Database tool for developers, DBAs and analysts.
This product includes software developed by other open source projects.
\u00A9 BSD

Plateform: {plate}
wxpython: {wx.__version__}
Python :{sys.version}"""
# .format(TITLE, VERSION, plate, sys.version)
#         msg=msg.unicode('utf-8')
        dlg = wx.MessageDialog(self, msg, TITLE,
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = EclipseMainFrame(None)
    frame.Show()
    app.MainLoop()
