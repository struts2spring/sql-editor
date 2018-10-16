'''
Created on 11-Jan-2017
@author: vijay
'''
import wx
import logging.config
import  wx.lib.mixins.listctrl  as  listmix
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin
import datetime
import os
# from collections import OrderedDict
from sqlite3 import OperationalError
import wx.stc as stc
from src.view.table import TableEditorPanel
from src.view.table.TableEditorPanel import SqlStyleTextCtrl
import sqlparse
from src.view.constants import TITLE, LOG_SETTINGS
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter, \
    ManageSqliteDatabase, SQLUtils
import time
try:
    from agw import ultimatelistctrl as ULC
except ImportError:  # if it's not there locally, try the wxPython lib.
    from wx.lib.agw import ultimatelistctrl as ULC
    
import logging

logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)
#---------------------------------------------------------------------------

dataTypeList = ['INTEGER', 'TEXT', 'NULL', 'REAL', 'BLOB', 'NUMERIC']

headerList = ["S. No.", "icon", "Column name", "Data type", "Primary Key", "Allow Null", "Unique", "Auto Increment", "Default Value"]


#---------------------------------------------------------------------------
class CreatingTableFrame(wx.Frame):

    def __init__(self, parent, title, connectionName, newTableName):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.allowAuiFloating = False 
        self.SetMinSize((640, 480))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonPanel = CreateButtonPanel(self)
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D)
#         splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D)
        self.creatingTable = CreatingTablePanel(splitter, connectionName, newTableName)
        
        self.sstc = SqlStyleTextCtrl(splitter, -1)
#         self.sstc.SetText( open('book.sql').read())
        self.sstc.EmptyUndoBuffer()
        self.sstc.Colourise(0, -1)
#         self.sstc.SetBestFittingSize(wx.Size(400, 400))

        # line numbers in the margin
        self.sstc.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.sstc.SetMarginWidth(1, 25)
        
        self.creatingTable.addRow()
#         self.tableEditorPanel = TableEditorPanel(splitter)
        splitter.SetMinimumPaneSize(20)
        splitter.SplitHorizontally(self.creatingTable, self.sstc)
        sizer.Add(splitter, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        self.SetSizer(sizer)
#         self.creatingToolbar()
        self.Center()
        self.createStatusBar()
        self.Show(True)
    
    def OnCloseFrame(self, event):
        self.Destroy()

    def createStatusBar(self):
        logger.info('createStatusBar')
        self.statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
#         self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
        self.statusbar.SetStatusText("Welcome {}".format(TITLE), 1)


class TableListCtrl(ULC.UltimateListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.TextEditMixin, CheckListCtrlMixin):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, agwStyle=0):
        ULC.UltimateListCtrl.__init__(self, parent, id, pos, size, style, agwStyle)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
             
                
class CreatingTablePanel(wx.Panel):

    def __init__(self, parent, connectionName, newTableName , *args, **kw):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS | wx.SUNKEN_BORDER)
        self.parent = parent
        self.generatedSQL = None
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.choiceId = 1000
        self.choices = ['INTEGER', 'TEXT', 'NUMERIC', 'REAL', 'BLOB']
        self.tableDict = dict()
        self.tableDict['schemaName'] = connectionName
        self.tableDict['tableName'] = newTableName
        self.tableDict['columns'] = dict()

        #---------------
        # Variables
        #---------------
        self.IsInControl = True
        self.startIndex = -1
        self.dropIndex = -1
        self.IsDrag = False
        self.dragIndex = -1

        ####################################################################
        vBox1 = wx.BoxSizer(wx.VERTICAL)
        import  wx.lib.rcsizer  as rcs
        sizer = rcs.RowColSizer()

        schemaNameLabel = wx.StaticText(self, -1, "Schema Name:")
        self.schemaNameText = wx.TextCtrl(self, -1, self.tableDict['schemaName'], style=wx.TE_PROCESS_ENTER, size=(250, -1))
        self.Bind(wx.EVT_TEXT, self.onChangeSchema, self.schemaNameText)
        
        tableNameLabel = wx.StaticText(self, -1, "Table Name:")
        self.tableNameText = wx.TextCtrl(self, -1, self.tableDict['tableName'], size=(250, -1))
        self.Bind(wx.EVT_TEXT, self.onChangeTableName, self.tableNameText)
        
        sizer.Add(schemaNameLabel, flag=wx.EXPAND, row=1, col=1)
        sizer.Add(self.schemaNameText, row=1, col=2)
        
        sizer.Add(tableNameLabel, flag=wx.EXPAND, row=2, col=1)
        sizer.Add(self.tableNameText, row=2, col=2)

        vBox1.Add(sizer)
#         vBox1.Add(hBox1)
        
        self.tb = self.creatingToolbar()
        
        self.imageId = dict()
        self.imageList = ULC.PyImageList(16, 16)
         
        logger.info('not===============' + __file__) 
#         logger.info(os.path.realpath(__file__))
#         logger.info(os.path.dirname(os.path.abspath(__file__)))
#         logger.info(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
        path = os.path.abspath(__file__)
        tail = None
        while tail != 'src':
            path = os.path.abspath(os.path.join(path, '..'))
            head, tail = os.path.split(path)
        logger.info('while===============' + os.path.abspath(os.path.join(path, "images", "key.png"))) 
        logger.info(path)
        self.imageId["key.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "images", "key.png"))))
        self.imageId["textfield.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "images", "textfield.png"))))
        self.imageId["unique_constraint.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "images", "unique_constraint.png"))))
        self.imageId["unique_constraint.png"] = self.imageList.Add(wx.Bitmap(os.path.abspath(os.path.join(path, "images", "unique_constraint.png"))))

        self.list = TableListCtrl(self, -1,
                                         agwStyle=wx.LC_REPORT
                                         # | wx.BORDER_SUNKEN
                                         | wx.BORDER_NONE
                                         | wx.LC_EDIT_LABELS
                                         # | wx.LC_SORT_ASCENDING
                                         # | wx.LC_NO_HEADER
                                         | wx.LC_VRULES
                                         | wx.LC_HRULES
                                         # | wx.LC_SINGLE_SEL
                                         | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.list.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        
#         self.list.CheckItem(4)
#         self.list.CheckItem(7)
        self.PopulateList()
        self.evenBinding()
        
        vBox.Add(vBox1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        vBox.Add(self.tb, 0, wx.EXPAND)
        vBox.Add(self.list, 1, wx.EXPAND)
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
    def onChangeSchema(self, event):
        logger.debug('onChangeSchema')
        self.tableDict['schemaName'] = event.GetString()
        self.updateTableEditorPanel()

    def onChangeTableName(self, event):
        logger.debug('onChangetableName')
        self.tableDict['tableName'] = event.GetString()
        self.updateTableEditorPanel()
        
    def evenBinding(self):
        self.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(ULC.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(ULC.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(ULC.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(ULC.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(ULC.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(ULC.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)
        self.Bind(ULC.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.list)
        self.Bind(ULC.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.list)
        self.Bind(ULC.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)
        self.Bind(ULC.EVT_LIST_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(ULC.EVT_LIST_END_DRAG, self.OnEndDrag)

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        
#         self.Bind(wx.EVT_LEFT_UP, self._onMouseUp)
        self.Bind(wx.EVT_LEFT_DOWN, self._onMouseDown)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self._onInsert)
               
    def _onMouseUp(self, event):
        # Purpose: to generate a dropIndex.
        # Process: check self.IsInControl, check self.IsDrag, HitTest, compare HitTest value
        # The mouse can end up in 5 different places:
        # Outside the Control
        # On itself
        # Above its starting point and on another item
        # Below its starting point and on another item
        # Below its starting point and not on another item

        if self.IsInControl == False:  # 1. Outside the control : Do Nothing
            self.IsDrag = False
        else:  # In control but not a drag event : Do Nothing
            if self.IsDrag == False:
                pass
            else:  # In control and is a drag event : Determine Location
                self.hitIndex = self.list.HitTest(event.GetPosition())
                self.dropIndex = self.list.hitIndex[0]
                # -- Drop index indicates where the drop location is; what index number
                #---------
                # Determine dropIndex and its validity
                #--------
                if self.dropIndex == self.startIndex or self.dropIndex == -1:  # 2. On itself or below control : Do Nothing
                    pass
                else:
                    #----------
                    # Now that dropIndex has been established do 3 things
                    # 1. gather item data
                    # 2. delete item in list
                    # 3. insert item & it's data into the list at the new index
                    #----------
                    dropList = []  # Drop List is the list of field values from the list control
                    thisItem = self.list.GetItem(self.startIndex)
                    for x in range(self.list.GetColumnCount()):
                        dropList.append(self.list.GetItem(self.startIndex, x).GetText())
                    thisItem.SetId(self.dropIndex)
                    self.list.DeleteItem(self.startIndex)
                    self.list.InsertItem(thisItem)
                    for x in range(self.list.GetColumnCount()):
                        self.list.SetStringItem(self.dropIndex, x, dropList[x])
            #------------
            # I don't know exactly why, but the mouse event MUST
            # call the stripe procedure if the control is to be successfully
            # striped. Every time it was only in the _onInsert, it failed on
            # dragging index 3 to the index 1 spot.
            #-------------
            # Furthermore, in the load button on the wxFrame that this lives in,
            # I had to call the _onStripe directly because it would occasionally fail
            # to stripe without it. You'll notice that this is present in the example stub.
            # Someone with more knowledge than I probably knows why...and how to fix it properly.
            #-------------
        self._onStripe()
        self.IsDrag = False
        event.Skip()

    def _onMouseDown(self, event):
        logger.info('_onMouseDown')
        self.IsInControl = True
        event.Skip()        

    def PopulateList(self):

        self.list.Freeze()
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(12)
        boldfont.SetUnderlined(True)
        
        for idx, header in enumerate(headerList):    
            info = ULC.UltimateListItem()
            info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            info._image = []
            info._format = 0
            info._kind = 1
            info._font = font
            info._text = header
            self.list.InsertColumnInfo(idx, info)
            width = len(header) * 10
            if width < 40:
                width = 50
            if header == 'Data type':
                width = 160
            self.list.SetColumnWidth(idx, width)

#         self.display()
        self.list.Thaw()
        self.list.Update()

    def setColumnIcon(self , isPrimaryKey, dataType):    
        if isPrimaryKey:
            columnIcon = 'key.png'
        elif dataType:
            columnIcon = 'textfield.png'
        
        return columnIcon

    def addRow(self):
        
        if len(self.tableDict['columns']) == 0:
#             columnIcon = 'key.png'
            dataType = dataTypeList[0]
            isPrimaryKey = True
        else:
#             columnIcon = 'textfield.png'
            dataType = dataTypeList[1]
            isPrimaryKey = False
            
        columnId = len(self.tableDict['columns']) + 1
        column = {
          'id':len(self.tableDict['columns']) + 1,
          'columnIcon':self.setColumnIcon(isPrimaryKey, dataType),
          'columnName':'column ' + str(len(self.tableDict['columns']) + 1),
          'dataType':dataType,
          'isPrimaryKey':isPrimaryKey,
          "isNotNull":False,
          'isUnique':False,
          "isAutoIncrement":False,
          "description": 'No'
          
          }
#         for column in self.tableDict.columns:
        self._itemId = self.list.InsertStringItem(column['id'], str(column['id']), 0)
        self.list.SetStringItem(self._itemId , 1, '', imageIds=[self.imageId[column['columnIcon']]] , it_kind=0)
        self.list.SetStringItem(self._itemId , 2, column['columnName'], it_kind=0)
         
#         self.list.SetStringItem(self._itemId , 3, column['dataType'], it_kind=0)
        
        self.list.SetStringItem(self._itemId , 4, '' if column['isPrimaryKey'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 5, '' if column['isNotNull'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 6, '' if column['isUnique'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 7, '' if column['isAutoIncrement'] else '', it_kind=1)
        self.list.SetStringItem(self._itemId , 8, column['description'], it_kind=0)
        
        item = self.list.GetItem(self._itemId, 4)
        item.Check(isPrimaryKey)
        self.list.SetItem(item)
        
        item3 = self.list.GetItem(self._itemId, 3)
        self.choiceId = 1000 + int(column['id'])
        logger.info('=======================================>' + str(self.choiceId))
        dataTypeChoice = wx.Choice(self.list, self.choiceId, (100, 50), choices=self.choices)
        dataTypeChoice.Bind(wx.EVT_CHOICE, self.OnChoice)
        for idx , choice in enumerate(self.choices):
            if choice == column['dataType']:
                dataTypeChoice.SetSelection(idx)
                
        item3.SetWindow(dataTypeChoice)
        self.list.SetItem(item3)         
        self.list.SetColumnWidth(3, 110)
        self.tableDict['columns'][columnId] = column
        
        if len(self.tableDict['columns']) > 0:
            self.list.Focus(len(self.tableDict['columns']) - 1)
        logger.info(self.tableDict)  
        self.updateTableEditorPanel()  
        
    def OnChoice(self, event):
#         self.label.SetLabel("selected "+ self.choice.GetString( self.choice.GetSelection() ) +" from Choice")
        logger.info(self.list)
        logger.info(event.GetClientObject().GetId())
        logger.info(event.GetString())
        rowId = event.GetClientObject().GetId() - 1000
#         self.updateItemStatus(index=index)
        self.tableDict['columns'][rowId]['dataType'] = event.GetString()
        self.updateTableEditorPanel()

    def removeRow(self): 
        try:
            if self.list.GetFocusedItem() != -1:
                logger.info(self.list.GetSelectedItemCount())
                selectedItem = self.list.GetFocusedItem()
#                 self.list.Select(selectedItem._itemId-1, True)
                id = self.list.GetItemText(selectedItem)
                self.list.DeleteItem(self.list.GetFocusedItem())
                del self.tableDict['columns'][int(id)]
                self.choiceId = self.choiceId - int(id)
                if len(self.tableDict['columns']) > 0:
                    self.list.Focus(len(self.tableDict['columns']) - 1)
                self.updateTableEditorPanel()
                
        except KeyError:
            pass

#         logger.info(self.listctrldata)
#         self.display()
    def updateTableDict(self):
        pass
   
    def ChangeStyle(self, checks):

        style = 0
        for check in checks:
            if check.GetValue() == 1:
                style = style | eval("ULC." + check.GetLabel())
        
        if self.list.GetAGWWindowStyleFlag() != style:
            self.list.SetAGWWindowStyleFlag(style)
            
    def creatingToolbar(self):
        tb = wx.ToolBar(self, style=wx.TB_FLAT)
        tsize = (24, 24)
        plus_bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_TOOLBAR, tsize)
        minus_bmp = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_TOOLBAR, tsize)
        goUp_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, tsize)
        goDown_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, tsize)

        tb.SetToolBitmapSize(tsize)
        
        # tb.AddSimpleTool(10, new_bmp, "New", "Long help for 'New'")
        tb.AddTool(10, "Add a column", plus_bmp, "Add a new Column")
        self.Bind(wx.EVT_TOOL, self.onAddColumnClick, id=10)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=10)

        # tb.AddSimpleTool(20, open_bmp, "Open", "Long help for 'Open'")
        tb.AddTool(20, "Remove a column", minus_bmp, "Remove a column")
        self.Bind(wx.EVT_TOOL, self.onRemoveColumnClick, id=20)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=20)

        tb.AddSeparator()
        tb.AddTool(30, "Move field up", goUp_bmp, "move column up'")
        self.Bind(wx.EVT_TOOL, self.onMoveUpClick, id=30)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=30)

        tb.AddTool(40, "Move field down", goDown_bmp, "move column down")
        self.Bind(wx.EVT_TOOL, self.onMoveDownClick, id=40)
#         self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=40)

        tb.AddSeparator()
        tb.Realize()
        return tb

    def onAddColumnClick(self, event):
        logger.info('onAddColumn clicked')
        self.addRow()
        
    def onRemoveColumnClick(self, event):
        logger.info('onRemoveColumnClick clicked')
        self.removeRow()
#         self.updateItemStatus(event.GetIndex(), event.GetItem())
        
    def onMoveUpClick(self, event):
        logger.info('onMoveUpClick clicked')
        
    def onMoveDownClick(self, event):
        logger.info('onMoveDownClick clicked')
        
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

    def OnTimer(self, event):

        for key, renderer in self.renderers.items():
            renderer.UpdateValue()
            self.list.RefreshItem(key)
    
    def OnIdle(self, event):

        if self.gauge:
            try:
                if self.gauge.IsEnabled() and self.gauge.IsShown():
                    self.count = self.count + 1

                    if self.count >= 50:
                        self.count = 0

                    self.gauge.SetValue(self.count)

            except:
                self.gauge = None

        event.Skip()

    def OnRightDown(self, event):
        x = event.GetX()
        y = event.GetY()

#         logger.info("x, y = %s\n" % str((x, y)))
        
        item, flags = self.list.HitTest((x, y))
#         item, flags,subItem = self.list.HitTestSubItem((x, y))
        logger.info('---right down:' + item + ':' + flags)

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.list.Select(item)
            logger.info('right down:' + item)

        event.Skip()

    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        logger.info('OnItemSelected:')
        self.startIndex = event.GetIndex()
        self.currentItem = event.GetIndex()
        self.updateItemStatus(event.GetIndex(), event.GetItem())
#         logger.info("OnItemSelected: %s, %s, %s, %s\n" % (self.currentItem,
#                                                             self.list.GetItemText(self.currentItem),
#                                                             self.getColumnText(self.currentItem, 1),
#                                                             self.getColumnText(self.currentItem, 2)))
# 
#         if self.list.GetPyData(self.currentItem):
#             logger.info("PYDATA = %s\n" % repr(self.list.GetPyData(self.currentItem)))
# 
#         if self.currentItem == 10:
#             logger.info("OnItemSelected: Veto'd selection\n")
#             # event.Veto()  # doesn't work
#             # this does
#             self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

#         event.Skip()

    def OnItemDeselected(self, event):
        item = event.GetItem()
        logger.info("OnItemDeselected: {}".format(event.m_itemIndex))
#         self.updateItemStatus(event.GetIndex(), event.GetItem())
# #        # Show how to reselect something we don't want deselected
# #        if evt.m_itemIndex == 11:
# #            wx.CallAfter(self.list.SetItemState, 11, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        event.Skip()

    def updateItemStatus(self, index, item=None):
        
        logger.info('getColumnText0:' + self.getColumnText(index, 0))
        for col in range(4, 8):
            itemCol = self.list.GetItem(index, col)
            logger.info("{},{},{},{}".format(col, item._itemId, index, itemCol.IsChecked()))
        column = self.tableDict['columns'][int(self.getColumnText(index, 0))]
        
        dataTypeItem = self.list.GetItem(index, 3)
        dataTypeChoice = dataTypeItem.GetWindow()
        idx = dataTypeChoice.GetSelection()
        logger.info(idx)
        
#         item3 = self.list.GetItem(column['id'], 3)
#         dataTypeChoice = wx.Choice(self.list, -1, (100, 50), choices = self.choices)
#         
#         for idx , choice in enumerate(self.choices):
#             if choice==column['dataType']:
#                 dataTypeChoice.SetSelection(dataTypeChoice.SetSelection()
#                 
#         item3.SetWindow(dataTypeChoice)
#         self.list.SetItem(item3)  
        
        logger.info('before ----------------------------------------------->' + str(self.list.GetItem(index, 4).IsChecked()))
        isPrimaryKey = self.list.GetItem(index, 4).IsChecked()
        logger.info('after ----------------------------------------------->' + str(self.list.GetItem(index, 4).IsChecked()))
        column['isPrimaryKey'] = isPrimaryKey
        isNotNull = self.list.GetItem(index, 5).IsChecked()
        column["isNotNull"] = isNotNull
        isUnique = self.list.GetItem(index, 6).IsChecked()
        column['isUnique'] = isUnique
        autoIncrement = self.list.GetItem(index, 7).IsChecked()
        column["isAutoIncrement"] = autoIncrement
        column['columnIcon'] = self.setColumnIcon(column['isPrimaryKey'], column['dataType'])
        self.list.SetStringItem(index , 1, '', imageIds=[self.imageId[ self.setColumnIcon(isPrimaryKey, column['dataType'])]] , it_kind=0)
        self.tableDict['columns'][int(self.getColumnText(index, 0))] = column
#                 column=col
#                 break
#                     column["description"]= 'No'
        logger.info(self.tableDict)
        self.updateTableEditorPanel()
        
    def updateTableEditorPanel(self):
        self.generatedSQL = self.createSql()
        formatted_sql = sqlparse.format(self.generatedSQL, reindent=True, keyword_case='upper')
        self.GetTopLevelParent().sstc.SetText(formatted_sql)
        logger.info('updateTableEditorPanel')
    
    def createSql(self, withSchema=True):    
        logger.info('createSql')
        sqlList = list()
        sqlList.append("CREATE")
        if 'temp' in self.tableDict.keys():
            sqlList.append("TEMP")
        sqlList.append('TABLE')
        if 'ifNotExists' in  self.tableDict.keys():
            sqlList.append('IF NOT EXISTS')
        if 'schemaName' in self.tableDict.keys() and withSchema:
            sqlList.append("'" + self.tableDict['schemaName'] + "'.'" + self.tableDict['tableName'] + "'")
        else:
            sqlList.append("'" + self.tableDict['tableName'] + "'")
        sqlList.append('(')
        logger.info(self.tableDict['columns'])
        for key, column in self.tableDict['columns'].items():
            sqlList.append("'" + column['columnName'] + "'")
            sqlList.append(column['dataType'])
            if column['isPrimaryKey']:
                sqlList.append('PRIMARY KEY')
                if column['isAutoIncrement']:
                    sqlList.append('AUTOINCREMENT')
            elif column['isNotNull']:
                sqlList.append('NOT NULL')
            elif column['isUnique']:
                sqlList.append('UNIQUE')
            elif column['isUnique']:
                sqlList.append('UNIQUE')
            elif 'check' in column.keys():
                sqlList.append('CHECK ( ' + column['check'] + ' )')
            elif 'default' in column.keys():
                sqlList.append('DEFAULT ' + column['default'])
            
            sqlList.append(',')
        sqlList.pop()
        sqlList.append(')')  
        sqlList.append(';')  
        sql = " ".join(sqlList)
#         formatedSql=sqlparse.format(sql, encoding=None)
        return sql    
        
    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        logger.info("OnItemActivated: {} : {}".format(self.list.GetItemText(self.currentItem) , self.list.GetTopItem()))

    def OnBeginEdit(self, event):
        logger.info("OnBeginEdit\n")
#         event.Allow()
        
    def _onInsert(self, event):
        # Sequencing on a drop event is:
        # wx.EVT_LIST_ITEM_SELECTED
        # wx.EVT_LIST_BEGIN_DRAG
        # wx.EVT_LEFT_UP
        # wx.EVT_LIST_ITEM_SELECTED (at the new index)
        # wx.EVT_LIST_INSERT_ITEM
        #--------------------------------
        # this call to onStripe catches any addition to the list; drag or not
        self._onStripe()
        self.dragIndex = -1

#         event.Skip()
    def OnItemDelete(self, event):
        logger.info("OnItemDelete\n")
        self._onStripe()
        event.Skip()

    def _onStripe(self):
        if self.list.GetItemCount() > 0:
            for x in range(self.list.GetItemCount()):
                if x % 2 == 0:
                    self.list.SetItemBackgroundColour(x, wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
                else:
                    self.list.SetItemBackgroundColour(x, wx.WHITE)

    def OnColClick(self, event):
        logger.info("OnColClick: " + event.GetColumn())
        event.Skip()

    def OnColRightClick(self, event):
        item = self.list.GetColumn(event.GetColumn())
        logger.info("OnColRightClick: " + (event.GetColumn(), (item.GetText(), item.GetAlign(),
                                                                        item.GetWidth(), item.GetImage())))

    def OnColBeginDrag(self, event):
        logger.info("OnColBeginDrag\n")
        # # Show how to not allow a column to be resized
        # if event.GetColumn() == 0:
        #    event.Veto()

    def OnColDragging(self, event):
        logger.info("OnColDragging\n")

    def OnColEndDrag(self, event):
        logger.info("OnColEndDrag\n")

    def OnBeginDrag(self, event):
        self.IsDrag = True
        self.dragIndex = event.GetIndex()
        logger.info("OnBeginDrag\n" + self.dragIndex)
        event.Skip()
           
#         logger.info(event.GetIndex())
#         data=wx.PyTextDataObject()
#         index=event.GetIndex()
# #         logger.info(self.list.GetdragcursorData())
#         
#         
#         dropSource=wx.DropSource(self)
#         dropSource.SetData(index)
#         res=dropSource.DoDragDrop(flag=wx.Drag_DefaultMove)
#         dragItem=self.list.

    def OnEndDrag(self, event):     
        self.dropIndex = event.GetIndex()   
        logger.info("OnEndDrag: " + self.dropIndex)
        
        #----------
        # Now that dropIndex has been established do 3 things
        # 1. gather item data
        # 2. delete item in list
        # 3. insert item & it's data into the list at the new index
        #----------
        dropList = []  # Drop List is the list of field values from the list control
        columnDraged = None
        for idx, column in self.tableDict['columns'].items():
            if str(column['id']) == self.getColumnText(self.startIndex, 0):
                columnDraged = column
        
        thisItem = self.list.GetItem(self.startIndex)
        thisItem_3 = self.list.GetItem(self.startIndex, 3)
        idx = thisItem_3.GetWindow().GetSelection()
        
        thisItem_4 = self.list.GetItem(self.startIndex, 4)
        thisItem_5 = self.list.GetItem(self.startIndex, 5)
        thisItem_6 = self.list.GetItem(self.startIndex, 6)
        thisItem_7 = self.list.GetItem(self.startIndex, 7)
        
        logger.info('thisItem_3.GetWindow()----------' + thisItem_3.GetWindow())
        
        for x in range(self.list.GetColumnCount()):
            dropList.append(self.list.GetItem(self.startIndex, x).GetText())
        
        thisItem.SetId(self.dropIndex)
        logger.info('dropList------------>' + dropList)
        logger.info('thisItem------------>' + thisItem)
#         thisItem.set
        
        self.list.DeleteItem(self.startIndex)
        self.list.InsertItem(thisItem)
        for dropItemColumn in range(self.list.GetColumnCount()):
            self.list.SetStringItem(self.dropIndex, dropItemColumn, dropList[dropItemColumn])
            
        dropItem_4 = self.list.GetItem(self.dropIndex, 4)
        dropItem_4.Check(thisItem_4.IsChecked())
        self.list.SetItem(dropItem_4)
        
        dropItem_5 = self.list.GetItem(self.dropIndex, 5)
        dropItem_5.Check(thisItem_5.IsChecked())
        self.list.SetItem(dropItem_5)
        
        dropItem_6 = self.list.GetItem(self.dropIndex, 6)
        dropItem_6.Check(thisItem_6.IsChecked())
        self.list.SetItem(dropItem_6)
        
        dropItem_7 = self.list.GetItem(self.dropIndex, 7)
        dropItem_7.Check(thisItem_7.IsChecked())
        self.list.SetItem(dropItem_7)
        
        self.list.SetStringItem(self.dropIndex , 1, '', imageIds=[self.imageId[self.setColumnIcon(column['isPrimaryKey'], column['dataType'])]] , it_kind=0)
#         self.list.SetStringItem(self.dropIndex , 2, columnDraged['columnName'], it_kind=0)

        item3 = self.list.GetItem(self.dropIndex, 3)
        dataTypeChoice = wx.Choice(self.list, self.choiceId, (100, 50), choices=self.choices)
        dataTypeChoice.SetSelection(idx)
        dataTypeChoice.Bind(wx.EVT_CHOICE, self.OnChoice)
        item3.SetWindow(dataTypeChoice)
        self.list.SetItem(item3) 
        
        self.list.SetStringItem(self.dropIndex , 4, '' if columnDraged['isPrimaryKey'] else '', it_kind=1)
        self.list.SetStringItem(self.dropIndex , 5, '' if columnDraged['isNotNull'] else '', it_kind=1)
        self.list.SetStringItem(self.dropIndex , 6, '' if columnDraged['isUnique'] else '', it_kind=1)
        self.list.SetStringItem(self.dropIndex , 7, '' if columnDraged['isAutoIncrement'] else '', it_kind=1)
        
#         self.list.SetStringItem(self.dropIndex , 8, column['description'], it_kind=0)        
        logger.info(self.tableDict)
        self.updateTableEditorPanel()
        
    def OnDoubleClick(self, event):
        logger.info("OnDoubleClick item %s\n" + self.list.GetItemText(self.currentItem))
        event.Skip()

    def OnRightClick(self, event):
        logger.info("OnRightClick %s\n" + self.list.GetItemText(self.currentItem))
        logger.info('GetColumn:' + self.list.GetSizeTuple())
        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.onDeleteSelected, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.onDeleteAllItems, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "Delete Selected")
        menu.Append(self.popupID2, "Iterate Selected")
        menu.Append(self.popupID3, "ClearAll and repopulate")
        menu.Append(self.popupID4, "DeleteAllItems")
        menu.Append(self.popupID5, "GetItem")
        menu.Append(self.popupID6, "Edit")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def getAllSelectedItem(self):
        countSel = 0
        selectedIndexSet = set()
        count = self.list._mainWin.GetItemCount()
        for line in range(count):
            if self.list._mainWin.GetLine(line).IsHighlighted():
                countSel += 1
                selectedIndexSet.add(line)
        return countSel, selectedIndexSet

    def onDeleteSelected(self, event):
        countSel, selectedIndexSet1 = self.getAllSelectedItem()
        index = self.list.GetFirstSelected()
        selectedIndexSet = set()
        while index != -1:
            selectedIndexSet.add(self.list.GetItemText(index))
#             logger.info("      %s: %s" % (self.list.GetItemText(index), self.getColumnText(index, 1)))
#             self.list.DeleteItem(index)
            index = self.list.GetNextSelected(index)
            if index > -1:
                selectedIndexSet.add(self.list.GetItemText(index))
                
        count = self.list._mainWin.GetItemCount()
        for line in range(count):
            if self.list._mainWin.GetItem(line):
                countSel += 1
                selectedIndexSet.add(line)
        self.list._mainWin.GetItemCount()
        
        for idx in self.list:
            if idx > -1:
                try:
                    self.list.DeleteItem(idx)
                except Exception as e:
                    logger.error(e, exc_info=True)
        logger.info(selectedIndexSet)
#                 logger.info(idx, item)

    def OnPopupTwo(self, event):
        logger.info("Selected items:")
        index = self.list.GetFirstSelected()

        while index != -1:
            logger.info("      %s: %s" % (self.list.GetItemText(index), self.getColumnText(index, 1)))
#             self.list.Dele
            index = self.list.GetNextSelected(index)

        logger.info("\n")

    def OnPopupThree(self, event):
        logger.info("Popup three")
        self.list.ClearAll()
        wx.CallAfter(self.PopulateList)

    def onDeleteAllItems(self, event):
        self.list.DeleteAllItems()

    def OnPopupFive(self, event):
        item = self.list.GetItem(self.currentItem)
#         logger.info(("%s, %s, %s") % (item._text, item._itemId, self.list.GetItemData(self.currentItem)))

    def OnPopupSix(self, event):
        self.list.EditLabel(self.currentItem)

        
class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent         
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, 50, "Ok", (20, 220))
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
        sizer.Add(hbox, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

    def onOkClick(self, event):
        logger.debug('onOkClick')
        
        self.executeSQL(event)

    def onCancelButtonClick(self, event):
        logger.debug('onCancelButtonClick')
        self.GetTopLevelParent().Destroy()

    def executeSQL(self, event=None):
        '''
        '''
        error = 'success'
        ##################################################################################
        logger.info(self.GetTopLevelParent().sstc.GetText())
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        connectionName = self.GetTopLevelParent().creatingTable.tableDict['schemaName']
        dbFilePath = sqlExecuter.getDbFilePath(connectionName=connectionName)
        logger.debug("databaseAbsolutePath: %s", dbFilePath)
        ##################################################################################
        sqlText = self.GetTopLevelParent().creatingTable.createSql(withSchema=False)
#         sqlExecuter = SQLExecuter(database='_opal.sqlite')
        ##################################################################################
        logger.debug('executeSQL: %s' , sqlText)
        try:
            if os.path.isfile(dbFilePath):
                sqlOutput = None

                try:
                    manageSqliteDatabase = ManageSqliteDatabase(connectionName=connectionName, databaseAbsolutePath=dbFilePath)
                    sqlOutput = manageSqliteDatabase.executeText(sqlText)

                except Exception as e:
                    logger.error(e, exc_info=True)
        except TypeError as te:
            logger.error(te, exc_info=True)
            if not dbFilePath:
                error = 'Unable to connect. Please choose a database to execute Script.'
#                 self.GetTopLevelParent()._mgr.GetPane("scriptOutput").window.text.AppendText("\n" + error)
        except Exception as e:
            logger.error(e, exc_info=True)
#             self.GetTopLevelParent()._mgr.GetPane("scriptOutput").window.text.AppendText("\n" + str(e))
#             print(e)
            error = str(e)
        self.GetTopLevelParent().Destroy()
#         self.refreshSqlLogUi()


if __name__ == '__main__':
    app = wx.App(False)
    frame = CreatingTableFrame(None, 'table creation')
    frame.Show()
    app.MainLoop()
