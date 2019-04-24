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
        try:
            self.parent.refreshNode()
        except Exception as e:
            logger.error(e)
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

        selectImport = "Select an import wizard"
#         self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
#         self.filter.SetDescriptiveText(selectImport)
#         self.filter.ShowCancelButton(True)
# #         self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
#         self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
#         self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        selectImportLabel = wx.StaticText(self, -1, selectImport)
#         self.parentFolderCtrl = wx.TextCtrl(self, -1, self.parentFolderText, size=(400, -1))

#         fileLabel = ''
#         if title == 'New File':
#             fileLabel = "File name:"
#         elif title == 'New Folder':
#             fileLabel = "Folder name:"
#         fileNameLabel = wx.StaticText(self, -1, fileLabel)
#         self.fileNameCtrl = wx.TextCtrl(self, -1, self.fileNameText, size=(400, -1) , style=wx.TE_PROCESS_ENTER)
#         self.fileNameCtrl.SetFocus()
#         self.Bind(wx.EVT_TEXT , self.onEnteredText, self.fileNameCtrl)
#         self.Bind(wx.EVT_TEXT_ENTER, self.onEnterButtonPressed, self.fileNameCtrl)

        self.importProjectTreePanel = ImportProjectTreePanel(self)
        self.buttons = CreateButtonPanel(self)
        ####################################################################
#         v1.Add(self.filter, 0, wx.ALL, 2)
#         v1.Add(parentFolderLabel, 0, wx.ALL, 2)
#         v1.Add(self.parentFolderCtrl, 0, wx.ALL, 2)
#         h2.Add(fileNameLabel, 0, wx.ALL, 2)
#         h2.Add(self.fileNameCtrl, 0, wx.ALL, 2)

        ####################################################################

        vBox1 = wx.BoxSizer(wx.VERTICAL)
        vBox1.Add(v1, 0, wx.EXPAND , 0)
        vBox.Add(self.headerPanel, 0, wx.EXPAND, 0)
        vBox.Add(selectImportLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT , 15, 15)
#         vBox.Add(self.filter, 0, wx.EXPAND, 0)
        vBox.Add(vBox1, 0, wx.EXPAND, 0)
        vBox.Add(self.importProjectTreePanel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 15, 15)
#         vBox.Add(h2, 0, wx.EXPAND , 0)
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

#         self.parent = parent
        self.fileOperations = FileOperations()
        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.nextButton = wx.Button(self, -1, "Next >")
        self.Bind(wx.EVT_BUTTON, self.onCancelClicked, self.nextButton)
#         self.nextButton.Disable()

        self.previousButton = wx.Button(self, -1, "< Back")
        self.Bind(wx.EVT_BUTTON, self.onCancelClicked, self.previousButton)
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
        headerText = wx.StaticText(self, -1, title, (20, 10))
        font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        headerText.SetFont(font)
        
        subTitleText = wx.StaticText(self, -1, subTitle, (20, 10))
#         font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTSTYLE_NORMAL)
#         subTitleText.SetFont(font)

        bmp = self.fileOperations.getImageBitmap(imageName=imageName)
        rightsImage = wx.StaticBitmap(self, -1, bmp, (80, 150))
        vBox1 = wx.BoxSizer(wx.VERTICAL)
        vBox1.Add(headerText, 1, wx.EXPAND | wx.LEFT, 10)
        vBox1.Add(subTitleText, 1, wx.EXPAND | wx.LEFT, 15)
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
