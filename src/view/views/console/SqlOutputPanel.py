'''
Created on May 1, 2017

@author: vijay
'''
import wx
import wx.stc as stc
from src.view.views.console.worksheet.EditorPanel import SqlStyleTextCtrl

import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class SqlConsoleOutputPanel(wx.Panel):

    def __init__(self, parent, size=wx.DefaultSize, data=''):
        super().__init__(parent, id=-1, size=size)
        wx.Panel.__init__(self, parent, id=-1, size=size)
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        self.text = SqlStyleTextCtrl(self, -1, size=size)
#         self.text.initKeyShortCut()
        if not data:
            data = ''
        self.text.SetText(data)
        self.text.EmptyUndoBuffer()
        self.text.Colourise(0, -1)
#         self.text.SetInitialSize(wx.Size(400, 400))
#         self.sstc.SetBestFittingSize(wx.Size(400, 400))

        # line numbers in the margin
        self.text.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.text.SetMarginWidth(1, 25)
        self.text.SetWindowStyle(self.text.GetWindowStyle() | wx.DOUBLE_BORDER)
        self.text.StyleSetSpec(stc.STC_STYLE_DEFAULT, "size:10,face:Courier New")
#         self.text.SetWrapMode(stc.STC_WRAP_WORD)
#         self.text.SetMarginLeft(50)
        ####################################################################
        vBox.Add(self.text , 1, wx.EXPAND | wx.ALL, 1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = SqlConsoleOutputPanel(frame, size=(100, 100), data='abc')
    frame.Show()
    app.MainLoop()
