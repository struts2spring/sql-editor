'''
Created on 26-Jan-2019

@author: vijay
'''
#!/usr/bin/python
'''
Created on 13-Dec-2016

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


class CreatingMarkdownPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.fileOperations = FileOperations()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

#---------------------------------------------------------------------------
if __name__ == '__main__':

    app = wx.App(False)
    frame = wx.Frame(None)
    try: 
        panel = CreatingMarkdownPanel(frame, title='asfd')
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
