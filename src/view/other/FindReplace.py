
from wx import TreeCtrl
from src.view.util.FileOperationsUtil import FileOperations
import logging.config
import wx, os
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
##################################################


class FindAndReplaceFrame(wx.Frame):

    def __init__(self, parent, title, size=(350, 420),
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
#         self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        self.findAndReplacePanel = FindAndReplacePanel(self)
        ####################################################################

        sizer.Add(self.findAndReplacePanel, 1, wx.EXPAND)
#         sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)
        self.SetSizer(sizer)
        self.Center()
#         self.createStatusBar()ut527
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


class FindAndReplacePanel(wx.Panel):

    def __init__(self, parent, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        h3 = wx.BoxSizer(wx.HORIZONTAL)
        ###################################3333333333
        self.findText = ''
        self.replaceText = ''

        self.buttons = CreateButtonPanel(self)
        findLabel = wx.StaticText(self, -1, "F&ind:               ")
        self.findTextCtrl = wx.TextCtrl(self, -1, self.findText, size=(400, -1))
        self.findTextCtrl.SetFocus()
        self.setFindText(self.findTextCtrl)

        replaceLabel = wx.StaticText(self, -1, "Replace with:")
        self.replaceTextCtrl = wx.TextCtrl(self, -1, self.replaceText, size=(400, -1))
        h1.Add(findLabel, 0, wx.ALL, 2)
        h1.Add(self.findTextCtrl, 0, wx.ALL, 2)
        h2.Add(replaceLabel, 0, wx.ALL, 2)
        h2.Add(self.replaceTextCtrl, 0, wx.ALL, 2)
        ###################################3333333333
        ########################## Scope ##########################################
        self.directionRadioBox = wx.RadioBox(self, -1, "Direction", (10, 10), wx.DefaultSize, ['Forward', 'Backword'], 1, wx.RA_SPECIFY_COLS)
        self.scopeRadioBox = wx.RadioBox(self, -1, "Scope", (10, 10), wx.DefaultSize, ['All', 'Selected lines'], 1, wx.RA_SPECIFY_COLS)
        h3.Add(self.directionRadioBox, 1, wx.EXPAND | wx.ALL, 3)
        h3.Add(self.scopeRadioBox, 1, wx.EXPAND | wx.ALL, 3)

        ####################################################################
        ######################## Options checkboxes ############################################
        # first the static box
        box_10 = wx.StaticBox(self, -1, 'Options')
        self.cb1 = wx.CheckBox(box_10, -1, "Case sensitive")
        self.cb2 = wx.CheckBox(box_10, -1, "Whole word")
        self.cb3 = wx.CheckBox(box_10, -1, "Regular expressions")
        self.cb4 = wx.CheckBox(box_10, -1, "Wra&p search")
        self.cb5 = wx.CheckBox(box_10, -1, "&Incremental")
        # then the sizer
        staticBoxSizer_11 = wx.StaticBoxSizer(box_10, wx.VERTICAL)
        vb1 = wx.BoxSizer(wx.VERTICAL)
        vb1.Add(self.cb1, 0, wx.EXPAND | wx.ALL, 0)
        vb1.Add(self.cb2, 0, wx.EXPAND | wx.ALL, 0)
        vb1.Add(self.cb3, 0, wx.EXPAND | wx.ALL, 0)
        vb2 = wx.BoxSizer(wx.VERTICAL)
        vb2.Add(self.cb4, 0, wx.EXPAND | wx.ALL, 0)
        vb2.Add(self.cb5, 0, wx.EXPAND | wx.ALL, 0)
        hb = wx.BoxSizer(wx.HORIZONTAL)
        hb.Add(vb1, 0, wx.EXPAND | wx.ALL, 0)
        hb.Add(vb2, 0, wx.EXPAND | wx.ALL, 0)
#         rowColumnSizer1 = rcs.RowColSizer()
#         rowColumnSizer1.Add(cb1, row=1, col=1)
#         rowColumnSizer1.Add(cb2, row=2, col=1)
#         rowColumnSizer1.Add(cb3, row=3, col=1)
# #         rowColumnSizer1.Add( (2,2),row=1, col=2)
#         rowColumnSizer1.Add(cb4, row=1, col=2)
#         rowColumnSizer1.Add(cb5, row=2, col=2)
        staticBoxSizer_11.Add(hb)
        ####################################################################
        self.Bind(wx.EVT_CHECKBOX, self.onChecked)
        vBox1 = wx.BoxSizer(wx.VERTICAL)
        vBox1.Add(h1, 0, wx.EXPAND , 0)
        vBox1.Add(h2, 0, wx.EXPAND , 0)
        vBox1.Add(h3, 0, wx.EXPAND , 0)
        vBox1.Add(staticBoxSizer_11, 0, wx.EXPAND , 0)
#         scope_box.Add(hb1, 0, wx.EXPAND | wx.ALL, 0)
#         scope_box.Add(hb2, 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(scope_box, 0, wx.EXPAND | wx.ALL, 5)
        vBox.Add(vBox1, 1, wx.EXPAND, 0)
#         vBox1.Add(self.buttons, 0, wx.EXPAND, 0)
        vBox.Add(self.buttons, 0, wx.EXPAND , 0)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)

    def onChecked(self, event):
        logger.debug('onChecked')
        cb = event.GetEventObject()
        logger.debug(f'{cb.GetLabel()}, is clicked, {cb.GetValue()}')

    def setFindText(self, findText):
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                self.findTextCtrl.SetValue(do.GetText())

    def onChooseBtn(self):
        logger.debug('onChooseBtn')


class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):

        wx.Panel.__init__(self, parent, id=-1)

        self.parent = parent
        self.fileOperations = FileOperations()
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.findButton = wx.Button(self, -1, "Find")
        self.Bind(wx.EVT_BUTTON, self.onFindClicked, self.findButton)
        self.findButton.SetDefault()

        self.replaceButton = wx.Button(self, -1, "Replace")
        self.Bind(wx.EVT_BUTTON, self.onReplaceClicked, self.replaceButton)

        self.replaceAllButton = wx.Button(self, -1, "Replace All")
        self.Bind(wx.EVT_BUTTON, self.onReplaceAllClicked, self.replaceAllButton)
        self.closeButton = wx.Button(self, -1, "Close")
        self.Bind(wx.EVT_BUTTON, self.onCloseClicked, self.closeButton)

        self.replaceFindButton = wx.Button(self, -1, "Replace/Fin&d")
        self.Bind(wx.EVT_BUTTON, self.onReplaceFindClicked, self.replaceFindButton)

        hbox1.Add(self.findButton)
        hbox1.Add(self.replaceFindButton)
        hbox2.Add(self.replaceButton)
        hbox2.Add(self.replaceAllButton)
        hbox3.Add(self.closeButton)
#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox1, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox2, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox3, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

    def onFindClicked(self, event):
        logger.debug('onFindClicked: ')
        searchText = self.GetParent().findTextCtrl.GetValue()
        logger.debug(self.GetParent().directionRadioBox.GetSelection())
        mainStc = self.GetTopLevelParent().Parent
        back = False
        if self.GetParent().directionRadioBox.GetSelection():
            back = True

        regex = False
        try:
            if self.GetParent.cb3.GetValue():
                logger.debug(f'{self.GetParent.cb3.GetLabel()} : {self.GetParent().cb3.GetValue()}')
                regex = True
        except:
            pass
        logger.debug(self.GetParent().findTextCtrl.GetValue())
        res = mainStc.SearchText(self.GetParent().findTextCtrl.GetValue(), regex=regex, back=back)
        if res != -1:
#             mainStc.SetCurrentPos(res + len(searchText))
#             mainStc.SetSelection(res, res + len(searchText))
#             mainStc.SetSelectionEnd(res + len(searchText))
            mainStc.SetSelectionNCaret(res,res + len(searchText))
#             mainStc.GotoPos(res + len(searchText))

    def onReplaceClicked(self, event):
        logger.debug('onReplaceClicked')

    def onCloseClicked(self, event):
        logger.debug('onCloseClicked')
        self.GetTopLevelParent().Close()

    def onReplaceAllClicked(self, event):
        logger.debug('onReplaceAllClicked')

    def onReplaceFindClicked(self, event):
        logger.debug('onReplaceFindClicked')

#     def onReplaceAllClicked(self, event):
#         logger.debug('onReplaceAllClicked')


if __name__ == '__main__':
    app = wx.App(False)
    frame = FindAndReplaceFrame(None, 'Find/Replace')
    frame.Show()
    app.MainLoop()
