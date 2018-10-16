'''
Created on 17-Dec-2016

@author: vijay
'''


import wx
import wx.dataview as dv
from wx import ListCtrl

import string
import  wx.grid as gridlib
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter
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
        logger.debug("MyCellEditor ctor\n")
        gridlib.PyGridCellEditor.__init__(self)


    def Create(self, parent, id, evtHandler):
        """
        Called to create the control, which must derive from wx.Control.
        *Must Override*
        """
        logger.debug("MyCellEditor: Create\n")
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
        logger.debug("MyCellEditor: SetSize %s\n", rect)
        self._tc.SetDimensions(rect.x, rect.y, rect.width + 2, rect.height + 2,
                               wx.SIZE_ALLOW_MINUS_ONE)


    def Show(self, show, attr):
        """
        Show or hide the edit control.  You can use the attr (if not None)
        to set colours or fonts for the control.
        """
        logger.debug("MyCellEditor: Show(self, %s, %s)\n", show, attr)
        super(MyCellEditor, self).Show(show, attr)


    def PaintBackground(self, rect, attr):
        """
        Draws the part of the cell not occupied by the edit control.  The
        base  class version just fills it with background colour from the
        attribute.  In this class the edit control fills the whole cell so
        don't do anything at all in order to reduce flicker.
        """
        logger.debug("MyCellEditor: PaintBackground\n")


    def BeginEdit(self, row, col, grid):
        """
        Fetch the value from the table and prepare the edit control
        to begin editing.  Set the focus to the edit control.
        *Must Override*
        """
        logger.debug("MyCellEditor: BeginEdit (%d,%d)\n" ,row, col)
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
        logger.debug("MyCellEditor: EndEdit (%s)\n" ,oldVal)
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
        logger.debug("MyCellEditor: ApplyEdit (%d,%d)\n" . row, col)
        val = self._tc.GetValue()
        grid.GetTable().SetValue(row, col, val)  # update the table

        self.startValue = ''
        self._tc.SetValue('')
        

    def Reset(self):
        """
        Reset the value in the control back to its starting value.
        *Must Override*
        """
        logger.debug("MyCellEditor: Reset\n")
        self._tc.SetValue(self.startValue)
        self._tc.SetInsertionPointEnd()


    def IsAcceptedKey(self, evt):
        """
        Return True to allow the given key to start editing: the base class
        version only checks that the event has no modifiers.  F2 is special
        and will always start the editor.
        """
        logger.debug("MyCellEditor: IsAcceptedKey: %d\n" ,evt.GetKeyCode())

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
        logger.debug("MyCellEditor: StartingKey %d\n" , evt.GetKeyCode())
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
        logger.debug("MyCellEditor: StartingClick\n")


    def Destroy(self):
        """final cleanup"""
        logger.debug("MyCellEditor: Destroy\n")
        super(MyCellEditor, self).Destroy()


    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        logger.debug("MyCellEditor: Clone\n")
        return MyCellEditor()
        
            
class HistoryGrid(gridlib.Grid):
    def __init__(self, parent, model=None, data=None):
        gridlib.Grid.__init__(self, parent, -1)

        self.CreateGrid(0, 0)

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
#         self.SetColSize(0, 150)
#         self.SetColSize(1, 150)
#         self.SetColSize(2, 150)
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        sqlText='select * from sql_log order by created_time desc;'
        sqlOutput = sqlExecuter.executeText(sqlText)
        if sqlOutput:
            self.addData(data=sqlOutput)




    def addData(self, data=None):
#         logger.debug(self.GetRowSizes())
#         logger.debug(self.GetColSizes())
        self.ClearGrid()
        logger.debug('rows: %s', self.GetNumberRows())
        logger.debug('cols: %s', self.GetNumberCols())
#         self.DeleteRows()
        currentRows,currentCols = (self.GetNumberRows(), self.GetNumberCols())
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
#             logger.error("dataKey: %s dataValue: %s",dataKey, dataValue)
            for idx, colValue in enumerate(dataValue):
#                 print(idx, dataValue)
                if dataKey == 0:
                    self.SetColLabelValue(idx, str(colValue))
                    str(colValue)
                    if str(colValue)== 'id':
                        self.SetColSize(idx,25)
                    elif str(colValue)=='sql':
                        self.SetColSize(idx,250)
                    elif str(colValue)=='connection_name':
                        self.SetColSize(idx,120)
                    elif str(colValue)=='creation_time':
                        self.SetColSize(idx,100)
                    elif str(colValue)=='executed':
                        self.SetColSize(idx,100)
                    elif str(colValue)=='duration':
                        self.SetColSize(idx,100)
                else:
                    self.SetCellValue(dataKey - 1, idx, str(colValue))
        self.Refresh()        
#----------------------------------------------------------------------

# def runTest(frame, nb, log):
#     # Get the data from the ListCtrl sample to play with, converting it
#     # from a dictionary to a list of lists, including the dictionary key
#     # as the first element of each sublist.
#     import ListCtrl
#     musicdata = ListCtrl.musicdata.items()
#     musicdata.sort()
#     musicdata = [[str(k)] + list(v) for k,v in musicdata]
# 
#     win = TestPanel(nb, log, data=musicdata)
#     return win


class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Custom Grid Cell Editor Test", size=(640, 480))
        grid = HistoryGrid(self)

#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
#     frame = wx.Frame(None)

    frame = TestFrame(None)
    frame.Show()
    app.MainLoop()
