'''
Created on 26-Jan-2019

@author: vijay
'''
#!/usr/bin/python
from src.view.views.file.MainStcPanel import MainStc
import os
import sys

'''
Created on 13-Dec-2016

@author: vijay
'''

from src.view.util.FileOperationsUtil import FileOperations
import wx

# from src.view.table.CreateTable import CreateTableFrame
import logging.config
import wx.html2 as webview
import pypandoc
from src.view.constants import LOG_SETTINGS
from src.view.views.file.explorer._filetree import FileTree
from pubsub import pub
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD  
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
from pypandoc.pandoc_download import download_pandoc


pf = sys.platform
DEFAULT_TARGET_FOLDER = {
    "win32": "~\\AppData\\Local\\Pandoc",
    "linux": "~/bin",
    "darwin": "~/Applications/pandoc"
}
if os.path.isfile(DEFAULT_TARGET_FOLDER[pf]):
    download_pandoc()


class CreatingPandocPanel(wx.Panel):

    def __init__(self, parent=None, *args, filePath=None, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.fileOperations = FileOperations()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self._nb = aui.AuiNotebook(self)
        self.filePath = filePath
        text = FileOperations().readFile(filePath=filePath)
        self.htmlPanel = HtmlPanel(self, text=text)
        self.markdownSourcePanel = MarkdownSourcePanel(self, text=text)
        self.htmlSrc = HtmlSrcPanel(self, text=text)
        self._nb.AddPage(self.markdownSourcePanel, 'Src') 
        self._nb.AddPage(self.htmlPanel, 'HTML') 
        self._nb.AddPage(self.htmlSrc, 'HTML Src') 
        self._nb.Split(0, wx.LEFT)
        self._nb.Split(1, wx.RIGHT)
        self._nb.Split(2, wx.DOWN)
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

    def GetModify(self):
        
        return False
    
    def getHtmlFromMarkdown(self, markdownText=None):

        htmlsrc = pypandoc.convert_text(markdownText,'html', format='md', extra_args=['--atx-headers'])
        return htmlsrc
        
#---------------------------------------------------------------------------


class HtmlSrcPanel(wx.Panel):

    def __init__(self, parent=None, *args, text=None, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        pub.subscribe(self.setPage, 'setPage')
        self.parent = parent 
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        htmlsrc = self.GetParent().getHtmlFromMarkdown(text)
        self.stc = MainStc(self, text=htmlsrc)

        sizer.Add(self.stc, 1, wx.EXPAND)
        ####################################################################
        
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

    def setPage(self, markdownText=None, baseUrl='/'):
        try:
            window=None
            if isinstance(self.GetParent(), CreatingPandocPanel):
                window=self.GetParent()
            elif isinstance(self.GetParent().GetParent(), CreatingPandocPanel):
                window=self.GetParent().GetParent()
            html = window.getHtmlFromMarkdown(markdownText)
            self.stc.SetText(html)
        except Exception as e:
            logger.error(e)


    
class HtmlPanel(wx.Panel):

    def __init__(self, parent=None, *args, text=None, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent 
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        pub.subscribe(self.setPage, 'setPage')
        self.wv = webview.WebView.New(self)
        if self.GetParent().filePath:
            baseUrl = self.GetParent().filePath
        self.setPage(markdownText=text, baseUrl=baseUrl)
        
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.wv, 1, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        
    def setPage(self, markdownText=None, baseUrl='/'):
        
        if markdownText:
            window=None
            if isinstance(self.GetParent(), CreatingPandocPanel):
                window=self.GetParent()
            elif isinstance(self.GetParent().GetParent(), CreatingPandocPanel):
                window=self.GetParent().GetParent()
            htmlsrc = window.getHtmlFromMarkdown(markdownText)
            self.wv.SetPage(htmlsrc, baseUrl)
            self.GetTopLevelParent().FindFocus()
            self.GetParent().FindFocus()
            print(self.GetTopLevelParent().FindFocus())


class MarkdownSourcePanel(wx.Panel):

    def __init__(self, parent=None, *args, text=None, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent 
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.stc = MainStc(self, text=text)
        sizer.Add(self.stc, 1, wx.EXPAND)
        ####################################################################
        
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


    def loadFile(self, path):
        self.stc.LoadFile(path)


if __name__ == '__main__':

    app = wx.App(False)
    frame = wx.Frame(None)
    try: 
        panel = CreatingPandocPanel(frame, title='asfd', filePath=r'c:\1\sql_editor\README.md')
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
