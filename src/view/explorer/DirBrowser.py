

import wx
import logging.config
from src.view.constants import LOG_SETTINGS, keyMap
from wx import TreeCtrl
from src.view.util.FileOperationsUtil import FileOperations

logger = logging.getLogger('extensive')


logging.config.dictConfig(LOG_SETTINGS)


class DirTreePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.tree = ExplorerTree(self)
        ####################################################################
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        
class ExplorerTree(TreeCtrl):
    def __init__(self, parent):
        TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT)
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
    def BuildTreeImageList(self):
        logger.debug('BuildTreeImageList')
        self.fileOperations = FileOperations()
        imgList = wx.ImageList(16, 16)

        # add the image for modified demos.

        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="database.png")))  # 0
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "database_category.png")))  # 1
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "folder_view.png")))  # 2
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "folder.png")))  # 3
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "table.png")))  # 4
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "view.png")))  # 5
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "index.png")))  # 6
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "column.png")))  # 7 using to show integer column 
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "string.png")))  # 8
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "key.png")))  # 9
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "foreign_key_column.png")))  # 10
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "columns.png")))  # 11
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "unique_constraint.png")))  # 12
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "reference.png")))  # 13
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "datetime.png")))  # 14
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "columns.png")))  # 15
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "sqlite.png")))  # 16
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "h2.png")))  # 17 use to show h2 database icon
        imgList.Add(wx.Bitmap(self.fileOperations.getImageBitmap(imageName= "textfield.png")))  # 18 use to show [varchar, char, text data] type icon 
        self.AssignImageList(imgList)

    def GetItemIdentity(self, item):
        return self.GetItemData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(ExplorerTree, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(ExplorerTree, self).Thaw()
    #---------------------------------------------

    def OnKey(self, event):
        logger.debug('onkey')
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            logger.debug("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
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
                
        logger.debug("OnKeyDown: You Pressed : %s", keyname)

        event.Skip()  
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    try: 
        panel = DirTreePanel(frame, title='asfd')
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()