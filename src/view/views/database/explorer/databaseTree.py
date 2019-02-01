'''
Created on Jan 30, 2019


'''
import wx
from wx import TreeCtrl

import logging.config
from src.view.constants import LOG_SETTINGS, ID_ROOT_REFERESH, ID_DISCONNECT_DB, \
    ID_CONNECT_DB, ID_newWorksheet, ID_CONNECTION_PROPERTIES, ID_IMPORT, \
    ID_deleteWithDatabase
from src.view.util.FileOperationsUtil import FileOperations
import os
from src.sqlite_executer.ConnectExecuteSqlite import ManageSqliteDatabase, \
    SQLUtils, SQLExecuter

from wx.lib.pubsub import pub
from src.view.importing.importCsvExcel import ImportingCsvExcelFrame
from src.view.table.CreateTable import CreatingTableFrame
import datetime
from src.view.views.console.worksheet.tableInfoPanel import CreatingTableInfoPanel

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class DataSource():
    
    def __init__(self, connectionName=None, filePath=None):
        self.connectionName = connectionName
        self.filePath = filePath
        self.isConnected = False


class DataSourceTreeNode():
    
    def __init__(self, depth=None, dataSource=None, nodeLabel=None, imageName=None, children=None):
        self.depth = depth
        self.dataSource = dataSource
        self.imageName = imageName
        self.nodeLabel = nodeLabel
        self.children = children


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
        self._editlabels = False

        # Setup
        self.SetupImageList()
        
        self.initialize()
        
        # Event Handlers
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self._OnGetToolTip)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._OnItemActivated)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self._OnItemCollapsed)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self._OnItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self._OnMenu)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self._OnBeginEdit)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self._OnEndEdit)
#         self.Bind(wx.EVT_TREE_KEY_DOWN, self._onTreeKeyDown)
#         self.Bind(wx.EVT_TREE_BEGIN_DRAG, self._onTreeBeginDrag)
#         self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self._onItemExpanded)
#         self.Bind(wx.EVT_TREE_SEL_CHANGED, self.nSelChanged)
# 
#         self.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
#         self.Bind(wx.EVT_LEFT_DCLICK, self.OnTreeDoubleclick)
#         self.Bind(wx.EVT_RIGHT_DOWN, self.OnTreeRightDown)
#         self.Bind(wx.EVT_RIGHT_UP, self.OnTreeRightUp)

    def OnTreeDoubleclick(self, event):
        logger.info("OnTreeDoubleclick")
        pt = event.GetPosition();
        itemId, flags = self.HitTest(pt)
        dataSourceTreeNode = self.GetItemData(itemId)

        if dataSourceTreeNode.depth == 2:
            # Open a new tab in SQL execution Pane. It is for table info.
            # TODO 
            tableName = self.GetItemText(itemId)
            self.openWorksheet(sheetName=tableName)

#         if self.IsExpanded(itemId):
#             self.Collapse(itemId)
#         else:
#             self.Expand(itemId)
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
        dataSourceTreeNode = self.GetItemData(item)
        if dataSourceTreeNode:
            tt = dataSourceTreeNode.dataSource.connectionName
            evt.ToolTip = tt
        else:
            evt.Skip()

    def _OnItemActivated(self, evt):
        logger.debug('_OnItemActivated')
        itemId = evt.GetItem()
        dataSourceTreeNode = self.GetItemData(itemId)
        if dataSourceTreeNode.depth == 0:
            self.onConnectDb(evt, self.GetSelections())
        elif dataSourceTreeNode.depth == 2:
            tableName = self.GetItemText(itemId)
            self.openWorksheet(sheetName=tableName, dataSourceTreeNode=dataSourceTreeNode)
        evt.Skip()

    def openWorksheet(self, sheetName="tableName", dataSourceTreeNode=None):
        if hasattr(self.GetTopLevelParent(), '_mgr'):
            tableInfo = CreatingTableInfoPanel(self, -1, style=wx.CLIP_CHILDREN | wx.BORDER_NONE, tableName=sheetName, dataSourceTreeNode=dataSourceTreeNode)
            sqlExecutionTab = self.GetTopLevelParent()._mgr.addTabByWindow(window=tableInfo , imageName="script.png", captionName=sheetName, tabDirection=5)

    def _OnItemCollapsed(self, evt):
        logger.debug('_OnItemCollapsed')
        item = evt.GetItem()
#         self.DoItemCollapsed(item)
        evt.Skip()

    def _OnItemExpanding(self, evt):
        logger.debug('_OnItemExpanding')
        item = evt.GetItem()
#         self.DoItemExpanding(item)
        evt.Skip()

    def _OnMenu(self, evt):
        logger.debug('_OnMenu')
        try:
            item = evt.GetItem()
            
            menu = self.createMenu()
            self.PopupMenu(menu)
            menu.Destroy()
#             self.DoShowMenu(item)
        except Exception as e :
            logger.error(e)

    def onRefresh(self, event, nodes):
        logger.debug('onRootRefresh')
        '''
        1. find current active connection.
        2. refresh only that connection.
        '''
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            logger.debug(dataSourceTreeNode.dataSource.connectionName)
            if dataSourceTreeNode.dataSource.isConnected and dataSourceTreeNode.depth == 1:
                logger.debug(f'refreshing {dataSourceTreeNode.dataSource.connectionName}')

    def createMenu(self):
        logger.debug('createMenu')
        menu = wx.Menu()
        nodes = self.GetSelections()
        
        if len(nodes) == 1 :
            dataSourceTreeNode = self.GetItemData(nodes[0])
            logger.debug(dataSourceTreeNode.dataSource.connectionName)
            
            if dataSourceTreeNode.dataSource.isConnected:
                importBmp = wx.MenuItem(menu, ID_IMPORT, "&Import CSV / Excel")
                importBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="import.png")))
                importMenu = menu.Append(importBmp) 
                self.Bind(wx.EVT_MENU, lambda e: self.onImport(e, nodes), importMenu)
                
                sqlEditorBmp = wx.MenuItem(menu, ID_newWorksheet, "SQL Editor in new Tab")
                sqlEditorBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="script.png")))
                item3 = menu.Append(sqlEditorBmp)
                self.Bind(wx.EVT_MENU, lambda e: self.onOpenSqlEditorTab(e, nodes), item3)
            
            if dataSourceTreeNode.depth == 1:
                item = nodes[0]
                if 'table' in self.GetItemText(item):
                    newTableBmp = wx.MenuItem(menu, wx.ID_ANY, "Create new table")
                    newTableBmp.SetBitmap(self.fileOperations.getImageBitmap(imageName="table_add.png"))
                    newTableItem = menu.Append(newTableBmp)                 
                    
    #                 newTableItem = menu.Append(wx.ID_ANY, "Create new table")
                    erDiagramItem = menu.Append(wx.ID_ANY, "Create ER diagram")
#                     refreshTableItem = menu.Append(wx.ID_ANY, "Refresh  \tF5")
                    
                    self.Bind(wx.EVT_MENU, lambda e: self.onNewTable(e, item), newTableItem)
                    
                    self.Bind(wx.EVT_MENU, lambda e: self.onCreateErDiagramItem(e, item), erDiagramItem)
                    
#                     self.Bind(wx.EVT_MENU, lambda e: self.onRefreshTable(e, item), refreshTableItem)
                    
                if 'view' in self.GetItemText(item):
                    newViewItem = menu.Append(wx.ID_ANY, "Create new view")
#                     item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                    self.Bind(wx.EVT_MENU, lambda e: self.onNewView(e, item), newViewItem)
                if 'index' in self.GetItemText(item) :
                    newIndexItem = menu.Append(wx.ID_ANY, "Create new index")
#                     item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                    self.Bind(wx.EVT_MENU, lambda e: self.onNewIndex(e, item), newIndexItem)
        if len(nodes) == 2:
            
            bmp = wx.MenuItem(menu, wx.NewIdRef(), "Compare with each other")
            bmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="compare.png")))
            compareMenu = menu.Append(bmp)
            self.Bind(wx.EVT_MENU, lambda e:  self.onCompareDatabase(e, nodes), compareMenu)
            
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            logger.debug(dataSourceTreeNode.dataSource.connectionName)
            if dataSourceTreeNode.depth == 0:
                dataSourceTreeNode = self.GetItemData(node)
                     
        refreshBmp = wx.MenuItem(menu, ID_ROOT_REFERESH, "&Refresh \tF5")
        refreshBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="database_refresh.png")))
        rootRefresh = menu.Append(refreshBmp)

        infoMenuItem = wx.MenuItem(menu, ID_CONNECTION_PROPERTIES, "Properties")
        infoBmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU, (16, 16)) 
        infoMenuItem.SetBitmap(infoBmp)     
        item4 = menu.Append(infoMenuItem)    
        
#         refreshBmp = wx.MenuItem(menu, wx.ID_REFRESH, "&Refresh")
#         refreshBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="database_refresh.png")))
#         item5 = menu.Append(refreshBmp)
        
#             item6 = menu.Append(wx.ID_ANY, "Properties")
#             item7 = wx.MenuItem(menu, wx.ID_ANY, "&Smile!\tCtrl+S", "This one has an icon")
#             item7.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join(path, "index.png"))))
#             menu.AppendItem(item7)
        
        if self.isAllNodeOfGivenDepth(depth=0, nodes=nodes):
            menu.AppendSeparator()
            if self.isAllConnected(depth=0, nodes=nodes):

                def onDisconnectDb(event):
                    logger.debug('inner onDisconnectDb')   

                item1 = menu.Append(ID_DISCONNECT_DB, "Disconnect")
                self.Bind(wx.EVT_MENU, lambda e: self.onDisconnectDb(e, nodes), item1)
            elif self.isAllDisconnected(depth=0, nodes=nodes):         
                item2 = menu.Append(ID_CONNECT_DB, "Connect")
                self.Bind(wx.EVT_MENU, lambda e:  self.onConnectDb(e, nodes), item2)  
            else: 
                item2 = menu.Append(ID_CONNECT_DB, "Connect")
                self.Bind(wx.EVT_MENU, lambda e:  self.onConnectDb(e, nodes), item2)  
                item1 = menu.Append(ID_DISCONNECT_DB, "Disconnect")
                self.Bind(wx.EVT_MENU, lambda e: self.onDisconnectDb(e, nodes), item1)
                        
            deleteMenuItem = wx.MenuItem(menu, wx.ID_DELETE, "Delete reference \t Delete")
            delBmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
            deleteMenuItem.SetBitmap(delBmp)
            delMenu = menu.Append(deleteMenuItem)
            
            deleteWithDatabaseMenuItem = wx.MenuItem(menu, ID_deleteWithDatabase, "Delete with database \t Shift + Delete")
            delBmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
            deleteWithDatabaseMenuItem.SetBitmap(delBmp)
            deleteWithDatabaseMenu = menu.Append(deleteWithDatabaseMenuItem) 
            self.Bind(wx.EVT_MENU, lambda e: self.onDeleteConnection(e, nodes), delMenu)
            self.Bind(wx.EVT_MENU, lambda e: self.onDeleteWithDatabaseTable(e, nodes), deleteWithDatabaseMenu)  
        
        self.Bind(wx.EVT_MENU, lambda e: self.onProperties(e, nodes), item4)
        
#         self.Bind(wx.EVT_MENU, lambda e: self.onRefresh(e, nodes), item5)
#             self.Bind(wx.EVT_MENU, self.onEditConnection, item6)

        self.Bind(wx.EVT_MENU, lambda e: self.onRefresh(e, nodes), rootRefresh)
        return menu
    
    def onNewTable(self, event, node):
        logger.debug('onNewTable')
        connectionName = self.GetItemText(self.GetItemParent(node))
        
        newTableName = SQLUtils().definingTableName(connectionName)
        
        tableFrame = CreatingTableFrame(None, 'Table creation', connectionName, newTableName)
#         frame = CreateTableFrame(None, 'table creation')
    
#         tableDict = dict()
#         tableFrame.setData(tableDict)
        tableFrame.Show()
#         app.MainLoop()
        
    def onNewView(self, event):
        logger.debug('onNewView')

#         tableFrame = CreateTableFrame(None, 'Table creation')
    def onNewColumn(self, event):
        logger.debug('onNewColumn')
        logger.debug("TODO add a new column")

    def onNewIndex(self, event):
        logger.debug('onNewIndex')
        logger.debug("TODO add a new Index")   

    def isAllConnected(self, depth=0, nodes=None):
        allConnected = True
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            if not dataSourceTreeNode.dataSource.isConnected:
                allConnected = False
                break
        return allConnected

    def isAllDisconnected(self, depth=0, nodes=None):
        allDisconnected = True
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            if  dataSourceTreeNode.dataSource.isConnected:
                allDisconnected = False
                break
        return allDisconnected
    
    def isAllNodeOfGivenDepth(self, depth=None, nodes=None):
        allNodeOfGivenDepth = True
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            logger.debug(dataSourceTreeNode.dataSource.connectionName)
            if dataSourceTreeNode.depth != depth:
                allNodeOfGivenDepth = False
                break
        return allNodeOfGivenDepth
    
    def onOpenSqlEditorTab(self, event, nodes):
        logger.debug('onOpenSqlEditorTab')
#         self.openWorksheet(sheetName="Worksheet")
        pub.sendMessage('onNewWorksheet', event=event, extra1='onJavaPerspective')
        
    def onProperties(self, event, nodes):
        if event.Id == ID_CONNECTION_PROPERTIES:
            logger.debug('onProperties')
        
    def onImport(self, event, nodes):
        logger.debug('onImport')
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            frame = ImportingCsvExcelFrame(None, 'Import CSV Excel', dataSourceTreeNode.dataSource.connectionName)
            frame.Show()

    def onDeleteConnection(self, event, nodes):
        logger.debug('onDeleteConnection')
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            logger.debug(dataSourceTreeNode.dataSource.connectionName)
            self.sqlExecuter.removeConnctionRow(dataSourceTreeNode.dataSource.connectionName)
            self.recreateTree()
        selectedItemId = self.tree.GetSelection()
        selectedItemText = self.tree.GetItemText(self.tree.GetSelection())
        logger.debug(selectedItemText)

    def onCompareDatabase(self, event, nodes):
        logger.debug('onCompareDatabase')   
#         asf=self.OnCompareItems(nodes[0], nodes[1])
#         print(asf)

    def onDisconnectDb(self, event, nodes):
        logger.debug('onDisconnectDb')   
#         selectedItem = self.GetSelections()
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            dataSourceTreeNode.dataSource.isConnected = False
            self.SetItemHasChildren(node, self.hasNodeChildren(dataSourceTreeNode))
            self.DeleteChildren(node)

    def onConnectDb(self, event, nodes):
        logger.debug('onConnectDb')
        for node in nodes:
            itemId = node
            dataSourceTreeNode = self.GetItemData(node)
            dataSourceTreeNode.dataSource.isConnected = True
            self.SetItemHasChildren(itemId, self.hasNodeChildren(dataSourceTreeNode))
            # logic to connect
            self.deleteChildren(itemId)
            dataSource = dataSourceTreeNode.dataSource
            if os.path.isfile(dataSourceTreeNode.dataSource.filePath): 
                dbObjects = ManageSqliteDatabase(connectionName=dataSourceTreeNode.dataSource.connectionName , databaseAbsolutePath=dataSourceTreeNode.dataSource.filePath).getObject()
                
                for dbObject in dbObjects[1]:
                    for k0, v0 in dbObject.items():
                        logger.debug("k0 : %s, v0: %s", k0, v0)
                        nodeLabel = f'{k0} ( {len(v0)})'
                        dataSourceTreeNode = DataSourceTreeNode(depth=1, dataSource=dataSource, nodeLabel=nodeLabel, imageName=f"folder.png", children=None)
                         
                        child_itemId_0 = self.appendNode(targetNode=itemId, nodeLabel=dataSourceTreeNode.nodeLabel , dataSourceTreeNode=dataSourceTreeNode)
                        for v00 in v0:
                            for k1, v1 in v00.items():
                                dataSourceTreeNode = DataSourceTreeNode(depth=2, dataSource=dataSource, nodeLabel=f'{k0} ( {len(v0)})', imageName=f"{k0}.png", children=None)
                                if k0 == 'table':
                                    child_itemId_1 = self.appendNode(targetNode=child_itemId_0, nodeLabel=k1 , dataSourceTreeNode=dataSourceTreeNode)
    
                                    nodeLabel = 'Columns' + ' (' + str(len(v1)) + ')'
                                    dataSourceTreeNode = DataSourceTreeNode(depth=3, dataSource=dataSource, nodeLabel=nodeLabel, imageName=f"columns.png", children=None)
                                    child_itemId1_1 = self.appendNode(targetNode=child_itemId_1, nodeLabel=nodeLabel, dataSourceTreeNode=dataSourceTreeNode) 
                                    
                                    dataSourceTreeNode = DataSourceTreeNode(depth=3, dataSource=dataSource, nodeLabel=f'Unique Keys', imageName=f"columns.png", children=None)
                                    child_itemId1_2 = self.appendNode(targetNode=child_itemId_1, nodeLabel='Unique Keys', dataSourceTreeNode=dataSourceTreeNode) 
                                    
                                    dataSourceTreeNode = DataSourceTreeNode(depth=3, dataSource=dataSource, nodeLabel=f'Foreign Keys', imageName=f"columns.png", children=None)
                                    child_itemId1_3 = self.appendNode(targetNode=child_itemId_1, nodeLabel='Foreign Keys', dataSourceTreeNode=dataSourceTreeNode) 
                                    
                                    dataSourceTreeNode = DataSourceTreeNode(depth=3, dataSource=dataSource, nodeLabel=f'References', imageName=f"columns.png", children=None)
                                    child_itemId1_4 = self.appendNode(targetNode=child_itemId_1, nodeLabel='References', dataSourceTreeNode=dataSourceTreeNode)
                                elif k0 == 'index':
                                    dataSourceTreeNode = DataSourceTreeNode(depth=3, dataSource=dataSource, nodeLabel=f'{k0} ( {len(v1)})', imageName=f"index.png", children=None)
                                    child_itemId2_1 = self.appendNode(targetNode=child_itemId_0, nodeLabel=k1 , dataSourceTreeNode=dataSourceTreeNode)
                                elif k0 == 'view':
                                    dataSourceTreeNode = DataSourceTreeNode(depth=3, dataSource=dataSource, nodeLabel=f'{k0} ( {len(v1)})', imageName=f"index.png", children=None)
                                    child_itemId3_1 = self.appendNode(targetNode=child_itemId_0, nodeLabel=k1 , dataSourceTreeNode=dataSourceTreeNode)
             
                                for v2 in v1:
                                    if k0 == 'table':
                                        imageName = "textfield.png"  # setting VARCHAR image
                                        if v2[5] == 1:
                                            imageName = "key.png"  # setting primary key image
                                        elif v2[5] == 0 and v2[2] in ['INTEGER', 'INT']:
                                            imageName = "column.png"  # setting INTEGER image
                                            
                                        nodeLabel = v2[1]
                                        dataSourceTreeNode = DataSourceTreeNode(depth=4, dataSource=dataSource, nodeLabel=nodeLabel, imageName=imageName, children=None)
                                        child_itemId2 = self.appendNode(targetNode=child_itemId1_1, nodeLabel=nodeLabel, dataSourceTreeNode=dataSourceTreeNode)
            else:
                updateStatus = f"Unable to connect '{ dataSourceTreeNode.dataSource.filePath } , No such file. "
                self.consoleOutputLog(updateStatus)
                font = self.GetTopLevelParent().statusbar.GetFont() 
                font.SetWeight(wx.BOLD) 
                self.GetTopLevelParent().statusbar.SetFont(font) 
                self.GetTopLevelParent().statusbar.SetForegroundColour(wx.RED) 
                self.GetTopLevelParent().statusbar.SetStatusText(updateStatus, 1)
                logger.error(updateStatus)

    def consoleOutputLog(self, exception=None):
        now = datetime.datetime.now()
        strftime = now.strftime("%Y-%m-%d %H:%M:%S")
        newline = "\n"
        if self.GetTopLevelParent()._mgr.GetPane("consoleOutput").window.text.Value.strip() == "":
            newline = ""
        self.GetTopLevelParent()._mgr.GetPane("consoleOutput").window.text.AppendText("{}{} {}".format(newline, strftime, exception))
        
    def onEditTable(self, event):
        logger.debug('onEditTable')

    def deleteChildren(self, itemId):
        '''
        node: itemId 
        '''
        return TreeCtrl.DeleteChildren(self, itemId)

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
        
    def initialize(self):
        sqlExecuter = SQLExecuter()
        self.DeleteAllItems()
        dbList = sqlExecuter.getListDatabase()     
        self.AddRoot('root')
        self.SetItemData(self.RootItem, "root")   
        for db in dbList:
            dataSource = DataSource(connectionName=db[1], filePath=db[2])
#             dataSourceTreeNode = DataSourceTreeNode(depth=0, dataSource=dataSource, imageName='sqlite.png')
            self.addWatchConnection(dataSource=dataSource)
#             self.appendNode(targetNode=self.RootItem, nodeLabel=dataSourceTreeNode.dataSource.connectionName, dataSourceTreeNode=dataSourceTreeNode)
    
    def addWatchConnection(self, dataSource=None):

        logger.debug('AddWatchConnection')
        if dataSource.filePath not in self._watch:
            self._watch.append(dataSource.filePath)
            dataSourceTreeNode = DataSourceTreeNode(depth=0, dataSource=dataSource, imageName='sqlite.png')
            return self.appendNode(targetNode=self.RootItem, nodeLabel=dataSourceTreeNode.dataSource.connectionName, dataSourceTreeNode=dataSourceTreeNode)

    def appendNode(self, targetNode=None, nodeLabel=None, dataSourceTreeNode=None):
        """Append a child node to the tree
        @param item: TreeItem parent node
        @param path: path to add to node
        @return: new node

        """
#         logger.debug('AppendFileNode')
        img = self.getDataSourceTreeNodeImage(dataSourceTreeNode)
#         name = dataSourceTreeNode.dataSource.connectionName
        child = self.AppendItem(targetNode, nodeLabel, img)
        self.SetItemData(child, dataSourceTreeNode)
        if self.hasNodeChildren(dataSourceTreeNode):
            self.SetItemHasChildren(child, True)
        return child
    
    def hasNodeChildren(self, dataSourceTreeNode):
        hasChildren = False
        if dataSourceTreeNode.depth == 0 and dataSourceTreeNode.dataSource.isConnected:
            hasChildren = True
        return hasChildren

    def getDataSourceTreeNodeImage(self, dataSourceTreeNode=None):
        '''
        return image count number in self.ImageList
        '''
        imageIndex = self.iconsDictByImageName[dataSourceTreeNode.imageName]
        
        return imageIndex

    def connectDatabase(self):
        logger.debug('connectDatabase')


# Test
if __name__ == '__main__':
    app = wx.App(False)
    f = wx.Frame(None)
    databaseTree = DatabaseTree(f)
#     databaseTree.initialize()
#     dataSource = DataSource(connectionName="employee_9_jan_2019", filePath=r'C:\Users\xbbntni\eclipse-workspace2\pyTrack\src\employee.sqlite')
#     databaseTree.addWatchConnection(dataSource)
#     dataSource = DataSource(connectionName="one", filePath=r'C:\Users\xbbntni\one.sqlite')
#     databaseTree.addWatchConnection(dataSource)
#     dataSource = DataSource(connectionName="two", filePath=r'C:\Users\xbbntni\two.sqlite')
#     databaseTree.addWatchConnection(dataSource)
    
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
