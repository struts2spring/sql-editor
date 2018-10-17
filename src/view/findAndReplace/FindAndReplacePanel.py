'''
Created on 05-Feb-2017

@author: vijay
'''
import wx

import logging, logging.config
from src.view.constants import LOG_SETTINGS

logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)


class CreatingFindAndReplaceFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(350, 400),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        
#         self.pnl = pnl = MainPanel(self)        
        self.findAndReplacePanel = CreatingFindAndReplacePanel(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        self.Show()

    def OnCloseFrame(self, event):
        logger.debug('OnCloseFrame')
        self.OnExitApp(event)

    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        logger.debug('OnExitApp')
        if self.GetParent():
            self.GetParent().frame = None
        self.Destroy()


#---------------------------------------------------------------------------
class CreatingFindAndReplacePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.findText = ''
        self.replaceText = ''
        vBox = wx.BoxSizer(wx.VERTICAL)
        try:
            import  wx.lib.rcsizer  as rcs
        except Exception as e:
            logger.error(e, exc_info=True)
        rowColumnSizer = rcs.RowColSizer()
#         sizer = wx.GridBagSizer(hgap=3, vgap=3)
        sizer = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        
        h1.Add((1, 1), -1, wx.ALL)  # this is a spacer
        schemaNameLabel = wx.StaticText(self, -1, "F&ind:               ")
        schemaNameText = wx.TextCtrl(self, -1, self.findText, size=(400, -1))
        
        tableNameLabel = wx.StaticText(self, -1, "Replace with:")
        tableNameText = wx.TextCtrl(self, -1, self.replaceText, size=(400, -1))
        
        h1.Add(schemaNameLabel, 0, wx.ALL, 2)
        h1.Add(schemaNameText, 0, wx.ALL, 2)
        
        h2.Add((1, 1), -1, wx.ALL)  # this is a spacer
        h2.Add(tableNameLabel, 0, wx.ALL, 2)
        h2.Add(tableNameText, 0, wx.ALL, 2)
        
        directionRadioBox = wx.RadioBox(self, -1, "Direction", (10, 10), wx.DefaultSize, ['Forward', 'Backword'], 1, wx.RA_SPECIFY_COLS)
        scopeRadioBox = wx.RadioBox(self, -1, "Scope", (10, 10), wx.DefaultSize, ['All', 'Selected lines'], 1, wx.RA_SPECIFY_COLS)

        # first the static box
        box_10 = wx.StaticBox(self, -1, 'Options')
        cb1 = wx.CheckBox(box_10, -1, "Case sensitive", (35, 40), (150, 20))
        cb2 = wx.CheckBox(box_10, -1, "Wra&p search", (35, 60), (150, 20))
        cb3 = wx.CheckBox(box_10, -1, "&Incremental", (35, 80), (150, 20))
        cb4 = wx.CheckBox(box_10, -1, "Regular expressions", (35, 80), (150, 20))
        cb5 = wx.CheckBox(box_10, -1, "Whole word", (35, 80), (150, 20))
        # then the sizer
        staticBoxSizer_11 = wx.StaticBoxSizer(box_10, wx.VERTICAL)
        rowColumnSizer1 = rcs.RowColSizer()
        rowColumnSizer1.Add(cb1, row=1, col=1)
        rowColumnSizer1.Add(cb2, row=2, col=1)
        rowColumnSizer1.Add(cb3, row=3, col=1)
#         rowColumnSizer1.Add( (2,2),row=1, col=2)
        rowColumnSizer1.Add(cb4, row=2, col=2)
        rowColumnSizer1.Add(cb5, row=3, col=2)
        staticBoxSizer_11.Add(rowColumnSizer1)
#         staticBoxSizer_11.AddMany( [ cb1,
#                  cb2,
#                  cb3,
#                  cb4,
#                  cb5
#                  ])
#         sizer.AddGrowableCol(0)
#         sizer.AddGrowableCol(1)

        self.findButton = wx.Button(self, -1, "Find", pos=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.onFindClicked, self.findButton)
        self.findButton.SetDefault()
        
        self.replaceButton = wx.Button(self, -1, "Replace", pos=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.onReplaceClicked, self.replaceButton)
        self.replaceButton.SetDefault()
        
        self.replaceFindButton = wx.Button(self, -1, "Replace/Fin&d", pos=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.onReplaceFindClicked, self.replaceFindButton)
        self.replaceFindButton.SetDefault()
        
        self.replaceAllButton = wx.Button(self, -1, "Replace &All", pos=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.onReplaceAllClicked, self.replaceAllButton)
        self.replaceAllButton.SetDefault()
        
        self.closeButton = wx.Button(self, -1, "Close", pos=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnExitApp, self.closeButton)
        self.closeButton.SetDefault()
        
        rowColumnSizer.Add(self.findButton, row=1, col=1)
        rowColumnSizer.Add(self.replaceButton, row=2, col=1)
        rowColumnSizer.Add(self.replaceFindButton, row=1, col=2)
        rowColumnSizer.Add(self.replaceAllButton, row=2, col=2)
        rowColumnSizer.Add(self.closeButton, row=3, col=2)
        
        hbox000 = wx.BoxSizer(wx.HORIZONTAL)
        hbox000.Add((2, 2), 1, wx.EXPAND | wx.ALL , 2) 
        hbox000.Add(rowColumnSizer)
        
        vBox.Add(h1, 0, wx.EXPAND , 0)  
        vBox.Add(h2, 0, wx.EXPAND , 0)  
        
        hbox001 = wx.BoxSizer(wx.HORIZONTAL)
        hbox001.Add(directionRadioBox, 1, wx.EXPAND | wx.ALL , 2)  
        hbox001.Add(scopeRadioBox, 1, wx.EXPAND | wx.ALL , 2)  
        vBox.Add(hbox001, 0, wx.EXPAND | wx.ALL, 0)  
        vBox.Add(staticBoxSizer_11, 0, wx.EXPAND , 0)  
        vBox.Add(rowColumnSizer, 0, wx.LEFT , 0)  
#         vBox.Add(vBox1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
#         vBox.Add(self.tb, 0, wx.EXPAND)
#         vBox.Add(self.list, 1, wx.EXPAND)
        ####################################################################
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)       
        
    def onFindClicked(self, event):
        logger.debug('onFindClicked: ' + self.findText) 

    def onReplaceClicked(self, event):
        logger.debug('onReplaceClicked') 

    def onReplaceFindClicked(self, event):
        logger.debug('onReplaceFindClicked') 

    def onReplaceAllClicked(self, event):
        logger.debug('onReplaceAllClicked') 

    def setFindText(self):
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                self.findText.SetValue(do.GetText())
#---------------------------------------------------------------------------

      
if __name__ == '__main__':
    app = wx.App(False)
    frame = CreatingFindAndReplaceFrame(None, 'Find / Replace')
    frame.Show()
    app.MainLoop()

