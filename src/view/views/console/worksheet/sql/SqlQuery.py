'''
Created on 22-Mar-2019

@author: vijay
'''
import wx
from src.view.util.FileOperationsUtil import FileOperations


class SqlQueryFrame(wx.Frame):

    def __init__(self, parent, Id=wx.ID_ANY, Title="", sqlText=None, pos=wx.DefaultPosition,
             size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER | wx.STAY_ON_TOP):
        style = style & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, parent, Id, Title, pos, size, style)

        self.fileOperations = FileOperations()
        # set frame icon
        icon = wx.Icon()
        icon.CopyFromBitmap(self.fileOperations.getImageBitmap(imageName='eclipse16.png'))
        self.SetIcon(icon)
        sizer = wx.BoxSizer(wx.VERTICAL)
        ####################################################################

        self.sqlQueryPanel = SqlQueryPanel(self, sqlText)
        ####################################################################

        sizer.Add(self.sqlQueryPanel, 1, wx.EXPAND)
        self.BindEvents()
        self.Show(show=True)

    def BindEvents(self):
#         self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)

    def OnCloseWindow(self, event):
#         self._mgr.UnInit()
        event.Skip()
        self.Destroy()

    def OnKeyUP(self, event):
#         print "KEY UP!"
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip()


class SqlQueryPanel(wx.Panel):

    def __init__(self, parent, sqlText=None, style=wx.TR_DEFAULT_STYLE | wx.BORDER_NONE):
        super(SqlQueryPanel, self).__init__()
        wx.Panel.__init__(self, parent, -1, style=style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.sqlText = sqlText
        page = wx.TextCtrl(self, -1, self.sqlText, style=wx.TE_MULTILINE)
        ####################################################################
        sizer.Add(page, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Center()
#         self.createStatusBar()
        self.Show(True)


if __name__ == '__main__':
    app = wx.App()
    frm = SqlQueryFrame(None, size=(400, 300))
#     pnl = SqlQueryPanel(frm)
    frm.Show()
    app.MainLoop()
