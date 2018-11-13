'''
Created on 04-Feb-2017

@author: vijay
'''

import wx.adv
from wx.adv import Wizard
from wx.adv import WizardPage, WizardPageSimple
from src.view.connection.DatabaseNavigation import DatabaseNavigationTree
from src.sqlite_executer.ConnectExecuteSqlite import ManageSqliteDatabase, \
    SQLExecuter
from sqlite3 import OperationalError
from src.view.constants import LOG_SETTINGS
import logging.config
import os

logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)


class TitledPage(WizardPageSimple):

    def __init__(self, parent, title):
        WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        titleText.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0,
                wx.EXPAND | wx.ALL, 5)

        
class SelectDatabaseNamePage(WizardPageSimple):

    def __init__(self, parent, title='Select new connection type'):
        WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs + 4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs + 2, wx.SWISS, wx.NORMAL, wx.NORMAL)
        titleText.SetFont(bf)
        ####################################################################
        '''
        Header section
        '''        
        self.tree = DatabaseNavigationTree(self)
        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter database name")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.RecreateTree()
        
        ####################################################################        
        
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        
    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        try:
            for category, items in self._treeList[1]:
                self.searchItems[category] = []
                for childItem in items:
    #                 if SearchDemo(childItem, value):
                    self.searchItems[category].append(childItem)
        except Exception as e:
            logger.error(e, exc_info=True)
        wx.EndBusyCursor()
        self.RecreateTree()   

    #---------------------------------------------    
    def RecreateTree(self, evt=None):
        # Catch the search type (name or content)
#         searchMenu = self.filter.GetMenu().GetMenuItems()
#         fullSearch = searchMenu[1].IsChecked()
        fullSearch = False   
            
        if evt:
            if fullSearch:
                # Do not`scan all the demo files for every char
                # the user input, use wx.EVT_TEXT_ENTER instead
                return

        expansionState = self.tree.GetExpansionState()

        current = None
        item = self.tree.GetSelection()
        if item:
            prnt = self.tree.GetItemParent(item)
            if prnt:
                current = (self.tree.GetItemText(item),
                           self.tree.GetItemText(prnt))
                    
        self.tree.Freeze()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("Connections")
        self.tree.SetItemImage(self.root, 0)
        self.tree.SetItemData(self.root, 0)

        treeFont = self.tree.GetFont()
        catFont = self.tree.GetFont()

        # The native treectrl on MSW has a bug where it doesn't draw
        # all of the text for an item if the font is larger than the
        # default.  It seems to be clipping the item's label as if it
        # was the size of the same label in the default font.
        if 'wxMSW' not in wx.PlatformInfo:
            treeFont.SetPointSize(treeFont.GetPointSize() + 2)
            
        treeFont.SetWeight(wx.BOLD)
        catFont.SetWeight(wx.BOLD)
#         self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0

        databaseLeaf = self.tree.AppendItem(self.root, 'SQLite', image=16)


class ConncectionSettings(WizardPageSimple):

    def __init__(self, parent, title='define title'):
        WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        
        fs = self.GetFont().GetPointSize()
        bf = wx.Font(fs + 4, wx.SWISS, wx.NORMAL, wx.BOLD)
        nf = wx.Font(fs + 2, wx.SWISS, wx.NORMAL, wx.NORMAL)
        titleText.SetFont(bf)    
        
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        #################################################################### 
        self.panel = wx.Panel(self, -1)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL) 
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        hbox3 = wx.BoxSizer(wx.HORIZONTAL) 
        connectionNameLabel = wx.StaticText(self.panel, -1, "Connection name : ")
        self.connectionNameTextCtrl = wx.TextCtrl(self.panel, size=(300, -1))
        dbFileNameLabel = wx.StaticText(self.panel, -1, "Database File name : ")
        self.dbFileNameTextCtrl = wx.TextCtrl(self.panel, size=(300, -1))
        self.connectionNameTextCtrl.Bind(wx.EVT_TEXT, self.onConnectionName)
        hbox1.Add(connectionNameLabel) 
        hbox1.Add(self.connectionNameTextCtrl, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 1)
        hbox3.Add(dbFileNameLabel) 
        hbox3.Add(self.dbFileNameTextCtrl, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 1) 
        
        import wx.lib.filebrowsebutton as filebrowse
        self.dbb = filebrowse.DirBrowseButton(self.panel, -1, size=(450, -1), changeCallback=self.dbbCallback, startDirectory = wx.GetHomeDir())
        self.dbb.SetValue(wx.GetHomeDir(), self.dbbCallback)
#         self.markFile = brows.FileBrowseButton(self.panel, labelText="File path                  :", fileMode=wx.FD_OPEN, size=(400, 30), toolTip='Type database filename or click browse to choose file')
#         self.markFile.Bind(wx.EVT_TEXT, self.onMarkFile)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.dbb)

        vbox1.Add(hbox1)
        vbox1.Add(hbox2)
        vbox1.Add(hbox3)
        self.panel.SetSizer(vbox1) 
        self.sizer.Add(self.panel, 0, wx.ALL , 5)

        ####################################################################        
    def onConnectionName(self, event):
        logger.debug('onConnectionName')   
        if self.connectionNameTextCtrl.GetValue(): 
            self.GetParent().Children[1].Enable()
            dbFileName=self.connectionNameTextCtrl.GetValue().replace(" ","_")+".sqlite"
            self.dbFileNameTextCtrl.SetValue(dbFileName)
    def dbbCallback(self, evt):
        logger.debug('DirBrowseButton: {}\n'.format( evt.GetString()))
    def onMarkFile(self, event):
        logger.debug('onMarkFile')     


class CreateNewConncetionWixard(wx.Panel):
    
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.wizard = None
        self.pages = []

    def createWizard(self):
        self.wizard = Wizard(None, -1, "Create new connection")
        
        self.wizard.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.onPageChange)
        self.wizard.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.onPageChanging)
        self.wizard.Bind(wx.adv.EVT_WIZARD_CANCEL, self.onCancel)
        self.wizard.Bind(wx.adv.EVT_WIZARD_FINISHED, self.onFinished)
        
        page1 = SelectDatabaseNamePage(self.wizard, "Select new connection type")
        page2 = ConncectionSettings(self.wizard, "Connection settings")
        self.page1=page1
        
#         self.pages.append(page1)
#         self.pages.append(page2)
#         page3 = TitledPage(wizard, "Page 3")
#         page4 = TitledPage(wizard, "Page 4")
#         page1.sizer.Add(wx.StaticText(page1, -1, "Testing the wizard"))
#         page4.sizer.Add(wx.StaticText(page4, -1, "This is the last page."))
#         WizardPageSimple.Chain(page1, page2)
#         WizardPageSimple_Chain(page2, page3)
#         WizardPageSimple_Chain(page3, page4)
        self.wizard.FitToPage(page1)
        # Set the initial order of the pages
        page1.SetNext(page2)
        page2.SetPrev(page1)
        self.wizard.GetPageAreaSizer().Add(page1)
        if self.wizard.RunWizard(page1):
            logger.debug("Success")
            selectedItem = page1.tree.GetSelection()
            logger.debug(page1.tree.GetItemText(selectedItem))
            logger.debug("%s, %s", page2.connectionNameTextCtrl.GetValue(), page2.dbb.GetValue())
#             databasefile = page2.markFile.GetValue() 
            connectionName = page2.connectionNameTextCtrl.GetValue()
            databaseFileName=connectionName.replace(" ","_")+".sqlite"
            databasefile=os.path.join(page2.dbb.GetValue(), databaseFileName)
            self.createNewDatabase(connectionName=connectionName, databaseAbsolutePath=databasefile)
            self.GetTopLevelParent()._mgr.GetPane("databaseNaviagor").window.recreateTree()
        else:
            wx.MessageBox("Create new connection was cancelled", "Create new connection")
    
    def createNewDatabase(self, databaseAbsolutePath=None, connectionName=None):
        try:
            manageSqliteDatabase = ManageSqliteDatabase(databaseAbsolutePath=databaseAbsolutePath, connectionName=connectionName)
            manageSqliteDatabase.createTable()
            sqlExecuter = SQLExecuter()
            obj = sqlExecuter.getObject()
            if len(obj[1]) == 0:
                sqlExecuter.createOpalTables()
            sqlExecuter.addNewConnectionRow(databaseAbsolutePath, connectionName)
        except OperationalError as err:
            logger.error(err, exc_info=True)
            
    def onPageChange(self, event):
        '''Executed after the page has changed.'''
        logger.debug('onPageChange')
        if event.GetDirection():
            dir = "forward"
        else:
            dir = "backward"

        page = event.GetPage()
        logger.debug("OnWizPageChanged: %s, %s\n" % (dir, page.__class__))


    def onPageChanging(self, event):
        '''Executed before the page changes, so we might veto it.'''
        logger.debug('onPageChanging')
        if event.GetDirection():
            dir = "forward"
        else:
            dir = "backward"

        page = event.GetPage()
        logger.debug("OnWizPageChanging: %s, %s\n" % (dir, page.__class__))

    def onCancel(self, event):
        '''Cancel button has been pressed.  Clean up and exit without continuing.''' 
        logger.debug('onCancel')
        page = event.GetPage()
        logger.debug("on_cancel: %s\n", page.__class__)
        self.wizard.Destroy()

#         # Prevent cancelling of the wizard.
#         if page in self.pages:
# #             wx.MessageDialog("Cancelling on the first page has been prevented.", "Sorry")
# #             event.Veto()
#             dlg = wx.MessageDialog(page, 
#                 "Do you really want to close ?",
#                 "Confirm Exit", wx.YES_NO |wx.ICON_QUESTION)
#             result = dlg.ShowModal()
#             if result == wx.ID_YES:
#                 logger.debug( "Yes pressed")
#                 self.wizard.Destroy()
#             else:
#                 logger.debug( "No pressed")
#                 dlg.Destroy()
    def onFinished(self, event):
        logger.debug('onFinished')
        
        wx.GetApp().ExitMainLoop()

               
if __name__ == "__main__":

    app = wx.App()
    CreateNewConncetionWixard().createWizard()
