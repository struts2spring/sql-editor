import wx

import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.util.FileOperationsUtil import FileOperations
from wx.lib.mixins.treemixin import ExpansionState
from wx import TreeCtrl
from src.view.views.database.properties.ApplyResetBtnPanel import ApplyResetButtonPanel

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

propertiesDataList = [
    [wx.NewIdRef(), "Resource", 'folderType_filter.png', None, None]
    ]


class PropertiesFrame(wx.Frame):
    
    def __init__(self, parent, title=None, size=(970, 720), depth=None):
        wx.Frame.__init__(self, parent, -1, title, size=size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.fileOperations = FileOperations()
        icon = wx.Icon()
        icon.CopyFromBitmap(self.fileOperations.getImageBitmap(imageName='eclipse16.png'))
        self.SetIcon(icon)
#         self.connectionName = connectionName
        self.SetMinSize((640, 480))
        ####################################################################
        '''
        Footer section
        '''
        vBox = wx.BoxSizer(wx.VERTICAL)        
        self.buttonPanel = CreateButtonPanel(self)
        ####################################################################
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3DBORDER)
        self.splitter.SetMinimumPaneSize(20)
        
        self.createLeftPropertiesTreePanel = CreateLeftPropertiesTreePanel(self.splitter)
        self.rightPanel = RightPanel(self.splitter, name='Resource')
#         self.resultDataGrid = ResultDataGrid(self.splitter)
        self.splitter.SplitVertically(self.createLeftPropertiesTreePanel, self.rightPanel, sashPosition=210)
        logger.info(self.splitter.GetDefaultSashSize())
        ####################################################################
        
#         sizer.Add(self.createImportingCsvPanel, 1, wx.EXPAND)
#         sizer.Add(self.resultDataGrid, 1, wx.EXPAND)
        vBox.Add(self.splitter, 1, wx.EXPAND | wx.ALL)
        vBox.Add(self.buttonPanel, 0, wx.EXPAND | wx.ALL)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)   
        self.SetSizer(sizer)
#         self.creatingToolbar()
        self.Center()
        self.BindEvents()
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
#         self.createStatusBar()
        self.Show(True)

    def OnKeyUP(self, event):
        logger.info("KEY UP!")
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip() 

    def OnCloseFrame(self, event):
        self.Destroy()

    def OnSize(self, event):
        hsize = event.GetSize()
        logger.debug(hsize)
        
    def BindEvents(self):
#         self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)
        
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
        applyCloseButton = wx.Button(self, 50, "Apply and Close", (20, 220))
        applyCloseButton.SetToolTip("Apply and close.")
        self.Bind(wx.EVT_BUTTON, self.onApplyCloseClick, applyCloseButton)
        
        cancelButton = wx.Button(self, 51, "Cancel", (20, 220))
        cancelButton.SetToolTip("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, cancelButton)

#         b.SetBitmap(images.Mondrian.Bitmap,
#                     wx.LEFT    # Left is the default, the image can be on the other sides too
#                     #wx.RIGHT
#                     #wx.TOP
#                     #wx.BOTTOM
#                     )
        hbox.Add(applyCloseButton, 0, wx.EXPAND | wx.ALL, 1)    
        hbox.Add(cancelButton, 0, wx.EXPAND | wx.ALL, 1)    
#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox, 1, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        
    def onApplyCloseClick(self, event):
        logger.debug('onApplyCloseClick')
        data = self.GetTopLevelParent().createImportingCsvPanel.data
        tableName = self.GetTopLevelParent().createImportingCsvPanel.tableNameText.GetValue()
        fileOperations = FileOperations()
#         data = fileOperations.readCsvFile(filePath=filePath, columnNameFirstRow=True, delimiter=",", quotechar='|')
#         logger.info(len(data))    
#         logger.info(data)
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


class CreateLeftPropertiesTreePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
#         self.fileOperations = FileOperations()
        self.connDict = dict()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.treeMap = {}
        self.tree = PropertiesBaseTreePanel(self)
        
        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter search text")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
#         self.tree.SelectItem(self.root)
        
        searchMenu = wx.Menu()
        item = searchMenu.AppendRadioItem(-1, "Full search")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        item = searchMenu.AppendRadioItem(-1, "Sample Content")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        self.filter.SetMenu(searchMenu)
        self.RecreateTree()
        ####################################################################
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND | wx.ALL , 0)
        
        self.SetSizer(sizer)

    def OnSearchMenu(self, event):

        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        fullSearch = searchMenu[1].IsChecked()
        
        if fullSearch:
            self.OnSearch()
        else:
            self.RecreateTree()        

    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.RecreateTree()
            return

        wx.BeginBusyCursor()
        
#         for category, items in _treeList:
#             self.searchItems[category] = []
#             for childItem in items:
# #                 if SearchDemo(childItem, value):
#                 self.searchItems[category].append(childItem)

        wx.EndBusyCursor()
        self.RecreateTree()   

    #---------------------------------------------    
    def constructNode(self, parent=None, treeData=None):
        logger.debug(treeData)
        for treeItem in treeData:
            itemId = self.tree.AppendItem(parent, treeItem.name, image=self.tree.iconsDictIndex[treeItem.imageName])
            self.tree.SetItemData(itemId, treeItem)
            if treeItem.child:
#                     for childItem in treeItem.child:
                self.constructNode(parent=itemId, treeData=treeItem.child)

    def RecreateTree(self, evt=None):
        searchMenu = self.filter.GetMenu().GetMenuItems()
        fullSearch = searchMenu[1].IsChecked()
            
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
        self.root = self.tree.AddRoot("Properties")
        self.tree.SetItemImage(self.root, self.tree.iconsDictIndex['preference.png'])
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
        self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0
        treeSearch = TreeSearch()
        searchText = self.filter.GetValue()
        if searchText.strip() == '':
            searchText = None
        treeItems = treeSearch.searchedNodes(dataList=propertiesDataList, searchText=searchText)

        self.constructNode(parent=self.root, treeData=treeItems)
                    
        self.tree.Expand(self.root)
        if firstChild:
            self.tree.Expand(firstChild)
        if filter:
            self.tree.ExpandAll()
        elif expansionState:
            self.tree.SetExpansionState(expansionState)
        if selectItem:
            self.skipLoad = True
            self.tree.SelectItem(selectItem)
            self.skipLoad = False
        
        self.tree.Thaw()
        self.searchItems = {}

    #---------------------------------------------
    def OnItemExpanded(self, event):
        item = event.GetItem()
        logger.debug("OnItemExpanded: %s" , self.tree.GetItemText(item))
        if self.tree.GetItemParent(item):
            self.tree.SetItemImage(item, self.tree.iconsDictIndex['folder_view.png'])
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
        logger.debug("OnItemCollapsed: %s", self.tree.GetItemText(item))
        if self.tree.GetItemParent(item):
            self.tree.SetItemImage(item, self.tree.iconsDictIndex['folder.png'])
        event.Skip()

    #---------------------------------------------
    def OnTreeLeftDown(self, event):
        logger.debug('OnTreeLeftDown')
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item and item == self.tree.GetSelection():
            logger.debug(self.tree.GetItemText(item) + " Overview")
        event.Skip()

    #---------------------------------------------
    def OnSelectionChanged(self, event):
#         if self.dying or not self.loaded or self.skipLoad:
#             return

#         self.StopDownload()

        item = event.GetItem()
        itemText = self.tree.GetItemText(item)
        logger.debug(itemText)
        centerPane = self.GetTopLevelParent()._mgr.GetPane("center")
        if centerPane:
            logger.debug('centerPane')
            rightPanelItem = None   
            avalialbe = False
            for panel in centerPane.window.GetChildren():
                logger.debug(f'{panel.GetId()}: {panel.GetName()} ')
                if panel.GetName() == itemText:
                    rightPanelItem = panel
                    rightPanelItem.Show(show=True)
                    avalialbe = True
                else:
                    panel.Hide()
                    
            if not avalialbe:
                centerPane.window.addPanel(name=itemText)
            centerPane.window.Layout()
            centerPane.window.Refresh()
            

class PropertiesBaseTreePanel(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in preferences page
    '''

    def __init__(self, parent):
         
        TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.BORDER_NONE)
        
        self._il = None
        self.BuildTreeImageList()
        
#         if USE_CUSTOMTREECTRL:
#             self.SetSpacing(10)
#             self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)

        self.SetInitialSize((100, 80))
            
    def AppendItem(self, parent, text, image=-1, wnd=None):

        item = TreeCtrl.AppendItem(self, parent, text, image=image)
        return item
            
    def BuildTreeImageList(self):
#         imgList = wx.ImageList(16, 16)
# 
#         for png in _demoPngs:
#             imgList.Add(catalog[png].GetBitmap())
#             
#         # add the image for modified demos.
#         imgList.Add(catalog["custom"].GetBitmap())
# 
#         self.AssignImageList(imgList)
        if self._il:
            self._il.Destroy()
            self._il = None
        self._il = wx.ImageList(16, 16)
        self.SetImageList(self._il)
        
        self.ImageList.RemoveAll()
        self.iconsDictIndex = {}
        count = 0
        self.fileOperations = FileOperations()
        for imageName in ['preference.png', 'folder.png', 'folder_view.png', 'fileType_filter.png', 'usb.png', 'stop.png',
                          'java.png', 'python_module.png', 'xml.png', 'folderType_filter.png']:
            self.ImageList.Add(self.fileOperations.getImageBitmap(imageName=imageName))
            self.iconsDictIndex[imageName] = count
            count += 1

    def GetItemIdentity(self, item):
        return self.GetItemData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(PropertiesBaseTreePanel, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(PropertiesBaseTreePanel, self).Thaw()


class TreeSearch():

    def __init__(self):
        self.treeData = []
        self.traverse = []

    def searchedNodes(self, dataList=None, searchText=None):
        treeData = []
        for data in dataList:
            logger.info(data)
            node = self.getNode(data, searchText=searchText)
#             if searchText == None:
            if node:
                treeData.append(node)
#             else:
#                 for treeLabel in flatTreeLabelList :
#                     if searchText and re.search(searchText, treeLabel, re.I):
#                         treeData.append(node)
#                         break
                    
        return treeData

    def isSearchMatch(self, text, searchText):
        searchMatch = False
        if searchText == None:
            searchMatch = True
        elif searchText and re.search(searchText, text, re.I):
            searchMatch = True
        else:
            searchMatch = False
        return searchMatch
    
    def getNode(self, data, searchText=None):
        logger.info(data)
        node = None
        flatTreeLabelList = []
        try:
            if data :
                flatTreeLabelList.append(data[1])
#                 self.traverse.append(self.isSearchMatch(searchText, data[1]))
                node = Node(data[0], data[1], imageName=data[2], tooltip=data[3] , child=None)
                if data[4]:
                    node.child = []
                    for d in data[4]:
                        child = self.getNode(d, searchText=searchText)
                        
#                         child=self.someMethod(flatTreeLabelList, child, searchText)
                        if child:
                            node.child.append(child)
        except Exception as e:
            logger.info(data) 
            logger.error(e)
                
        return node
    
    def searchTreeData(self, searchText=None):
        for treeDataItem in self.treeData:
            pass

class Node():

    def __init__(self, id, name, imageName=None, tooltip=None, child=None):
        self.id = id,
        self.name = name.title()
        if tooltip:
            self.tooltip = tooltip
        else:
            self.tooltip = name

        self.imageName = imageName
        self.child = child
        
    def getFirstChildNode(self):
        firstChild = None
        if self.child:
            firstChild = self.child[0]
        return firstChild

    def __repr__(self):
        return f' name:{self.name},tooltip:{self.tooltip}, imageName:{self.imageName}  child:{self.child}'        
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
        logger.info()
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
        # logger.info("b4 CloseOutput")
        self.process.CloseOutput()
        # logger.info("after CloseOutput")

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
class RightPanel(wx.Panel):

    def __init__(self, parent=None, id=wx.ID_ANY, pos=wx.DefaultPosition,
                size=wx.DefaultSize, name=None):
        wx.Panel.__init__(self, parent, id, pos, size, style=wx.NO_BORDER)
        self.parent = parent
        
        self.vBox = wx.BoxSizer(wx.VERTICAL)
        ####
        
        self.addPanel(name=name)
        ####
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.vBox, 0, wx.EXPAND , 1)
        self.SetSizer(self.vBox)

    def addPanel(self, name=None):
        rightPanelItem = self.getPreferencePanelObj(name=name)
        if rightPanelItem:
            self.vBox.Add(rightPanelItem, 1, wx.EXPAND)

#             self.GetChildren().append(rightPanelItem)

    def getPreferencePanelObj(self, name='Preferences'):
        preferencePanelObj = None
        if name == 'Resource':
            preferencePanelObj = ResourcePanel(self, name=name)
#         elif name == 'Preferences':
#             preferencePanelObj = PreferencePanel(self, name=name)
#         elif name == 'Appearance':
#             preferencePanelObj = AppearancePreferencePanel(self, name=name)
#         elif name == 'Search':
#             preferencePanelObj = SearchPanel(self, name=name)
#         elif name == 'Workspace':
#             preferencePanelObj = WorkspacePanel(self, name=name)
#         elif name == 'Keys':
#             preferencePanelObj = KeysPanel(self, name=name)
#         elif name == 'Sharing':
#             preferencePanelObj = PreferencePanel(self, name=name)
#         elif name == 'Calibre':
#             preferencePanelObj = CalibreGeneralPreferencePanel(self, name=name)
#         else :
#             preferencePanelObj = GeneralPreferencePanel(rightPanel, preferenceName=preferenceName)
        
        if preferencePanelObj:
            preferencePanelObj.SetName(name)
            preferencePanelObj.Show(show=True)
        return preferencePanelObj


class SizeReportCtrl(wx.Control):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                size=wx.DefaultSize, mgr=None):

        wx.Control.__init__(self, parent, id, pos, size, style=wx.NO_BORDER)
        self._mgr = mgr

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        size = self.GetClientSize()

        s = "Size: %d x %d" % (size.x, size.y)

        dc.SetFont(wx.NORMAL_FONT)
        w, height = dc.GetTextExtent(s)
        height += 3
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        dc.DrawRectangle(0, 0, size.x, size.y)
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawLine(0, 0, size.x, size.y)
        dc.DrawLine(0, size.y, size.x, 0)
        dc.DrawText(s, (size.x - w) / 2, (size.y - height * 5) / 2)

        if self._mgr:

            pi = self._mgr.GetPane(self)

            s = "Layer: %d" % pi.dock_layer
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 1))

            s = "Dock: %d Row: %d" % (pi.dock_direction, pi.dock_row)
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 2))

            s = "Position: %d" % pi.dock_pos
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 3))

            s = "Proportion: %d" % pi.dock_proportion
            w, h = dc.GetTextExtent(s)
            dc.DrawText(s, (size.x - w) / 2, ((size.y - (height * 5)) / 2) + (height * 4))

    def OnEraseBackground(self, event):

        pass

    def OnSize(self, event):

        self.Refresh()


class ResourcePanel(wx.Panel):

    def __init__(self, parent=None, name='', *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
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
        ####################################################################
        
        resourceDict={
                'Path':'_exam',
                'Type':'sqlite connection',
                'Location':'c:\\'
                }
            
        
        for k, v in resourceDict.items():
            kLabel = wx.StaticText(self, -1, f"{k}:") 
            vLabel = wx.StaticText(self, -1, f"{v}") 
            hBox1 = wx.BoxSizer(wx.HORIZONTAL)
            hBox1.Add(kLabel, 2, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            hBox1.Add(vLabel, 8, wx.EXPAND | wx.ALL)
            vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        
#         booShortkNameLabel = wx.StaticText(self, -1, "Short Title:") 
#         bookShortName = ExpandoTextCtrl(self, -1, "", size=(150, -1));

#         authorsLabel = wx.StaticText(self, -1, "Authors:") 
#         authorName = wx.TextCtrl(self, -1, "", size=(50, -1));
        
#         numberOfPagesLabel = wx.StaticText(self, -1, "Number of pages:") 
#         numberOfPages = wx.TextCtrl(self, -1, "", size=(70, -1));
        
#         hBox1.Add(bookNameLabel, 2, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
#         hBox1.Add(bookName, 8, wx.EXPAND | wx.ALL)
        
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
#         vBoxBody.Add(hBox1, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox2, 0, wx.EXPAND | wx.ALL, 5)
        vBoxBody.Add(hBox3, 0, wx.EXPAND | wx.ALL, 1)
        vBoxBody.Add(hBox4, 0, wx.EXPAND | wx.ALL, 1)
        
        vBox.Add(vBoxHeader, 1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxBody, 99, wx.EXPAND | wx.ALL, 1)
        vBox.Add(vBoxFooter, 1, wx.EXPAND | wx.ALL, 1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 0, wx.EXPAND , 1)
        self.SetSizer(sizer)
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
    frame = PropertiesFrame(None, 'Table properties', size=(500, 420))
    frame.Show()
    app.MainLoop()
