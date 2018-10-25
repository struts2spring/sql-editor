import wx



'''
Create tabs with 
Columns, Indexes, Data, References, Triggers, SQL, ER diagram

Columns Tab:
    should have tablualted data with columns
    Position #, Name, Datatype, Nullable,Auto increment, Default data, 
Indexes Tab:
    Index Name, Table, Index Type, Ascending, Unique, Qualifier, Cardinality, Index Description
Data Tab:
    Table data with 20 row.

References Tab:
    Name , Owner, Ref Table, Type, Ref Object, On Delete, On Update, Deferability
ER diagram Tab:
    
Triggers Tab:
    Name, Table, Description
SQL Tab:
    sql stamt 
    create table
    create index
    

'''

class CreatingTableInfoFrame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(500, 200),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.SetMinSize((400, 100))
        sizer = wx.BoxSizer(wx.VERTICAL)        
        # self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        
        
        self.creatingTableInfoPanel = CreatingTableInfoPanel(self)
        ####################################################################
        
        sizer.Add(self.creatingTableInfoPanel, 1, wx.EXPAND)
        # sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        
        self.SetSizer(sizer)
        self.Center()
#         self.createStatusBar()
        self.Show(True)

    def OnCloseFrame(self, event):
        self.Destroy()  
class CreatingTableInfoPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        ####################################################################
        # vBox.Add(worksheetToolbar , 0, wx.EXPAND | wx.ALL, 0)
        # vBox.Add(self.worksheetPanel , 1, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)  

if __name__ == '__main__':
    
    app = wx.App(False)
    frame = CreatingTableInfoFrame(None, 'Open Existing Connection')
    frame.Show()
    app.MainLoop()
