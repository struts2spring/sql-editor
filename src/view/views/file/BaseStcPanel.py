
import wx
import wx.stc as stc

class BaseStc(stc.StyledTextCtrl):
    
    def __init__(self, parent, id_=wx.ID_ANY,
             pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        
        stc.StyledTextCtrl.__init__(self, parent, id_, pos, size, style)