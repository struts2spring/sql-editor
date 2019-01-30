'''
Created on Jan 30, 2019


'''
import wx
from wx import TreeCtrl

import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.util.FileOperationsUtil import FileOperations
import os
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class DataSource():
    
    def __init__(self, connectionName=None, filePath=None):
        self.connectionName = connectionName
        self.filePath = filePath
        self.isConnectionOpen = True


class DataSourceTreeNode():
    
    def __init__(self, depth=None, dataSource=None, imageName=None):
        self.depth = depth
        self.dataSource = dataSource
        self.imageName = imageName


class DatabaseTree(TreeCtrl):

    def __init__(self, parent, style=wx.TR_HIDE_ROOT | 
                                             wx.TR_FULL_ROW_HIGHLIGHT | 
                                             wx.TR_LINES_AT_ROOT | 
                                             wx.TR_HAS_BUTTONS | 
                                             wx.TR_MULTIPLE | 
                                             wx.TR_EDIT_LABELS | wx.BORDER_NONE):
        super(DatabaseTree, self).__init__(parent, style=style)
        # Attributes
        self._watch = list()  # this will contain list of database filePath
        self._il = None
        self._editlabels = True

        # Setup
        self.SetupImageList()
        self.AddRoot('root')
        self.SetItemData(self.RootItem, "root")

        # Event Handlers
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self._OnGetToolTip)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._OnItemActivated)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self._OnItemCollapsed)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self._OnItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self._OnMenu)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self._OnBeginEdit)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self._OnEndEdit)
        
    def SetupImageList(self):
        """Setup/Refresh the control's ImageList.
        Override DoSetupImageList to customize the behavior of this method.

        """
        logger.debug('SetupImageList')
        if self._il:
            self._il.Destroy()
            self._il = None
        self._il = wx.ImageList(16, 16)
        self.SetImageList(self._il)
        self.doSetupImageList()
        
    def _OnGetToolTip(self, evt):
#         logger.debug('_OnGetToolTip')
        item = evt.GetItem()
        tt = self.DoGetToolTip(item)
        if tt:
            evt.ToolTip = tt
        else:
            evt.Skip()

    def _OnItemActivated(self, evt):
        logger.debug('_OnItemActivated')
        item = evt.GetItem()
        self.DoItemActivated(item)
        evt.Skip()

    def _OnItemCollapsed(self, evt):
        logger.debug('_OnItemCollapsed')
        item = evt.GetItem()
        self.DoItemCollapsed(item)
        evt.Skip()

    def _OnItemExpanding(self, evt):
        logger.debug('_OnItemExpanding')
        item = evt.GetItem()
        self.DoItemExpanding(item)
        evt.Skip()

    def _OnMenu(self, evt):
        logger.debug('_OnMenu')
        try:
            item = evt.GetItem()
            self.DoShowMenu(item)
        except:
            pass

    def _OnBeginEdit(self, evt):
        logger.debug('_OnBeginEdit')
        if not self._editlabels:
            evt.Veto()
        else:
            item = evt.GetItem()
            if self.DoBeginEdit(item):
                evt.Skip()
            else:
                evt.Veto()

    def _OnEndEdit(self, evt):
        logger.debug('_OnEndEdit')
        if self._editlabels:
            item = evt.GetItem()
            newlabel = evt.GetLabel()
            if self.DoEndEdit(item, newlabel):
                evt.Skip()
                return
        evt.Veto()

    def doSetupImageList(self):
        """Add the images to the control's ImageList. It is guaranteed
        that self.ImageList is valid and empty when this is called.

        """
        logger.debug('DoSetupImageList')
        self.fileOperations = FileOperations()
        
        imageNameList = ['database.png',
            'database_category.png',
            'folder_view.png',
            'folder.png',
            'table.png',
            'view.png',
            'index.png',
            'column.png',
            'string.png',
            'key.png',
            'foreign_key_column.png',
            'columns.png',
            'unique_constraint.png',
            'reference.png',
            'datetime.png',
            'columns.png',
            'sqlite.png',
            'h2.png',
            'textfield.png',
        ]
        self.iconsDictByIndex = {}
        self.iconsDictByImageName = {}
        count = 0
        for imageName in imageNameList:
            self.ImageList.Add(self.fileOperations.getImageBitmap(imageName=imageName))
            self.iconsDictByIndex[count] = imageName
            self.iconsDictByImageName[imageName] = count
            count += 1

    def GetChildNodes(self, parent):
        """Get all the TreeItemIds under the given parent
        @param parent: TreeItem
        @return: list of TreeItems

        """
        logger.debug('GetChildNodes')
        rlist = list()
        child, cookie = self.GetFirstChild(parent)
        if not child or not child.IsOk():
            return rlist

        rlist.append(child)
        while True:
            child, cookie = self.GetNextChild(parent, cookie)
            if not child or not child.IsOk():
                return rlist
            rlist.append(child)
        return rlist

    def GetExpandedNodes(self):
        """Get all nodes that are currently expanded in the view
        this logically corresponds to all parent directory nodes which
        are expanded.
        @return: list of TreeItems

        """
        logger.debug('GetExpandedNodes')

        def NodeWalker(parent, rlist):
            """Recursively find expanded nodes
            @param parent: parent node
            @param rlist: list (outparam)

            """
            children = self.GetChildNodes(parent)
            for node in children:
                if self.IsExpanded(node):
                    rlist.append(node)
                    NodeWalker(node, rlist)

        nodes = list()
        NodeWalker(self.RootItem, nodes)
        return nodes

    def EnableLabelEditing(self, enable=True):
        """Enable/Disable label editing. This functionality is
        enabled by default.
        @keyword enable: bool

        """
        logger.debug('EnableLabelEditing')
        self._editlabels = enable
        
    def addWatchConnection(self, dataSource=None):

        logger.debug('AddWatchConnection')
        if dataSource.filePath not in self._watch:
            self._watch.append(dataSource.filePath)
            dataSourceTreeNode = DataSourceTreeNode(depth=0, dataSource=dataSource, imageName='sqlite.png')
            return self.appendConnectionNode(self.RootItem, dataSourceTreeNode)

    def appendConnectionNode(self, item, dataSourceTreeNode=None):
        """Append a child node to the tree
        @param item: TreeItem parent node
        @param path: path to add to node
        @return: new node

        """
        logger.debug('AppendFileNode')
        img = self.getDataSourceTreeNodeImage(dataSourceTreeNode)
        name = dataSourceTreeNode.dataSource.connectionName
        child = self.AppendItem(item, name, img)
        self.SetItemData(child, dataSourceTreeNode)
        if self.hasNodeChildren(dataSourceTreeNode):
            self.SetItemHasChildren(child, True)
        return child
    
    def hasNodeChildren(self, dataSourceTreeNode):
        hasChildren=False
        if dataSourceTreeNode.depth==0 and dataSourceTreeNode.dataSource.isConnectionOpen:
            hasChildren=True
        return hasChildren

    def getDataSourceTreeNodeImage(self, dataSourceTreeNode=None):
        '''
        return image count number in self.ImageList
        '''
        imageIndex=self.iconsDictByImageName[dataSourceTreeNode.imageName]
        
        return imageIndex

        
# Test
if __name__ == '__main__':
    app = wx.App(False)
    f = wx.Frame(None)
    databaseTree = DatabaseTree(f)
    dataSource=DataSource(connectionName="one",filePath=r'C:\Users\xbbntni\one.sqlite' )
    databaseTree.addWatchConnection(dataSource)
    
#     drives = GetWindowsDrives()
# #     d = wx.GetUserHome()
#     for drive in drives:
#         try:
#             logger.debug(drive)
#             ft.AddWatchDirectory(drive.Name)
#         except:
#             pass
# #         break
    f.Show()
    app.MainLoop()
