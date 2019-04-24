import wx
from src.view.preference.layout.PreferencesTree import PrefrencesTreePanel
from src.view.util.FileOperationsUtil import FileOperations
from src.view.preference.layout.ApplyCloseBtn import ApplyCloseButtonPanel
from src.view.preference.general.Workspace import WorkspacePanel

try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD
import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class Preference(wx.Frame):

    def __init__(self, parent, title, size=(700, 440)):
        wx.Frame.__init__(self, parent, -1, title, size=size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Center()
#         self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.allowAuiFloating = False
        self.SetMinSize((640, 480))
        self.fileOperations = FileOperations()
        icon = wx.Icon()
        icon.CopyFromBitmap(self.fileOperations.getImageBitmap(imageName='eclipse16.png'))
        self.SetIcon(icon)
        self._mgr = aui.AuiManager()
        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)
        self.BuildPanes()
        self.BindEvents()
        self.Show()

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

    def BindEvents(self):
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)

    def BuildPanes(self):
        self.SetMinSize(wx.Size(700, 440))
        # add a bunch of panes
        self._mgr.AddPane(self.createPreferenceTree(), aui.AuiPaneInfo().
                          Name("left").Caption("Pane Caption").BestSize(wx.Size(200, 100))
                          .CaptionVisible(False, left=False)
                          .Left().MinimizeButton(True))
#                           .MinSize(wx.Size(200,100))

        self._mgr.AddPane(self.rightPanel(), aui.AuiPaneInfo().
                          Name("center").Caption("Client Size Reporter").
                          Center().Position(1).CloseButton(True).MaximizeButton(True).
                          MinimizeButton(True).CaptionVisible(False, left=False))
        
        self._mgr.AddPane(self.bottomPanel(), aui.AuiPaneInfo().
                          Name("bottom").Caption("Client Size Reporter")
                          .BestSize(wx.Size(200, 40))
                          .MinSize(wx.Size(200, 40))
                          .MaxSize(wx.Size(200, 40))
                          .Bottom().Position(0).CloseButton(True).MaximizeButton(True).
                          MinimizeButton(True).CaptionVisible(False, left=False))
        
        self._mgr.Update()

    def createPreferenceTree(self):
        prefrencesTreePanel = PrefrencesTreePanel(self)
        return prefrencesTreePanel

    def CreateSizeReportCtrl(self, width=80, height=80):

        ctrl = SizeReportCtrl(self, -1, wx.DefaultPosition, wx.Size(width, height), self._mgr)
        return ctrl
    
    def rightPanel(self):
        ctrl = RightPanel(self, -1, wx.DefaultPosition)
        return ctrl
    
    def bottomPanel(self):
        applyResetButtonPanel = ApplyCloseButtonPanel(self)
        return applyResetButtonPanel


from src.view.preference.general.GeneralPanel import GeneralPreferencePanel
from src.view.preference.general.AppearancePanel import AppearancePreferencePanel
from src.view.preference.calibre.CalibreGeneralPreference import CalibreGeneralPreferencePanel
from src.view.preference.PreferencePanel import PreferencePanel, \
    SearchPanel, KeysPanel


class RightPanel(wx.Panel):

    def __init__(self, parent=None, id=wx.ID_ANY, pos=wx.DefaultPosition,
                size=wx.DefaultSize,):
        wx.Panel.__init__(self, parent, id, pos, size, style=wx.NO_BORDER)
        self.parent = parent
        
        self.vBox = wx.BoxSizer(wx.VERTICAL)
        ####
        
        self.addPanel()
        ####
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.vBox, 0, wx.EXPAND , 1)
        self.SetSizer(self.vBox)

    def addPanel(self, name=None):
        rightPanelItem = self.getPreferencePanelObj(name=name)
        if rightPanelItem:
            self.vBox.Add(rightPanelItem, 1, wx.EXPAND)

#             self.GetChildren().append(rightPanelItem)

    def getPreferencePanelObj(self, name='Preferences'):
        preferencePanelObj = None
        if name == 'General':
            preferencePanelObj = GeneralPreferencePanel(self, name=name)
        elif name == 'Preferences':
            preferencePanelObj = PreferencePanel(self, name=name)
        elif name == 'Appearance':
            preferencePanelObj = AppearancePreferencePanel(self, name=name)
        elif name == 'Search':
            preferencePanelObj = SearchPanel(self, name=name)
        elif name == 'Workspace':
            preferencePanelObj = WorkspacePanel(self, name=name)
        elif name == 'Keys':
            preferencePanelObj = KeysPanel(self, name=name)
        elif name == 'Sharing':
            preferencePanelObj = PreferencePanel(self, name=name)
        elif name == 'Calibre':
            preferencePanelObj = CalibreGeneralPreferencePanel(self, name=name)
#         else :
#             preferencePanelObj = GeneralPreferencePanel(rightPanel, preferenceName=preferenceName)
        
        if preferencePanelObj:
            preferencePanelObj.SetName(name)
            preferencePanelObj.Show(show=True)
        return preferencePanelObj


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


if __name__ == '__main__':
    app = wx.App(0)
#     frame = wx.Frame(None)
    frame = Preference(None, "Preferences", size=(700, 518))
#     panel = GeneralPreferencePanel(frame, preferenceName="")
#     frame.Show(show=True)
    app.MainLoop()
