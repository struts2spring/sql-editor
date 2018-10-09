'''
Created on May 1, 2017

@author: vijay
'''
import wx
import wx.stc as stc
import logging

logger = logging.getLogger('extensive')

class SqlScriptOutputPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        self.text = stc.StyledTextCtrl(self, -1)
#         self.text.initKeyShortCut()
        self.text.SetText('')
        self.text.EmptyUndoBuffer()
        self.text.Colourise(0, -1)
        self.text.SetInitialSize(wx.Size(400, 400))
#         self.sstc.SetBestFittingSize(wx.Size(400, 400))

        # line numbers in the margin
        self.text.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.text.SetMarginWidth(1, 25)
        self.text.SetWindowStyle(self.text.GetWindowStyle() | wx.DOUBLE_BORDER)
        self.text.StyleSetSpec(stc.STC_STYLE_DEFAULT, "size:10,face:Courier New")
#         self.text.SetWrapMode(stc.STC_WRAP_WORD)
#         self.text.SetMarginLeft(50)
        ####################################################################
        vBox.Add(self.text , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = SqlScriptOutputPanel(frame)
    frame.Show()
    app.MainLoop()
