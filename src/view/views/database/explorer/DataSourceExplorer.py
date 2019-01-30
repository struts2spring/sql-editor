'''
Created on Jan 30, 2019

@author: xbbntni
'''

import wx

from src.view.views.database.explorer._databaseTree import DatabaseTree

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
#         self.SetDropTarget(DatabaseFileDropTarget(self))
    #         self.tree.SetExpansionState(self.expansionState)

        ####################################################################
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


if __name__ == '__main__':
    app = wx.App(False)
    f = wx.Frame(None)
    ft = DataSourcePanel(f)

    f.Show()
    app.MainLoop()
