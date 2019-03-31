'''
Created on 30-Dec-2018

@author: vijay
'''

import wx
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.util.FileOperationsUtil import FileOperations
import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.other.TreeData import TreeSearch, viewdataList

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
##################################################


class OtherViewTreeFrame(wx.Frame):

    def __init__(self, parent, title, size=(313, 441),
                 style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.SUNKEN_BORDER | wx.STAY_ON_TOP):
        style = style & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, parent, -1, title, size=size,
                          style=style)

        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.SetMinSize((100, 100))
        self.fileOperations = FileOperations()
        # set frame icon
        icon = wx.Icon()
        icon.CopyFromBitmap(self.fileOperations.getImageBitmap(imageName='eclipse16.png'))
        self.SetIcon(icon)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonPanel = CreateButtonPanel(self)
        ####################################################################

        self.otherViewTreePanel = OtherViewTreePanel(self)
        ####################################################################

        sizer.Add(self.otherViewTreePanel, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)
        self.SetSizer(sizer)
        self.Center()
#         self.createStatusBar()
        self.Show(True)

#         self.Bind(wx.EVT_SIZE, self.OnSize)
    def OnKeyUP(self, event):
#         print "KEY UP!"
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip() 

    def OnCloseFrame(self, event):
        self.Destroy()

    def OnSize(self, event):
        hsize = event.GetSize()
        logger.debug(hsize)


class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):

        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, 50, "Open", (20, 220))
        okButton.SetToolTip("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onOkClick, okButton)

        cancelButton = wx.Button(self, 51, "Cancel", (20, 220))
        cancelButton.SetToolTip("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, cancelButton)

#         b.SetBitmap(images.Mondrian.Bitmap,
#                     wx.LEFT    # Left is the default, the image can be on the other sides too
#                     #wx.RIGHT
#                     #wx.TOP
#                     #wx.BOTTOM
#                     )
        hbox.Add(okButton)
        hbox.Add(cancelButton)
#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

    def onOkClick(self, event):
        logger.debug('onOkClick')
        # TODO : need to implement
#         sqlExecuter=SQLExecuter()
#         obj=sqlExecuter.getObject()
#         if len(obj[1])==0:
#             sqlExecuter.createOpalTables()
#         sqlExecuter.addNewConnectionRow(self.GetParent().CreateOpenConnectionPanel.filePath, self.GetParent().CreateOpenConnectionPanel.connectionNameText.GetValue())
#         data = self.GetTopLevelParent().createImportingCsvPanel.data
#         tableName = self.GetTopLevelParent().createImportingCsvPanel.tableNameText.GetValue()
#         fileOperations = FileOperations()
# #         data = fileOperations.readCsvFile(filePath=filePath, columnNameFirstRow=True, delimiter=",", quotechar='|')
# #         print(len(data))
# #         print(data)
#         createTableScript = fileOperations.createTableScript(tableName=tableName, columnHeader=data[0])
#         print(createTableScript)
#         sqlList = fileOperations.sqlScript(tableName=tableName, data=data)
#         print(sqlList)
#         connectionName = self.GetTopLevelParent().connectionName
#         importStatus = SQLUtils().importingData(connectionName=connectionName, sqlList=sqlList)
#         dlg = wx.MessageDialog(self, "Some status",
#                        'Importing data status',
#                        wx.OK | wx.ICON_INFORMATION
#                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
#                        )
#         dlg.ShowModal()
#         dlg.Destroy()
        self.GetTopLevelParent().Destroy()

    def onCancelButtonClick(self, event):
        logger.debug('onCancelButtonClick')
        self.GetTopLevelParent().Destroy()


class OtherViewTreePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
#         self.fileOperations = FileOperations()
        self.connDict = dict()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.treeMap = {}
        self.tree = OtherViewBaseTreePanel(self)

        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter search text")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
#         self.tree.SelectItem(self.root)

        searchMenu = wx.Menu()
        item = searchMenu.AppendRadioItem(-1, "Full search")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        item = searchMenu.AppendRadioItem(-1, "Sample Content")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        self.filter.SetMenu(searchMenu)
        self.RecreateTree()
        ####################################################################
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

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
# 
#         for category, items in _treeList:
#             self.searchItems[category] = []
#             for childItem in items:
# #                 if SearchDemo(childItem, value):
#                 self.searchItems[category].append(childItem)

        wx.EndBusyCursor()
        self.RecreateTree()

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
#         self.tree.SetItemFont(self.root, treeFont)

        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0

        treeSearch = TreeSearch()
        searchText = self.filter.GetValue()
        if searchText.strip() == '':
            searchText = None
        treeItems = treeSearch.searchedNodes(dataList=viewdataList, searchText=searchText)

        self.constructNode(parent=self.root, treeData=treeItems)
#         for category, items in _treeList:
#             category, items
#             count += 1
#             if filter:
#                 if fullSearch:
#                     items = self.searchItems[category]
#                 else:
#                     items = [item for item in items if filter.lower() in item.lower()]
#             if items:
#                 child = self.tree.AppendItem(self.root, category, image=count)
#                 self.tree.SetItemFont(child, catFont)
#                 self.tree.SetItemData(child, count)
#                 if not firstChild: firstChild = child
#                 for childItem in items:
#                     image = count
# #                     if DoesModifiedExist(childItem):
# #                         image = len(_demoPngs)
#                     theDemo = self.tree.AppendItem(child, childItem, image=image)
#                     self.tree.SetItemData(theDemo, count)
#                     self.treeMap[childItem] = theDemo
#                     if current and (childItem, category) == current:
#                         selectItem = theDemo

#         self.tree.Expand(self.root)
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
    def RecreateTree1(self, evt=None):
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
            category, items
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
        if self.tree.GetItemParent(item):
            self.tree.SetItemImage(item, self.tree.iconsDictIndex['eclipse_folder.png'])
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
        logger.debug("OnItemCollapsed: %s", self.tree.GetItemText(item))
        if self.tree.GetItemParent(item):
            self.tree.SetItemImage(item, self.tree.iconsDictIndex['folderType_filter.png'])
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
        itemText = self.tree.GetItemText(item)
        logger.debug(itemText)
        opalPreference = self.GetTopLevelParent()
        if opalPreference:
    #         rightPanel=opalPreference.rightPanelItem.GetParent()
    #         opalPreference.rightPanelItem.Hide()
    #         opalPreference.rightPanelItem.Hide()
    #         opalPreference.rightPanelItem=opalPreference.getPreferencePanelObj(rightPanel,preferenceName=itemText)
    #         opalPreference.rightPanelItem.Show(True)
    #         opalPreference.rightPanelItem.Layout()
            pnl_children = list()
            if hasattr(opalPreference, 'png'):
                pnl_children = opalPreference.pnl.GetChildren()
            for pnl in pnl_children:
    #             print(pnl)
                if pnl.GetName() == 'rightPanel':
                    opalPreference = self.GetTopLevelParent()
                    for child in pnl.GetChildren():
#                         if 'preference' in child.name.lower():
                        child.Hide()
    #                     break
    #                     child.opalPreference.getPreferencePanelObj(pnl,preferenceName=itemText)
                    rightPanelItem = opalPreference.getPreferencePanelObj(pnl, preferenceName=itemText)
                    opalPreference.addPanel(rightPanelItem)
                    pnl.Layout()
                    pnl.Refresh()
                    pnl.Fit()
            opalPreference.Layout()
    #         print(opalPreference.GetChildrenCount())
    #         opalPreference.GetChildrenCount().rightpanel.Refresh()
            if hasattr(opalPreference, 'mgr'):
                opalPreference.mgr.Update()


#         self.UpdateNotebook(preferenceName=itemText)
class OtherViewBaseTreePanel(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in preferences page
    '''

    def __init__(self, parent):

        TreeCtrl.__init__(self, parent, style=wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.BORDER_NONE)

        self._il = None
        self.BuildTreeImageList()

#         if USE_CUSTOMTREECTRL:
#             self.SetSpacing(10)
#             self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)

        self.SetInitialSize((100, 80))

    def AppendItem(self, parent, text, image=-1, wnd=None):

        item = TreeCtrl.AppendItem(self, parent, text, image=image)
        return item

    def BuildTreeImageList(self):
#         imgList = wx.ImageList(16, 16)
#
#         for png in _demoPngs:
#             imgList.Add(catalog[png].GetBitmap())
#
#         # add the image for modified demos.
#         imgList.Add(catalog["custom"].GetBitmap())
#
#         self.AssignImageList(imgList)
        if self._il:
            self._il.Destroy()
            self._il = None
        self._il = wx.ImageList(16, 16)
        self.SetImageList(self._il)

        self.ImageList.RemoveAll()
        self.iconsDictIndex = {}
        count = 0
        self.fileOperations = FileOperations()
        for imageName in ['preference.png', 'folderType_filter.png', 'eclipse_folder.png', 'fileType_filter.png', 'usb.png', 'stop.png',
                          'java.png', 'python_module.png', 'xml.png', "other_view.png", 'console_view.png', 'register_view.png',
                          'debug_view.png' , 'history_view.png', 'compare_view.png', 'breakpoint_view.png', 'watchlist_view.png',
                          'history_view.png', 'synch_synch.png', 'variable_view.png', 'internal_browser.png', 'reflog.png', 'staging.png',
                          'rebase_interactive.png', 'repo_rep.png', 'gitrepository.png','filenav_nav.png','welcome16.png','tasks_tsk.png',
                          'resource_persp.png','outline_co.png']:
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
            return super(OtherViewBaseTreePanel, self).Freeze()

    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(OtherViewBaseTreePanel, self).Thaw()


if __name__ == '__main__':
    app = wx.App(False)
    frame = OtherViewTreeFrame(None, 'Show View')
    frame.Show()
    app.MainLoop()
