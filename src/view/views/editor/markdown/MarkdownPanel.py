'''
Created on 26-Jan-2019

@author: vijay
'''
#!/usr/bin/python
from src.view.views.file.MainStcPanel import MainStc
import os
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
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD  
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class CreatingMarkdownPanel(wx.Panel):

    def __init__(self, parent=None, filePath=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.fileOperations = FileOperations()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self._nb = aui.AuiNotebook(self)
        self.markdownSourcePanel = MarkdownSourcePanel(self, filePath=filePath)
        self.htmlPanel = HtmlPanel(self)
        self._nb.AddPage(self.markdownSourcePanel, 'src') 
        self._nb.AddPage(self.htmlPanel, 'html') 
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

    def GetModify(self):
        
        return False
#---------------------------------------------------------------------------


class HtmlPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent 
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


class MarkdownSourcePanel(wx.Panel):

    def __init__(self, parent=None, *args, filePath=None, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent 
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        text = ''
        if filePath:
            fileExtension = filePath.split('.')[-1]
            text = FileOperations().readFile(filePath=filePath)
            self.stc = MainStc(self, text=text)
            self.stc.SetFileName(filePath)
            self.stc.SetModTime(os.path.getmtime(filePath))
    #                 mainStc.SetText(FileOperations().readFile(filePath=fileWithImage[0]))
            self.stc.ConfigureLexer(fileExtension)
            self.stc.SetModified(False)
    #             imageName = self.iconManager.getFileImageNameByExtension(fileExtension)
    #             (name, captionName) = self.getTitleString(stc=mainStc, path=fileWithImage[0])
            self.stc.SetSavePoint()
            sizer.Add(self.stc, 1, wx.EXPAND)
        ####################################################################
        
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


if __name__ == '__main__':

    app = wx.App(False)
    frame = wx.Frame(None)
    try: 
        panel = CreatingMarkdownPanel(frame, title='asfd')
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
