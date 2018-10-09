import wx
from wx.lib.agw import aui
# from wx.aui import AuiManager, AuiPaneInfo, AUI_MGR_TRANSPARENT_DRAG
# from src.ui.view.preference.images import catalog, WXPdemo
from wx.lib.mixins.treemixin import ExpansionState
from wx import TreeCtrl
from src.view.preference.General import GeneralPreferencePanel
from src.view.preference.PreferencePanel import PreferencePanel, AppearancePanel,\
    SearchPanel, WorkspacePanel, KeysPanel
from src.view.preference.images import catalog
# from src.view.images import WXPdemo
import logging
from src.view.constants import TITLE

logger = logging.getLogger('extensive')

logger.debug('preferences logger init')

_demoPngs = ["overview", "recent", "frame", "dialog", "moredialog", "core",
     "book", "customcontrol", "morecontrols", "layout", "process",
     "clipboard", "images", "miscellaneous"]
_treeList = [
    # new stuff
    (
     'General', [
        'Appearance',
        'Search',
        'Workspace',
        'Keys'
        ]
     ),
    (
     'Sharing', [
        'Email book',
        'Open cloud',
        'Configure device',
        ]
     ),
    (
     'Account', [
        'Email book',
        'Open cloud',
        'Configure device',
        ]
     ),
    (
     'Install/Update', [
        'Automatic Updates',
        'Available plugins',
        ]
     ),

 


    ('Check out the samples dir too', []),

]

class PrefrencesTree(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in preferences page
    '''
    def __init__(self, parent):
        TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.BuildTreeImageList()
#         if USE_CUSTOMTREECTRL:
#             self.SetSpacing(10)
#             self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)

        self.SetInitialSize((100, 80))
        
            
    def AppendItem(self, parent, text, image=-1, wnd=None):

        item = TreeCtrl.AppendItem(self, parent, text, image=image)
        return item
            
    def BuildTreeImageList(self):
        imgList = wx.ImageList(16, 16)

        for png in _demoPngs:
            imgList.Add(catalog[png].GetBitmap())
            
        # add the image for modified demos.
        imgList.Add(catalog["custom"].GetBitmap())

        self.AssignImageList(imgList)

    def GetItemIdentity(self, item):
        return self.GetPyData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(PrefrencesTree, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(PrefrencesTree, self).Thaw()
#---------------------------------------------------------------------------

class MainPanel(wx.Panel):
    """
    Just a simple derived panel where we override Freeze and Thaw so they are
    only used on wxMSW.    
    """
    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Thaw()
#---------------------------------------------------------------------------
class OpalPreference(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.allowAuiFloating = False
        self.SetMinSize((640, 480))
#         icon = WXPdemo.GetIcon()
        icon=wx.Icon()
        self.SetIcon(icon)
        
        self.statusBar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        self.statusBar.SetStatusWidths([-2, -1])

        statusText = TITLE
        self.statusBar.SetStatusText(statusText, 0)

        self.pnl = pnl = MainPanel(self)
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)
        
     
        # Create a Notebook
                # Create a Notebook
        imgList = wx.ImageList(16, 16)
        for png in ["overview", "code", "demo"]:
            bmp = catalog[png].GetBitmap()
            imgList.Add(bmp)
            
        rightPanel = wx.Panel(pnl, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
        self.nb = wx.Notebook(rightPanel, -1, style=wx.CLIP_CHILDREN)
        self.nb.AssignImageList(imgList)
#         self.panel = PreferencePanel(self.nb, -1, style=wx.CLIP_CHILDREN, preferenceName="Preferences")
        self.panel = self.getPreferencePanelObj(preferenceName="Preferences")
        self.nb.AddPage(self.panel, "Preferences", imageId=0)
        # Create a TreeCtrl
        leftPanel = wx.Panel(pnl, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
        self.treeMap = {}
        self.searchItems = {}
        self.tree = PrefrencesTree(leftPanel)
        
        self.filter = wx.SearchCtrl(leftPanel, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter search text")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        
        searchMenu = wx.Menu()
        item = searchMenu.AppendRadioItem(-1, "Sample Name")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        item = searchMenu.AppendRadioItem(-1, "Sample Content")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        self.filter.SetMenu(searchMenu)
        self.RecreateTree()
        
#         self.tree.SetExpansionState(self.expansionState)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        # add the windows to the splitter and split it.
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(self.filter, 0, wx.EXPAND | wx.ALL, 5)
        leftBox.Add(self.tree, 1, wx.EXPAND)
#         leftBox.Add(wx.StaticText(leftPanel, label="Type filter search text:"), 0, wx.TOP | wx.LEFT, 5)
        if 'wxMac' in wx.PlatformInfo:
            leftBox.Add((5, 5))  # Make sure there is room for the focus ring
        leftPanel.SetSizer(leftBox)

        rightBox=wx.BoxSizer(wx.VERTICAL)
        rightBox.Add(self.nb, 1, wx.EXPAND)
        self.buttonBar=ButtonPanel(rightPanel)
        rightBox.Add(self.buttonBar,  flag=wx.EXPAND | wx.ALIGN_RIGHT)
        rightPanel.SetSizer(rightBox)
        
        self.tree.SelectItem(self.root)
        # Use the aui manager to set up everything
        self.mgr.AddPane(rightPanel, aui.AuiPaneInfo().CenterPane().Name("Notebook"))
        self.mgr.AddPane(leftPanel,
                         aui.AuiPaneInfo().
                         Left().Layer(2).BestSize((240, -1)).MinSize((240, -1)).
                         Floatable(self.allowAuiFloating).FloatingSize((240, 700)).
                         Caption("Preferences").
                         CloseButton(False).
                         Name("preferencesTree"))

        self.mgr.Update()

#         self.mgr.SetFlags(self.mgr.GetFlags() ^ AUI_MGR_TRANSPARENT_DRAG)
        
        self.Show()
    # Makes sure the user was intending to quit the application
    def OnCloseFrame(self, event):
        logger.debug('OnCloseFrame')
        self.OnExitApp(event)
    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        logger.debug('OnExitApp')
        self.Destroy()
        
    def OnSearchMenu(self, event):

        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        fullSearch = searchMenu[1].IsChecked()
        
        if fullSearch:
            self.OnSearch()
        else:
            self.RecreateTree()        
    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        
        for category, items in _treeList:
            self.searchItems[category] = []
            for childItem in items:
#                 if SearchDemo(childItem, value):
                self.searchItems[category].append(childItem)

        wx.EndBusyCursor()
        self.RecreateTree()   
    #---------------------------------------------    
    def RecreateTree(self, evt=None):
        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        fullSearch = searchMenu[1].IsChecked()
            
        if evt:
            if fullSearch:
                # Do not`scan all the demo files for every char
                # the user input, use wx.EVT_TEXT_ENTER instead
                return

        expansionState = self.tree.GetExpansionState()

        current = None
        item = self.tree.GetSelection()
        if item:
            prnt = self.tree.GetItemParent(item)
            if prnt:
                current = (self.tree.GetItemText(item),
                           self.tree.GetItemText(prnt))
                    
        self.tree.Freeze()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("Preferences")
        self.tree.SetItemImage(self.root, 0)
        self.tree.SetItemData(self.root, 0)

        treeFont = self.tree.GetFont()
        catFont = self.tree.GetFont()

        # The native treectrl on MSW has a bug where it doesn't draw
        # all of the text for an item if the font is larger than the
        # default.  It seems to be clipping the item's label as if it
        # was the size of the same label in the default font.
        if 'wxMSW' not in wx.PlatformInfo:
            treeFont.SetPointSize(treeFont.GetPointSize() + 2)
            
        treeFont.SetWeight(wx.BOLD)
        catFont.SetWeight(wx.BOLD)
        self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0
        
        for category, items in _treeList:
            count += 1
            if filter:
                if fullSearch:
                    items = self.searchItems[category]
                else:
                    items = [item for item in items if filter.lower() in item.lower()]
            if items:
                child = self.tree.AppendItem(self.root, category, image=count)
                self.tree.SetItemFont(child, catFont)
                self.tree.SetItemData(child, count)
                if not firstChild: firstChild = child
                for childItem in items:
                    image = count
#                     if DoesModifiedExist(childItem):
#                         image = len(_demoPngs)
                    theDemo = self.tree.AppendItem(child, childItem, image=image)
                    self.tree.SetItemData(theDemo, count)
                    self.treeMap[childItem] = theDemo
                    if current and (childItem, category) == current:
                        selectItem = theDemo
                        
                    
        self.tree.Expand(self.root)
        if firstChild:
            self.tree.Expand(firstChild)
        if filter:
            self.tree.ExpandAll()
        elif expansionState:
            self.tree.SetExpansionState(expansionState)
        if selectItem:
            self.skipLoad = True
            self.tree.SelectItem(selectItem)
            self.skipLoad = False
        
        self.tree.Thaw()
        self.searchItems = {}

    #---------------------------------------------
    def OnItemExpanded(self, event):
        item = event.GetItem()
        logger.debug("OnItemExpanded: %s" , self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
        logger.debug("OnItemCollapsed: %s",self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnTreeLeftDown(self, event):
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item == self.tree.GetSelection():
            print(self.tree.GetItemText(item) + " Overview")
        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):
#         if self.dying or not self.loaded or self.skipLoad:
#             return

#         self.StopDownload()

        item = event.GetItem()
        itemText = self.tree.GetItemText(item)
        print(itemText)
        self.UpdateNotebook(preferenceName=itemText)
        
#         self.StartDownload()
    #---------------------------------------------
    def UpdateNotebook(self, select=-1, preferenceName=None):
        logger.debug("UpdateNotebook: %s",preferenceName)
        self.pnl.Freeze()
        self.nb.DeletePage(0)
        self.nb.InsertPage(0, self.getPreferencePanelObj(preferenceName), preferenceName, imageId=0)
        self.pnl.Thaw()
    
    def getPreferencePanelObj(self, preferenceName='Preferences'):
        preferencePanelObj = None
        if preferenceName == 'General':
            preferencePanelObj = GeneralPreferencePanel(self.nb,preferenceName=preferenceName)
        elif preferenceName == 'Preferences':
            preferencePanelObj = PreferencePanel(self.nb,preferenceName=preferenceName)
        elif preferenceName == 'Appearance':
            preferencePanelObj = AppearancePanel(self.nb,preferenceName=preferenceName)
        elif preferenceName == 'Search':
            preferencePanelObj = SearchPanel(self.nb,preferenceName=preferenceName)
        elif preferenceName == 'Workspace':
            preferencePanelObj = WorkspacePanel(self.nb,preferenceName=preferenceName)
        elif preferenceName == 'Keys':
            preferencePanelObj = KeysPanel(self.nb,preferenceName=preferenceName)
        elif preferenceName == 'Sharing':
            preferencePanelObj = PreferencePanel(self.nb,preferenceName=preferenceName)
        else :
            preferencePanelObj = GeneralPreferencePanel(self.nb, preferenceName=preferenceName)
        
        return preferencePanelObj

class ButtonPanel(wx.Panel):
    
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.HORIZONTAL)
        self.cancelButton=wx.Button(self, 1, 'Cancel', (50, 130))
        self.okButton=wx.Button(self, 1, 'OK', (50, 130))
        vBox.Add(self.cancelButton, 0,flag=wx.RIGHT)
        vBox.Add(self.okButton, 0, flag=wx.RIGHT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox , 0, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.SetSizer(sizer)
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.onCancelButton, id=wx.ID_ANY)
        self.Bind(wx.EVT_BUTTON, self.onOkButton, id=wx.ID_ANY)
    def onCancelButton(self, event):
        self.Close(True)
    def onOkButton(self, event):
        self.Close(True)
#---------------------------------------------------------------------------

# class MyApp(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent, -1, title='Opal preferences', size=(1100, 650))
#         frame = OpalPreference(None, "Opal preferences")
#         frame.Show()

if __name__ == '__main__':
    app = wx.App(0)
    frame = OpalPreference(None, "Preferences")
    app.MainLoop()
