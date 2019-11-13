import os

import wx.grid
import wx.stc as stc

# from src.view.worksheet.EditorPanel import CreatingEditorPanel
import logging.config
from src.view.constants import LOG_SETTINGS
# from src.view.table.TableEditorPanel import CreatingEditorPanel
from src.view.util.FileOperationsUtil import FileOperations
from wx._grid import GridCellRenderer
from src.sqlite_executer.ConnectExecuteSqlite import Column, SqlType
from pubsub import pub
from src.view.views.console.worksheet.EditorPanel import CreatingEditorPanel

try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD   

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

# class CreateTableFrame(wx.Frame):
#     '''
#     frame contains splitter between (table head, toolbar and grid) and editor panel..
#     '''
# 
#     def __init__(self, parent, title):
#         wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
#                           style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
#         
# #         self.tableDict = dict()
# #         self.setData(self.tableDict)
#         
#         self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
#         self.allowAuiFloating = False 
#         self.SetMinSize((640, 480))
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         self.buttonPanel = CreateButtonPanel(self)
#         
#         splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D)
#         self.createTablePanel = CreateTablePanel(splitter)
# #         self.createTablePanel.setData(self.tableDict)
# #         self.createTablePanel.headPanel.setData(self.tableDict)
#         self.editPanel = CreatingEditorPanel(splitter)
# #         self.sstc = wx.stc.StyledTextCtrl(splitter, -1)
#         splitter.SetMinimumPaneSize(20)
#         splitter.SplitHorizontally(self.createTablePanel, self.editPanel)
#         sizer.Add(splitter, 1, wx.EXPAND)
#         sizer.Add(self.buttonPanel, 0, wx.EXPAND)
#         self.SetSizer(sizer)
# #         self.creatingTable = CreatingTablePanel(splitter)
# #         grid = SimpleGrid(self)
#         self.Center()
#         self.createNewTableStatusBar()
#         self.Show(True)
#         
#     def getEditorPanel(self):
#         return self.editPanel
#         
#     def setData(self, tableDict=None):
#         if tableDict:
#             self.tableDict = tableDict
#         else:
#             self.tableDict = dict()
#             self.tableDict['schemaName'] = 'schema_1'
#             self.tableDict['tableName'] = 'Table_1'
#             self.tableDict['rows'] = list()
#             self.tableDict['row'] = dict()
#             self.tableDict['row'][0] = ["icon", "Column name", "Data type", "Primary key", "Allow null", "Unique", "Auto increment", "Default value"]
#         self.createTablePanel.setData(self.tableDict)
#         self.createTablePanel.headPanel.setData(self.tableDict)    
#         
#     def OnCloseFrame(self, event):
#         self.Destroy()
# 
#     def createNewTableStatusBar(self):
#         logger.debug('creating status bar')
#         self.statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
#         self.statusbar.SetStatusWidths([-2, -3])
#         self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
#         self.statusbar.SetStatusText("Welcome Opal Database Visualizer", 1)
# 
#     def getCurrentCursorPosition(self):
#         lineNo = 1
#         column = 1
#         return "Line " + str(lineNo) + " , Column " + str(column)


class CreateTableHeadPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent     
        import  wx.lib.rcsizer  as rcs
        sizer = rcs.RowColSizer()
#         vBox = wx.BoxSizer(wx.VERTICAL)
        self.tableDict = dict()
#         self.setData(self.tableDict)
        
#         schemaNameLabel = wx.StaticText(self, -1, "Schema Name:")
#         self.schemaNameText = wx.TextCtrl(self, -1, '', size=(250, -1))
#         self.schemaNameText.Bind(wx.EVT_TEXT, self.onSchemaName) 
        
        tableNameLabel = wx.StaticText(self, -1, "Table Name:")
        self.tableNameText = wx.TextCtrl(self, -1, '', size=(250, -1))
        self.tableNameText.Bind(wx.EVT_TEXT, self.onTableName) 
        
#         sizer.Add(schemaNameLabel, flag=wx.EXPAND, row=1, col=1)
#         sizer.Add(self.schemaNameText, row=1, col=2)
        
        sizer.Add(tableNameLabel, flag=wx.EXPAND, row=0, col=1)
        sizer.Add(self.tableNameText, row=0, col=2)

#         vBox.Add(sizer)
        self.SetSizer(sizer)
#         self.Layout()

    def setData(self, tableDict=None):
        if tableDict and len(tableDict) > 1:
            self.tableDict = tableDict
            self.schemaNameText.SetValue(self.tableDict['schemaName'])
            self.tableNameText.SetValue(self.tableDict['tableName'])
        else:
            self.tableDict['schemaName'] = ''
            self.tableDict['tableName'] = ''

    def onSchemaName(self, event):
        logger.debug("onSchemaName")    
        try:   
            self.GetParent().tableDict['schemaName'] = self.schemaNameText.GetValue()
            
            self.GetParent().updateTableEditorPanel()
        except Exception as e:
            logger.error(e, exc_info=True)

    def onTableName(self, event):
        logger.debug("onTableName") 
        try:   
            self.GetParent().sqlType.name = self.tableNameText.GetValue()
            pub.sendMessage('OnCellChange', sqlType=self.GetParent().sqlType)
        except Exception as e:
            logger.error(e, exc_info=True)


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

    def onCancelButtonClick(self, event):
        logger.debug('onCancelButtonClick')
        self.GetTopLevelParent().Destroy()

        
class CreateTablePanel(wx.Panel):
    '''
    This panel is going to contain table head, toolbar and grid.
    '''

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        vBox = wx.BoxSizer(wx.VERTICAL)
        #######################################33
        
#         self.row = dict()
#         self.row[0] = ["icon", "Column name", "Data type", "Primary key", "Allow null", "Unique", "Auto increment", "Default value"]
#         self.row[1] = ["1", "One", "INT", "1", "0", "1", "1", None ]        
        try:
            self.headPanel = CreateTableHeadPanel(self)
            self.tb = self.creatingToolbar()
            self.grid = SimpleGrid(self)
            self.initialize()
        except Exception as e:
            logger.error(e, exc_info=True)
        
        vBox.Add(self.headPanel, 0, wx.EXPAND)
        vBox.Add(self.tb, 0, wx.EXPAND)
        vBox.Add(self.grid, 0, wx.EXPAND)
        
        #######################################33
        
#         sizer.Add(self.headPanel, 1, wx.EXPAND , 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        
    def initialize(self):
        self.sqlType = SqlType(type="table", name='table_name', tbl_name='table_name', rootpage='', sql='')
        self.sqlType.columns = []
        self.addColumn()
    
    def addColumn(self):
        
        sequence = len(self.sqlType.columns)
        if sequence == 0:
            name = 'Id'
            dataType = 'INTEGER'
            primaryKey = 1
        else:
            name = f'column_{sequence}'
            dataType = 'VARCHAR'
            primaryKey = 0
            
        column = Column(sequence, name, dataType, 0, '', primaryKey, unique=0, description='', autoIncrement=0)
        self.sqlType.columns.append(column)
        
        self.grid.addData(self.sqlType.columns)
        pub.sendMessage('OnCellChange', sqlType=self.sqlType)

    def setData(self, tableDict=None):
        logger.debug('setData')
        
        if tableDict:
            self.tableDict = tableDict

    def getData(self):
        logger.debug('getData')
        return self.tableDict

    def creatingToolbar(self):
        logger.debug('creatingToolbar')
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
        logger.debug('onAddColumn clicked')
        self.addColumn()
        
#         table=self.GetTopLevelParent().createTablePanel.grid
#         tableData=table.data
#         table.AppendRow()
#         self.GetTopLevelParent().createTablePanel.grid.addData()
#         print(tableData)
        
#     def updateTableEditorPanel(self):
#         logger.debug('updateTableEditorPanel')
        # TODO update sql editor using pub sub
#         tableDict = self.GetParent().GetChildren()[0].tableDict
#         if self.GetTopLevelParent().getEditorPanel():
#             self.GetTopLevelParent().getEditorPanel().sstc.SetText(self.createSql(tableDict))
        
    def createSql(self, tableDict=None):    
        '''
        This method creates sql script for create table sql.
        '''
        sqlList = list()
        if tableDict:
            sqlList.append("CREATE")
            if 'temp' in tableDict.keys():
                sqlList.append("TEMP")
            sqlList.append('TABLE')
            if 'ifNotExists' in  tableDict.keys():
                sqlList.append('IF NOT EXISTS')
            if 'schemaName' in tableDict.keys():
                if tableDict['schemaName'].strip() != '':
                    sqlList.append("'" + tableDict['schemaName'] + "'.'" + tableDict['tableName'] + "'")
                else:
                    sqlList.append("'" + tableDict['tableName'] + "'")
                    
            else:
                sqlList.append("'" + tableDict['tableName'] + "'")
            sqlList.append('(')
            logger.debug(tableDict['rows'])
            for idx, column in enumerate(tableDict['rows']):
                sqlList.append("'" + column['columnName'] + "'")
                sqlList.append(column['dataType'])
                if column['isPrimaryKey'] == '1':
                    sqlList.append('PRIMARY KEY')
                    if column['isAutoIncrement'] == '1':
                        sqlList.append('AUTOINCREMENT')
                elif column['isNotNull'] == '1':
                    sqlList.append('NOT NULL')
                elif column['isUnique'] == '1':
                    sqlList.append('UNIQUE')
                elif column['isUnique'] == '1':
                    sqlList.append('UNIQUE')
                elif 'check' in column.keys():
                    sqlList.append('CHECK ( ' + column['check'] + ' )')
                elif 'default' in column.keys():
                    sqlList.append('DEFAULT ' + str(column['default']))
                
                sqlList.append(',')
            sqlList.pop()
            sqlList.append(')')  
            sqlList.append(';')  
        sql = " ".join(sqlList)
        logger.debug('sql: %s', sql)
#         formatedSql=sqlparse.format(sql, encoding=None)
        return sql                      

    def onRemoveColumnClick(self, event):
        logger.debug('onRemoveColumnClick clicked')
        self.removeRow()
#         self.updateItemStatus(event.GetIndex(), event.GetItem())
        
    def onMoveUpClick(self, event):
        logger.debug('onMoveUpClick clicked')
        
    def onMoveDownClick(self, event):
        logger.debug('onMoveDownClick clicked')


class SimpleGrid(wx.grid.Grid):

    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1, size=(600, 500))

        self.CreateGrid(1, 1)
        self.RowLabelSize = 32
        self.dataTypeList = [("INTEGER", 0), ("VARCHAR", 1), ("TEXT", 2), ("REAL", 3), ("BLOB", 4), ("NUMERIC", 5)]
        self.checkBoxColumns = ['nullable', 'unique', 'primaryKey', 'autoIncrement']
        self.textBoxColumns = ['name', 'defultValue', 'description']
        self.comboBoxList = ['dataType']
        self.iconColumns = [0]
        self.columns = None
        
        self.fileOperations = FileOperations()
        self.addImages()
        
        self.lastSelectedCell = None
        
        self.bindAllEvent()

    def addImages(self):
        self.bmpList = list()

        self.bmpList.append(self.fileOperations.getImageBitmap(imageName="key.png"))  # 0 for primary key
        self.bmpList.append(self.fileOperations.getImageBitmap(imageName="textfield.png"))  # 1 for varchar, char, text column
        self.bmpList.append(self.fileOperations.getImageBitmap(imageName="unique_constraint.png"))  # 2  for unique key column
        self.bmpList.append(self.fileOperations.getImageBitmap(imageName="datetime.png"))  # 3 for datetime field column
        self.bmpList.append(self.fileOperations.getImageBitmap(imageName="column.png"))  #  4 for integer key column
    
    def bindAllEvent(self):
        # test all the events
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
 
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)
 
        self.Bind(wx.grid.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(wx.grid.EVT_GRID_COL_SIZE, self.OnColSize)
 
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSelectCell)
 
        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        self.Bind(wx.grid.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)
        
    ########################### Check box start ###################################    
    def OnCellLeftClick(self, evt):
        logger.debug(f"OnCellLeftClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()}")
        row = evt.GetRow()
        col = evt.GetCol()
        if evt.GetCol() in self.checkBoxColumns:
            logger.debug(self.GetCellValue(row, col))
            wx.MilliSleep(100)
#             self.toggleCheckBox(row, col)
            wx.CallLater(100, self.toggleCheckBox, (row, col))
        evt.Skip()

    def toggleCheckBox(self, cell):
        logger.debug(f'toggleCheckBox {cell}')
        try:
            self.cb.Value = not self.cb.Value
            self.afterCheckBox(self.cb.Value, cell)
        except Exception as e:
            logger.error(e, exc_info=True)

    def afterCheckBox(self, isChecked, cell):
        logger.debug(f'afterCheckBox  GridCursorRow:{self.GridCursorRow} , isChecked:{isChecked} , cell:{cell}')
        try:
            self.isChecked = isChecked
            row, col = cell
            if self.isChecked:
                self.SetCellValue(row, col, '1')
                if col == 3:
                    # Setting image icon for primary key
                    self.SetCellValue(row, 0, "0")
            else:
                # setting blank for un-check column
                self.SetCellValue(row, col, '')
                
                dataType = self.GetCellValue(row, 2)
                if dataType == 'INTEGER':
                    # setting image icon for integer column
                    self.SetCellValue(row, 0, "4")
                elif dataType in ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
                    for d in  ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
                        if dataType.lower().startswith(d.lower()):
                            self.SetCellValue(row, 0, "1")
                            break
                    # setting image icon for integer column
                
            self.Refresh()
        except Exception as e:
            logger.error(e, exc_info=True)
              
    def OnEditorCreated(self, evt):
        logger.debug(f"OnEditorCreated: ({evt.GetRow()}, {evt.GetCol()}) {evt.GetControl().Value}")
        row = evt.GetRow()
        col = evt.GetCol()
        self.lastSelectedCell = (row, col)
        # In this example, all cells in row 0 are GridCellChoiceEditors,
        # so we need to setup the selection list and bindings. We can't
        # do this in advance, because the ComboBox control is created with
        # the editor.
        if self.GetColLabelValue(col) in self.comboBoxList:
            # Get a reference to the underlying ComboBox control.
            self.comboBox = evt.GetControl()
            
            # Bind the ComboBox events.
            self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnGridComboBox)
            self.comboBox.Bind(wx.EVT_TEXT, self.OnGridComboBoxText)
            
            # Load the initial choice list.
            for (item, data) in self.dataTypeList:
                self.comboBox.Append(item, data)
        elif self.GetColLabelValue(col) in self.checkBoxColumns:
            
            self.cb = evt.Control
            self.cb.WindowStyle |= wx.WANTS_CHARS

            self.cb.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
            self.cb.Bind(wx.EVT_CHECKBOX, self.onCheckBox)  
            
        logger.debug(f"After change OnEditorCreated: ({evt.GetRow()}, {evt.GetCol()}) {evt.GetControl().Value}")   
        evt.Skip()
        
    def onKeyDown(self, evt):
        if evt.KeyCode == wx.WXK_UP:
            if self.GridCursorRow > 0:
                self.DisableCellEditControl()
                self.MoveCursorUp(False)
        elif evt.KeyCode == wx.WXK_DOWN:
            if self.GridCursorRow < (self.NumberRows - 1):
                self.DisableCellEditControl()
                self.MoveCursorDown(False)
        elif evt.KeyCode == wx.WXK_LEFT:
            if self.GridCursorCol > 0:
                self.DisableCellEditControl()
                self.MoveCursorLeft(False)
        elif evt.KeyCode == wx.WXK_RIGHT:
            if self.GridCursorCol < (self.NumberCols - 1):
                self.DisableCellEditControl()
                self.MoveCursorRight(False)
        else:
            evt.Skip()

    def onCheckBox(self, evt):
        logger.debug('onCheckBox lastSelectedCell:%s', self.lastSelectedCell)
        if self.lastSelectedCell:
            self.afterCheckBox(evt.IsChecked(), cell=self.lastSelectedCell)

    ########################### Check box close ###################################    
                 
    def OnCellRightClick(self, evt):
        logger.debug(f"OnCellRightClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()})")
        evt.Skip()
 
    def OnCellLeftDClick(self, evt):
        logger.debug(f"OnCellLeftDClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()})")
        evt.Skip()
 
    def OnCellRightDClick(self, evt):
        logger.debug(f"OnCellRightDClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()})")
        evt.Skip()
 
    def OnLabelLeftClick(self, evt):
        logger.debug(f"OnLabelLeftClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()})")
        evt.Skip()
 
    def OnLabelRightClick(self, evt):
        logger.debug(f"OnLabelRightClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()})")
        evt.Skip()
 
    def OnLabelLeftDClick(self, evt):
        logger.debug(f"OnLabelLeftDClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()})")
        evt.Skip()
 
    def OnLabelRightDClick(self, evt):
        logger.debug(f"OnLabelRightDClick: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()})")
        evt.Skip()
 
    def OnRowSize(self, evt):
        logger.debug(f"OnRowSize: row {evt.GetRowOrCol()}, {evt.GetPosition()}")
        evt.Skip()
 
    def OnColSize(self, evt):
        logger.debug("OnColSize: col %d, %s" , evt.GetRowOrCol(),
                                           evt.GetPosition())
        evt.Skip()
 
    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        logger.debug(f"OnRangeSelect: {msg}  top-left {evt.GetTopLeftCoords()}, bottom-right { evt.GetBottomRightCoords()}")
        evt.Skip()
 
    def updateIconColumn(self, cell=None, cellValue=None):
        row, col = cell
        logger.debug(f'updateIconColumn {cell}, {cellValue}')
        self.columns[row].__setattr__(self.GetColLabelValue(col), cellValue)
        self.GetParent().sqlType.columns = self.columns
        pub.sendMessage('OnCellChange', sqlType=self.GetParent().sqlType)
#         if self.GetColLabelValue(col) == 'dataType':
#         targetRow = row
#         targetCol=0
#         if cellValue in ["INTEGER", "INT"]:
#             self.SetCellValue(targetRow, targetCol, "4")
#         elif cellValue.upper() in ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
# #                 self.SetCellValue(targetRow, targetCol,"1")
#             isPrimaryKey = self.GetCellValue(row, 3)
#             if not isPrimaryKey == 1:
#                 for d in  ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
#                     if cellValue.lower().startswith(d.lower()):
#                         self.SetCellValue(targetRow, targetCol, "1")
#                         break 

    def OnCellChange(self, evt):
 
        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        sourceValue = self.GetCellValue(evt.GetRow(), evt.GetCol())
        logger.debug(f"OnCellChange: ({evt.GetRow()},{evt.GetCol()}) {evt.GetPosition()} , cellValue : {sourceValue}")
        sourceRow = evt.GetRow()
        sourceCol = evt.GetCol()
        
        self.updateIconColumn(cell=(evt.GetRow(), evt.GetCol()), cellValue=sourceValue)
        
#         if sourceCol == 2:
#             targetRow = sourceRow
#             targetCol = 0
#             if sourceValue in ["INTEGER", "INT"]:
#                 self.SetCellValue(targetRow, targetCol, "4")
#             elif sourceValue.upper() in ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
# #                 self.SetCellValue(targetRow, targetCol,"1")
#                 isPrimaryKey = self.GetCellValue(sourceRow, 3)
#                 if not isPrimaryKey == 1:
#                     for d in  ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
#                         if sourceValue.lower().startswith(d.lower()):
#                             self.SetCellValue(targetRow, targetCol, "1")
#                             break
        self.Refresh()

#         if value == 'no good':
#             self.moveTo = evt.GetRow(), evt.GetCol()
#         #All cells have a value, regardless of the editor.
#         print 'Changed cell: (%u, %u)' % (Row, Col)
#         print 'value: %s' % self.grid1.GetCellValue(Row, Col)
#         
#         #Row 0 means a GridCellChoiceEditor, so we should have associated
#         #an index and client data.
#         if Row == 0:
#             print 'index: %u' % self.index
#             print 'data: %s' % self.data
#         
#         print ''            #blank line to make it pretty.
#         event.Skip()
    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        logger.debug("OnSelectCell: %s (%d,%d) %s" , msg, evt.GetRow(),
                                                 evt.GetCol(), evt.GetPosition())
#  
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
#  
#         if self.IsCellEditControlEnabled():
#             self.HideCellEditControl()
#             self.DisableCellEditControl()
#         if row > -1 and col > -1:
#             value = self.GetCellValue(row, col)
#      
#             if value == 'no good 2':
#                 return  # cancels the cell selection
     
#         evt.Skip()
        if evt.Col in self.checkBoxColumns:
            wx.CallAfter(self.EnableCellEditControl)
        evt.Skip()
 
    def OnEditorShown(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to edit this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return
 
        logger.debug("OnEditorShown: (%d,%d) %s" , evt.GetRow(), evt.GetCol(),
                                               evt.GetPosition())
        evt.Skip()
 
    def OnEditorHidden(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to  finish editing this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return
 
        logger.debug("OnEditorHidden: (%d,%d) %s" , evt.GetRow(),
                                                evt.GetCol(),
                                                evt.GetPosition())
        evt.Skip()

    # This method fires when the underlying GridCellChoiceEditor ComboBox
    # is done with a selection.
    def OnGridComboBox(self, event):
        # Save the index and client data for later use.
        self.index = self.comboBox.GetSelection()
        self.data = self.comboBox.GetClientData(self.index)
        
        logger.debug('ComboBoxChanged: %s' , self.comboBox.GetValue())
        logger.debug('ComboBox index: %u' , self.index)
        logger.debug('ComboBox data: %u' , self.data)
        event.Skip()        
        
    # This method fires when any text editing is done inside the text portion
    # of the ComboBox. This method will fire once for each new character, so
    # the print statements will show the character by character changes.
    def OnGridComboBoxText(self, event):
        # The index for text changes is always -1. This is how we can tell
        # that new text has been entered, as opposed to a simple selection
        # from the drop list. Note that the index will be set for each character,
        # but it will be -1 every time, so the final result of text changes is
        # always an index of -1. The value is whatever text that has been 
        # entered. At this point there is no client data. We will have to add
        # that later, once all of the text has been entered.
        self.index = self.comboBox.GetSelection()
        
        logger.debug('ComboBoxText: %s' , self.comboBox.GetValue())
        logger.debug('ComboBox index: %u' , self.index)
#         self.sql
#         selectedColName = self.GetParent().tableDict['row'][0][self.lastSelectedCell[1]]
#         colName = "".join(selectedColName.split(' ')).lower()
#         columns = self.GetParent().tableDict['rows'][self.lastSelectedCell[0]].keys()
#         for col in columns:
#             if colName in col.lower():
#                 colName = col
#                 break
#         
#         logger.debug("currentValue:%s", self.GetParent().tableDict['rows'][self.lastSelectedCell[0]][colName])
#         self.GetParent().tableDict['rows'][self.lastSelectedCell[0]][colName] = self.comboBox.GetValue()
#         self.GetParent().updateTableEditorPanel()
#         self.updateGridCell()
        event.Skip()
           
    def updateGridCell(self):
        '''
        This method will be called as soon as a comboBox value changes.
        '''
        pass
                     
    def addData(self, columns=None):
        self.columns = columns
#         print(self.GetRowSizes())
#         print(self.GetColSizes())
        self.ClearGrid()
        
        if columns and len(columns) > 0:
            logger.debug('rows:%s', self.GetNumberRows())
            logger.debug('cols:%s', self.GetNumberCols())
    #         self.DeleteRows()
            currentRows, currentCols = (self.GetNumberRows(), self.GetNumberCols())
            newRows = len(columns)
            newCols = len(columns[0].__dict__)
    #         self.AppendRows(numRows=len(data)-1, updateLabels=True)   
    #         if len(data) > 0 :
    #             self.AppendCols(numCols=len(data[0]), updateLabels=True)  
            if newRows < currentRows:
                # - Delete rows:
                self.DeleteRows(0, currentRows - newRows, True)
    
            if newRows > currentRows:
                # - append currentRows:
                self.AppendRows(newRows - currentRows)
                
            if newCols < currentCols:
                # - Delete rows:
                self.DeleteCols(pos=0, numCols=currentCols - newCols, updateLabels=True)
    
            if newCols > currentCols:
                # - append currentRows:
                self.AppendCols(newCols - currentCols)
    
            self.loadGridData(columns)
        else:
            numCols = self.GetNumberCols()
            numRows = self.GetNumberRows()
            if numRows > 0:
                self.DeleteRows(pos=0, numRows=numRows, updateLabels=True)
            if numCols > 0:
                self.DeleteCols(pos=0, numCols=numCols, updateLabels=True)
            
        self.Refresh()
#         self.Update()
    
    def setColumnWidth(self, col):
        if col == 0:
            self.SetColSize(col, 30)  
        elif col == 1:  
            self.SetColSize(col, 140)  
        elif col == 2:  
            self.SetColSize(col, 90)  
        elif col == 3:  
            self.SetColSize(col, 60)  
        elif col == 4:  
            self.SetColSize(col, 100)  
        elif col == 5:  
            self.SetColSize(col, 70)  
        elif col == 6:  
            self.SetColSize(col, 70)  
        elif col == 7:  
            self.SetColSize(col, 150)
        elif col == 8:  
            self.SetColSize(col, 150)
        elif col == 9:  
            self.SetColSize(col, 80)
            
    def getImageIndex(self, column):
        imageIndex = 1
        if column.primaryKey == 1:
            imageIndex = 0
        elif column.dataType in ['VARCHAR', 'TEXT']:
            imageIndex = 1
        elif column.unique == 1:
            imageIndex = 4
        return imageIndex
        
    def loadGridData(self, columns=None):
        logger.debug('loadGridData')
        for row, column in enumerate(columns):
            for col, (k, v) in enumerate(column.__dict__.items()):
                self.setColumnWidth(col)
                logger.debug(f'({row},{col}),{k}:{v}')
                if row == 0 :
                    self.SetColLabelValue(col, str(k))
                if col == 2:
                    #  row == 2 means data type
                    # Create the GridCellChoiceEditor with a blank list. Items will
                    # be added later at runtime. "allowOthers" allows the user to
                    # create new selection items on the fly.
                    tChoiceEditor = wx.grid.GridCellChoiceEditor([], allowOthers=True)
                    self.SetCellEditor(row , col, tChoiceEditor)
                    
                    selectedDataType = None
                    for dataType in self.dataTypeList:
                        if v.upper() == dataType[0]:
                            selectedDataType = k
                            break
                    self.SetCellValue(row, col, str(v))
                    self.SetColSize(col, 100)
                elif k in self.comboBoxList:
                    self.SetCellValue(row, col, str(v))      
                elif k in self.checkBoxColumns:
                    attr = wx.grid.GridCellAttr()
                    attr.SetEditor(wx.grid.GridCellBoolEditor())
                    attr.SetRenderer(wx.grid.GridCellBoolRenderer())
                    self.SetColAttr(col, attr)  
                    self.SetCellValue(row , col, str(v))    
                elif k in self.textBoxColumns:
                    self.SetCellValue(row, col, str(v))  
                elif col in self.iconColumns:
                    logger.debug("self.iconColumns: %s", self.iconColumns)
                    self.SetColLabelValue(col, 'Icon')
                    attr = wx.grid.GridCellAttr()
                    attr.SetRenderer(GridCellIconRenderer(self.bmpList))
                    self.SetColAttr(col, attr)  
                    self.SetCellValue(row, col, str(self.getImageIndex(column)))
                    self.SetColSize(col, 50)
                                               
    def fillTableData(self, data=None):  
        for dataKey, dataValue in data.items():
            logger.debug("dataKey:%s , dataValue: %s", dataKey, dataValue)
            for idx, colValue in enumerate(dataValue):
#                 logger.debug(idx, dataValue)
                if dataKey == 0:
                    self.SetColLabelValue(idx, str(colValue))
                elif dataKey > 0 and idx == 2:
                    #  idx == 2 means data type
                    # Create the GridCellChoiceEditor with a blank list. Items will
                    # be added later at runtime. "allowOthers" allows the user to
                    # create new selection items on the fly.
                    tChoiceEditor = wx.grid.GridCellChoiceEditor([], allowOthers=True)
                    self.SetCellEditor(dataKey - 1, idx, tChoiceEditor)
                    
                    selectedDataType = None
                    for dataType in self.dataTypeList:
                        if dataType[0] == colValue:
                            selectedDataType = dataType
                            break
                    self.SetCellValue(dataKey - 1, idx, selectedDataType[0])
                    self.SetColSize(idx, 100)
                    
                elif dataKey > 0 and idx in self.comboBoxList:
                    self.SetCellValue(dataKey - 1, idx, str(colValue))      
                elif dataKey > 0 and idx in self.checkBoxColumns:
                    attr = wx.grid.GridCellAttr()
                    attr.SetEditor(wx.grid.GridCellBoolEditor())
                    attr.SetRenderer(wx.grid.GridCellBoolRenderer())
                    self.SetColAttr(idx, attr)  
                    self.SetCellValue(dataKey - 1, idx, str(colValue))    
                elif dataKey > 0 and idx in self.textBoxColumns:
                    self.SetCellValue(dataKey - 1, idx, str(colValue))  
                elif dataKey > 0 and idx in self.iconColumns:
                    logger.debug("self.iconColumns: %s", self.iconColumns)
                    attr = wx.grid.GridCellAttr()
                    attr.SetRenderer(GridCellIconRenderer(self.bmpList))
                    self.SetColAttr(idx, attr)  
                    self.SetCellValue(dataKey - 1, idx, str(colValue))
                    self.SetColSize(idx, 50)
                
                if idx == 0:
                    self.SetColSize(idx, 50)  
                elif idx == 1:  
                    self.SetColSize(idx, 140)  
                elif idx == 2:  
                    self.SetColSize(idx, 150)  
                elif idx == 3:  
                    self.SetColSize(idx, 120)  
                elif idx == 4:  
                    self.SetColSize(idx, 100)  
                elif idx == 5:  
                    self.SetColSize(idx, 70)  
                elif idx == 6:  
                    self.SetColSize(idx, 150)  
                elif idx == 7:  
                    self.SetColSize(idx, 150)  


class GridCellIconRenderer(wx.grid.PyGridCellRenderer):
    """
    Utility class for displaying an icon in a table column.
    """
    
    def __init__(self, *arg, **kw):
        super(GridCellRenderer, self).__init__()
        self.bmpList = arg[0]
        self.selectBmpIndex = 0
                  
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):  
        self.selectBmpIndex = grid.GetCellValue(row, col)
        try: 
            selectedBmp = self.bmpList[int(self.selectBmpIndex)]
        except Exception as e:
            logger.error(e , exc_info=True) 
        
        image = wx.MemoryDC()
        image.SelectObject(selectedBmp)
        # clear the background
        dc.SetBackgroundMode(wx.SOLID)
        if isSelected:
#             dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangle(rect)        
        # copy the image but only to the size of the grid cell
        width, height = selectedBmp.GetWidth(), selectedBmp.GetHeight()

        if width > rect.width - 2:
            width = rect.width - 2

        if height > rect.height - 2:
            height = rect.height - 2

        dc.Blit(rect.x + 1, rect.y + 1, width, height,
                image,
                0, 0, wx.COPY, True)

                      
class GenericTable(wx.grid.PyGridTableBase):

    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        
    def GetNumberRows(self):
        """Return the number of rows in the grid"""
        return len(self.data)

    def GetNumberCols(self):
        """Return the number of columns in the grid"""
        return len(self.data[0])

    def GetColLabelValue(self, *args, **kw):
        if self.colLabels:
            return self.colLabels[args[0]]
        else:
            return super(GenericTable, self).GetColLabelValue(*args, **kw)
        
    def GetRowLabelValue(self, *args, **kw):
        if self.rowLabels:
            return self.rowLabels[args[0]]
        else:
            return super(GenericTable, self).GetRowLabelValue(*args, **kw)
        
    def IsEmptyCell(self, row, col):
        """Return True if the cell is empty"""
        return False

    def GetValue(self, row, col):
        """Return the value of a cell"""
        return self.data[row][col]

    def SetValue(self, row, col, value):
        """Set the value of a cell"""
        pass       
    
    def GetTypeName(self, row, col):
        """Return the name of the data type of the value in the cell"""
        return None


#####################################################################################################
class CreateTableFrame(wx.Frame):
    
    def __init__(self, parent, id=wx.ID_ANY, Title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER, log=None):

        wx.Frame.__init__(self, parent, id, Title, pos, size, style)
        
        self.fileOperations = FileOperations()
        pub.subscribe(self.__OnCellChange, 'OnCellChange')
        self._mgr = aui.AuiManager()

        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)

        # set frame icon
#         self.SetIcon(self.fileOperations.getImageBitmap(imageName='eclipse16.png'))

        # set up default notebook style
#         self._mgr._autoNBStyle = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self._notebook_theme = 0
        self.createStatusBar()

        self.BuildPanes()
        self.BindEvents()

    def createStatusBar(self):
        logger.info('createStatusBar')
        self.statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
#         self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
        self.statusbar.SetStatusText(f"Welcome {self.Title}", 1)

    def BuildPanes(self):

        # min size for the frame itself isn't completely done.
        # see the end up AuiManager.Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))
        # create some toolbars
#         tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
#                              agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
#         tb1.SetToolBitmapSize(wx.Size(16, 16))
#         tb1.AddSimpleTool(wx.NewIdRef(), "Test", wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE))
#         tb1.Realize()      
#         
# #         self.creatingTable = CreatingTablePanel(splitter, connectionName, newTableName)
#         self._mgr.AddPane(tb1, aui.AuiPaneInfo().Name("tb1").Caption("Big Toolbar").
#                           ToolbarPane().Top())
        # add a bunch of panes
        self.buttonPanel = CreateButtonPanel(self)
        self.editPanel = CreatingEditorPanel(self)
        self._mgr.AddPane(self.creatingTablePanel(), aui.AuiPaneInfo().
                          Name("table").Caption("Table").BestSize(wx.Size(200, 100))
                          .Layer(1).Center().CaptionVisible(True, left=True)
                          .MinimizeButton(True).CloseButton(False))
        self._mgr.AddPane(self.editPanel, aui.AuiPaneInfo().
                          Name("sql").Caption("SQL").BestSize(wx.Size(100, 100))
                          .Layer(1).Center().CaptionVisible(True, left=True)
                          .MinimizeButton(True).CloseButton(False))
        self._mgr.AddPane(self.buttonPanel, aui.AuiPaneInfo().
                          Name("button").Caption("Button")
                          .Layer(1).Bottom().CaptionVisible(False, left=True)
                          .MinimizeButton(True).CloseButton(False))

        self._mgr.Update()

    def __OnCellChange(self, sqlType=None):
        logger.debug(f'__OnCellChange {sqlType}')
        self.editPanel.sstc.SetText(sqlType.getCreateSql())

    def BindEvents(self):
        pass

    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition, wx.Size(width, height), self._mgr)
        return ctrl

    def creatingTablePanel(self, width=80, height=80):

        tablePanel = CreateTablePanel(self, 'connectionName', 'newTableName')
        return tablePanel

#     def creatingSQLPanel(self, width=80, height=80):
# 
#         self.editPanel = CreatingEditorPanel(self)
# 
#         return self.editPanel


class SizeReportCtrl(wx.Control):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                size=wx.DefaultSize, mgr=None):

        wx.Control.__init__(self, parent, id, pos, size, style=wx.NO_BORDER)
        self._mgr = mgr

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        size = self.GetClientSize()

        s = "Size: %d x %d" % (size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height += 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x - w) / 2, (size.y - height * 5) / 2)

        if self._mgr:

            pi = self._mgr.GetPane(self)

            s = "Layer: %d" % pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 1))

            s = "Dock: %d Row: %d" % (pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 2))

            s = "Position: %d" % pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 3))

            s = "Proportion: %d" % pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 4))

    def OnEraseBackground(self, event):

        pass

    def OnSize(self, event):

        self.Refresh()


#####################################################################################################
if __name__ == '__main__':
    app = wx.App(False)
#     frame = CreateTableFrame(None, 'table creation')
    frame = CreateTableFrame(None, size=(1000, 600))
    tableDict = dict()
#     frame.setData(tableDict)
    frame.Show()
    app.MainLoop()
