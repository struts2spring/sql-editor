import wx

import wx.lib.filebrowsebutton as filebrowse
import logging.config
from src.view.constants import TITLE, LOG_SETTINGS
from src.view.worksheet.ResultGrid import ResultDataGrid
import os
from src.view.util.FileOperationsUtil import FileOperations
import ntpath
from src.sqlite_executer.ConnectExecuteSqlite import SQLUtils

logger = logging.getLogger('extensive')
logging.config.dictConfig(LOG_SETTINGS)


class ImportingCsvExcelFrame(wx.Frame):
    
    def __init__(self, parent, title, connectionName):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.connectionName = connectionName
        self.SetMinSize((640, 480))
        sizer = wx.BoxSizer(wx.VERTICAL)        
        self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3DBORDER)
        self.splitter.SetMinimumPaneSize(20)
        
        self.createImportingCsvPanel = CreateImportingCsvPanel(self.splitter)
        self.resultDataGrid = ResultDataGrid(self.splitter)
        self.splitter.SplitHorizontally(self.createImportingCsvPanel, self.resultDataGrid, sashPosition=210)
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
        self.statusbar.SetStatusText("Welcome {}".format(TITLE), 1)

        
class CreateImportingCsvPanel(wx.Panel):
    
    def __init__(self, parent, *args, **kw):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS | wx.SUNKEN_BORDER)
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)  
        
        ####################################################################
        
        self.tableDict = dict()
        self.tableDict['tableName'] = ''        
        vBox1 = wx.BoxSizer(wx.VERTICAL)
        import  wx.lib.rcsizer  as rcs
        sizer = rcs.RowColSizer()
        
        fbbLabel = wx.StaticText(self, -1, "Select CSV / Excel File")
        
        os.chdir(wx.GetHomeDir())
        self.fbb = filebrowse.FileBrowseButton(
            self, -1, size=(450, -1), labelText="", fileMask='CSV (*.csv)|*.csv|Excel (*.xls)|*.xls*|All Files|*.*', changeCallback=self.fbbCallback
            )
        
        tableNameLabel = wx.StaticText(self, -1, "Table Name")
        self.tableNameText = wx.TextCtrl(self, -1, self.tableDict['tableName'], style=wx.TE_PROCESS_ENTER, size=(250, -1))
        self.Bind(wx.EVT_TEXT, self.onChangeTableName, self.tableNameText)
        
        columnNameFirstRowLabel = wx.StaticText(self, -1, "Column Name in first row")
        self.columNameFirstRow = wx.CheckBox(self, -1, "", style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.evtColumNameFirstRowCheckBox, self.columNameFirstRow)

        fieldSeparatorLabel = wx.StaticText(self, -1, "Field Separator")
        self.fieldSeparatorChoice = wx.Choice(self, choices=[",", ";", "Tab", "|", "Other"])
        self.Bind(wx.EVT_CHOICE, self.evtFieldSeparatorChoice, self.fieldSeparatorChoice)
        self.fieldSeparatorChoice.SetSelection(0)

        quoteCharacterLabel = wx.StaticText(self, -1, "Quote Character")
        self.quoteCharacterChoice = wx.Choice(self, choices=['"', "'", " ", "Other"])
        self.Bind(wx.EVT_CHOICE, self.evtQuoteCharacterChoice, self.quoteCharacterChoice)
        self.quoteCharacterChoice.SetSelection(0)

        encodingLabel = wx.StaticText(self, -1, "Encoding")
        self.encodingLabelChoice = wx.Choice(self, choices=["UTF-8", "UTF-16", "ISO-8859-1", "Other"])
        self.Bind(wx.EVT_CHOICE, self.evtEncodingLabelChoice, self.encodingLabelChoice)
        self.encodingLabelChoice.SetSelection(0)

        trimFieldsLabel = wx.StaticText(self, -1, "Trim Fields ?")
        self.trimFieldCheck = wx.CheckBox(self, -1, "", style=wx.ALIGN_RIGHT)
        self.trimFieldCheck.SetValue(1)

        sizer.Add(fbbLabel, flag=wx.EXPAND, row=1, col=1)
        sizer.Add(self.fbb, flag=wx.EXPAND, row=1, col=2)
        sizer.Add(tableNameLabel, flag=wx.EXPAND, row=2, col=1)
        sizer.Add(self.tableNameText, row=2, col=2)
        sizer.Add(columnNameFirstRowLabel, flag=wx.EXPAND, row=3, col=1)
        sizer.Add(self.columNameFirstRow, row=3, col=2)
        sizer.Add(fieldSeparatorLabel, flag=wx.EXPAND, row=4, col=1)
        sizer.Add(self.fieldSeparatorChoice, row=4, col=2)

        sizer.Add(quoteCharacterLabel, flag=wx.EXPAND, row=5, col=1)
        sizer.Add(self.quoteCharacterChoice, row=5, col=2)
        sizer.Add(encodingLabel, flag=wx.EXPAND, row=6, col=1)
        sizer.Add(self.encodingLabelChoice, row=6, col=2)
        sizer.Add(trimFieldsLabel, flag=wx.EXPAND, row=7, col=1)
        sizer.Add(self.trimFieldCheck, row=7, col=2)
#         sizer.Add(self.tableNameText, row=1, col=2)
        
        vBox1.Add(sizer)
        vBox.Add(vBox1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
#         vBox.Add(self.tb, 0, wx.EXPAND)
#         vBox.Add(self.list, 1, wx.EXPAND)
        ####################################################################
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
    def fbbCallback(self, evt):
        logger.info('FileBrowseButton: %s\n' % evt.GetString())
        self.filePath = evt.GetString()
        self.loadingData(filePath=self.filePath, columnNameFirstRow=self.columNameFirstRow.GetValue())
                       
    def onChangeTableName(self, event):
        logger.info('onChangeTableName')
        if self.tableNameText.GetValue() and self.tableNameText.GetValue() != '' :
            pass
#             self.loadingData(filePath=self.filePath, columnNameFirstRow=self.columNameFirstRow.GetValue())
        
    def evtFieldSeparatorChoice(self, event):
        logger.info('EvtFieldSeparatorChoice')
        if self.filePath:
            self.loadingData(filePath=self.filePath, columnNameFirstRow=self.columNameFirstRow.GetValue())

    def evtQuoteCharacterChoice(self, event):
        logger.info('EvtQuoteCharacterChoice')
        if self.filePath:
            self.loadingData(filePath=self.filePath, columnNameFirstRow=self.columNameFirstRow.GetValue())

    def evtEncodingLabelChoice(self, event):
        logger.info('EvtEncodingLabelChoice')
        if self.filePath:
            self.loadingData(filePath=self.filePath, columnNameFirstRow=self.columNameFirstRow.GetValue())
        
    def evtColumNameFirstRowCheckBox(self, event):
        logger.info('EvtCheckBox: %d\n' % event.IsChecked())
        if self.filePath:
            self.loadingData(filePath=self.filePath, columnNameFirstRow=event.IsChecked())

    def loadingData(self, filePath=None, columnNameFirstRow=False, delimiter=",", quotechar='|'):
        head, tail = ntpath.split(filePath)
        tableName = "_".join(tail.split(sep=".")[:-1])
        self.tableNameText.SetValue(tableName)
        fileOperations = FileOperations()
        self.data = fileOperations.readCsvFile(filePath=filePath, columnNameFirstRow=columnNameFirstRow, delimiter=delimiter, quotechar=quotechar)
        self.GetTopLevelParent().resultDataGrid.addData(self.data)

                
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
        print(createTableScript)
        sqlList = fileOperations.sqlScript(tableName=tableName, data=data)
        print(sqlList)
        connectionName = self.GetTopLevelParent().connectionName
        importStatus = SQLUtils().importingData(connectionName=connectionName, sqlList=sqlList)
        dlg = wx.MessageDialog(self, importStatus,
                       'Importing data status',
                       wx.OK | wx.ICON_INFORMATION
                       #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                       )
        dlg.ShowModal()
        dlg.Destroy()
        self.GetTopLevelParent().Destroy()
        
    def onCancelButtonClick(self, event):
        logger.debug('onCancelButtonClick')
        self.GetTopLevelParent().Destroy()

        
if __name__ == '__main__':
    
    app = wx.App(False)
    frame = ImportingCsvExcelFrame(None, 'Import CSV Excel')
    frame.Show()
    app.MainLoop()
