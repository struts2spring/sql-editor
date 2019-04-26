'''
Created on 25-Apr-2019

@author: vijay
'''

import wx

class ProjectFromFolderPanel(wx.Panel):

    def __init__(self, parent=None, name='', *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBoxHeader = wx.BoxSizer(wx.VERTICAL)
        vBoxBody = wx.BoxSizer(wx.VERTICAL)
        vBoxFooter = wx.BoxSizer(wx.VERTICAL)
        ####################################################################


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = ProjectFromFolderPanel(frame, name='General')
    frame.Show()
    app.MainLoop()
