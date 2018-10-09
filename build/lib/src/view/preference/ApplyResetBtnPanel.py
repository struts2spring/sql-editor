import wx


class ApplyResetButtonPanel(wx.Panel):
    
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.HORIZONTAL)
        self.resetButton=wx.Button(self, 1, 'Restore defaults', (50, 130))
        self.applyButton=wx.Button(self, 1, 'Apply', (50, 130))
        vBox.Add(self.resetButton, 0,flag=wx.RIGHT)
        vBox.Add(self.applyButton, 0, flag=wx.RIGHT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox , 0, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.SetSizer(sizer)
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.onResetButton, id=wx.ID_ANY)
        self.Bind(wx.EVT_BUTTON, self.onApplyButton, id=wx.ID_ANY)
    def onResetButton(self, event):
        print('reset button')
    def onApplyButton(self, event):
        print('apply button')