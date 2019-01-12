import logging.config
import wx

from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
from src.view.AutoCompleteTextCtrl import TextCtrlAutoComplete
from src.view.TreePanel import CreatingTreePanel
from src.view.constants import LOG_SETTINGS, ID_newConnection, ID_openConnection, \
    ID_newWorksheet, ID_SAVE, ID_SAVE_ALL, ID_NEW, ID_TERMINAL, ID_OPEN_PERSPECTIVE, \
    ID_JAVA_PERSPECTIVE, ID_JAVA_EE_PERSPECTIVE, ID_DEBUG_PERSPECTIVE, ID_PYTHON_PERSPECTIVE, \
    ID_GIT_PERSPECTIVE, ID_DEBUG_AS, ID_RUN_AS, ID_OPEN_TASK, ID_BACKWARD, ID_FORWARD, ID_LAST_EDIT, \
    ID_SEARCH, ID_OPEN_TYPE, ID_DATABASE_PERSPECTIVE, ID_TEXTCTRL_AUTO_COMPLETE, \
    ID_SKIP_ALL_BREAKPOINTS, ID_NEW_JAVA_PACKAGE, ID_NEW_JAVA_CLASS, ID_RESUME_DEBUG, ID_SUSPEND_DEBUG, \
    ID_TERMNATE_DEBUG, ID_DISCONNECT_DEBUG, ID_STEP_INTO_DEBUG, ID_STEP_OVER_DEBUG, ID_STEP_RETURN_DEBUG, \
    ID_RESOURCE_PERSPECTIVE, ID_OTHER_PERSPECTIVE

from wx.lib.agw.aui.aui_constants import actionDragFloatingPane, AUI_DOCK_NONE, \
    ITEM_NORMAL, ITEM_CHECK, ITEM_RADIO, ID_RESTORE_FRAME
from src.view.views.file.explorer.FileBrowserPanel import FileBrowser
from src.view.views.console.SqlOutputPanel import SqlConsoleOutputPanel
from src.view.views.console.worksheet.WorksheetPanel import CreateWorksheetTabPanel, \
    CreatingWorksheetWithToolbarPanel
from src.view.views.sql.history.HistoryListPanel import HistoryGrid
from src.view.views.console.worksheet.WelcomePage import WelcomePanel
from wx.lib.agw.aui.framemanager import NonePaneInfo, wxEVT_AUI_PANE_MIN_RESTORE, \
    AuiManagerEvent
from src.view.util.FileOperationsUtil import FileOperations
from wx.lib.platebtn import PlateButton, PB_STYLE_DEFAULT, PB_STYLE_DROPARROW

# from wx.lib.pubsub import setupkwargs
# regular pubsub import
from wx.lib.pubsub import pub
from wx.lib.agw.aui.auibar import AuiToolBarEvent, \
    wxEVT_COMMAND_AUITOOLBAR_BEGIN_DRAG, wxEVT_COMMAND_AUITOOLBAR_MIDDLE_CLICK, \
    wxEVT_COMMAND_AUITOOLBAR_RIGHT_CLICK

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD
############################################################


class EclipseAuiToolbar(aui.AuiToolBar):

    def __init__(self, parent):
        super().__init__(parent, -1, agwStyle=aui.AUI_TB_DEFAULT_STYLE | wx.NO_BORDER)
        pub.subscribe(self.__onObjectAdded, 'perspectiveClicked')

    def __onObjectAdded(self, data, extra1, extra2=None):
        # no longer need to access data through message.data.
        print('Object', repr(data), 'is added')
        print(extra1)
        if extra2:
            print(extra2)
    
    def getToolBarItemById(self, id=None):
        item = None
        for _item in self._items:
            if _item.id == id:
                item = _item
                break
        return item

    def OnLeaveWindow(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`AuiToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self.RefreshOverflowState()
#         self.SetHoverItem(None)
#         self.SetPressedItem(None)
# 
#         self._tip_item = None
        self.StopPreviewTimer()

    def SetPressedItem(self, pitem):
        """
        Sets a toolbar item to be currently in a "pressed" state.

        :param `pitem`: an instance of :class:`AuiToolBarItem`.
        """

        if pitem and pitem.label != 'Open Perspective':
            former_item = None
    
            for item in self._items:
    
                if item.state & aui.AUI_BUTTON_STATE_PRESSED:
                    former_item = item
    
                item.state &= ~aui.AUI_BUTTON_STATE_PRESSED
                
            pitem.state &= ~aui.AUI_BUTTON_STATE_HOVER
            pitem.state |= aui.AUI_BUTTON_STATE_PRESSED

            if former_item != pitem:
                self.Refresh(False)
                self.Update()

    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`AuiToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self.SetPressedItem(None)

        hit_item = self.FindToolForPosition(*event.GetPosition())

        if hit_item and not hit_item.state & aui.AUI_BUTTON_STATE_DISABLED:
            self.SetHoverItem(hit_item)

        if self._dragging:
            # reset drag and drop member variables
            self._dragging = False
            self._action_pos = wx.Point(-1, -1)
            self._action_item = None

        else:

            if self._action_item and hit_item == self._action_item:
                self.SetToolTip("")

                if hit_item.kind in [ITEM_CHECK, ITEM_RADIO]:
                    toggle = not (self._action_item.state & aui.AUI_BUTTON_STATE_CHECKED)
                    self.ToggleTool(self._action_item.id, toggle)

                    # repaint immediately
                    self.Refresh(False)
                    self.Update()

                    e = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, self._action_item.id)
                    e.SetEventObject(self)
                    e.SetInt(toggle)
                    self._action_pos = wx.Point(-1, -1)
                    self._action_item = None

                    self.ProcessEvent(e)
                    self.DoIdleUpdate()

                else:

                    if self._action_item.id == ID_RESTORE_FRAME:
                        # find aui manager
                        manager = self.GetAuiManager()

                        if not manager:
                            return

                        if self._action_item.target:
                            pane = manager.GetPane(self._action_item.target)
                        else:
                            pane = manager.GetPane(self)

#                         from . import framemanager
                        e = AuiManagerEvent(wxEVT_AUI_PANE_MIN_RESTORE)

                        e.SetManager(manager)
                        e.SetPane(pane)

                        manager.ProcessEvent(e)
                        self.DoIdleUpdate()

                    else:

                        e = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, self._action_item.id)
                        e.SetEventObject(self)
                        self.ProcessEvent(e)
                        self.DoIdleUpdate()

        # reset drag and drop member variables
        self._dragging = False
        self._action_pos = wx.Point(-1, -1)
        self._action_item = None

    def OnRightDown(self, event):
        """
        Handles the ``wx.EVT_RIGHT_DOWN`` event for :class:`AuiToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        cli_rect = wx.Rect(wx.Point(0, 0), self.GetClientSize())

        if self._gripper_sizer_item:
            gripper_rect = self._gripper_sizer_item.GetRect()
            if gripper_rect.Contains(event.GetPosition()):
                return

        if self.GetOverflowVisible():

            dropdown_size = self._art.GetElementSize(aui.AUI_TBART_OVERFLOW_SIZE)
            if dropdown_size > 0 and event.GetX() > cli_rect.width - dropdown_size and \
               event.GetY() >= 0 and event.GetY() < cli_rect.height and self._art:
                return

        self._action_pos = wx.Point(*event.GetPosition())
        self._action_item = self.FindToolForPosition(*event.GetPosition())

        if self._action_item:
            if self._action_item.state & aui.AUI_BUTTON_STATE_DISABLED:

                self._action_pos = wx.Point(-1, -1)
                self._action_item = None
                return

    def OnRightUp(self, event):
        """
        Handles the ``wx.EVT_RIGHT_UP`` event for :class:`AuiToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        hit_item = self.FindToolForPosition(*event.GetPosition())

        if self._action_item and hit_item == self._action_item:

            e = AuiToolBarEvent(wxEVT_COMMAND_AUITOOLBAR_RIGHT_CLICK, self._action_item.id)
            e.SetEventObject(self)
            e.SetToolId(self._action_item.id)
            e.SetClickPoint(self._action_pos)
            self.ProcessEvent(e)
            self.DoIdleUpdate()

        else:

            # right-clicked on the invalid area of the toolbar
            e = AuiToolBarEvent(wxEVT_COMMAND_AUITOOLBAR_RIGHT_CLICK, -1)
            e.SetEventObject(self)
            e.SetToolId(-1)
            e.SetClickPoint(self._action_pos)
            self.ProcessEvent(e)
            self.DoIdleUpdate()

        # reset member variables
        self._action_pos = wx.Point(-1, -1)
        self._action_item = None

    def OnMiddleDown(self, event):
        """
        Handles the ``wx.EVT_MIDDLE_DOWN`` event for :class:`AuiToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        cli_rect = wx.Rect(wx.Point(0, 0), self.GetClientSize())

        if self._gripper_sizer_item:

            gripper_rect = self._gripper_sizer_item.GetRect()
            if gripper_rect.Contains(event.GetPosition()):
                return

        if self.GetOverflowVisible():

            dropdown_size = self._art.GetElementSize(aui.AUI_TBART_OVERFLOW_SIZE)
            if dropdown_size > 0 and event.GetX() > cli_rect.width - dropdown_size and \
               event.GetY() >= 0 and event.GetY() < cli_rect.height and self._art:
                return

        self._action_pos = wx.Point(*event.GetPosition())
        self._action_item = self.FindToolForPosition(*event.GetPosition())

        if self._action_item:
            if self._action_item.state & aui.AUI_BUTTON_STATE_DISABLED:

                self._action_pos = wx.Point(-1, -1)
                self._action_item = None
                return

    def OnMiddleUp(self, event):
        """
        Handles the ``wx.EVT_MIDDLE_UP`` event for :class:`AuiToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        hit_item = self.FindToolForPosition(*event.GetPosition())

        if self._action_item and hit_item == self._action_item:
            if hit_item.kind == ITEM_NORMAL:

                e = AuiToolBarEvent(wxEVT_COMMAND_AUITOOLBAR_MIDDLE_CLICK, self._action_item.id)
                e.SetEventObject(self)
                e.SetToolId(self._action_item.id)
                e.SetClickPoint(self._action_pos)
                self.ProcessEvent(e)
                self.DoIdleUpdate()

        # reset member variables
        self._action_pos = wx.Point(-1, -1)
        self._action_item = None

    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`AuiToolBar`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        # start a drag event
        if not self._dragging and self._action_item != None and self._action_pos != wx.Point(-1, -1) and \
           abs(event.GetX() - self._action_pos.x) + abs(event.GetY() - self._action_pos.y) > 5:

            self.SetToolTip("")
            self._dragging = True

            e = AuiToolBarEvent(wxEVT_COMMAND_AUITOOLBAR_BEGIN_DRAG, self.GetId())
            e.SetEventObject(self)
            e.SetToolId(self._action_item.id)
            self.ProcessEvent(e)
            self.DoIdleUpdate()
            return

        hit_item = self.FindToolForPosition(*event.GetPosition())

        if hit_item:
            if not hit_item.state & aui.AUI_BUTTON_STATE_DISABLED:
                self.SetHoverItem(hit_item)
            else:
                self.SetHoverItem(None)

        else:
            # no hit item, remove any hit item
            self.SetHoverItem(hit_item)

        # figure out tooltips
        packing_hit_item = self.FindToolForPositionWithPacking(*event.GetPosition())

        if packing_hit_item:

            if packing_hit_item != self._tip_item:
                self._tip_item = packing_hit_item

                if packing_hit_item.short_help != "":
                    self.StartPreviewTimer()
                    self.SetToolTip(packing_hit_item.short_help)
                else:
                    self.SetToolTip("")
                    self.StopPreviewTimer()

        else:

            self.SetToolTip("")
            self._tip_item = None
            self.StopPreviewTimer()

        # if we've pressed down an item and we're hovering
        # over it, make sure it's state is set to pressed
        if self._action_item:

            if self._action_item == hit_item:
                self.SetPressedItem(self._action_item)
            else:
                self.SetPressedItem(None)

        # figure out the dropdown button state (are we hovering or pressing it?)
        self.RefreshOverflowState()    


class MyAuiManager(aui.AuiManager):
    
    def __init__(self, managed_window=None, agwFlags=None):

        super().__init__(managed_window=managed_window, agwFlags=agwFlags)
    
    def addTabByWindow(self, window=None , imageName="script.png", captionName=None, tabDirection=5):
        '''
        This method always create a new tab for the window.
        tabDirection=5 is the center 
        '''
        self.SetAutoNotebookStyle(aui.AUI_NB_DEFAULT_STYLE | wx.BORDER_NONE)
        for pane in self.GetAllPanes():
#             logger.debug(pane.dock_direction_get())
            if pane.dock_direction_get() == tabDirection:  # adding to center tab
                auiPanInfo = aui.AuiPaneInfo().Icon(FileOperations().getImageBitmap(imageName=imageName)).\
                    Name(captionName).Caption(captionName).LeftDockable(True).Direction(wx.TOP).\
                    Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True).CaptionVisible(visible=True)
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

    def OnSize(self, event):
        super().OnSize(event)
        (x, y) = self._frame.GetClientSize()
        perspectiveToolbar = self.GetPane("perspectiveToolbar")
        perspectiveToolbar.dock_pos = x - ((len(perspectiveToolbar.window._items) - 2) * 32) + 5
        self.Update()  
#         self.DoDropToolbar(self._docks, self._panes, perspectiveToolbar, point, wx.Point(0,0))


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
        pub.subscribe(self.__onObjectAdded, 'perspectiveClicked')

    def __onObjectAdded(self, data, extra1, extra2=None):
        # no longer need to access data through message.data.
        print('PerspectiveManager', repr(data), 'is added')
        print(extra1)
        if extra2:
            print(extra2)
        
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
                          ToolbarPane().Top().Row(1).Position(1).CloseButton(True).
                          LeftDockable(False).RightDockable(False).Gripper(True), self.definePoint())    
        
        self._mgr.AddPane(self.creatingFileExplorer(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="file_explorer.png")).BestSize(500, -1).
                          Name("fileExplorer").Caption("File Explorer").Dockable(True).Movable(True).MinSize(500, -1).Resizable(True).
                          Left().Layer(1).Position(2).CloseButton(True).MaximizeButton(True).MinimizeButton(True))
        
#         self._mgr.AddPane(self.creatingTreeCtrl(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="folder_database.png")).BestSize(500, -1).
#                           Name("databaseNaviagor").Caption("Database Navigator").Dockable(True).Movable(True).MinSize(500, -1).
#                           Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).MinimizeButton(True), target=self._mgr.GetPane("fileExplorer"))
        
        self._mgr.AddPane(WelcomePanel(self), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="welcome16.png")).BestSize(500, -1).
                          Name("onWelcome").Caption("Welcome").Dockable(True).Movable(True).MinSize(500, -1).CaptionVisible(visible=True).Direction(wx.TOP).
                          Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True))  
#         self._mgr.AddPane(self.constructCenterPane(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="script.png")).
#                           Name("centerPane").Caption("Center Pane").LeftDockable(True).Direction(wx.TOP).
#                           Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True).CaptionVisible(visible=True), target=self._mgr.GetPane("onWelcome"))
#         self._mgr.AddPane(self.getWorksheet(), aui.AuiPaneInfo().Icon(self.fileOperations.getImageBitmap(imageName="script.png")).
#                           Name("Worksheet-0").Caption("Worksheet-0").LeftDockable(True).Direction(wx.TOP).
#                           Center().Layer(0).Position(0).CloseButton(True).MaximizeButton(True).MinimizeButton(True).CaptionVisible(visible=True), target=self._mgr.GetPane("onWelcome"))
        
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
        
        viewToolbar = self._mgr.GetPane("viewToolbar")
        viewToolbar.Show()
        
        perspectiveToolbar = self._mgr.GetPane("perspectiveToolbar")
        perspectiveToolbar.dock_row = viewToolbar.dock_row
        perspectiveToolbar.Show()
        
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
    def definePoint(self):
        managed_window = self._mgr.GetManagedWindow()
        wnd_pos = managed_window.GetPosition()
        (x, y) = wnd_size = managed_window.GetSize()
        point = wx.Point(x - ((len(self.perspectiveList) - 1) * 32) + 5, 0)
        return point
        
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
#         tb1 = aui.AuiToolBar(self, -1, agwStyle=aui.AUI_TB_DEFAULT_STYLE | wx.NO_BORDER)
        tb1 = EclipseAuiToolbar(self)
        
        self.perspectiveList = [
            [ID_OTHER_PERSPECTIVE, "Open Perspective", 'new_persp.png', 'Open Perspective', self.onOpenPerspecitve ],
            [],
            [ID_JAVA_PERSPECTIVE, "Java", 'jperspective.png', 'Java', self.onJavaPerspective],
            [ID_JAVA_EE_PERSPECTIVE, "Java EE", 'javaee_perspective.png', 'Java EE', self.onJavaEEPerspective],
            [ID_DEBUG_PERSPECTIVE, "Debug", 'debug_persp.png', 'Debug', self.onDebugPerspecitve],
            [ID_PYTHON_PERSPECTIVE, "Python", 'python_perspective.png', 'Python', self.onPythonPerspecitve],
            [ID_DATABASE_PERSPECTIVE, "Database", 'database.png', 'Database', self.onDatabasePerspecitve],
            [ID_GIT_PERSPECTIVE, "Git", 'gitrepository.png', 'Git', self.onGitPerspecitve],
            [ID_RESOURCE_PERSPECTIVE, "Resources", 'resource_persp.png', 'Git', self.onResourcePerspecitve],
            ]
        for perspectiveName in self.perspectiveList:
            if len(perspectiveName) > 1:
                toolBarItem = tb1.AddSimpleTool(perspectiveName[0], perspectiveName[1], self.fileOperations.getImageBitmap(imageName=perspectiveName[2]), short_help_string=perspectiveName[3])
                self.Bind(wx.EVT_MENU, perspectiveName[4], id=perspectiveName[0])
                if toolBarItem.label == 'Python':
                    self.selectedPerspectiveName = 'python'
                    tb1.SetPressedItem(toolBarItem)
            else:
                tb1.AddSeparator()
            
        return tb1

    def onOpenPerspecitve(self, event):
        logger.debug('onOpenPerspecitve')

    def selectItem(self, id=None):
        perspectiveToolbar = self._mgr.GetPane("perspectiveToolbar")
        item = perspectiveToolbar.window.getToolBarItemById(id)   
        perspectiveToolbar.window.EnableTool(item, True) 
    
    def viewToolBarByPerspective(self, perspectiveName):
        viewToolbar = self._mgr.GetPane("viewToolbar")
        
#         viewToolbar.window.DeleteTool(wx.ID_PREFERENCES)
        self.constructViewToolBar(viewToolbar.window, perspectiveName)
        s = viewToolbar.window.GetMinSize()
        viewToolbar.BestSize(s)
        self._mgr.Update()  
        
        print('viewToolBarByPerspective')
        
#         item.state=4   
    def onJavaPerspective(self, event):
        logger.debug('onJavaPerspective')
        pub.sendMessage('perspectiveClicked', data=42, extra1='onJavaPerspective')
        self.selectItem(ID_JAVA_PERSPECTIVE)
        self.selectedPerspectiveName = 'java'
        self.viewToolBarByPerspective(self.selectedPerspectiveName)
        print('perspectiveToolbar')

    def onJavaEEPerspective(self, event):
        logger.debug('onJavaEEPerspective')
        self.selectItem(ID_JAVA_EE_PERSPECTIVE)
        self.selectedPerspectiveName = 'java ee'
        self.viewToolBarByPerspective(self.selectedPerspectiveName)
#         perspectiveToolbar=self._mgr.GetPane("perspectiveToolbar")
#         perspectiveToolbar.window.SetPressedItem(perspectiveToolbar.window.getToolBarItemById(ID_JAVA_EE_PERSPECTIVE))

    def onDebugPerspecitve(self, event):
        logger.debug('onDebugPerspecitve')
        self.selectItem(ID_DEBUG_PERSPECTIVE)
        self.selectedPerspectiveName = 'debug'
        self.viewToolBarByPerspective(self.selectedPerspectiveName)
#         perspectiveToolbar=self._mgr.GetPane("perspectiveToolbar")
#         perspectiveToolbar.window.SetPressedItem(perspectiveToolbar.window.getToolBarItemById(ID_DEBUG_PERSPECTIVE))

    def onPythonPerspecitve(self, event):
        logger.debug('onPythonPerspecitve')
        self.selectItem(ID_PYTHON_PERSPECTIVE)
        self.selectedPerspectiveName = 'python'
        self.viewToolBarByPerspective(self.selectedPerspectiveName)
#         perspectiveToolbar=self._mgr.GetPane("perspectiveToolbar")
#         perspectiveToolbar.window.SetPressedItem(perspectiveToolbar.window.getToolBarItemById(event.EventObject.GetId()))

    def onGitPerspecitve(self, event):
        logger.debug('onGitPerspecitve')
        self.selectItem(ID_GIT_PERSPECTIVE)
        self.selectedPerspectiveName = 'git'
        self.viewToolBarByPerspective(self.selectedPerspectiveName)
        
    def onResourcePerspecitve(self, event):
        logger.debug('onResourcePerspecitve')
        self.selectItem(ID_RESOURCE_PERSPECTIVE)
        self.selectedPerspectiveName = 'resource'
        self.viewToolBarByPerspective(self.selectedPerspectiveName)
        
    def onDatabasePerspecitve(self, event):
        logger.debug('onDatabasePerspecitve')
        self.selectItem(ID_DATABASE_PERSPECTIVE)
        self.selectedPerspectiveName = 'database'
        self.viewToolBarByPerspective(self.selectedPerspectiveName)
#         perspectiveToolbar=self._mgr.GetPane("perspectiveToolbar")
#         perspectiveToolbar.window.SetPressedItem(perspectiveToolbar.window.getToolBarItemById(ID_GIT_PERSPECTIVE))

    def constructViewToolBar(self, toobar=None, perspectiveName='python'):
        # create some toolbars
#         tb1 = aui.AuiToolBar(self, -1, agwStyle=aui.AUI_TB_DEFAULT_STYLE | wx.NO_BORDER)
        if toobar == None:
            self._ctrl = None
            toobar = EclipseAuiToolbar(self)
        
#         tb1.SetToolBitmapSize(wx.Size(42, 42))
#         tb1.AddSimpleTool(tool_id=ID_newConnection, label="New Connection", bitmap=wx.Bitmap(self.fileOperations.getImageBitmap(imageName="connect.png")), short_help_string='Create a new connection')
#         tb1.AddSeparator()
        
#         :TODO:FIXnew_con
#         tb4_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
#         tb4_bmp1 = self.fileOperations.getImageBitmap(imageName='new_con.png')
#         toobar.AddSimpleTool(ID_NEW, "Item 1", tb4_bmp1, short_help_string='New')
#         toobar.SetToolDropDown(ID_NEW, True)
#         toobar.AddSeparator()
#         id, name, imageName, fullName, methodName, IsDropdonw, prospectives, isDisable
        tools = [
            (ID_NEW, "New", "new_con.png", 'New', self.onNewMenu, True, ['resource', 'python', 'java', 'debug', 'java ee'], True),
            (),
            (ID_SAVE, "Save (Ctrl+S)", "save.png", 'Save (Ctrl+S)', self.onSave, False, ['resource', 'python', 'java', 'debug', 'java ee'], False),
            (ID_SAVE_ALL, "Save All (Ctrl+Shift+S)", "saveall_edit.png", 'Save All (Ctrl+Shift+S)', self.onSaveAll, False, ['resource', 'python', 'java', 'debug', 'java ee'], False),
            (ID_TERMINAL, "Open a Terminal", "linux_terminal.png", "Open a Terminal (Ctrl+Shift+Alt+T)", self.onOpenTerminal, False, ['resource', 'python', 'java', 'debug', 'java ee'], True),
            (),
            (ID_SKIP_ALL_BREAKPOINTS, "Skip All Breakpoints (Ctrl+Alt+B)", "skip_brkp.png", "Skip All Breakpoints (Ctrl+Alt+B)", self.onOpenTerminal, False, ['resource', 'python', 'java', 'debug', 'java ee'], True),
            (ID_NEW_JAVA_PACKAGE, "New Java Package", "newpack_wiz.png", "New Java Package", self.onOpenTerminal, False, ['resource', 'java', 'java ee'], True),
            (ID_NEW_JAVA_CLASS, "New Java Class", "newclass_wiz.png", "New Java Class", self.onOpenTerminal, True, ['resource', 'java', 'java ee'], True),
            (ID_RESUME_DEBUG, "Resume", "resume_co.png", "Resume", self.onOpenTerminal, False, ['debug'], False),
            (ID_SUSPEND_DEBUG, "Suspend", "suspend_co.png", "Suspend", self.onOpenTerminal, False, ['debug'], False),
            (ID_TERMNATE_DEBUG, "Terminate", "terminatedlaunch_obj.png", "Terminate", self.onOpenTerminal, False, ['debug'], False),
            (ID_DISCONNECT_DEBUG, "Disconnect", "disconnect_co.png", "Terminate", self.onOpenTerminal, False, ['debug'], False),
            (ID_STEP_INTO_DEBUG, "Step Into", "stepinto_co.png", "Step Into", self.onOpenTerminal, False, ['debug'], False),
            (ID_STEP_OVER_DEBUG, "Step Over", "stepover_co.png", "Step Over", self.onOpenTerminal, False, ['debug'], False),
            (ID_STEP_RETURN_DEBUG, "Step Return", "stepreturn_co.png", "Step Return", self.onOpenTerminal, False, ['debug'], False),
            
            (),
            (ID_DEBUG_AS, "Debug As...", "debug_exc.png", "Debug As...", self.onOpenTerminal, True, ['python', 'java', 'debug'], True),
            (ID_RUN_AS, "Run As...", "run_exc.png", "Run As...", self.onOpenTerminal, True, ['python', 'java', 'debug'], True),
            (ID_OPEN_TYPE, "Open Type", "opentype.png", "Open Type", self.onOpenTerminal, True, ['resource', 'python', 'java', 'debug'], True),
            (ID_OPEN_TASK, "Open Task (Ctrl+F12)", "open_task.png", "Run As...", self.onOpenTerminal, True, ['resource', 'python', 'java', 'debug'], True),
            (ID_SEARCH, "Search", "searchres.png", "Search", self.onOpenTerminal, True, ['resource', 'python', 'java', 'debug'], True),
            (ID_LAST_EDIT, "Last Edit Location", "last_edit_pos.png", "Last Edit Location", self.onOpenTerminal, False, ['resource', 'python', 'java', 'debug'], True),
            (ID_BACKWARD, "Back", "backward_nav.png", "Back", self.onOpenTerminal, True, ['python', 'java', 'debug'], True),
            (ID_FORWARD, "Forward", "forward_nav.png", "Forward", self.onOpenTerminal, True, ['python', 'java', 'debug'], False),
            (ID_newConnection, "New Connection", "connect.png", "New Connection", None, False, ['database'], True),
            (ID_openConnection, "Open Connection", "database_connect.png", 'Open Connection', None, False, ['database'], True),
            (ID_newWorksheet, "Script", "script.png", 'Open a new script worksheet', None, False, ['database'], True),
#             (wx.ID_PREFERENCES, "Preferences", "preference.png", 'Preference', None),
            ]
        
        toobar._items.clear()
        if self._ctrl:
            self._ctrl.Hide()
        
        for tool in tools:
            
            if len(tool) == 0:
                toobar.AddSeparator()
            elif perspectiveName in tool[6]:
                logger.debug(tool)
                state = tool[7]
                toolItem = toobar.AddSimpleTool(tool[0], tool[1], self.fileOperations.getImageBitmap(imageName=tool[2]), short_help_string=tool[3])
                if state:
                    toolItem.state &= ~aui.AUI_BUTTON_STATE_DISABLED
                else:
                    toolItem.state |= aui.AUI_BUTTON_STATE_DISABLED
                if tool[4]:
                    self.Bind(wx.EVT_MENU, tool[4], tool[0])
                if tool[5]:
                    toobar.SetToolDropDown(tool[0], tool[5])
                
        ###################################################################################################
        
        if perspectiveName == 'database':
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
    
            self._ctrl = TextCtrlAutoComplete(toobar, id=ID_TEXTCTRL_AUTO_COMPLETE, size=(250, 20), **args)
            self._ctrl.SetSize((250, 15))
            self._ctrl.SetChoices(self.dynamic_choices)
            self._ctrl.SetEntryCallback(self.setDynamicChoices)
            self._ctrl.SetMatchFunction(self.match)
            toobar.AddControl(self._ctrl) 

        ###################################################################################################
#         tb1.AddControl( self.choice ) 
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
#         tb1.AddLabelTool(103, "Test"t1 = wx.TextCtrl(self, -1, "Test it out and see", size=(125, -1)), wx.ArtProvider_GetBitmap(wx.ART_WARNING))
#         tb1.AddLabelTool(103, "Test", wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE))
        toobar.Realize()
        self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.onNewDropDown, id=ID_NEW)
        return toobar
    
    def onOpenTerminal(self, event):
        logger.debug('onOpenTerminal')

    def onNewMenu(self, event):
        logger.debug('onNewMenu')

    def onSave(self, event):
        logger.debug('onSave1')

    def onSaveAll(self, event):
        logger.debug('onSaveAll1')        

    def onNewDropDown(self, event):

        if event.IsDropDownClicked():

            tb = event.GetEventObject()
            tb.SetToolSticky(event.GetId(), True)

            # create the popup menu
            # menuPopup = wx.Menu()
            menuPopup = self.createMenuByPerspective(perspectiveName=self.selectedPerspectiveName)

            # line up our menu with the button
            rect = tb.GetToolRect(event.GetId())
            pt = tb.ClientToScreen(rect.GetBottomLeft())
            pt = self.ScreenToClient(pt)

            self.PopupMenu(menuPopup, pt)

            # make sure the button is "un-stuck"
            tb.SetToolSticky(event.GetId(), False)    

    def createMenuByPerspective(self, perspectiveName='python'):
        
        baseList = [
                [30001, 'Project', "new_con.png", None],
                [],
                [30002, 'Example', "new_con.png", None],
                [],
                [30003, 'Other (Ctrl+N)', "new_con.png", None],
                ]
        
        menuItemList = {
            "java": 
                [[10001, 'Java Project', 'newjprj_wiz.png', None], ] + 
                baseList[0:1] + 
                [
                    [],
                    [10003, 'Package', "newpack_wiz.png", None],
                    [10004, 'Class', 'newclass_wiz.png', None],
                    [10005, 'Interface', 'newint_wiz.png', None],
                    [10006, 'Enum', 'newenum_wiz.png', None],
                    [10007, 'Annotation', 'newannotation_wiz.png', None],
                    [10008, 'Source Folder', "newpackfolder_wiz.png", None],
                    [10009, 'Java Working Set', "newjworkingSet_wiz.png", None],
                    [10010, 'Folder', "new_folder.png", None],
                    [20007, 'File', "newfile_wiz.png", None],
                    [20007, 'Untitled text file', "new_untitled_text_file.png", None],
                    [10011, 'Task', "new_task.png", None],
                    [10012, 'JUnit Test Case', "new_testcase.png", None],
                ]
                +baseList[1:],
            "python": 
                [
                    [10001, 'Java Project', 'newjprj_wiz.png', None],
                ] + 
                baseList[0:1] + 
                [
                    [],
                    [20003, 'Source Folder', "packagefolder_obj.png", None],
                    [20004, 'Python Project', "package_obj.png", None],
                    [20005, 'Python Module', "project.png", None],
                    [20006, 'Folder', "project.png", None],
                    [20007, 'File', "newfile_wiz.png", None],
                ]
                +baseList[1:],
            "resource": baseList[0:1] + 
                [
                    [],
                    [20006, 'Folder', "project.png", None],
                    [20007, 'File', "newfile_wiz.png", None],
                ]
                +baseList[1:],
            "debug": baseList,
            "database": baseList
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
