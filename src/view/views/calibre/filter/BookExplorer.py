'''
Created on Apr 5, 2019

@author: vijay
'''

import wx
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.util.FileOperationsUtil import FileOperations
import logging.config
from src.view.constants import LOG_SETTINGS, ID_COLLAPSE_ALL, \
    ID_LINK_WITH_EDITOR, ID_VIEW_MENU
from src.view.other.TreeData import TreeSearch, bookExplorerList

try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD

logging.config.dictConfig(LOG_SETTINGS)

logger = logging.getLogger('extensive')
##################################################


class BookExplorerPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
#         self.fileOperations = FileOperations()
        self.connDict = dict()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.treeMap = {}
        self.fileOperations = FileOperations()
        self.topToolbar = self.constructTopToolBar()
        self.tree = BookExplorerTreePanel(self)

        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)

        self.RecreateTree()
        ####################################################################
        vBox.Add(self.topToolbar , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

    def OnContextMenu(self, event):
        logger.debug("OnContextMenu\n")

    def constructTopToolBar(self):

        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, (10, 10), agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)

#         tb1.SetToolBitmapSize(wx.Size(16, 16))
        # id, name, image, name, method, kind
        tools = [
            (ID_COLLAPSE_ALL, "Collapse All", "collapseall-small.png", 'Collapse All', self.onCollapseAll, wx.ITEM_NORMAL),
            (ID_LINK_WITH_EDITOR, "Link with Editor", "icon_link_with_editor.png", 'Link with Editor', self.onLinkWithEditor, wx.ITEM_CHECK),
            (),
            (ID_VIEW_MENU, "View Menu", "icon_menu.png", 'View Menu', self.onViewMenu, wx.ITEM_NORMAL),
#             (ID_REFRESH_ROW, "Result refresh", "resultset_refresh.png", 'Result refresh \tF5', self.onRefresh),
#             (ID_ADD_ROW, "Add a new row", "row_add.png", 'Add a new row', self.onAddRow),
#             (ID_DUPLICATE_ROW, "Duplicate selected row", "row_copy.png", 'Duplicate selected row', self.onDuplicateRow),
#             (ID_DELETE_ROW, "Delete selected row", "row_delete.png", 'Delete selected row', self.onDeleteRow),
            ]
        for tool in tools:
            if len(tool) == 0:
                tb1.AddSeparator()
            else:
                logger.debug(tool)
                toolItem = tb1.AddSimpleTool(tool[0], tool[1], self.fileOperations.getImageBitmap(imageName=tool[2]), kind=tool[5], short_help_string=tool[3])
                
                if tool[4]:
                    self.Bind(wx.EVT_MENU, tool[4], id=tool[0])

        tb1.Realize()

        return tb1

    def onCollapseAll(self, event):
        logger.debug('onCollapseAll')
        self.tree.CollapseAll()

    def onLinkWithEditor(self, event):
        logger.debug('onLinkWithEditor')
        self.linkWithEditor = event.IsChecked()
        logger.debug(f'{self.linkWithEditor}')
#         event.

    def onViewMenu(self, event):
        logger.debug('onViewMenu')

    #---------------------------------------------
    def constructNode(self, parent=None, treeData=None):
        logger.debug(treeData)
        for treeItem in treeData:
            itemId = self.tree.AppendItem(parent, treeItem.name, image=self.tree.iconsDictIndex[treeItem.imageName])
            self.tree.SetItemData(itemId, treeItem)
            if treeItem.child:
#                     for childItem in treeItem.child:
                self.constructNode(parent=itemId, treeData=treeItem.child)

    def RecreateTree(self, evt=None):

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
        self.root = self.tree.AddRoot("Other View")
        self.tree.SetItemImage(self.root, self.tree.iconsDictIndex['other_view.png'])
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

        firstChild = None
        selectItem = None
        count = 0

        treeSearch = TreeSearch()
        searchText = None
        treeItems = treeSearch.searchedNodes(dataList=bookExplorerList, searchText=searchText)

        self.constructNode(parent=self.root, treeData=treeItems)

        if firstChild:
            self.tree.Expand(firstChild)
#         if filter:
#             self.tree.ExpandAll()
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
        imageName = self.tree.GetItemData(item).imageName
#         explandedImageName = 'eclipse_open_folder.png'
        data = self.tree.GetItemData(item)
        if imageName == 'user.png':
            explandedImageName = 'folder_user.png'
            data = self.tree.GetItemData(item)
            data.imageName = explandedImageName
            self.tree.SetItemData(item, data)
        elif data.imageName:
            explandedImageName = data.imageName
        
        if self.tree.GetItemParent(item):
            self.tree.SetItemImage(item, self.tree.iconsDictIndex[explandedImageName])
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
        logger.debug("OnItemCollapsed: %s", self.tree.GetItemText(item))
        imageName = self.tree.GetItemData(item).imageName
        data = self.tree.GetItemData(item)
        collapsedImageName = 'folderType_filter.png'
        if imageName == 'folder_user.png':
            collapsedImageName = 'user.png'
            data.imageName = collapsedImageName
            self.tree.SetItemData(item, data)
        elif data.imageName:
            collapsedImageName = data.imageName
        if self.tree.GetItemParent(item):
            self.tree.SetItemImage(item, self.tree.iconsDictIndex[collapsedImageName])
        event.Skip()

    #---------------------------------------------
    def OnTreeLeftDown(self, event):
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item and item == self.tree.GetSelection():
            print(self.tree.GetItemText(item) + " Overview")
        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):
#         if self.dying or not self.loaded or self.skipLoad:
#             return

#         self.StopDownload()

        item = event.GetItem()
        try:
            itemText = self.tree.GetItemText(item)
            logger.debug(itemText)
            opalPreference = self.GetTopLevelParent()
            if opalPreference:
                pnl_children = list()
                if hasattr(opalPreference, 'png'):
                    pnl_children = opalPreference.pnl.GetChildren()
                for pnl in pnl_children:
        #             print(pnl)
                    if pnl.GetName() == 'rightPanel':
                        opalPreference = self.GetTopLevelParent()
                        for child in pnl.GetChildren():
                            child.Hide()
                        rightPanelItem = opalPreference.getPreferencePanelObj(pnl, preferenceName=itemText)
                        opalPreference.addPanel(rightPanelItem)
                        pnl.Layout()
                        pnl.Refresh()
                        pnl.Fit()
                opalPreference.Layout()
                if hasattr(opalPreference, 'mgr'):
                    opalPreference.mgr.Update()
        except:
            pass


class BookExplorerTreePanel(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in preferences page
    '''

    def __init__(self, parent):

        TreeCtrl.__init__(self, parent, style=wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.BORDER_NONE)

        self._il = None
        self.BuildTreeImageList()
        self.SetInitialSize((100, 80))

    def AppendItem(self, parent, text, image=-1, wnd=None):

        item = TreeCtrl.AppendItem(self, parent, text, image=image)
        return item

    def BuildTreeImageList(self):
        if self._il:
            self._il.Destroy()
            self._il = None
        self._il = wx.ImageList(16, 16)
        self.SetImageList(self._il)

        self.ImageList.RemoveAll()
        self.iconsDictIndex = {}
        count = 0
        self.fileOperations = FileOperations()
        imageIconsName= ['preference.png', 'folderType_filter.png', 'eclipse_open_folder.png', 'fileType_filter.png', 'usb.png', 'stop.png',
                          'java.png', 'python_module.png', 'xml.png', "other_view.png", 'console_view.png', 'register_view.png',
                          'debug_view.png' , 'history_view.png', 'compare_view.png', 'breakpoint_view.png', 'watchlist_view.png',
                          'history_view.png', 'synch_synch.png', 'variable_view.png', 'internal_browser.png', 'reflog.png', 'staging.png',
                          'rebase_interactive.png', 'repo_rep.png', 'gitrepository.png', 'filenav_nav.png', 'welcome16.png', 'tasks_tsk.png',
                          'resource_persp.png', 'outline_co.png','folder_user.png' ]
        for item in bookExplorerList:
            imageIconsName.append(item[2])
        for imageName in imageIconsName:
            try:
                self.ImageList.Add(self.fileOperations.getImageBitmap(imageName=imageName))
                self.iconsDictIndex[imageName] = count
                count += 1
            except Exception as e:
                logger.error(e)

    def GetItemIdentity(self, item):
        return self.GetItemData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(BookExplorerTreePanel, self).Freeze()

    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(BookExplorerTreePanel, self).Thaw()


if __name__ == '__main__':

    app = wx.App(False)
    frame = wx.Frame(None)
    try:
        panel = BookExplorerPanel(frame)
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
