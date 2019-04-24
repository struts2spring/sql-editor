'''
Created on 24-Apr-2019

@author: vijay
'''
import logging.config

from src.view.util.FileOperationsUtil import FileOperations
import wx, os
from wx.lib.pubsub import pub
import  wx.lib.filebrowsebutton as filebrowse
from src.view.preference.general.Workspace import WorkspaceHelper
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
##################################################


class SelectWorkspaceFrame(wx.Frame):
    '''
    This is for select workspace
    '''

    def __init__(self, parent, title, titleHead='', subTitle='', size=(550, 400),
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
        self.newFileFrame = NewFilePanel(self, title=titleHead, subTitle=subTitle)
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


class NewFilePanel(wx.Panel, WorkspaceHelper):

    def __init__(self, parent, *args, title=None, subTitle='', **kw):
        wx.Panel.__init__(self, parent, id=-1) 
        WorkspaceHelper.__init__(self)
        self.info = wx.InfoBar(self)
#         self.parent = parent
        self.title = title
        vBox = wx.BoxSizer(wx.VERTICAL)

        vBoxFooter = wx.BoxSizer(wx.VERTICAL)
        ###################################3333333333
        self.headerPanel = HeaderPanel(self, title=title, subTitle=subTitle, imageName='import_wiz.png')
        startDirectory = self.getWorkpacePath()
        self.dbb = filebrowse.DirBrowseButton(
            self, -1, size=(450, -1), changeCallback=self.dbbCallback, startDirectory=startDirectory,
            dialogTitle=startDirectory,
            labelText="Workspace: "
            )
        self.dbb.SetValue(startDirectory)
        self.buttons = CreateButtonPanel(self)
        ####################################################################
        vBoxFooter.Add(self.buttons, 0, wx.EXPAND, 0)
        vBox.Add(self.headerPanel, 0, wx.EXPAND, 0)
        vBox.Add(self.info, 0, wx.EXPAND)
        vBox.Add(self.dbb, 1, wx.EXPAND, 0)
        vBox.Add(vBoxFooter, 0, wx.EXPAND | wx.ALL , 5)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)

    def OnDismiss(self, evt):
        self.info.Dismiss()

    def dbbCallback(self, evt):
#         print ('DirBrowseButton: %s\n' % evt.GetString())
#         print os.path.isdir(evt.GetString())
        
        if not os.path.isdir(evt.GetString()):
            self.info.ShowMessage('This directory path does not exist. OK will create a new directory path.', wx.ICON_WARNING)
            self.newPath = evt.GetString()
        else:
            self.info.Dismiss()
        if os.path.isdir(evt.GetString()):
            os.chdir(evt.GetString())


class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):

        wx.Panel.__init__(self, parent, id=-1)

#         self.parent = parent
        self.fileOperations = FileOperations()
        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.launchButton = wx.Button(self, -1, "Launch")
        self.Bind(wx.EVT_BUTTON, self.onLaunchClicked, self.launchButton)
        self.launchButton.SetDefault()

        self.cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.onCancelClicked, self.cancelButton)

        hbox1.Add(self.launchButton)
        hbox1.Add(self.cancelButton)

        sizer.Add(hbox1, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox2, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox3, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

    def onCancelClicked(self, event):
        logger.debug('onCancelClicked: ')
        self.GetTopLevelParent().Close()

    def onLaunchClicked(self, event):
        logger.debug('onLaunchClicked')


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
    frame = SelectWorkspaceFrame(None, 'Select Workspace',
                                 size=(550, 200),
                                 titleHead='Select a directory as a workspace',
                                 subTitle='Use the directory to store its preferences and development artifacts',
                                 )
    frame.Show()
    app.MainLoop()
