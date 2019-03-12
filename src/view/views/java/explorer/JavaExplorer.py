#!/usr/bin/python
'''
Created on Jan 10, 2019

@author: vijay
'''

from src.view.util.FileOperationsUtil import FileOperations
import wx


# from src.view.table.CreateTable import CreateTableFrame
import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.views.file.explorer._filetree import FileTree

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class CreatingJavaExplorerPanel(FileTree):

    def __init__(self, parent, size=wx.DefaultSize):
        super(CreatingJavaExplorerPanel, self).__init__(parent)
        try:
            self.AddWatchDirectory("c:\\1")
        except :
            pass
        self.Bind(wx.EVT_MENU, self.OnMenu)

    def OnMenu(self, evt):
        """Handle the context menu events for performing
        filesystem operations

        """
        e_id = evt.Id
        path = self._menu.GetUserData('active_node')
        paths = self._menu.GetUserData('selected_nodes')
#---------------------------------------------------------------------------
if __name__ == '__main__':
#     treeImageLevel = dict()
#     treeImageLevel[(0, 0)] = (0, 'database.png')
#     treeImageLevel[(1, 0)] = (0, 'database_category.png')
#     treeImageLevel[(1, 1)] = (0, 'folder_view.png')
#     treeImageLevel[(1, 2)] = (0, 'folder.png')
#
#     print(treeImageLevel[(0, 0)])
    app = wx.App(False)
    frame = wx.Frame(None)
    try:
        panel = CreatingJavaExplorerPanel(frame)
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
