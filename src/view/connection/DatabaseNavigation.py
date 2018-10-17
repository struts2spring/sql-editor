'''
Created on 04-Feb-2017

@author: vijay
'''
import wx
import os
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.constants import keyMap
import logging

logger = logging.getLogger('extensive')

class DatabaseNavigationTree(ExpansionState, TreeCtrl):
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
                keyname = "\"" + event.GetUnicodeKey() + "\""
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
            return super(DatabaseNavigationTree, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(DatabaseNavigationTree, self).Thaw()