'''
Created on 24-Apr-2019

@author: vijay
'''
import wx
from src.view.preference.ApplyResetBtnPanel import ApplyResetButtonPanel
from src.dao.workspace.WorkspaceDao import WorkspaceDatasource
from src.logic.WorkspaceUtil import WorkspaceHelper
import wx.lib.filebrowsebutton as filebrowse
import os


class WorkspacePanel(wx.Panel, WorkspaceHelper):

    def __init__(self, parent=None, name='', *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        WorkspaceHelper.__init__(self)
        self.parent = parent
        self.info = wx.InfoBar(self)
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBoxHeader = wx.BoxSizer(wx.VERTICAL)
        vBoxBody = wx.BoxSizer(wx.VERTICAL)
        vBoxFooter = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        '''
        Header section
        '''
        self.st = wx.StaticLine(self, wx.ID_ANY)
        # Make and layout the controls
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs + 4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs + 2, wx.SWISS, wx.NORMAL, wx.NORMAL)

        self.header = wx.StaticText(self, -1, name)
        self.header.SetFont(bf)
        vBoxHeader.Add(self.header, 0, wx.ALL | wx.EXPAND, 5)
        vBoxHeader.Add(self.st, 0, wx.ALL | wx.EXPAND, 5)
        ####################################################################)
        workspacePath = self.getWorkpacePath()
#         self.workspacePathLabel = wx.StaticText(self, -1, "Workspace path:")
        self.workspacePathText = filebrowse.DirBrowseButton(
            self, -1, size=(450, -1), changeCallback=self.dbbCallback, labelText="Workspace path:"
            )
        self.workspacePathText.startDirectory = workspacePath
        self.workspacePathText.SetValue(workspacePath) 
#         self.workspacePathText = wx.TextCtrl(self, -1, self.getWorkpacePath(), size=(150, -1));
        self.workspacePathText.SetHelpText("Workspace Path")
#         self.workspacePathText.SetBackgroundColour("light Gray")
#         self.workspacePathText.SetBackgroundStyle(wx.TE_READONLY)
        
#         bookNameLabel = wx.StaticText(self, -1, "Title:") 
#         bookName = wx.TextCtrl(self, -1, "", size=(150, -1));
#         
#         booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
#         bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

#         authorsLabel = wx.StaticText(self, -1, "Authors:") 
#         authorName = wx.TextCtrl(self, -1, "", size=(50, -1));
#         
#         numberOfPagesLabel = wx.StaticText(self, -1, "Number of pages:") 
#         numberOfPages = wx.TextCtrl(self, -1, "", size=(70, -1));
#         
        
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox1.Add(self.workspacePathLabel , 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hBox1.Add(self.workspacePathText , 0, wx.EXPAND | wx.ALL)
        
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox2.Add(authorsLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox2.Add(authorName, 0, wx.EXPAND | wx.ALL)
        
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)

#         hBox3.Add(booShortkNameLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox3.Add(bookShortName, 0, wx.EXPAND|wx.ALL)
        
        hBox4 = wx.BoxSizer(wx.HORIZONTAL)
#         hBox4.Add(numberOfPagesLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox4.Add(numberOfPages, 0, wx.EXPAND | wx.ALL)
        ####################################################################
        '''
        Footer section
        '''
        self.applyResetButtonPanel = ApplyResetButtonPanel(self)
        vBoxFooter.Add(self.applyResetButtonPanel, 0, wx.EXPAND | wx.ALL, 1)
        
        ####################################################################        
        vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox2, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox3, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox4, 0, wx.EXPAND | wx.ALL, 1)
        vBox.Add(self.info, 0, wx.EXPAND)
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)

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


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = WorkspacePanel(frame, name='Workspace')
    frame.Show()
    app.MainLoop()
