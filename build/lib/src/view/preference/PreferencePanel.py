import wx
from src.view.preference.CommandList import CommandKeyListCtrlPanel
from src.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel

from sys import exc_info
import logging

logger = logging.getLogger('extensive')


class UserPanel(wx.Panel):
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
        
        self.isPaginationCheckBox = wx.CheckBox(self, -1, "Pagination enable result:", style=wx.ALIGN_RIGHT)
        
        self.pageSizeLabel = wx.StaticText(self, -1, "Number of search result per page:")
        self.pageSizeText = wx.TextCtrl(self, -1, "100", (30, 50), (60, -1))
        h = self.pageSizeText.GetSize().height
        w = self.pageSizeText.GetSize().width + self.pageSizeText.GetPosition().x + 2
        self.spin = wx.SpinButton(self, -1, (w, 50), (h * 2 / 3, h), wx.SP_VERTICAL)
        self.spin.SetRange(1, 100)
        self.spin.SetValue(1) 
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.isPaginationCheckBox , 0, wx.EXPAND | wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(self.pageSizeLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        hBox2.Add(self.pageSizeText, 0, wx.EXPAND | wx.ALL)
        hBox2.Add(self.spin , 0, wx.EXPAND | wx.ALL)
        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)

        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel=ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        
        ####################################################################        
        vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox2, 0, wx.EXPAND | wx.ALL, 5)
        vBoxBody.Add(hBox3, 0, wx.EXPAND | wx.ALL, 1)
#         vBox.Add(hBox4, 0, wx.EXPAND | wx.ALL, 1)
        
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_SPIN, self.OnSpin, self.spin)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.isPaginationCheckBox)
    def OnSpin(self, event):
        self.pageSizeText.SetValue(str(event.GetPosition()))
    
    def EvtCheckBox(self, event):
        print(self.isPaginationCheckBox)
        print ('EvtCheckBox: %d\n' % event.IsChecked())
        cb = event.GetEventObject()
        if cb.Is3State():
            print ("\t3StateValue: %s\n" % cb.Get3StateValue())

class SearchPanel(wx.Panel):
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
        
#         self.isPaginationEnableLabel = wx.StaticText(self, -1, "Pagination enable result:") 
        self.isPaginationCheckBox = wx.CheckBox(self, -1, "Pagination enable result:", style=wx.ALIGN_RIGHT)
        
#         bookNameLabel = wx.StaticText(self, -1, "Title:") 
#         bookName = wx.TextCtrl(self, -1, "", size=(150, -1));
#         
#         booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
#         bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

        self.pageSizeLabel = wx.StaticText(self, -1, "Number of search result per page:")
        self.pageSizeText = wx.TextCtrl(self, -1, "100", (30, 50), (60, -1))
        h = self.pageSizeText.GetSize().height
        w = self.pageSizeText.GetSize().width + self.pageSizeText.GetPosition().x + 2
        self.spin = wx.SpinButton(self, -1, (w, 50), (h * 2 / 3, h), wx.SP_VERTICAL)
        self.spin.SetRange(1, 100)
        self.spin.SetValue(1) 
        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel=ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        
        ####################################################################        
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox1.Add(self.isPaginationEnableLabel , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox1.Add(self.isPaginationCheckBox , 0, wx.EXPAND | wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(self.pageSizeLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        hBox2.Add(self.pageSizeText, 0, wx.EXPAND | wx.ALL)
        hBox2.Add(self.spin , 0, wx.EXPAND | wx.ALL)
        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)

#         hBox3.Add(booShortkNameLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox3.Add(bookShortName, 0, wx.EXPAND|wx.ALL)
        
#         hBox4 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox4.Add(numberOfPagesLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox4.Add(numberOfPages, 0, wx.EXPAND | wx.ALL)
        
        vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox2, 0, wx.EXPAND | wx.ALL, 5)
        vBoxBody.Add(hBox3, 0, wx.EXPAND | wx.ALL, 1)
#         vBox.Add(hBox4, 0, wx.EXPAND | wx.ALL, 1)
        
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_SPIN, self.OnSpin, self.spin)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.isPaginationCheckBox)
    def OnSpin(self, event):
        self.pageSizeText.SetValue(str(event.GetPosition()))
    
    def EvtCheckBox(self, event):
        print(self.isPaginationCheckBox)
        print('EvtCheckBox: %d\n' % event.IsChecked())
        cb = event.GetEventObject()
        if cb.Is3State():
            print ("\t3StateValue: %s\n" % cb.Get3StateValue())

class WorkspacePanel(wx.Panel):
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
        ####################################################################)
        
        self.workspacePathLabel = wx.StaticText(self, -1, "Workspace path:") 
        self.workspacePathText = wx.TextCtrl(self, -1, "/docs/new", size=(150, -1));
        self.workspacePathText.SetHelpText("Workspace Path")
        self.workspacePathText.SetBackgroundColour("light Gray")
        self.workspacePathText.SetBackgroundStyle(wx.TE_READONLY)
        
#         bookNameLabel = wx.StaticText(self, -1, "Title:") 
#         bookName = wx.TextCtrl(self, -1, "", size=(150, -1));
#         
#         booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
#         bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

#         authorsLabel = wx.StaticText(self, -1, "Authors:") 
#         authorName = wx.TextCtrl(self, -1, "", size=(50, -1));
#         
#         numberOfPagesLabel = wx.StaticText(self, -1, "Number of pages:") 
#         numberOfPages = wx.TextCtrl(self, -1, "", size=(70, -1));
#         
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.workspacePathLabel , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox1.Add(self.workspacePathText , 0, wx.EXPAND | wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
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
        self.applyResetButtonPanel=ApplyResetButtonPanel(self)
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
        toolbarStyleBox = wx.StaticBox(self,-1,"Toolbar styles")
        boxSizer = wx.StaticBoxSizer(toolbarStyleBox,wx.VERTICAL)
        self.showToolbarIcons = wx.CheckBox(self,-1,'Show toolbar icons')
        boxSizer.Add(self.showToolbarIcons)
        self.showToolbarText = wx.CheckBox(self,-1,'Show toolbar text')
        boxSizer.Add(self.showToolbarText)
        self.showToolbar = wx.CheckBox(self,-1,'Show toolbar')
        boxSizer.Add(self.showToolbar)
        
        
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.themeCb)

        
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.themeLabel , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox1.Add(self.themeCb , 0, wx.EXPAND | wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2.Add(boxSizer,0,wx.ALL,10)
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
        self.applyResetButtonPanel=ApplyResetButtonPanel(self)
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
        print ('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))

        if evt.GetString() == 'one':
            print ("You follow directions well!\n\n")

class KeysPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBoxHeader = wx.BoxSizer(wx.VERTICAL)
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
        try:
            self.commandKeyListCtrlPanel = CommandKeyListCtrlPanel(self) 
        except Exception as e:
            logger.error(e, exc_info=True)
        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel=ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        
        ####################################################################
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(self.commandKeyListCtrlPanel, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)
            # When the user selects something, we go here.
    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
        data = cb.GetClientData(evt.GetSelection())
        print ('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))

        if evt.GetString() == 'one':
            print ("You follow directions well!\n\n")

class PreferencePanel(wx.Panel):
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
        
#         bookNameLabel = wx.StaticText(self, -1, "Title:") 
#         bookName = wx.TextCtrl(self, -1, "", size=(150, -1));
        
#         booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
#         bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

#         authorsLabel = wx.StaticText(self, -1, "Authors:") 
#         authorName = wx.TextCtrl(self, -1, "", size=(50, -1));
        
#         numberOfPagesLabel = wx.StaticText(self, -1, "Number of pages:") 
#         numberOfPages = wx.TextCtrl(self, -1, "", size=(70, -1));
        
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox1.Add(bookNameLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox1.Add(bookName, 0, wx.EXPAND | wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
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
        self.applyResetButtonPanel=ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        
        ####################################################################        
        vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox2, 0, wx.EXPAND | wx.ALL, 5)
        vBoxBody.Add(hBox3, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox4, 0, wx.EXPAND | wx.ALL, 1)
        
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = SearchPanel(frame, preferenceName='asfd')
    frame.Show()
    app.MainLoop()
