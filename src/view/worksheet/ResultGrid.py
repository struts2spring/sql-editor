'''
Created on 17-Feb-2017

@author: vijay
'''

import wx
import wx.dataview as dv
from wx import ListCtrl
from src.view.constants import ID_COPY_COLUMN_HEADER
import string
import  wx.grid as gridlib
import logging

logger = logging.getLogger('extensive')


#---------------------------------------------------------------------------
class MyCellEditor(gridlib.PyGridCellEditor):
    """
    This is a sample GridCellEditor that shows you how to make your own custom
    grid editors.  All the methods that can be overridden are shown here.  The
    ones that must be overridden are marked with "*Must Override*" in the
    docstring.
    """

    def __init__(self):
        logger.info("MyCellEditor ctor\n")
        gridlib.PyGridCellEditor.__init__(self)

    def Create(self, parent, id, evtHandler):
        """
        Called to create the control, which must derive from wx.Control.
        *Must Override*
        """
        logger.info("MyCellEditor: Create\n")
        self._tc = wx.TextCtrl(parent, id, "")
        self._tc.SetInsertionPoint(0)
        self.SetControl(self._tc)

        if evtHandler:
            self._tc.PushEventHandler(evtHandler)

    def SetSize(self, rect):
        """
        Called to position/size the edit control within the cell rectangle.
        If you don't fill the cell (the rect) then be sure to override
        PaintBackground and do something meaningful there.
        """
        logger.info("MyCellEditor: SetSize %s\n" % rect)
        self._tc.SetDimensions(rect.x, rect.y, rect.width + 2, rect.height + 2,
                               wx.SIZE_ALLOW_MINUS_ONE)

    def Show(self, show, attr):
        """
        Show or hide the edit control.  You can use the attr (if not None)
        to set colours or fonts for the control.
        """
        logger.info("MyCellEditor: Show(self, %s, %s)\n" % (show, attr))
        super(MyCellEditor, self).Show(show, attr)

    def PaintBackground(self, rect, attr):
        """
        Draws the part of the cell not occupied by the edit control.  The
        base  class version just fills it with background colour from the
        attribute.  In this class the edit control fills the whole cell so
        don't do anything at all in order to reduce flicker.
        """
        logger.info("MyCellEditor: PaintBackground\n")

    def BeginEdit(self, row, col, grid):
        """
        Fetch the value from the table and prepare the edit control
        to begin editing.  Set the focus to the edit control.
        *Must Override*
        """
        logger.info("MyCellEditor: BeginEdit (%d,%d)\n" % (row, col))
        self.startValue = grid.GetTable().GetValue(row, col)
        self._tc.SetValue(self.startValue)
        self._tc.SetInsertionPointEnd()
        self._tc.SetFocus()

        # For this example, select the text
        self._tc.SetSelection(0, self._tc.GetLastPosition())

    def EndEdit(self, row, col, grid, oldVal):
        """
        End editing the cell.  This function must check if the current
        value of the editing control is valid and different from the
        original value (available as oldval in its string form.)  If
        it has not changed then simply return None, otherwise return
        the value in its string form.
        *Must Override*
        """
        logger.info("MyCellEditor: EndEdit (%s)\n" % oldVal)
        val = self._tc.GetValue()
        if val != oldVal:  # self.startValue:
            return val
        else:
            return None

    def ApplyEdit(self, row, col, grid):
        """
        This function should save the value of the control into the
        grid or grid table. It is called only after EndEdit() returns
        a non-None value.
        *Must Override*
        """
        logger.info("MyCellEditor: ApplyEdit (%d,%d)\n" % (row, col))
        val = self._tc.GetValue()
        grid.GetTable().SetValue(row, col, val)  # update the table

        self.startValue = ''
        self._tc.SetValue('')

    def Reset(self):
        """
        Reset the value in the control back to its starting value.
        *Must Override*
        """
        logger.info("MyCellEditor: Reset\n")
        self._tc.SetValue(self.startValue)
        self._tc.SetInsertionPointEnd()

    def IsAcceptedKey(self, evt):
        """
        Return True to allow the given key to start editing: the base class
        version only checks that the event has no modifiers.  F2 is special
        and will always start the editor.
        """
        logger.info("MyCellEditor: IsAcceptedKey: %d\n" % (evt.GetKeyCode()))

        # # We can ask the base class to do it
        # return super(MyCellEditor, self).IsAcceptedKey(evt)

        # or do it ourselves
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)

    def StartingKey(self, evt):
        """
        If the editor is enabled by pressing keys on the grid, this will be
        called to let the editor do something about that first key if desired.
        """
        logger.info("MyCellEditor: StartingKey %d\n" % evt.GetKeyCode())
        key = evt.GetKeyCode()
        ch = None
        if key in [ wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2, wx.WXK_NUMPAD3,
                    wx.WXK_NUMPAD4, wx.WXK_NUMPAD5, wx.WXK_NUMPAD6, wx.WXK_NUMPAD7,
                    wx.WXK_NUMPAD8, wx.WXK_NUMPAD9
                    ]:

            ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)

        elif key < 256 and key >= 0 and chr(key) in string.printable:
            ch = chr(key)

        if ch is not None:
            # For this example, replace the text.  Normally we would append it.
            # self._tc.AppendText(ch)
            self._tc.SetValue(ch)
            self._tc.SetInsertionPointEnd()
        else:
            evt.Skip()

    def StartingClick(self):
        """
        If the editor is enabled by clicking on the cell, this method will be
        called to allow the editor to simulate the click on the control if
        needed.
        """
        logger.info("MyCellEditor: StartingClick\n")

    def Destroy(self):
        """final cleanup"""
        logger.info("MyCellEditor: Destroy\n")
        super(MyCellEditor, self).Destroy()

    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        logger.info("MyCellEditor: Clone\n")
        return MyCellEditor()
        
            
class ResultDataGrid(gridlib.Grid):

    def __init__(self, parent, model=None, data=None):
        gridlib.Grid.__init__(self, parent, -1)

        self.CreateGrid(0, 0)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.showGridCellPopupMenu)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.showHeaderPopupMenu)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        
        # Somebody changed the grid so the type registry takes precedence
        # over the default attribute set for editors and renderers, so we
        # have to set null handlers for the type registry before the
        # default editor will get used otherwise...
        # self.RegisterDataType(wxGRID_VALUE_STRING, None, None)
        # self.SetDefaultEditor(MyCellEditor())

        # Or we could just do it like this:
        # self.RegisterDataType(wx.GRID_VALUE_STRING,
        #                      wx.GridCellStringRenderer(),
        #                      MyCellEditor())
        #                       )

        # but for this example, we'll just set the custom editor on one cell
#         self.SetCellEditor(1, 0, MyCellEditor())
#         self.SetCellValue(1, 0, "Try to edit this box")
# 
#         # and on a column
#         attr = gridlib.GridCellAttr()
#         attr.SetEditor(MyCellEditor())
#         self.SetColAttr(2, attr)
#         self.SetCellValue(1, 2, "or any in this column")
# 
#         self.addData()

    def addData(self, data=None):
#         logger.info(self.GetRowSizes())
#         logger.info(self.GetColSizes())
        self.ClearGrid()
        try:
            if data and len(data) > 0:
#                 logger.info('rows:', self.GetNumberRows())
#                 logger.info('cols:', self.GetNumberCols())
        #         self.DeleteRows()
                currentRows, currentCols = (self.GetNumberRows(), self.GetNumberCols())
                newRows = len(data) - 1
                newCols = len(data[0])
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
        
                for dataKey, dataValue in data.items():
#                     logger.info(dataKey, dataValue)
                    for idx, colValue in enumerate(dataValue):
        #                 logger.info(idx, dataValue)
                        if dataKey == 0:
                            self.SetColLabelValue(idx, str(colValue))
                        else:
                            try:
                                self.SetCellValue(dataKey - 1, idx, str(colValue))
                            except Exception as e:
                                logger.error(e, exc_info=True)  
            else:
                numCols = self.GetNumberCols()
                numRows = self.GetNumberRows()
                logger.debug("numRows:%s, numCol: %s", numRows, numCols)
                if numRows > 0 and numCols > 0:
                    self.DeleteCols(pos=0, numCols=numCols, updateLabels=True)
                    self.DeleteRows(pos=0, numRows=numRows, updateLabels=True)
        except Exception as e:
            logger.error(e, exc_info=True)    
        self.Refresh()
#         self.SetColSize(0, 150)
#         self.SetColSize(1, 150)
#         self.SetColSize(2, 150)

    def selection(self):
        # Show cell selection
        # If selection is cell...
        if self.GetSelectedCells():
            logger.info("Selected cells " + str(self.GetSelectedCells()))
        # If selection is block...
        if self.GetSelectionBlockTopLeft():
            logger.info("Selection block top left " + str(self.GetSelectionBlockTopLeft()))
        if self.GetSelectionBlockBottomRight():
            logger.info("Selection block bottom right " + str(self.GetSelectionBlockBottomRight()))
        
        # If selection is col...
        if self.GetSelectedCols():
            logger.info("Selected cols " + str(self.GetSelectedCols()))
        
        # If selection is row...
        if self.GetSelectedRows():
            logger.info("Selected rows " + str(self.GetSelectedRows()))

    def currentcell(self):
        # Show cursor position
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        cell = (row, col)
        logger.info("Current cell " + str(cell))
        
    def OnKey(self, event):
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            logger.info("Ctrl+C")
            self.selection()
            # Call copy method
            self.copy()
            
        # If Ctrl+V is pressed...
        if event.ControlDown() and event.GetKeyCode() == 86:
            logger.info("Ctrl+V")
            self.currentcell()
            # Call paste method
            self.paste()
            
        # If Supr is presed
        if event.GetKeyCode() == 127:
            logger.info("Supr")
            # Call delete method
            self.delete()
            
        # Skip other Key events
        if event.GetKeyCode():
            event.Skip()
            return

    def copy(self):
        logger.info("Copy method")
        # Number of rows and cols
        rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
        cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
        
        # data variable contain text that must be set in the clipboard
        data = ''
        
        # For each cell in selected range append the cell value in the data variable
        # Tabs '\t' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                data = data + str(self.GetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c))
                if c < cols - 1:
                    data = data + '\t'
            data = data + '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")
            
    def paste(self):
        logger.info("Paste method")
        clipboard = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")
        data = clipboard.GetText()
        table = []
        y = -1
        # Convert text in a array of lines
        for r in data.splitlines():
            y = y + 1
            x = -1
            # Convert c in a array of text separated by tab
            for c in r.split('\t'):
                x = x + 1
                self.SetCellValue(self.GetGridCursorRow() + y, self.GetGridCursorCol() + x, c)

    #----------------------------------------------------------------------
    def onCellEdit(self, event):
        '''
        When cell is edited, get a handle on the editor widget
        and bind it to EVT_KEY_DOWN
        '''        
        editor = event.GetControl()        
        editor.Bind(wx.EVT_KEY_DOWN, self.onEditorKey)
        event.Skip()
 
    #----------------------------------------------------------------------
    def onEditorKey(self, event):
        '''
        Handler for the wx.grid's cell editor widget's keystrokes. Checks for specific
        keystrokes, such as arrow up or arrow down, and responds accordingly. Allows
        all other key strokes to pass through the handler.
        '''
        keycode = event.GetKeyCode() 
        if keycode == wx.WXK_UP:
            logger.info('you pressed the UP key!')
            self.grid.MoveCursorUp(False)
        elif keycode == wx.WXK_DOWN:
            logger.info('you pressed the down key!')
            self.grid.MoveCursorDown(False)
        elif keycode == wx.WXK_LEFT:
            logger.info('you pressed the left key!')
            self.grid.MoveCursorLeft(False)
        elif keycode == wx.WXK_RIGHT:
            logger.info('you pressed the right key')
            self.grid.MoveCursorRight(False)
        else:
            pass
        event.Skip()        

#----------------------------------------------------------------------
    def showHeaderPopupMenu(self, event):
        """
        Create and display a popup menu on right-click event
        """
        col=event.GetCol()
        if col>=0:
            header = self.GetColLabelValue(event.GetCol())
            menu = GridHeaderPopupMenu(header=header)
            self.PopupMenu(menu, event.GetPosition())
            menu.Destroy()

#----------------------------------------------------------------------
    def showGridCellPopupMenu(self, event):
        """
        Create and display a popup menu on right-click event
        """
        menu = GridCellPopupMenu()
        self.PopupMenu(menu, event.GetPosition())
        menu.Destroy()

class GridCellPopupMenu(wx.Menu):

    def __init__(self, header=None):
        wx.Menu.__init__(self)

        item = wx.MenuItem(self, wx.NewId(), "Export...")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.onExport, item)

        item = wx.MenuItem(self, wx.NewId(), "Count rows")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.countRows, item)

    def onExport(self, event):
        logger.info('onExport')
#         print "Item Two selected in the %s window" % self.WinName
        pass

    def countRows(self, event):
        logger.info('countRows')
#         print "Item Three selected in the %s window"%self.WinName
#         copyValue = self.GetColLabelValue(event.GetCol())
              
class GridHeaderPopupMenu(wx.Menu):

    def __init__(self, header=None):
        wx.Menu.__init__(self)
        self.header = header
#         self.WinName = WinName
    
#         item = wx.MenuItem(self, wx.NewId(), "Item One")
#         self.Append(item)
#         self.Bind(wx.EVT_MENU, self.OnItem1, item)

        item = wx.MenuItem(self, wx.NewId(), "Sort...")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem2, item)

        item = wx.MenuItem(self, wx.NewId(), "Copy Selected Header")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)

    def OnItem1(self, event):
#         print "Item One selected in the %s window" % self.WinName
        pass

    def OnItem2(self, event):
#         print "Item Two selected in the %s window" % self.WinName
        pass

    def OnItem3(self, event):
#         print "Item Three selected in the %s window"%self.WinName
#         copyValue = self.GetColLabelValue(event.GetCol())
        self.onCopy(self.header)
        
#----------------------------------------------------------------------
    def onCopy(self, copyValue=None):
        """"""
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText(copyValue)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(self.dataObj)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")


class TestFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Custom Grid Cell Editor Test", size=(640, 480))
        resultDataGrid = ResultDataGrid(self)
        data = {
            0: ('ID', 'PICTURE', 'TYPE', 'FILE_NAME'),
            1: (1, None, u'.jpg', u'IMG_20180918_115610'),
            2: (1, None, u'.jpg', u'IMG_20180918_115610')
            }
        resultDataGrid.addData(data)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
#     frame = wx.Frame(None)

    frame = TestFrame(None)
    frame.Show()
    app.MainLoop()
