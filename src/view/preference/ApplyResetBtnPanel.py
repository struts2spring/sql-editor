import wx
import logging.config
from src.view.constants import LOG_SETTINGS


logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
################################################

class ApplyResetButtonPanel(wx.Panel):
    
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.resetButton=wx.Button(self, 1, 'Restore Defaults', (50, 130))
        self.applyButton=wx.Button(self, 1, 'Apply', (50, 130))
        hBox.Add(self.resetButton, 0,flag=wx.RIGHT)
        hBox.Add(self.applyButton, 0, flag=wx.RIGHT)
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(hBox , 0,wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP,0)
#         self.SetSizer(sizer)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND | wx.ALIGN_RIGHT  , 0)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.onResetButton, id=wx.ID_ANY)
        self.Bind(wx.EVT_BUTTON, self.onApplyButton, id=wx.ID_ANY)
    def onResetButton(self, event):
        logger.debug('reset button')
    def onApplyButton(self, event):
        logger.debug('apply button')
        
        
if __name__=='__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    ApplyResetButtonPanel(frame)
    frame.Show(show=True)
    app.MainLoop()
    