import wx
import os

import wx.lib.filebrowsebutton as filebrowse
import logging.config
from src.view.constants import TITLE, LOG_SETTINGS
from src.view.util.FileOperationsUtil import FileOperations
import ntpath
from src.sqlite_executer.ConnectExecuteSqlite import SQLUtils, SQLExecuter

logger = logging.getLogger('extensive')
logging.config.dictConfig(LOG_SETTINGS)


class OpenExistingConnectionFrame(wx.Dialog):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(500, 200),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.SetMinSize((400, 100))
        sizer = wx.BoxSizer(wx.VERTICAL)        
        self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        
        
        self.CreateOpenConnectionPanel = CreateOpenConnectionPanel(self)
        ####################################################################
        
        sizer.Add(self.CreateOpenConnectionPanel, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        
        self.SetSizer(sizer)
        self.Center()
#         self.createStatusBar()
        self.Show(True)
    
    def OnCloseFrame(self, event):
        self.Destroy()  
    
    def createStatusBar(self):
        logger.info('createStatusBar')
        self.statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Welcome {}".format(TITLE), 1)

        
class CreateOpenConnectionPanel(wx.Panel):
    
    def __init__(self, parent, *args, **kw):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS | wx.SUNKEN_BORDER)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)  
        
        ####################################################################
        
        vBox1 = wx.BoxSizer(wx.VERTICAL)
        import  wx.lib.rcsizer  as rcs
        sizer = rcs.RowColSizer()
        
        fbbLabel = wx.StaticText(self, -1, "Database File")
        
        os.chdir(wx.GetHomeDir())
        self.fbb = filebrowse.FileBrowseButton(
            self, -1, size=(350, -1), labelText="", fileMask='sqlite (*.sqlite)|*.sqlite|Database (*.db)|*.db*|All Files|*.*', changeCallback=self.fbbCallback
            )
        
        connectionNameLabel = wx.StaticText(self, -1, "Connection Name    ")
        self.connectionNameText = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER, size=(250, -1))
        self.Bind(wx.EVT_TEXT, self.onChangeConnectionName, self.connectionNameText)
        

        sizer.Add(fbbLabel, flag=wx.EXPAND, row=1, col=1)
        sizer.Add(self.fbb, flag=wx.EXPAND, row=1, col=2)
        sizer.Add(connectionNameLabel, flag=wx.EXPAND, row=2, col=1)
        sizer.Add(self.connectionNameText, row=2, col=2)
        
        vBox1.Add(sizer)
        vBox.Add(vBox1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
    def fbbCallback(self, evt):
        logger.info('FileBrowseButton: %s\n' % evt.GetString())
        self.filePath = evt.GetString()
        self.setConnectionName(filePath=self.filePath)
        sqlExecuter=SQLExecuter()
        obj=sqlExecuter.getObject()
        if len(obj[1])==0:
            sqlExecuter.createOpalTables()
        sqlExecuter.addNewConnectionRow(self.filePath, self.connectionNameText.GetValue())
                       
    def onChangeConnectionName(self, event):
        logger.info('onChangeConnectionName')
        if self.connectionNameText.GetValue() and self.connectionNameText.GetValue() != '' :
            pass
#             self.loadingData(filePath=self.filePath, columnNameFirstRow=self.columNameFirstRow.GetValue())
        


    def setConnectionName(self, filePath=None):
        head, tail = ntpath.split(filePath)
        connectionName = "_".join(tail.split(sep=".")[:-1])
        self.connectionNameText.SetValue(connectionName)
        
#         fileOperations = FileOperations()
#         self.data = fileOperations.readCsvFile(filePath=filePath, columnNameFirstRow=columnNameFirstRow, delimiter=delimiter, quotechar=quotechar)
#         self.GetTopLevelParent().resultDataGrid.addData(self.data)

                
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
#         data = self.GetTopLevelParent().createImportingCsvPanel.data
#         tableName = self.GetTopLevelParent().createImportingCsvPanel.tableNameText.GetValue()
#         fileOperations = FileOperations()
# #         data = fileOperations.readCsvFile(filePath=filePath, columnNameFirstRow=True, delimiter=",", quotechar='|')
# #         print(len(data))    
# #         print(data)
#         createTableScript = fileOperations.createTableScript(tableName=tableName, columnHeader=data[0])
#         print(createTableScript)
#         sqlList = fileOperations.sqlScript(tableName=tableName, data=data)
#         print(sqlList)
#         connectionName = self.GetTopLevelParent().connectionName
#         importStatus = SQLUtils().importingData(connectionName=connectionName, sqlList=sqlList)
#         dlg = wx.MessageDialog(self, "Some status",
#                        'Importing data status',
#                        wx.OK | wx.ICON_INFORMATION
#                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
#                        )
#         dlg.ShowModal()
#         dlg.Destroy()
        self.GetTopLevelParent().Destroy()
        
    def onCancelButtonClick(self, event):
        logger.debug('onCancelButtonClick')
        self.GetTopLevelParent().Destroy()

        
if __name__ == '__main__':
    
    app = wx.App(False)
    frame = OpenExistingConnectionFrame(None, 'Open Existing Connection')
    frame.Show()
    app.MainLoop()
