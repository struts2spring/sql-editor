'''
Created on Apr 5, 2019

@author: vijay
'''

import wx
from src.view.views.calibre.book.browser.BookThumbPagination import ThumbnailCtrlPaginationPanel

import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

class BookBrowserPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        thumbnailCtrlPaginationPanel = ThumbnailCtrlPaginationPanel(self)
        ####################################################################
        vBox.Add(thumbnailCtrlPaginationPanel , 1, wx.EXPAND | wx.ALL)
#         vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


if __name__ == '__main__':

    app = wx.App(False)
    frame = wx.Frame(None)
    try:
        panel = BookBrowserPanel(frame)
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
