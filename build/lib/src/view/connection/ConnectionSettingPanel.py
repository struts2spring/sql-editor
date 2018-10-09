'''
Created on 05-Feb-2017

@author: vijay
'''
import wx



class CreatingConnectionSettingFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(400, 300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        
#         self.pnl = pnl = MainPanel(self)        
#         self.newConnectionFrame = CreatingNewConnectionPanel(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        self.Show()
    def OnCloseFrame(self, event):
        logger.debug('OnCloseFrame')
        self.OnExitApp(event)
    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        logger.debug('OnExitApp')
        self.Destroy()

#---------------------------------------------------------------------------
      
if __name__ == '__main__':
    app = wx.App(False)
    frame = CreatingConnectionSettingFrame(None, 'Connection settings')
    app.MainLoop()
