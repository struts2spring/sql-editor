'''
Created on Jan 30, 2019

@author: xbbntni
'''

import wx
import os
import ntpath
from src.view.views.database.explorer.databaseTree import DatabaseTree

from wx.lib.pubsub import pub
import logging.config
from src.view.util.FileOperationsUtil import FileOperations
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD

from src.view.constants import LOG_SETTINGS, ID_COLLAPSE_ALL, \
    ID_LINK_WITH_EDITOR, ID_VIEW_MENU
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class DataSourcePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.fileOperations = FileOperations()
        self.toolbar = self.constructTopToolBar()
        self.tree = DatabaseTree(self)
        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter table name")
        self.filter.ShowCancelButton(True)
#         self.filter.Bind(wx.EVT_TEXT, self.recreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
#         self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
#         self.recreateTree()

        # add drop target
        self.SetDropTarget(DatabaseFileDropTarget(self))
    #         self.tree.SetExpansionState(self.expansionState)

        ####################################################################
        ####################################################################
        vBox.Add(self.toolbar , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

    def constructTopToolBar(self):

        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, (10, 10), agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)

#         tb1.SetToolBitmapSize(wx.Size(16, 16))

        tools = [
            (ID_COLLAPSE_ALL, "Collapse All", "collapseall-small.png", 'Collapse All', self.onCollapseAll),
            (ID_LINK_WITH_EDITOR, "Link with Editor", "icon_link_with_editor.png", 'Link with Editor', self.onLinkWithEditor),
            (),
            (ID_VIEW_MENU, "View Menu", "icon_menu.png", 'View Menu', self.onViewMenu),
#             (ID_REFRESH_ROW, "Result refresh", "resultset_refresh.png", 'Result refresh \tF5', self.onRefresh),
#             (ID_ADD_ROW, "Add a new row", "row_add.png", 'Add a new row', self.onAddRow),
#             (ID_DUPLICATE_ROW, "Duplicate selected row", "row_copy.png", 'Duplicate selected row', self.onDuplicateRow),
#             (ID_DELETE_ROW, "Delete selected row", "row_delete.png", 'Delete selected row', self.onDeleteRow),
            ]
        for tool in tools:
            if len(tool) == 0:
                tb1.AddSeparator()
            else:
                logger.debug(tool)
                toolItem = tb1.AddSimpleTool(tool[0], tool[1], self.fileOperations.getImageBitmap(imageName=tool[2]), short_help_string=tool[3])
                if tool[4]:
                    self.Bind(wx.EVT_MENU, tool[4], id=tool[0])

        tb1.Realize()

        return tb1

    def onCollapseAll(self, event):
        logger.debug('onCollapseAll')

    def onLinkWithEditor(self, event):
        logger.debug('onLinkWithEditor')

    def onViewMenu(self, event):
        logger.debug('onViewMenu')


class DatabaseFileDropTarget(wx.FileDropTarget):

    def __init__(self, dirwin):
        wx.FileDropTarget.__init__(self)
        self.dirwin = dirwin

    def OnDropFiles(self, x, y, fileNams):
        logger.debug("dropFiles {}".format(fileNams))

        try:
            for fileAbsoluteName in fileNams:
                if os.path.isdir(fileAbsoluteName):
                    continue
                logger.debug(fileAbsoluteName)
                if self.isSQLite3(fileAbsoluteName):
                    self.getConnectionName(filePath=fileAbsoluteName)
                    sqlExecuter = SQLExecuter()
                    sqlTypeObjectList = sqlExecuter.getSqlObjects()
                    if len(sqlTypeObjectList) == 0:
                        sqlExecuter.createOpalTables()
                    sqlExecuter.addNewConnectionRow(fileAbsoluteName, self.getConnectionName(filePath=fileAbsoluteName))
                    self.dirwin.tree.initialize()
        except Exception as ex:
            logger.error(ex)

        return True

    def getConnectionName(self, filePath=None):
        head, tail = ntpath.split(filePath)
        connectionName = "_".join(tail.split(sep=".")[:-1])
        return connectionName

    def isSQLite3(self, fileName):
        ''' this is to check a valid SQLite file dropped.
        '''
        from os.path import isfile, getsize

        if not isfile(fileName):
            return False
        if getsize(fileName) < 100:  # SQLite database file header is 100 bytes
            return False

        with open(fileName, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == b'SQLite format 3\x00'


if __name__ == '__main__':
    app = wx.App(False)
    f = wx.Frame(None)
    ft = DataSourcePanel(f)

    f.Show()
    app.MainLoop()
