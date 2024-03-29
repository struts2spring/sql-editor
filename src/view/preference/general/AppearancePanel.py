'''
Created on 16-Dec-2018

@author: vijay
'''

# from src.logic.search_book import FindingBook
import wx
from wx.lib.expando import ExpandoTextCtrl
from src.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel
# from src.ui.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel
import logging.config
from src.view.constants import LOG_SETTINGS

logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)


class Window(wx.App):

    def __init__(self, book=None):
        wx.App.__init__(self)
        self.init_ui()
        self.mainWindow.Show()

    def init_ui(self):
        self.mainWindow = wx.Frame(None)
        self.mainWindow.SetSize((800, 510))
        panel = AppearancePreferencePanel(self.mainWindow, preferenceName="Appearance")

        
class AppearancePreferencePanel(wx.Panel):

    def __init__(self, parent=None, name='', * args, **kw):
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

        self.header = wx.StaticText(self, -1, name)
        self.header.SetFont(bf)
        vBoxHeader.Add(self.header, 0, wx.ALL | wx.EXPAND, 5)
        vBoxHeader.Add(self.st, 0, wx.ALL | wx.EXPAND, 5)
        ####################################################################
        
        self.systemTray = wx.CheckBox(self, -1, "Enable system tray icon (needs restart)", style=wx.ALIGN_RIGHT)
        
        sampleList = ['Title', 'authors', 'comment', 'publisher', 'rating']

        self.fieldsUnderCoverLabel = wx.StaticText(self, -1, "Field to show under cover.", (45, 15))

        lb = wx.CheckListBox(self, -1, (80, 50), wx.DefaultSize, sampleList)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, lb)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, lb)
        lb.SetSelection(0)
        self.lb = lb
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.systemTray, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3.Add(self.fieldsUnderCoverLabel, 0, wx.EXPAND | wx.ALL, 4)
        hBox3.Add(self.lb , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel = ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        ####################################################################        
        vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox3, 0, wx.EXPAND | wx.ALL, 1)
        
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)
        
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

 
class AppearancePanel(wx.Panel):

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
        '''
        Body section
        '''
        self.themeLabel = wx.StaticText(self, -1, "Theme:") 
        # This combobox is created with a preset list of values.
        themeList = ['Classic', 'Dark']
        self.themeCb = wx.ComboBox(self, 500, "Classic", (90, 50),
                         (160, -1), themeList,
                         wx.CB_DROPDOWN
                         # | wx.TE_PROCESS_ENTER
                         # | wx.CB_SORT
                         )

#         sizer = wx.BoxSizer(wx.HORIZONTAL)
        toolbarStyleBox = wx.StaticBox(self, -1, "Toolbar styles")
        boxSizer = wx.StaticBoxSizer(toolbarStyleBox, wx.VERTICAL)
        self.showToolbarIcons = wx.CheckBox(self, -1, 'Show toolbar icons')
        boxSizer.Add(self.showToolbarIcons)
        self.showToolbarText = wx.CheckBox(self, -1, 'Show toolbar text')
        boxSizer.Add(self.showToolbarText)
        self.showToolbar = wx.CheckBox(self, -1, 'Show toolbar')
        boxSizer.Add(self.showToolbar)
        
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.themeCb)
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.themeLabel , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox1.Add(self.themeCb , 0, wx.EXPAND | wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(boxSizer, 0, wx.ALL, 10)
#         hBox2.Add(authorsLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox2.Add(authorName, 0, wx.EXPAND | wx.ALL)
        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)

#         hBox3.Add(booShortkNameLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox3.Add(bookShortName, 0, wx.EXPAND|wx.ALL)
        
        hBox4 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox4.Add(numberOfPagesLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox4.Add(numberOfPages, 0, wx.EXPAND | wx.ALL)
        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel = ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        ####################################################################        
        vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox2, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox3, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox4, 0, wx.EXPAND | wx.ALL, 1)
        
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)

            # When the user selects something, we go here.
    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
        data = cb.GetClientData(evt.GetSelection())
        logger.debug('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))

        if evt.GetString() == 'one':
            logger.debug("You follow directions well!\n\n")


if __name__ == "__main__":
#     books = FindingBook().findAllBooks()
#     book = None
#     for b in books:
#         book = b
#         break
#     print book
    app = Window()
    app.MainLoop()
