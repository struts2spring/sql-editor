
from wx import TreeCtrl
from src.view.util.FileOperationsUtil import FileOperations
import logging.config
import wx, os
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
##################################################


class FindAndReplaceFrame(wx.Frame):

    def __init__(self, parent, title, size=(413, 441),
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
        self.findAndReplacePanel = FindAndReplacePanel(self, parent)
        ####################################################################

        sizer.Add(self.findAndReplacePanel, 1, wx.EXPAND)
#         sizer.Add(self.buttonPanel, 0, wx.EXPAND)
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


class FindAndReplacePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        ###################################3333333333
        self.findText = ''
        self.replaceText = ''

        self.buttons = CreateButtonPanel(self)
        findLabel = wx.StaticText(self, -1, "F&ind:               ")
        findText = wx.TextCtrl(self, -1, self.findText, size=(400, -1))

        replaceLabel = wx.StaticText(self, -1, "Replace with:")
        replaceText = wx.TextCtrl(self, -1, self.replaceText, size=(400, -1))
        h1.Add(findLabel, 0, wx.ALL, 2)
        h1.Add(findText, 0, wx.ALL, 2)
        h2.Add(replaceLabel, 0, wx.ALL, 2)
        h2.Add(replaceText, 0, wx.ALL, 2)
        ###################################3333333333

        vBox.Add(h1, 0, wx.EXPAND , 0)
        vBox.Add(h2, 0, wx.EXPAND , 0)
        vBox.Add(self.buttons, 1, wx.EXPAND , 0)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)


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

    def onReplaceClicked(self, event):
        logger.debug('onReplaceClicked')

    def onCloseClicked(self, event):
        logger.debug('onCloseClicked')

    def onReplaceAllClicked(self, event):
        logger.debug('onReplaceAllClicked')

    def onReplaceFindClicked(self, event):
        logger.debug('onReplaceFindClicked')

    def onReplaceAllClicked(self, event):
        logger.debug('onReplaceAllClicked')


if __name__ == '__main__':
    app = wx.App(False)
    frame = FindAndReplaceFrame(None, 'Find/Replace')
    frame.Show()
    app.MainLoop()
