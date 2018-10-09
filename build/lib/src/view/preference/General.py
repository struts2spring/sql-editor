# from src.logic.search_book import FindingBook
import wx
from wx.lib.expando import ExpandoTextCtrl
from src.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel
# from src.ui.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel


class Window(wx.App):
    def __init__(self, book=None):
        wx.App.__init__(self)
        self.init_ui()
        self.mainWindow.Show()

    def init_ui(self):
        self.mainWindow = wx.Frame(None)
        self.mainWindow.SetSize((800, 510))
        panel = GeneralPreferencePanel(self.mainWindow)
        
class GeneralPreferencePanel(wx.Panel):
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
        
        self.systemTray = wx.CheckBox(self, -1, "Enable system tray icon (needs restart)", style=wx.ALIGN_RIGHT)
        
        sampleList = ['Title', 'authors', 'comment', 'publisher', 'rating']

        self.fieldsUnderCoverLabel=wx.StaticText(self, -1, "Field to show under cover.", (45, 15))

        lb = wx.CheckListBox(self, -1, (80, 50), wx.DefaultSize, sampleList)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, lb)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, lb)
        lb.SetSelection(0)
        self.lb = lb
 
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.systemTray, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3.Add(self.fieldsUnderCoverLabel, 0, wx.EXPAND|wx.ALL,4)
        hBox3.Add(self.lb , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        

        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel=ApplyResetButtonPanel(self)
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
        

    def EvtListBox(self, event):
        print ('EvtListBox: %s\n' % event.GetString())

    def EvtCheckListBox(self, event):
        index = event.GetSelection()
        label = self.lb.GetString(index)
        status = 'un'
        if self.lb.IsChecked(index):
            status = ''
        print ('Box %s is %schecked \n' % (label, status))
        self.lb.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
 

if __name__ == "__main__":
#     books = FindingBook().findAllBooks()
#     book = None
#     for b in books:
#         book = b
#         break
#     print book
    app = Window()
    app.MainLoop()
