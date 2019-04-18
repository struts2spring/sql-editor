import wx
import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
################################################


class ApplyCloseButtonPanel(wx.Panel):
    
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.applyCloseButton = wx.Button(self, -1, 'Apply and Close', (50, 130))
        self.cancelButton = wx.Button(self, -1, 'Cancel', (50, 130))
        hBox.Add(self.applyCloseButton, 0, flag=wx.RIGHT)
        hBox.Add(self.cancelButton, 0, flag=wx.RIGHT)
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(hBox , 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 0)
#         self.SetSizer(sizer)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND | wx.ALIGN_RIGHT  , 0)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.onApplyCloseButton, self.applyCloseButton)
        self.Bind(wx.EVT_BUTTON, self.onCancelButton, self.cancelButton)

    def onApplyCloseButton(self, event):
        logger.debug('onApplyCloseButton')
#         self.GetParent().reset(event)

    def onCancelButton(self, event):
        logger.debug('onCancelButton')
        self.GetTopLevelParent().Close()
#         self.GetParent().apply(event)
        
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    ApplyCloseButtonPanel(frame)
    frame.Show(show=True)
    app.MainLoop()
    
