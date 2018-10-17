
import wx
import logging.config
from src.view.sql_editor_view import DatabaseMainFrame
from src.view.constants import LOG_SETTINGS

logger = logging.getLogger('extensive')


logging.config.dictConfig(LOG_SETTINGS)



def main():
    app = wx.App()
    frame = DatabaseMainFrame(None)
    frame.Show()
    app.MainLoop()




if __name__ == '__main__':
    main()
