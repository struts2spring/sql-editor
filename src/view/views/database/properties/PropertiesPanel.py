import wx

import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class PropertiesFrame(wx.Frame):
    
    def __init__(self, parent, title=None, depth=None):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
#         self.connectionName = connectionName
        self.SetMinSize((640, 480))
        sizer = wx.BoxSizer(wx.VERTICAL)        
        self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3DBORDER)
        self.splitter.SetMinimumPaneSize(20)
        
#         self.createImportingCsvPanel = CreateImportingCsvPanel(self.splitter)
#         self.resultDataGrid = ResultDataGrid(self.splitter)
#         self.splitter.SplitHorizontally(self.createImportingCsvPanel, self.resultDataGrid, sashPosition=210)
        logger.info(self.splitter.GetDefaultSashSize())
        ####################################################################
        
#         sizer.Add(self.createImportingCsvPanel, 1, wx.EXPAND)
#         sizer.Add(self.resultDataGrid, 1, wx.EXPAND)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        
        self.SetSizer(sizer)
#         self.creatingToolbar()
        self.Center()
        self.createStatusBar()
        self.Show(True)
    
    def OnCloseFrame(self, event):
        self.Destroy()  
    
    def createStatusBar(self):
        logger.info('createStatusBar')
        self.statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
#         self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
        self.statusbar.SetStatusText("Welcome {}".format(""), 1)


class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
    
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent         
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, 50, "Ok", (20, 220))
        okButton.SetToolTip("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onOkClick, okButton)
        
        cancelButton = wx.Button(self, 51, "Cancel", (20, 220))
        cancelButton.SetToolTip("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, cancelButton)

#         b.SetBitmap(images.Mondrian.Bitmap,
#                     wx.LEFT    # Left is the default, the image can be on the other sides too
#                     #wx.RIGHT
#                     #wx.TOP
#                     #wx.BOTTOM
#                     )
        hbox.Add(okButton)    
        hbox.Add(cancelButton)    
#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        
    def onOkClick(self, event):
        logger.debug('onOkClick')
        data = self.GetTopLevelParent().createImportingCsvPanel.data
        tableName = self.GetTopLevelParent().createImportingCsvPanel.tableNameText.GetValue()
        fileOperations = FileOperations()
#         data = fileOperations.readCsvFile(filePath=filePath, columnNameFirstRow=True, delimiter=",", quotechar='|')
#         print(len(data))    
#         print(data)
        createTableScript = fileOperations.createTableScript(tableName=tableName, columnHeader=data[0])
        logger.debug(createTableScript)
        sqlList = fileOperations.sqlScript(tableName=tableName, data=data)
        logger.debug(sqlList)
        connectionName = self.GetTopLevelParent().connectionName
        importStatus = SQLUtils().importingData(connectionName=connectionName, sqlList=sqlList)
        dlg = wx.MessageDialog(self, importStatus,
                       'Importing data status',
                       wx.OK | wx.ICON_INFORMATION
                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                       )
        dlg.ShowModal()
        dlg.Destroy()
        self.GetTopLevelParent().Destroy()
        
    def onCancelButtonClick(self, event):
        logger.debug('onCancelButtonClick')
        self.GetTopLevelParent().Destroy()


class CreatePropertiesPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent

        self.process = None
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        # We can either derive from wx.Process and override OnTerminate
        # or we can let wx.Process send this window an event that is
        # caught in the normal way...
        self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)

        # Make the controls
        prompt = wx.StaticText(self, -1, 'Command line:')
        print()
        cmd = ''
        if wx.PlatformInformation.Get().GetOperatingSystemIdName() in ['Linux', 'Unix', 'OS/2']:
            cmd = 'bash'
        elif wx.PlatformInformation.Get().GetOperatingSystemIdName() in ['DOS', 'Windows']:
            cmd = 'cmd'
        
        self.cmd = wx.TextCtrl(self, -1, cmd)
        self.exBtn = wx.Button(self, -1, 'Execute')

        self.out = wx.TextCtrl(self, -1, '',
                               style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)

        self.inp = wx.TextCtrl(self, -1, '', style=wx.TE_PROCESS_ENTER)
        self.sndBtn = wx.Button(self, -1, 'Send')
        self.termBtn = wx.Button(self, -1, 'Close Stream')
        self.inp.Enable(False)
        self.sndBtn.Enable(False)
        self.termBtn.Enable(False)

        # Hook up the events
        self.Bind(wx.EVT_BUTTON, self.OnExecuteBtn, self.exBtn)
        self.Bind(wx.EVT_BUTTON, self.OnSendText, self.sndBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCloseStream, self.termBtn)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSendText, self.inp)

        # Do the layout
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(prompt, 0, wx.ALIGN_CENTER)
        box1.Add(self.cmd, 1, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        box1.Add(self.exBtn, 0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(self.inp, 1, wx.ALIGN_CENTER)
        box2.Add(self.sndBtn, 0, wx.LEFT, 5)
        box2.Add(self.termBtn, 0, wx.LEFT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box1, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.out, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(box2, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnExecuteBtn(self, evt):
        cmd = self.cmd.GetValue()

        self.process = wx.Process(self)
        self.process.Redirect()
        pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
        logger.debug('OnExecuteBtn: "%s" pid: %s\n' % (cmd, pid))

        self.inp.Enable(True)
        self.sndBtn.Enable(True)
        self.termBtn.Enable(True)
        self.cmd.Enable(False)
        self.exBtn.Enable(False)
        self.inp.SetFocus()

    def OnSendText(self, evt):
        text = self.inp.GetValue()
        self.inp.SetValue('')
        logger.debug('OnSendText: "%s"\n' % text)
        text += '\n'
        self.process.GetOutputStream().write(text.encode('utf-8'))

        self.inp.SetFocus()

    def OnCloseStream(self, evt):
        logger.debug('OnCloseStream\n')
        # print("b4 CloseOutput")
        self.process.CloseOutput()
        # print("after CloseOutput")

    def OnIdle(self, evt):
        if self.process is not None:
            stream = self.process.GetInputStream()

            if stream.CanRead():
                text = stream.read()
                self.out.AppendText(text)

    def OnProcessEnded(self, evt):
        logger.debug('OnProcessEnded, pid:%s,  exitCode: %s\n' % 
                       (evt.GetPid(), evt.GetExitCode()))

        stream = self.process.GetInputStream()

        if stream.CanRead():
            text = stream.read()
            self.out.AppendText(text)

        self.process.Destroy()
        self.process = None
        self.inp.Enable(False)
        self.sndBtn.Enable(False)
        self.termBtn.Enable(False)
        self.cmd.Enable(True)
        self.exBtn.Enable(True)

    def ShutdownDemo(self):
        # Called when the demo application is switching to a new sample. Tell
        # the process to close (by closign its output stream) and then wait
        # for the termination signals to be received and processed.
        if self.process is not None:
            self.process.CloseOutput()
            wx.MilliSleep(250)
            wx.Yield()
            self.process = None

#----------------------------------------------------------------------


overview = """\
<html><body>
<h2>wx.Process</h2>

wx.Process lets you get notified when an asyncronous child process
started by wxExecute terminates, and also to get input/output streams
for the child process's stdout, stderr and stdin.

<p>
This demo launches a simple python script that echos back on stdout
lines that it reads from stdin.  You can send text to the echo
process' stdin by typing in the lower textctrl and clicking Send.

<p>
Clicking the Close Stream button will close the demo's end of the
stdin pipe to the child process.  In our case that will cause the
child process to exit its main loop.

</body><html>
"""

if __name__ == '__main__':
#     app = wx.App(False)
#     frame = wx.Frame(None)
#     panel = CreatePropertiesPanel(frame)
#     frame.Show()
#     app.MainLoop()
    app = wx.App(False)
    frame = PropertiesFrame(None, 'Table properties')
    frame.Show()
    app.MainLoop()
