'''
Created on Nov 20, 2018

@author: xbbntni
'''
import wx.adv
import os
import wx.lib.eventStack as events
from src.view.sql_editor_view import DatabaseMainFrame
from wx._adv import SplashScreen
from src.view.util.FileOperationsUtil import FileOperations

# def opj(path):
#     """Convert paths to the platform-specific separator"""
#     st = os.path.join(*tuple(path.split('/')))
#     # HACK: on Linux, a leading / gets lost...
#     if path.startswith('/'):
#         st = '/' + st
#     return st

class MySplashScreen(SplashScreen):
    def __init__(self):
#         bmp = wx.Image(opj("../images/splash.png")).ConvertToBitmap()
        self.fileOperations=FileOperations()
        bmp = self.fileOperations.getImageBitmap("splash.png")
        SplashScreen.__init__(self, bmp,
                                 wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                 2000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.CallLater(1, self.ShowMain)


    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()


    def ShowMain(self):
        frame = DatabaseMainFrame(None)
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()
#         wx.CallAfter(frame.ShowTip)

class MyApp(wx.App, events.AppEventHandlerMixin):
    def __init__(self, *args, **kargs):
        wx.App.__init__(self, *args, **kargs)
        events.AppEventHandlerMixin.__init__(self)
        
    def OnInit(self):
        """Initialize the Editor
        
        @note: this gets called before __init__
        @postcondition: custom artprovider and plugins are loaded

        """
        splash = MySplashScreen()
        splash.Show()

        return True
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
