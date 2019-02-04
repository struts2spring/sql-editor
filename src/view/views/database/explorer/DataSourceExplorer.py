'''
Created on Jan 30, 2019

@author: xbbntni
'''

import wx
import ntpath
from src.view.views.database.explorer.databaseTree import DatabaseTree

from wx.lib.pubsub import pub
import logging.config
from src.view.constants import LOG_SETTINGS
import os
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

class DataSourcePanel(wx.Panel):
    
    
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################

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
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

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
                    obj = sqlExecuter.getObject()
                    if len(obj[1]) == 0:
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
