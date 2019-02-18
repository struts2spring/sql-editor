'''
Created on Feb 15, 2019

@author: xbbntni
'''

import wx
from src.view.util.FileOperationsUtil import FileOperations
from wx.lib.pubsub import pub
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD  
import logging.config
from src.view.constants import LOG_SETTINGS    
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class SearchPanelsFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, Title="", pos=wx.DefaultPosition,
             size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER|wx.STAY_ON_TOP):

        wx.Frame.__init__(self, parent, id, Title, pos, size, style)
        
        self.fileOperations = FileOperations()
#         pub.subscribe(self.__OnCellChange, 'OnCellChange')
        self._mgr = aui.AuiManager()
 
        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)
 
        # set frame icon
#         self.SetIcon(self.fileOperations.getImageBitmap(imageName='eclipse16.png'))
 
        # set up default notebook style
#         self._mgr._autoNBStyle = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0
 
        self.BuildPanes()
        self.BindEvents()
        self.Show(show=True)

    def BindEvents(self):
#         self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self._mgr.UnInit()
        event.Skip()
        self.Destroy()

    def BuildPanes(self):
#         self.SetMinSize(wx.Size(400, 300))
        self.buttonPanel = CreateButtonPanel(self)
        self.fileSearchPanel = CreateFileSearchPanel(self)
        
        self._mgr.AddPane(self.fileSearchPanel, aui.AuiPaneInfo().
                          Name("sql").Caption("SQL")
                          .Layer(1).Center().CaptionVisible(False, left=True)
                          .MinimizeButton(True).CloseButton(False))
        
        self._mgr.AddPane(self.buttonPanel, aui.AuiPaneInfo().
                          Name("button").Caption("Button")
                          .Layer(1).Bottom().CaptionVisible(False, left=True)
                          .MinimizeButton(True).CloseButton(False))

        self._mgr.Update()


class CreateFileSearchPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
#         pub.subscribe(self.__OnCellChange, 'OnCellChange')
        vBox = wx.BoxSizer(wx.VERTICAL)
        ########################## Search ##########################################
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        containgTextLabel = wx.StaticText(self, label='Containing Text:')
        wildTextLabel = wx.StaticText(self, label='(*= any string, ?= any character, \= escape for literals: *?\)')
#         self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        initialList = []
        searchTextCb = wx.ComboBox(self, wx.NewIdRef(), "", (90, 50),
                         (160, -1), initialList,
                         wx.CB_DROPDOWN
                         # | wx.TE_PROCESS_ENTER
                         # | wx.CB_SORT
                         )
        
        caseSensitiveOpt = wx.CheckBox(self, -1, "Case Sensitive")
        regularExpressionOpt = wx.CheckBox(self, -1, "Regular expression")
        wholeWordOpt = wx.CheckBox(self, -1, "Whole word")
        vbox2.AddMany([caseSensitiveOpt, regularExpressionOpt, wholeWordOpt])
        
        vbox1.Add(containgTextLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.Top, 0)
        vbox1.Add(searchTextCb, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.Top, 0)
        vbox1.Add(wildTextLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.Top, 0)

#         vbox1.Add(vbox1, 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        ########################## Search ##########################################
#         hbox = wx.BoxSizer(wx.HORIZONTAL)     

        vBoxFileName = wx.BoxSizer(wx.VERTICAL)
        fileNamePatternLabel = wx.StaticText(self, label='File name patterns (separated by comma):')
        wildFileNameTextLabel = wx.StaticText(self, label='(*= any string, ?= any character, \= escape for literals: *?\)')
        initialList = []
        fileNameCb = wx.ComboBox(self, wx.NewIdRef(), "", (90, 50),
                         (160, -1), initialList,
                         wx.CB_DROPDOWN
                         # | wx.TE_PROCESS_ENTER
                         # | wx.CB_SORT
                         )        
        fileNameChooseBtn = wx.Button(self, 50, "Choose...")
        fileNameChooseBtn.SetToolTip("Choose...")
        self.Bind(wx.EVT_BUTTON, self.onFileNameChooseBtn, fileNameChooseBtn)        
#         hbox.Add(fileNamePatternLabel, 0, wx.EXPAND | wx.ALL, 0)
        vBoxFileName.Add(fileNamePatternLabel, 0, wx.EXPAND | wx.ALL, 0)
        vBoxFileName.Add(fileNameCb, 0, wx.EXPAND | wx.ALL, 0)
        vBoxFileName.Add(wildFileNameTextLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 0)
        vbox2.Add(fileNameChooseBtn, 0, wx.EXPAND | wx.TOP, 35)
        
        vbox1.Add(vBoxFileName, 1, wx.EXPAND | wx.TOP, 25)
        hbox.Add(vbox1, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(vbox2, 0, wx.EXPAND | wx.TOP, 20)   
             
        vBox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        ########################## Search in ##########################################
        search_in_title = wx.StaticBox(self, -1, "Search In")
        search_in_box = wx.StaticBoxSizer(search_in_title, wx.HORIZONTAL)
        cb1 = wx.CheckBox(self, -1, "Derived resources")
        cb2 = wx.CheckBox(self, -1, "Binary files")
        search_in_box.AddMany([ cb1, cb2, ])
        vBox.Add(search_in_box, 0, wx.EXPAND | wx.ALL, 5)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb1)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb2)        
        ########################## Scope ##########################################
        
#         panel = wx.Panel(self, -1)
        box1_title = wx.StaticBox(self, -1, "Scope")
        scope_box = wx.StaticBoxSizer(box1_title, wx.VERTICAL)
#         grid1 = wx.FlexGridSizer(cols=3)
        workspaceRadio = wx.RadioButton(self, -1, " Workspace", style=wx.RB_GROUP)
        resourceInActiveEditorRadio = wx.RadioButton(self, -1, " Resource in active editor")
        enclosingProjectRadio = wx.RadioButton(self, -1, "Enclosing project")
        workingSetRadio = wx.RadioButton(self, -1, "Working set:")
        wokingSetText = wx.TextCtrl(self, -1, "")

        chooseBtn = wx.Button(self, 50, "Choose...")
        chooseBtn.SetToolTip("Choose...")
        self.Bind(wx.EVT_BUTTON, self.onChooseBtn, chooseBtn)
        
        hb1 = wx.BoxSizer(wx.HORIZONTAL)
        hb1.Add(workspaceRadio, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hb1.Add(resourceInActiveEditorRadio, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hb1.Add(enclosingProjectRadio, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        
        hb2 = wx.BoxSizer(wx.HORIZONTAL)
        hb2.Add(workingSetRadio, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hb2.Add(wokingSetText, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        hb2.Add(chooseBtn, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        scope_box.Add(hb1, 0, wx.EXPAND | wx.ALL, 5)
        scope_box.Add(hb2, 1, wx.EXPAND | wx.ALL, 5)
        vBox.Add(scope_box, 0, wx.EXPAND | wx.ALL, 5)

        ####################################################################
#         vBox.Add(self.sstc , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

    def onFileNameChooseBtn(self):
        logger.debug('onFileNameChooseBtn')

    def onChooseBtn(self):
        logger.debug('onChooseBtn')

    def EvtCheckBox(self, event):
        logger.debug('EvtCheckBox: %d\n' % event.IsChecked())
        cb = event.GetEventObject()
        if cb.Is3State():
            logger.debug("\t3StateValue: %s\n" % cb.Get3StateValue())

        
class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent         
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        replaceBtn = wx.Button(self, 50, "Replace", (20, 220))
        replaceBtn.SetToolTip("Replace")
        self.Bind(wx.EVT_BUTTON, self.onReplace, replaceBtn)
        searchBtn = wx.Button(self, 50, "Search", (20, 220))
        searchBtn.SetToolTip("Search")
        self.Bind(wx.EVT_BUTTON, self.onSearch, searchBtn)
        
        cancelButton = wx.Button(self, 51, "Cancel", (20, 220))
        cancelButton.SetToolTip("Cancel")
        self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, cancelButton)

#         b.SetBitmap(images.Mondrian.Bitmap,
#                     wx.LEFT    # Left is the default, the image can be on the other sides too
#                     #wx.RIGHT
#                     #wx.TOP
#                     #wx.BOTTOM
#                     )
        hbox.Add(replaceBtn)    
        hbox.Add(searchBtn)    
        hbox.Add(cancelButton)    
#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox, 0, wx.ALIGN_RIGHT | wx.ALL,10)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

    def onReplace(self, event):
        logger.debug('onReplace')

    def onSearch(self, event):
        logger.debug('onSearch')

    def onCancelButtonClick(self, event):
        logger.debug('onCancelButtonClick')

        self.GetTopLevelParent().OnCloseWindow(event)        


if __name__ == '__main__':
    app = wx.App(False)
#     frame = CreateTableFrame(None, 'table creation')
    frame = SearchPanelsFrame(None, size=(800, 400))
    frame.CenterOnScreen()
#     frame.setData(tableDict)
#     frame.Show()
    app.MainLoop()
