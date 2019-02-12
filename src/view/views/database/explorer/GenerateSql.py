'''
Created on Feb 11, 2019

@author: xbbntni
'''

import wx
import wx.stc as stc
from src.view.views.console.worksheet.EditorPanel import SqlStyleTextCtrl
import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class GenerateSqlPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        self.findData = wx.FindReplaceData()
        ####################################################################
        self.sstc = SqlStyleTextCtrl(self, -1)
        self.sstc.initKeyShortCut()
        self.sstc.SetText(kw['sqlText'])
        self.sstc.EmptyUndoBuffer()
        self.sstc.Colourise(0, -1)
        self.sstc.SetInitialSize(wx.Size(400, 400))
#         self.sstc.SetBestFittingSize(wx.Size(400, 400))

        # line numbers in the margin
        self.sstc.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.sstc.SetMarginWidth(1, 25)
        ####################################################################
        vBox.Add(self.sstc , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


class GenerateSqlFrame(wx.Frame):

    def __init__(self, parent, title, size=(313, 441), sqlText='asfd', style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT):
        wx.Frame.__init__(self, parent, -1, title, size=size,
                          style=style)
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.SetMinSize((100, 100))
        sizer = wx.BoxSizer(wx.VERTICAL)        
        self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        
        self.generateSqlPanel = GenerateSqlPanel(self, sqlText=sqlText)
        ####################################################################
        
        sizer.Add(self.generateSqlPanel, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Center()
#         self.createStatusBar()
        self.Show(True)
#         self.Bind(wx.EVT_SIZE, self.OnSize)
    
    def OnCloseFrame(self, event):
        self.Destroy()  

    def OnSize(self, event):
        hsize = event.GetSize()
        logger.debug(hsize)


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
        sizer.Add(hbox, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        
    def onOkClick(self, event):
        logger.debug('onOkClick')
        # TODO : need to implement
#         sqlExecuter=SQLExecuter()
#         obj=sqlExecuter.getObject()
#         if len(obj[1])==0:
#             sqlExecuter.createOpalTables()
#         sqlExecuter.addNewConnectionRow(self.GetParent().CreateOpenConnectionPanel.filePath, self.GetParent().CreateOpenConnectionPanel.connectionNameText.GetValue())
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
    frame = GenerateSqlFrame(None, 'Generate Sql', sqlText='asfd')
    frame.Show()
    app.MainLoop()
