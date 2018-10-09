'''
Created on 17-Dec-2016

@author: vijay
'''
import wx



class CreatingWorksheetToolbarPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = CreatingWorksheetToolbarPanel(frame)
    frame.Show()
    app.MainLoop()