
import wx
import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.views.calibre.book.browser.BookThumbCrtl import ThumbnailCtrl, NativeImageHandler
import os

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class ThumbnailCtrlPaginationPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        thumbnailCtrl = ThumbnailCtrl(self, -1, imagehandler=NativeImageHandler)
        os.chdir(r'C:\Users\vijay\Pictures')
        thumbnailCtrl.ShowDir(os.getcwd())
        ####################################################################
        vBox.Add(thumbnailCtrl , 1, wx.EXPAND | wx.ALL)
#         vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    try:
        panel = ThumbnailCtrlPaginationPanel(frame)
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()