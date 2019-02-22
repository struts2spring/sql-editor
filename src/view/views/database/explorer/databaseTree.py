'''
Created on Jan 30, 2019


'''
import wx
from wx import TreeCtrl

import logging.config
from src.view.constants import LOG_SETTINGS, ID_ROOT_REFERESH, ID_DISCONNECT_DB, \
    ID_CONNECT_DB, ID_newWorksheet, ID_CONNECTION_PROPERTIES, ID_IMPORT, \
    ID_deleteWithDatabase, keyMap, ID_EXPORT, ID_SELECT_SQL, ID_INSERT_SQL, ID_UPDATE_SQL, \
    ID_DELETE_SQL
from src.view.util.FileOperationsUtil import FileOperations
import os
from src.sqlite_executer.ConnectExecuteSqlite import ManageSqliteDatabase, \
    SQLUtils, SQLExecuter

from wx.lib.pubsub import pub
from src.view.importing.importCsvExcel import ImportingCsvExcelFrame
from src.view.table.CreateTable import CreateTableFrame
import datetime
from src.view.views.console.worksheet.tableInfoPanel import CreatingTableInfoPanel
from src.view.schema.CreateSchemaViewer import CreateErDiagramFrame

from src.view.views.database.explorer.GenerateSql import GenerateSqlFrame

import itertools

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class DataSource():
    
    def __init__(self, connectionName=None, filePath=None):
        self.connectionName = connectionName
        self.filePath = filePath
        self.isConnected = False


class DataSourceTreeNode():
    
    def __init__(self, depth=None, dataSource=None, nodeLabel=None, imageName=None, children=None, sqlType=None, nodeType=None):
        self.depth = depth
        self.dataSource = dataSource
        self.imageName = imageName
        self.nodeLabel = nodeLabel
        self.children = children
        self.sqlType = sqlType
        self.nodeType = nodeType

    def setSqlType(self, sqlType=None):
        self.sqlType = sqlType

    
class DatabaseTree(TreeCtrl):

    def __init__(self, parent, style=wx.TR_HIDE_ROOT | 
                                             wx.TR_FULL_ROW_HIGHLIGHT | 
                                             wx.TR_LINES_AT_ROOT | 
                                             wx.TR_HAS_BUTTONS | 
                                             wx.TR_MULTIPLE | 
                                             wx.TR_EDIT_LABELS | wx.BORDER_NONE):
        super(DatabaseTree, self).__init__(parent, style=style)
        self.sqlExecuter = SQLExecuter()
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

        self.Bind(wx.EVT_TREE_KEY_DOWN, self.onTreeKeyDown)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        
        self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('C'), wx.ID_COPY),
                                              (wx.ACCEL_CTRL, ord('V'), wx.ID_PASTE),
                                              (wx.ACCEL_ALT, ord('X'), wx.ID_PASTE),
                                              (wx.ACCEL_SHIFT | wx.ACCEL_ALT, ord('Y'), wx.ID_PASTE)
                                             ])
        self.SetAcceleratorTable(self.accel_tbl)
        self.Bind(wx.EVT_MENU, self.onTreeCopy, id=wx.ID_COPY)
        
    def OnChar(self, evt):
        logger.debug('OnChar')
        
        modifiers, keyname = self.LogKeyEvent("Char", evt)
        if keyname == 'Ctrl+C':
            self.onTreeCopy(evt)
        elif keyname == 'WXK_F2':
            self.onF2KeyPress(evt)
        elif keyname == 'WXK_DELETE':
            self.onDeleteKeyPress(evt)

    def LogKeyEvent(self, evType, evt):
        keycode = evt.GetKeyCode()
        keyname = keyMap.get(keycode, None)

        if keyname is None:
            if keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    char_keycode = chr(ord('A') + keycode - 1)
                    keyname = f"Ctrl+{char_keycode}"
                else:
                    keyname = u"\"%s\"" % chr(keycode)
            else:
                keyname = u"(%s)" % keycode

        modifiers = ""
        for mod, ch in [(evt.ControlDown(), 'C'),
                        (evt.AltDown(), 'A'),
                        (evt.ShiftDown(), 'S'),
                        (evt.MetaDown(), 'M'),
                        (evt.RawControlDown(), 'R'), ]:
            if mod:
                modifiers += ch
            else:
                modifiers += '-'
        logger.debug(modifiers + keyname)
        return modifiers, keyname

    def onTreeKeyDown(self, event):
        logger.debug('onTreeKeyDown')
#         self.LogKeyEvent('KeyDown', event.GetKeyEvent())
        keypress = self.GetKeyPress(event)
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
        logger.debug(f'onTreeKeyDown keycode: {keycode}  keypress: {keypress} keyname: {keyname}')
#         logger.debug(keypress == 'WXK_F2')
#         
# #         if keypress == 'Ctrl+C':
# #             pass
# #             self.onTreeCopy(event)
        if keypress == 'WXK_F2':
            self.onF2KeyPress(event)
        elif keypress == 'WXK_DELETE':
            self.onDeleteKeyPress(event)
        event.Skip()

    def GetKeyPress(self, evt):
        keycode = evt.GetKeyCode()
        keyname = keyMap.get(keycode, None)
        modifiers = ""
        for mod, ch in ((evt.GetKeyEvent().ControlDown(), 'Ctrl+'),
                        (evt.GetKeyEvent().AltDown(), 'Alt+'),
                        (evt.GetKeyEvent().ShiftDown(), 'Shift+'),
                        (evt.GetKeyEvent().MetaDown(), 'Meta+')):
            if mod:
                modifiers += ch
            else:
                modifiers += '-'
#         if keyname is None:
#             if keycode < 256:
#                 if keycode == 0:
#                     keyname = "NUL"
#                 elif keycode < 27:
#                     char_keycode=chr(ord('A') + keycode-1)
#                     keyname = f"Ctrl-{char_keycode}" % (ord('A') + keycode - 1)
#                 else:
#                     keyname = u"\"%s\"" % keycode
#             else:
#                 keyname = u"(%s)" % keycode    
        if keyname is None:
            if keycode == 0:
                keyname = "NUL"
            elif  27 < keycode < 256  :
                keyname = chr(keycode)
            elif  keycode < 27 :
                keyname = chr(ord('A') + keycode - 1)
                logger.debug(keyname)
            else:
                keyname = f"({chr(keycode)})unknown"
        logger.debug(f'modifiers:{modifiers},keyname:{keyname}')
        return modifiers + keyname

    #----------------------------------------------------------------------
    def onDeleteKeyPress(self, event):
        try:
            nodes = self.GetSelections()
            for node in nodes:
                dataSourceTreeNode = self.GetItemData(node)
                if dataSourceTreeNode.depth == 0:
                    self.onDeleteConnection(event, nodes=[node])
                elif dataSourceTreeNode.depth == 2:
                    
                    logger.debug("TODO delete table")
                    self.onDeleteTable(event)
                elif dataSourceTreeNode.depth == 4:
                    logger.debug("TODO delete column")
        except Exception as e:
            logger.error(e, exc_info=True)
            
    def onF2KeyPress(self, event):
        try:
            nodes = self.GetSelections()
            dataSourceTreeNode = self.GetItemData(nodes[0])
            if dataSourceTreeNode.depth == 0:
                self.onRenameConnection(event, dataSourceTreeNode=dataSourceTreeNode, node=nodes[0])
            elif dataSourceTreeNode.depth == 2:
                self.onRenameTable(event, dataSourceTreeNode=dataSourceTreeNode, node=nodes[0])
            elif dataSourceTreeNode.depth == 4:
                self.onRenameColumn(event, dataSourceTreeNode=dataSourceTreeNode, node=nodes[0])
                
        except Exception as e:
            logger.error(e, exc_info=True)       

    def onTreeCopy(self, event):
        """"""
        logger.debug('onTreeCopy')
        nodes = self.GetSelections()
        nodeTexts = []
        for node in nodes:
            nodeTexts.append(self.GetItemText(node))
        
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText("\n".join(nodeTexts))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(self.dataObj)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
#         if wx.TheClipboard.Open():
#             wx.TheClipboard.SetData(wx.TextDataObject("\n".join(nodeTexts)))
#             wx.TheClipboard.Close()

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
        nodes = self.GetSelections()
        dataSourceTreeNode = self.GetItemData(itemId)
        if dataSourceTreeNode.nodeType == 'connection':
            self.onConnectDb(evt, nodes)
            self.connectingDatabase(event=evt, nodes=nodes)
            
        if dataSourceTreeNode.nodeType == 'table':
            self.openWorksheet(sheetName=dataSourceTreeNode.sqlType.name, dataSourceTreeNode=dataSourceTreeNode)
        if dataSourceTreeNode.nodeType == 'view':
            # TODO : need to write a view panel
            pass
        if dataSourceTreeNode.nodeType == 'trigger':
            # TODO : need to write a trigger panel
            pass
        evt.Skip()
        
    def connectingDatabase(self, event=None, nodes=None):
        '''
            This method will open new worksheet
        '''
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
#                 logic to connect worksheet goes here
#             for dataSourceTreeNode in dataSourceTreeNodeList:
            pub.sendMessage('onNewWorksheet', event=event, dataSourceTreeNode=dataSourceTreeNode)        

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

    def onRefresh(self, event, nodes=None):
        logger.debug('onRootRefresh')
        '''
        1. find current active connection.
        2. refresh only that connection.
        '''
        if nodes:
            self.onDisconnectDb(event, nodes)
            self.onConnectDb(event, nodes)
        else:
#             nodes = self.GetSelections()
            for node in self.GetChildNodes(self.RootItem):
                dataSourceTreeNode = self.GetItemData(node)
                if dataSourceTreeNode.dataSource.isConnected:
                    self.onDisconnectDb(event, [node])
                    self.onConnectDb(event, [node])
            pass
#         for node in nodes:
#             dataSourceTreeNode = self.GetItemData(node)
#             logger.debug(dataSourceTreeNode.dataSource.connectionName)
#             if dataSourceTreeNode.dataSource.isConnected and dataSourceTreeNode.depth == 1:
#                 logger.debug(f'refreshing {dataSourceTreeNode.dataSource.connectionName}')

    def createMenu(self):
        logger.debug('createMenu')
        menu = wx.Menu()
        nodes = self.GetSelections()
        
        if len(nodes) == 1 :
            dataSourceTreeNode = self.GetItemData(nodes[0])
            logger.debug(dataSourceTreeNode.dataSource.connectionName)
            
            if dataSourceTreeNode.dataSource.isConnected :
                if dataSourceTreeNode.nodeType in ('table', 'folder_table') :  # and 'table' in self.GetItemText(nodes[0])
                    importBmp = wx.MenuItem(menu, ID_IMPORT, "&Import Data")
                    importBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="import.png")))
                    importMenu = menu.Append(importBmp) 
                    self.Bind(wx.EVT_MENU, lambda e: self.onImport(e, nodes), importMenu)
                    
                    exportBmp = wx.MenuItem(menu, ID_EXPORT, "&Export Data")
                    exportBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="export.png")))
                    exportMenu = menu.Append(exportBmp) 
                    self.Bind(wx.EVT_MENU, lambda e: self.onExport(e, nodes), exportMenu)
                
                if dataSourceTreeNode.nodeType == 'connection':
                    sqlEditorBmp = wx.MenuItem(menu, ID_newWorksheet, "SQL Editor in new Tab")
                    sqlEditorBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="script.png")))
                    item3 = menu.Append(sqlEditorBmp)
                    self.Bind(wx.EVT_MENU, lambda e: self.onOpenSqlEditorTab(e, nodes), item3)
                if dataSourceTreeNode.nodeType == 'table':
                    secondLevelMenuItem = wx.Menu()
#                     generateBmp = wx.MenuItem(menu, wx.ID_ANY, "Generate SQL")
#                     generateBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="table_edit.png")))
#                     generateItem = menu.Append(generateBmp)

                    secondLevelMenuList = [
                                            [ID_SELECT_SQL, "SELECT"],
                                            [ID_INSERT_SQL, "INSERT"],
                                            [ID_UPDATE_SQL, "UPDATE"],
                                            [ID_DELETE_SQL, "DELETE"],
                                            
                                        ]
                    for secondLevelMenu in secondLevelMenuList:
                        menuItem = wx.MenuItem(secondLevelMenuItem, secondLevelMenu[0], secondLevelMenu[1]) 
                        menuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName="textfield.png"))
                        secondLevelMenuItem.Append(menuItem)
                        self.Bind(wx.EVT_MENU, lambda e: self.onGenerateSql(e, dataSourceTreeNode), id=secondLevelMenu[0])
                    
                    menu.Append(-1, "Generate SQL", secondLevelMenuItem)
                    
                    editTableBmp = wx.MenuItem(menu, wx.ID_ANY, "Edit table")
                    editTableBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="table_edit.png")))
                    editTableItem = menu.Append(editTableBmp) 
                    
        #             editTableItem = menu.Append(wx.ID_ANY, "Edit table ")
                    copyItemBmp = wx.MenuItem(menu,wx.ID_COPY, "Copy \tCtrl+C")
                    copyItemBmp.SetBitmap(self.fileOperations.getImageBitmap(imageName="copy_edit_co.png"))
                    copyItemItem = menu.Append(copyItemBmp)
                    
                    renameTableItem = menu.Append(wx.ID_ANY, "Rename Table \tF2")
                    copyCreateTableItem = menu.Append(wx.ID_ANY, "Copy create table statement")
        
                    deleteTableBmp = wx.MenuItem(menu, wx.ID_ANY, "&Delete table \tDelete")
                    deleteTableBmp.SetBitmap(self.fileOperations.getImageBitmap(imageName="table_delete.png"))
                    deleteTableItem = menu.Append(deleteTableBmp)
        
                    self.Bind(wx.EVT_MENU, lambda e: self.onDeleteTable(e, dataSourceTreeNode=dataSourceTreeNode, node=nodes[0]), deleteTableItem)
                    
                    self.Bind(wx.EVT_MENU, lambda e: self.onEditTable(e, dataSourceTreeNode=dataSourceTreeNode, node=nodes[0]), editTableItem)
                    self.Bind(wx.EVT_MENU, lambda e: self.onRenameTable(e, dataSourceTreeNode=dataSourceTreeNode, node=nodes[0]), renameTableItem)
                    self.Bind(wx.EVT_MENU, self.onCopyCreateTableStatement, copyCreateTableItem)
                        
#             if dataSourceTreeNode.depth == 1:
                node = item = nodes[0]
            if dataSourceTreeNode.nodeType in ('folder_table', 'table'):
                newTableBmp = wx.MenuItem(menu, wx.ID_ANY, "Create new table")
                newTableBmp.SetBitmap(self.fileOperations.getImageBitmap(imageName="table_add.png"))
                newTableItem = menu.Append(newTableBmp)                 
                
#                 newTableItem = menu.Append(wx.ID_ANY, "Create new table")
                erDiagramItem = menu.Append(wx.ID_ANY, "Create ER diagram")
#                     refreshTableItem = menu.Append(wx.ID_ANY, "Refresh  \tF5")
                
                self.Bind(wx.EVT_MENU, lambda e: self.onNewTable(e, dataSourceTreeNode=dataSourceTreeNode, node=node), newTableItem)
                
                self.Bind(wx.EVT_MENU, lambda e: self.onCreateErDiagramItem(e, dataSourceTreeNode=dataSourceTreeNode, node=node), erDiagramItem)
                
#                     self.Bind(wx.EVT_MENU, lambda e: self.onRefreshTable(e, item), refreshTableItem)
                
            if dataSourceTreeNode.nodeType == 'folder_view':
                newViewItem = menu.Append(wx.ID_ANY, "Create new view")
#                     item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                self.Bind(wx.EVT_MENU, lambda e: self.onNewView(e, dataSourceTreeNode=dataSourceTreeNode, node=item), newViewItem)
            if dataSourceTreeNode.nodeType == 'folder_index':
                newIndexItem = menu.Append(wx.ID_ANY, "Create new index")
#                     item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                self.Bind(wx.EVT_MENU, lambda e: self.onNewIndex(e, dataSourceTreeNode=dataSourceTreeNode, node=item), newIndexItem)
            elif dataSourceTreeNode.nodeType in ('folder_column', 'table'):
                    newColumnItem = menu.Append(wx.ID_ANY, "Add new column")
                    self.Bind(wx.EVT_MENU, lambda e: self.onNewColumn(e, dataSourceTreeNode=dataSourceTreeNode, node=node), newColumnItem)  
            elif dataSourceTreeNode.nodeType in ('column') :
                copyColumnItem = menu.Append(wx.ID_COPY, "Copy \tCtrl+C")
                copyColumnItem.SetBitmap(self.fileOperations.getImageBitmap(imageName="copy_edit_co.png"))
                renameColumnItem = menu.Append(wx.ID_ANY, "Rename Column \tF2")
                self.Bind(wx.EVT_MENU, lambda e: self.onColumnCopy(e, dataSourceTreeNode=dataSourceTreeNode, node=node), copyColumnItem)
                self.Bind(wx.EVT_MENU, lambda e: self.onRenameColumn(e, dataSourceTreeNode=dataSourceTreeNode, node=node), renameColumnItem)                            
        if len(nodes) == 2:
            
            bmp = wx.MenuItem(menu, wx.NewIdRef(), "Compare with each other")
            bmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="compare.png")))
            compareMenu = menu.Append(bmp)
            self.Bind(wx.EVT_MENU, lambda e:  self.onCompareDatabase(e, nodes), compareMenu)
            
#         for node in nodes:
#             dataSourceTreeNode = self.GetItemData(node)
#             logger.debug(dataSourceTreeNode.dataSource.connectionName)
#             if dataSourceTreeNode.depth == 0:
#                 dataSourceTreeNode = self.GetItemData(node)
                     
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
        
#         if self.isAllNodeOfGivenDepth(depth=0, nodes=nodes):
        if dataSourceTreeNode.nodeType == 'connection':        
            menu.AppendSeparator()
            if self.isAllConnected(nodes=nodes):
    
                def onDisconnectDb(event):
                    logger.debug('inner onDisconnectDb')   
    
                item1 = menu.Append(ID_DISCONNECT_DB, "Disconnect")
                self.Bind(wx.EVT_MENU, lambda e: self.onDisconnectDb(e, nodes), item1)
            elif self.isAllDisconnected(nodes=nodes):         
                item2 = menu.Append(ID_CONNECT_DB, "Connect")
                self.Bind(wx.EVT_MENU, lambda e:  self.onConnectDatabase(e, nodes), item2)  
            else: 
                item2 = menu.Append(ID_CONNECT_DB, "Connect")
                self.Bind(wx.EVT_MENU, lambda e:  self.onConnectDatabase(e, nodes), item2)  
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

    def onGenerateSql(self, event, dataSourceTreeNode=None):
        logger.debug('onGenerateSql')
        sqlText = ''
        manageSqliteDatabase = ManageSqliteDatabase(connectionName=dataSourceTreeNode.dataSource.connectionName ,
                                                    databaseAbsolutePath=dataSourceTreeNode.dataSource.filePath)
        if event.Id == ID_SELECT_SQL:
            sqlText = manageSqliteDatabase.getSelectForTable(dataSourceTreeNode.nodeLabel)
        if event.Id == ID_INSERT_SQL:
            sqlText = manageSqliteDatabase.getInsertForTable(dataSourceTreeNode.nodeLabel)
        if event.Id == ID_UPDATE_SQL:
            sqlText = manageSqliteDatabase.getUpdateForTable(dataSourceTreeNode.nodeLabel)
        if event.Id == ID_DELETE_SQL:
            sqlText = manageSqliteDatabase.getDeleteForTable(dataSourceTreeNode.nodeLabel)
        logger.debug(f'{sqlText}')
        frame = GenerateSqlFrame(self, 'Generate Sql', size=(513, 441), sqlText=sqlText)
        frame.Show()

    def onDeleteWithDatabaseTable(self, event, nodes=None):
        logger.debug('onDeleteWithDatabaseTable')
#         self.onDeleteConnection(event)
        ##################################################################################
#         sqlExecuter = SQLExecuter(database='_opal.sqlite')
#         selectedItemId = self.tree.GetSelection()
#         dbFilePath = sqlExecuter.getDbFilePath(selectedItemText)
#         logger.debug("dbFilePath: %s", dbFilePath)
        fileOperations = FileOperations()
        for node in nodes:
            selectedItemText = self.GetItemText(node)
            dataSourceTreeNode = self.GetItemData(node)
            fileRemoved = fileOperations.removeFile(filename=dataSourceTreeNode.dataSource.filePath)
            if selectedItemText and fileRemoved:
                self.sqlExecuter.removeConnctionRow(selectedItemText)
        self.initialize()
        ##################################################################################

    def onColumnCopy(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onColumnCopy')
        logger.debug('onTreeCopy')
        nodes = self.GetSelections()
        nodeTexts = []
        for node in nodes:
            nodeTexts.append(self.GetItemText(node))
        
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText("\n".join(nodeTexts))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(self.dataObj)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
            
    def onRenameColumn(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onRenameColumn')
        initialColumnName = self.GetItemText(node)
        dlg = wx.TextEntryDialog(self, 'Rename column ' + initialColumnName, 'Rename column ' + initialColumnName, 'Python')
        dlg.SetValue(initialColumnName)

        if dlg.ShowModal() == wx.ID_OK:
            logger.info('You entered: %s\n', dlg.GetValue())
            if dlg.GetValue() != initialColumnName:
                logger.info('update table execute')

                if os.path.isfile(dataSourceTreeNode.dataSource.filePath):     
                    '''
                    First you rename the old table:
                    ALTER TABLE orig_table_name RENAME TO tmp_table_name;
                    Then create the new table, based on the old table but with the updated column name:
                    Then copy the contents across from the original table.
                    

                    '''
                    logger.debug("TODO logic for rename column goes here.")
#                     dbObjects = ManageSqliteDatabase(connectionName=connectionName , databaseAbsolutePath=databaseAbsolutePath).executeText(text) 
        dlg.Destroy()

    def onCreateErDiagramItem(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onCreateErDiagramItem')
       
        dbObjects = ManageSqliteDatabase(connectionName=dataSourceTreeNode.dataSource.connectionName , databaseAbsolutePath=dataSourceTreeNode.dataSource.filePath).getObject()   
             
        createErDiagramFrame = CreateErDiagramFrame(None)
        createErDiagramFrame.setDbObjects(dbObjects=dbObjects)
        createErDiagramFrame.Show()        

    def onNewColumn(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onNewColumn')
        logger.debug("TODO add a new column")    

    def onDeleteTable(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onDeleteTable')
        nodes = self.GetSelections()
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            text = "DROP TABLE '{}'".format(dataSourceTreeNode.nodeLabel)
            dbObjects = ManageSqliteDatabase(connectionName=dataSourceTreeNode.dataSource.connectionName , databaseAbsolutePath=dataSourceTreeNode.dataSource.filePath).executeText(text)
            self.Delete(node)
    
    def onEditTable(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onEditTable')

    def onRenameConnection(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onRenameConnection')
        '''
        1. disconnect Connection.
        2. fire database conn alter connectionName
        3. call init method to load all the connection
        '''

    def onRenameTable(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onRenameTable')
        oldTableName = initialTableName = self.GetItemText(node)
        dlg = wx.TextEntryDialog(self, 'Rename table {} to'.format(initialTableName), 'Rename table {} '.format(initialTableName), 'Python')
        dlg.SetValue(initialTableName)

        if dlg.ShowModal() == wx.ID_OK:
            logger.info('You entered: %s\n', dlg.GetValue())
            if dlg.GetValue() != initialTableName:
                logger.info('update table execute')
                newTableName = dlg.GetValue()
                if os.path.isfile(dataSourceTreeNode.dataSource.filePath):     
                    '''
                    First you rename the old table:
                    '''
                    logger.debug("TODO logic to rename table should go here.")
#                     dropTableSql="DROP TABLE '{}'".format()
                    alterTableSql = f"ALTER TABLE '{oldTableName}' RENAME TO {newTableName}"
                    db = ManageSqliteDatabase(connectionName=dataSourceTreeNode.dataSource.connectionName , databaseAbsolutePath=dataSourceTreeNode.dataSource.filePath)
                    try:
                        db.executeText(alterTableSql)
                    except Exception as e:
                        self.consoleOutputLog(e)
            self.onRefresh(event, nodes=[node])
        dlg.Destroy()

    def onCopyCreateTableStatement(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onCopyCreateTableStatement')

    def onNewTable(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onNewTable')
        connectionName = self.GetItemText(self.GetItemParent(node))
        
        newTableName = SQLUtils().definingTableName(connectionName)
        
        tableFrame = CreateTableFrame(None, Title='Table creation', size=(1000, 600))
#         frame = CreateTableFrame(None, 'table creation')
    
#         tableDict = dict()
#         tableFrame.setData(tableDict)
        tableFrame.Show()
#         app.MainLoop()
        
    def onNewView(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onNewView')

#         tableFrame = CreateTableFrame(None, 'Table creation')

    def onNewIndex(self, event, dataSourceTreeNode=None, node=None):
        logger.debug('onNewIndex')
        logger.debug("TODO add a new Index")   

    def isAllConnected(self, nodes=None):
        allConnected = True
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            if not dataSourceTreeNode.dataSource.isConnected and dataSourceTreeNode.nodeType == 'connection':
                allConnected = False
                break
        return allConnected

    def isAllDisconnected(self, nodes=None):
        allDisconnected = True
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            if  dataSourceTreeNode.dataSource.isConnected and dataSourceTreeNode.nodeType == 'connection':
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
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            pub.sendMessage('onNewWorksheet', event=event, dataSourceTreeNode=dataSourceTreeNode)
        
    def onProperties(self, event, nodes):
        if event.Id == ID_CONNECTION_PROPERTIES:
            logger.debug('onProperties')
        
    def onExport(self, event, nodes):
        logger.debug('onExport')

    def onImport(self, event, nodes):
        logger.debug('onImport')
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            frame = ImportingCsvExcelFrame(None, 'Import CSV Excel', dataSourceTreeNode.dataSource.connectionName)
            frame.Show()

    def onDeleteConnection(self, event, nodes=None):
        logger.debug('onDeleteConnection')
        for node in nodes:
            dataSourceTreeNode = self.GetItemData(node)
            logger.debug(dataSourceTreeNode.dataSource.connectionName)
            SQLExecuter().removeConnctionRow(dataSourceTreeNode.dataSource.connectionName)
            self.Delete(node)
#         self.onRefresh(event, nodes)

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
            
    def onConnectDatabase(self, event, nodes):
        logger.debug('onConnectDatabase')
        self.onConnectDb(event, nodes)
        self.connectingDatabase(event, nodes)
    
    def onConnectDb(self, event, nodes):
        '''
            this method have been used to expand database navigator tree.
        '''
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
                manageSqliteDatabase = ManageSqliteDatabase(connectionName=dataSourceTreeNode.dataSource.connectionName , databaseAbsolutePath=dataSourceTreeNode.dataSource.filePath)
                sqlTypeObjectList = manageSqliteDatabase.getSqlObjects()
                
#                 group for table , view, index and trigger type
                for key, group in itertools.groupby(sqlTypeObjectList, key=lambda sqlTypeObj:sqlTypeObj.type):
#                     logger.debug(f'{key}:{group}')
                    groupList = list(group)
                    nodeLabel = f'{key} ( {len(groupList)})'
                    imageName = f"folder.png"
                    if key in ['view', 'table']:
                        imageName = f"folder_{key}.png"
                    dataSourceTreeNode = DataSourceTreeNode(dataSource=dataSource, nodeLabel=nodeLabel, imageName=imageName, children=None, nodeType=f'folder_{key}')
                    
                    tableNode = self.appendNode(targetNode=itemId, nodeLabel=dataSourceTreeNode.nodeLabel , dataSourceTreeNode=dataSourceTreeNode)
                    for sqlTypeObject in groupList:
                        dataSourceTreeNode = DataSourceTreeNode(dataSource=dataSource, nodeLabel=f'{sqlTypeObject.name}', imageName=f"{sqlTypeObject.type}.png", children=None, nodeType=f"{sqlTypeObject.type}")
                        dataSourceTreeNode.setSqlType(sqlTypeObject)
                        child_itemId_1 = self.appendNode(targetNode=tableNode, nodeLabel=f'{sqlTypeObject.name}' , dataSourceTreeNode=dataSourceTreeNode)
                        if sqlTypeObject.type == 'table':
                            
                            dataSourceTreeNode = DataSourceTreeNode(dataSource=dataSource, nodeLabel=nodeLabel, imageName=f"folder.png", children=None, nodeType="folder_column")
                            dataSourceTreeNode.setSqlType(sqlTypeObject)
                            child1_1 = self.appendNode(targetNode=child_itemId_1, nodeLabel=f'Columns ({len(sqlTypeObject.columns)})', dataSourceTreeNode=dataSourceTreeNode) 
                            
                            dataSourceTreeNode = DataSourceTreeNode(dataSource=dataSource, nodeLabel=nodeLabel, imageName=f"folder.png", children=None, nodeType="folder_unique_key")
                            dataSourceTreeNode.setSqlType(sqlTypeObject)
                            child1_2 = self.appendNode(targetNode=child_itemId_1, nodeLabel='Unique Keys', dataSourceTreeNode=dataSourceTreeNode) 
                            
                            dataSourceTreeNode = DataSourceTreeNode(dataSource=dataSource, nodeLabel=nodeLabel, imageName=f"folder.png", children=None, nodeType="folder_foreign_key")
                            dataSourceTreeNode.setSqlType(sqlTypeObject)
                            child1_3 = self.appendNode(targetNode=child_itemId_1, nodeLabel='Foreign Keys', dataSourceTreeNode=dataSourceTreeNode) 
                            
                            dataSourceTreeNode = DataSourceTreeNode(dataSource=dataSource, nodeLabel=nodeLabel, imageName=f"folder.png", children=None, nodeType="folder_references")
                            dataSourceTreeNode.setSqlType(sqlTypeObject)
                            child1_4 = self.appendNode(targetNode=child_itemId_1, nodeLabel='References', dataSourceTreeNode=dataSourceTreeNode) 
                            for column in sqlTypeObject.columns:

                                dataSourceTreeNode = DataSourceTreeNode(dataSource=dataSource, nodeLabel=f'{column.name}', imageName=self.getColumnImageName(column), children=None, nodeType="column")
                                dataSourceTreeNode.setSqlType(sqlTypeObject)
                                child_itemId_1_0 = self.appendNode(targetNode=child1_1, nodeLabel=f'{column.name}' , dataSourceTreeNode=dataSourceTreeNode)
                
            else:
                updateStatus = f"Unable to connect '{ dataSourceTreeNode.dataSource.filePath } , No such file. "
                self.consoleOutputLog(updateStatus)
                font = self.GetTopLevelParent().statusbar.GetFont() 
                font.SetWeight(wx.BOLD) 
                self.GetTopLevelParent().statusbar.SetFont(font) 
                self.GetTopLevelParent().statusbar.SetForegroundColour(wx.RED) 
                self.GetTopLevelParent().statusbar.SetStatusText(updateStatus, 1)
                logger.error(updateStatus)

    def getColumnImageName(self, column):
        imageName = "string.png"
        if column.primaryKey == 1:
            imageName = 'key.png'
        elif column.dataType in ['INTEGER', 'INT']:
            imageName = "column.png"
        elif column.dataType in ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
            imageName = "textfield.png"
        return imageName

    def consoleOutputLog(self, exception=None):
        now = datetime.datetime.now()
        strftime = now.strftime("%Y-%m-%d %H:%M:%S")
        newline = "\n"
        if self.GetTopLevelParent()._mgr.GetPane("consoleOutput").window.text.Value.strip() == "":
            newline = ""
        self.GetTopLevelParent()._mgr.GetPane("consoleOutput").window.text.AppendText("{}{} {}".format(newline, strftime, exception))
        
#     def onEditTable(self, event):
#         logger.debug('onEditTable')

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
            'folder_table.png',
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
        try:
            dbList = self.sqlExecuter.getListDatabase()     
            self.DeleteAllItems()
            self._watch = []
            self.AddRoot('root')
            self.SetItemData(self.RootItem, "root")   
            for db in dbList:
                dataSource = DataSource(connectionName=db[1], filePath=db[2])
    #             dataSourceTreeNode = DataSourceTreeNode(depth=0, dataSource=dataSource, imageName='sqlite.png')
                self.addWatchConnection(dataSource=dataSource)
        except Exception as e:
            logger.error(e)
    #             self.appendNode(targetNode=self.RootItem, nodeLabel=dataSourceTreeNode.dataSource.connectionName, dataSourceTreeNode=dataSourceTreeNode)
    
    def addWatchConnection(self, dataSource=None):

        logger.debug('AddWatchConnection')
        if dataSource.filePath not in self._watch:
            self._watch.append(dataSource.filePath)
            dataSourceTreeNode = DataSourceTreeNode(depth=0, dataSource=dataSource, imageName='sqlite.png', nodeType='connection')
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
        try:
            imageIndex = self.iconsDictByImageName[dataSourceTreeNode.imageName]
        except Exception as e:
            logger.error(e)
            imageIndex = 0
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
