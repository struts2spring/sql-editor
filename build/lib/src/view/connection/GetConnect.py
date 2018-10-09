'''
Created on 31-Dec-2016

@author: vijay
'''
import wx
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.Constant import keyMap
import os
import logging

logger = logging.getLogger('extensive')

class CreatingNewConnectionFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(400, 300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        
#         self.pnl = pnl = MainPanel(self)        
        self.newConnectionFrame = CreatingNewConnectionPanel(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)

        self.Show()
    def OnCloseFrame(self, event):
        logger.debug('OnCloseFrame')
        self.OnExitApp(event)
    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        logger.debug('OnExitApp')
        self.Destroy()
        
        

class CreatingNewConnectionPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        '''
        Header section
        '''
        self.st = wx.StaticLine(self, wx.ID_ANY)
        # Make and layout the controls
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs + 4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs + 2, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.initialText = '''Select new connection type'''
        self.header = wx.StaticText(self, -1, self.initialText)
        self.selectedConnectionTypeText = wx.StaticText(self, -1, "This is to create a new connection.") 
        self.header.SetFont(bf)
        
        self.tree = databaseNavigationTree(self)
        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter database name")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.RecreateTree()
        
        
        ####################################################################
        vBox.Add(self.header , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.selectedConnectionTypeText , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        
    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        try:
            for category, items in self._treeList[1]:
                self.searchItems[category] = []
                for childItem in items:
    #                 if SearchDemo(childItem, value):
                    self.searchItems[category].append(childItem)
        except Exception as e:
            logger.error(e, exc_info=True)
        wx.EndBusyCursor()
        self.RecreateTree()   
    #---------------------------------------------    
    def RecreateTree(self, evt=None):
        # Catch the search type (name or content)
#         searchMenu = self.filter.GetMenu().GetMenuItems()
#         fullSearch = searchMenu[1].IsChecked()
        fullSearch = False   
            
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
        self.root = self.tree.AddRoot("Connections")
        self.tree.SetItemImage(self.root, 0)
        self.tree.SetItemPyData(self.root, 0)

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
#         self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0
        

        databaseLeaf = self.tree.AppendItem(self.root, 'SQLite', image=16)

                                   
class databaseNavigationTree(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in database page
    '''
    def __init__(self, parent):
        TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT)
        self.BuildTreeImageList()
#         if USE_CUSTOMTREECTRL:
#             self.SetSpacing(10)
#             self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)
        self.eventdict = {
#                           'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
#                           'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
#                           'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
#                           'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
#                           'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
#                           'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
#                           'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
#                           'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                          'EVT_TREE_KEY_DOWN': self.OnKey,
#                           'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
#                           'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink
                          }
        self.SetInitialSize((100, 80))
        
            
    def AppendItem(self, parent, text, image=-1, wnd=None):

        item = TreeCtrl.AppendItem(self, parent, text, image=image)
        return item
    #---------------------------------------------

    def OnKey(self, event):
        logger.debug('onkey')
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)
                
            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode
                
        self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

        event.Skip()            
    def BuildTreeImageList(self):
        imgList = wx.ImageList(16, 16)
        
        path = os.path.abspath(__file__)
        tail = None
        while tail != 'src':
            path = os.path.abspath(os.path.join(path, '..'))
            head, tail = os.path.split(path)
        path = os.path.join(path, "images")
        # add the image for modified demos.
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "database.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "database_category.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "folder_view.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "folder.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "table.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "view.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "index.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "column.png"))))
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "string.png"))))  # 8
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "key.png"))))  # 9
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "foreign_key_column.png"))))  # 10
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "columns.png"))))  # 11
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "unique_constraint.png"))))  # 12
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "reference.png"))))  # 13
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "datetime.png"))))  # 14
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "columns.png"))))  # 15
        imgList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "sqlite.png"))))  # 16
#         imgList.Add(wx.Bitmap(path2))
#         for png in _demoPngs:
#             imgList.Add(catalog[png].GetBitmap())
            

        self.AssignImageList(imgList)

    def GetItemIdentity(self, item):
        return self.GetPyData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(databaseNavigationTree, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(databaseNavigationTree, self).Thaw()
#---------------------------------------------------------------------------
      
if __name__ == '__main__':
    app = wx.App(False)
    frame = CreatingNewConnectionFrame(None, 'asf')
    app.MainLoop()
