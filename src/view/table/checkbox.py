import wx, wx.grid as grd

class MyGrid(grd.Grid):
    def __init__(self, parent):
        grd.Grid.__init__(self, parent, -1, pos=(10,40), size=(420,95))

        self.CreateGrid(3,3)
        self.RowLabelSize = 0
        self.ColLabelSize = 20

        attr = grd.GridCellAttr()
        attr.SetEditor(grd.GridCellBoolEditor())
        attr.SetRenderer(grd.GridCellBoolRenderer())
        self.SetColAttr(1,attr)
        self.SetColSize(1,20)

        self.Bind(grd.EVT_GRID_CELL_LEFT_CLICK,self.onMouse)
        self.Bind(grd.EVT_GRID_SELECT_CELL,self.onCellSelected)
        self.Bind(grd.EVT_GRID_EDITOR_CREATED, self.onEditorCreated)

    def onMouse(self,evt):
        if evt.Col == 1:
            wx.CallLater(100,self.toggleCheckBox)
        evt.Skip()

    def toggleCheckBox(self):
        self.cb.Value = not self.cb.Value
        self.afterCheckBox(self.cb.Value)

    def onCellSelected(self,evt):
        if evt.Col == 1:
            wx.CallAfter(self.EnableCellEditControl)
        evt.Skip()

    def onEditorCreated(self,evt):
        if evt.Col == 1:
            self.cb = evt.Control
            self.cb.WindowStyle |= wx.WANTS_CHARS
            self.cb.Bind(wx.EVT_KEY_DOWN,self.onKeyDown)
            self.cb.Bind(wx.EVT_CHECKBOX,self.onCheckBox)
        evt.Skip()

    def onKeyDown(self,evt):
        if evt.KeyCode == wx.WXK_UP:
            if self.GridCursorRow > 0:
                self.DisableCellEditControl()
                self.MoveCursorUp(False)
        elif evt.KeyCode == wx.WXK_DOWN:
            if self.GridCursorRow < (self.NumberRows-1):
                self.DisableCellEditControl()
                self.MoveCursorDown(False)
        elif evt.KeyCode == wx.WXK_LEFT:
            if self.GridCursorCol > 0:
                self.DisableCellEditControl()
                self.MoveCursorLeft(False)
        elif evt.KeyCode == wx.WXK_RIGHT:
            if self.GridCursorCol < (self.NumberCols-1):
                self.DisableCellEditControl()
                self.MoveCursorRight(False)
        else:
            evt.Skip()

    def onCheckBox(self,evt):
        self.afterCheckBox(evt.IsChecked())

    def afterCheckBox(self,isChecked):
        # print 'afterCheckBox',self.GridCursorRow,isChecked
        pass

class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Custom cell editor test", size=(250,200))
        panel = wx.Panel(self,style=0)
        grid = MyGrid(panel)
        grid.SetFocus()
        self.CentreOnScreen()

class MyApp(wx.App):
    def OnInit(self):
        frame = TestFrame(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

MyApp(0).MainLoop()