import logging.config
from pathlib import Path
import stat
import time

from src.view.constants import LOG_SETTINGS, ID_NEW_FILE, ID_NEW, \
    keyMap
from src.view.util.FileOperationsUtil import FileOperations
from src.view.util.common.eclutil import Freezer
from src.view.util.osutil import GetWindowsDriveType, RemovableDrive, CDROMDrive
from src.view.views.editor.EditorManager import EditorWindowManager
import wx, os
from wx.lib.pubsub import pub

from src.view.other.imported.project.ImportProjectTree import ImportProjectTreePanel
from src.view.other.imported.project.ImportBody import BodyPanel

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
##################################################


class ImportProjectFrame(wx.Frame):
    '''
    This is for new file and new folder.
    '''

    def __init__(self, parent, title, selectedPath=None, size=(550, 400),
                 style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.SUNKEN_BORDER | wx.STAY_ON_TOP):
        style = style & (~wx.MINIMIZE_BOX)
        self.parent = parent
        wx.Frame.__init__(self, None, -1, title, size=size,
                          style=style)
        self.title = title
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
        self.newFileFrame = NewFilePanel(self, title=title, subTitle='Some Text', selectedPath=selectedPath)
        ####################################################################
        sizer.Add(self.newFileFrame, 1, wx.EXPAND)
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


class NewFilePanel(wx.Panel):

    def __init__(self, parent, *args, title=None, subTitle='', selectedPath=None, **kw):
        wx.Panel.__init__(self, parent, id=-1)
#         self.parent = parent
        self.title = title
        vBox = wx.BoxSizer(wx.VERTICAL)

        v1 = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        ###################################3333333333
        self.headerPanel = HeaderPanel(self, title='Select', subTitle=subTitle, imageName='import_wiz.png')
        self.parentFolderText = selectedPath
        self.fileNameText = ''
#         selectImport = "Select an import wizard"
#         selectImportLabel = wx.StaticText(self, -1, selectImport)
        self.bodyPanel = BodyPanel(self, -1, wx.DefaultPosition)
        pan = self.bodyPanel.addPanel(name="ImportProjectTree")
#         self.bodyPanel.importProjectTreePanel = ImportProjectTreePanel(self.bodyPanel)
        self.buttons = CreateButtonPanel(self)
        ####################################################################
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
#         v1.Add(self.filter, 0, wx.ALL, 2)
#         v1.Add(parentFolderLabel, 0, wx.ALL, 2)
#         v1.Add(self.parentFolderCtrl, 0, wx.ALL, 2)
#         h2.Add(fileNameLabel, 0, wx.ALL, 2)
#         h2.Add(self.fileNameCtrl, 0, wx.ALL, 2)

        ####################################################################

        vBox1 = wx.BoxSizer(wx.VERTICAL)
        vBox1.Add(v1, 0, wx.EXPAND , 0)
        vBox.Add(self.headerPanel, 0, wx.EXPAND, 0)
#         vBox.Add(selectImportLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT , 15, 15)
#         vBox.Add(self.filter, 0, wx.EXPAND, 0)
        vBox.Add(vBox1, 0, wx.EXPAND, 0)
        vBox.Add(self.bodyPanel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15, 15)
#         vBox.Add(h2, 0, wx.EXPAND , 0)
        vBox.Add(line, 0, wx.EXPAND , 0)
        vBox.Add(self.buttons, 0, wx.EXPAND | wx.ALL , 15)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)

    def onEnterButtonPressed(self, event):
        text = event.GetString()
        logger.debug(f'onEnterButtonPressed: {text}')
        self.buttons.onFinishClicked(event)

    def onEnteredText(self, event):
        text = event.GetString()
        logger.debug(f'fileName: {text}')
        if text.strip() != '':
            self.buttons.finishButton.Enable(enable=True)
            self.buttons.finishButton.SetFocus()
            self.fileNameCtrl.SetFocus()

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
        
        # stack for next and previous
        self.stack = list()
#         self.parent = parent
        self.fileOperations = FileOperations()
        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.nextButton = wx.Button(self, -1, "Next >")
        self.Bind(wx.EVT_BUTTON, self.onNextClicked, self.nextButton)
#         self.nextButton.Disable()

        self.previousButton = wx.Button(self, -1, "< Back")
        self.Bind(wx.EVT_BUTTON, self.onPreviousClicked, self.previousButton)
        self.previousButton.Disable()

        self.cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.onCancelClicked, self.cancelButton)
#         self.cancelButton.SetDefault()

        self.finishButton = wx.Button(self, -1, "Finish")
        self.Bind(wx.EVT_BUTTON, self.onFinishClicked, self.finishButton)
        self.finishButton.Disable()

        hbox1.Add(self.previousButton)
        hbox1.Add(self.nextButton)
        hbox1.Add(self.finishButton)
        hbox1.Add(self.cancelButton)

#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)

        sizer.Add(hbox1, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox2, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox3, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
    
    def isPanelPresent(self, name=None):
        p = None
        if name:
            for panel in self.GetParent().bodyPanel.GetChildren():
                if panel.GetName() == name:
                    p = panel
        return p

    def onNextClicked(self, event):
        logger.debug('onNextClicked: ')
        logger.info(self.GetParent().bodyPanel.GetChildren())
        self.GetParent().bodyPanel.GetChildren()
        node = None
        for panel in self.GetParent().bodyPanel.GetChildren():
            if panel.IsShown() and panel.GetName() == 'ImportProjectTree':
                node = panel.selection
            panel.Hide()
        if node:
            pan = self.isPanelPresent(node.name)
            if pan:
                pan.Show()
            else:
                panelObj = self.GetParent().bodyPanel.addPanel(name=node.name)

        if len(self.GetParent().bodyPanel.GetChildren()) > 1:
            self.previousButton.Enable(enable=True)
            self.nextButton.Enable(enable=False)
        self.GetParent().bodyPanel.Layout()
        self.GetParent().bodyPanel.Refresh()
        
    def onPreviousClicked(self, event):
        logger.debug('onPreviousClicked: ')
#         self.GetParent().bodyPanel.RemoveChild(self.GetParent().bodyPanel.GetChildren()[-1])
        self.GetParent().bodyPanel.GetChildren()[-1].Hide()
        self.GetParent().bodyPanel.GetChildren()[-2].Show()
#         self.stack.pop()
#         for panel in self.GetParent().bodyPanel.GetChildren():
#             panel.Hide()

#         if len(self.GetParent().bodyPanel.GetChildren()) == 1:
#             self.previousButton.Enable(enable=False)
        self.previousButton.Enable(enable=False)
        self.nextButton.Enable(enable=True)
        self.GetParent().bodyPanel.Layout()
        self.GetParent().bodyPanel.Refresh()        

    def onCancelClicked(self, event):
        logger.debug('onCancelClicked: ')
        self.GetTopLevelParent().Close()

    def onFinishClicked(self, event):
        logger.debug('onFinishClicked')
        logger.debug(self.GetParent().parentFolderCtrl.GetValue())
        logger.debug(self.GetParent().fileNameCtrl.GetValue())
        try:
            parentDir = self.GetParent().parentFolderCtrl.GetValue()
            fname = self.GetParent().fileNameCtrl.GetValue()
            if self.GetParent().title == 'New File':
                os.makedirs(parentDir, mode=511, exist_ok=True)
                os.chdir(parentDir)
                Path(os.path.join(parentDir, fname)).touch(mode=0o777, exist_ok=True)
            elif self.GetParent().title == 'New Folder':
                os.makedirs(os.path.join(parentDir, fname), mode=511, exist_ok=True)
        except Exception as e:
            logger.error(e)
#         os.makedirs(self.GetParent().parentFolderCtrl.GetValue(), mode=511, exist_ok=False)
        self.GetTopLevelParent().Close()

#     def onReplaceAllClicked(self, event):
#         logger.debug('onReplaceAllClicked')


class HeaderPanel(wx.Panel):

    def __init__(self, parent, *args,
                 title="Python Project",
                 subTitle='',
                 imageName='python-wizban.png',
                 selectedPath=None, **kw):
        wx.Panel.__init__(self, parent, id=-1)

        vBox = wx.BoxSizer(wx.VERTICAL)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetBackgroundColour(wx.WHITE)
        self.fileOperations = FileOperations()
        self.headerText = wx.StaticText(self, -1, title, (20, 10))
        font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.headerText.SetFont(font)

        self.subTitleText = wx.StaticText(self, -1, subTitle, (20, 10))
#         font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTSTYLE_NORMAL)
#         subTitleText.SetFont(font)

        bmp = self.fileOperations.getImageBitmap(imageName=imageName)
        rightsImage = wx.StaticBitmap(self, -1, bmp, (80, 150))
        vBox1 = wx.BoxSizer(wx.VERTICAL)
        vBox1.Add(self.headerText, 1, wx.EXPAND | wx.LEFT, 10)
        vBox1.Add(self.subTitleText, 1, wx.EXPAND | wx.LEFT, 15)
        hBox.Add(vBox1, 1, wx.EXPAND , 0)
        hBox.Add(rightsImage, 0, wx.EXPAND , 0)
        vBox.Add(hBox, 0, wx.EXPAND , 0)
        vBox.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)


if __name__ == '__main__':
    app = wx.App(False)
    frame = ImportProjectFrame(None, 'Import Project', size=(550, 400), selectedPath="c:\work\python-project")
    frame.Show()
    app.MainLoop()
