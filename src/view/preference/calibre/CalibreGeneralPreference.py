'''
Created on Apr 10, 2019

@author: xbbntni
'''
# from src.logic.search_book import FindingBook
import wx
from wx.lib.expando import ExpandoTextCtrl
from src.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel
# from src.ui.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel
import logging.config
from src.view.constants import LOG_SETTINGS
import wx.lib.filebrowsebutton as filebrowse
logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)


class Window(wx.App):

    def __init__(self, preferenceName=None):
        wx.App.__init__(self)
        self.init_ui(preferenceName=preferenceName)
        self.mainWindow.Show()

    def init_ui(self, preferenceName=None):
        self.mainWindow = wx.Frame(None)
        self.mainWindow.SetSize((800, 510))
        panel = CalibreGeneralPreferencePanel(self.mainWindow, preferenceName=preferenceName)

        
class CalibreGeneralPreferencePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBoxHeader = wx.BoxSizer(wx.VERTICAL)
        vBoxBody = wx.BoxSizer(wx.VERTICAL)
        vBoxFooter = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        '''
        Header section
        '''
        self.st = wx.StaticLine(self, wx.ID_ANY)
        # Make and layout the controls
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs + 4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs + 2, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.header = wx.StaticText(self, -1, kw['preferenceName'])
        self.header.SetFont(bf)
        vBoxHeader.Add(self.header, 0, wx.ALL | wx.EXPAND, 5)
        vBoxHeader.Add(self.st, 0, wx.ALL | wx.EXPAND, 5)
        ####################################################################
        
#         self.runInBackground = wx.CheckBox(self, -1, "Always run in background", style=wx.ALIGN_LEFT)
#         self.next_previous = wx.CheckBox(self, -1, "Keep next/previous editor, view and perspectives dialog open", style=wx.ALIGN_LEFT)
#         self.showHeapStatus = wx.CheckBox(self, -1, "Show heap status", style=wx.ALIGN_LEFT)
#        
#         hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
#         l1 = wx.StaticText(self, -1, "Workbench save interval (in minutes): ") 
#         hbox1.Add(l1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5) 
#         self.t1 = wx.TextCtrl(self, value="5") 
#         hbox1.Add(self.t1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5) 
#         
#         box_title = wx.StaticBox(self, -1, "Open mode")
#         radio1 = wx.RadioButton(self, -1, " Double click ")
#         radio2 = wx.RadioButton(self, -1, " Single click ")
#         l2 = wx.StaticText(self, -1, "Note : This preference may not take effect on all views ") 
#         box = wx.StaticBoxSizer(box_title, wx.VERTICAL)
#         grid = wx.FlexGridSizer(cols=1)        
#         grid.Add(radio1, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT | wx.TOP, 5)
#         grid.Add(radio2, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT | wx.TOP, 5)
#         box.Add(grid, 0, wx.ALIGN_LEFT | wx.ALL, 5)
#         box.Add(l2 , 0, wx.ALIGN_LEFT | wx.ALL, 5)
#         
#         vBox1 = wx.BoxSizer(wx.VERTICAL)
#         vBox1.Add(self.runInBackground, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
#         vBox1.Add(self.next_previous, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
#         vBox1.Add(self.showHeapStatus, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
#         vBox1.Add(hbox1, 0, wx.EXPAND | wx.ALL, 5)
#         vBox1.Add(box, 0, wx.EXPAND | wx.ALL, 5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        self.dbb = filebrowse.DirBrowseButton(
            self, -1, size=(450, -1), changeCallback=self.dbbCallback, labelText="Library path:"
            )
        
        hbox1.Add(self.dbb, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)            

#         btn = wx.Button(self, wx.ID_HELP)
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)

        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel = ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        ####################################################################        
#         vBoxBody.Add(vBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hbox1, 0, wx.EXPAND | wx.ALL, 1)
        
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)

    def dbbCallback(self, evt):
        logger.debug('DirBrowseButton: %s\n' % evt.GetString())

    def apply(self, event):
        logger.debug('apply')
        

    def reset(self, event):
        logger.debug('reset')

    def EvtListBox(self, event):
        logger.debug('EvtListBox: %s\n' % event.GetString())

    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'un'
        if self.lb.IsChecked(index):
            status = ''
        print ('Box %s is %schecked \n' % (label, status))
        self.lb.SetSelection(index)  # so that (un)checking also selects (moves the highlight)
 

if __name__ == "__main__":

    app = Window(preferenceName="Calibre")
    app.MainLoop()
