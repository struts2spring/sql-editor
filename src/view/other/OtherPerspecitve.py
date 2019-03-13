'''
Created on 30-Dec-2018

@author: vijay
'''

import wx
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.util.FileOperationsUtil import FileOperations
import logging.config
from src.view.constants import LOG_SETTINGS, ID_JAVA_EE_PERSPECTIVE, \
    ID_JAVA_PERSPECTIVE, ID_DEBUG_PERSPECTIVE, ID_GIT_PERSPECTIVE, \
    ID_PYTHON_PERSPECTIVE, ID_DATABASE_PERSPECTIVE, ID_RESOURCE_PERSPECTIVE

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
##################################################

perspectiveList = [
        [wx.NewIdRef(), "Database Debug", 'database_debug_perspective.png', None],
        [ID_DATABASE_PERSPECTIVE, "Database Development", 'database.png', None],
        [ID_DEBUG_PERSPECTIVE, "Debug", 'debug_persp.png', None],
        [ID_GIT_PERSPECTIVE, "Git", 'gitrepository.png', None],
        [ID_JAVA_PERSPECTIVE, "Java", 'jperspective.png', None],
        [ID_PYTHON_PERSPECTIVE, "Python", 'python_perspective.png', None],
        [wx.NewIdRef(), "Java Browsing", 'browse_persp.png', None],
        [ID_JAVA_EE_PERSPECTIVE, "Java EE", 'javaee_perspective.png', None],
        [wx.NewIdRef(), "Java Type Hierarchy", 'java_type_hierarchy.png', None],
        [wx.NewIdRef(), "JavaScript", 'javascript_perspective.png', None],
        [wx.NewIdRef(), "JPA", 'jpa.png', None],
        [wx.NewIdRef(), "Planning", 'perspective-planning.png', None],
        [wx.NewIdRef(), "Plug-in Development", 'plugin_perspecitve.png', None],
        [wx.NewIdRef(), "Remote System Explorer", 'remote_perspective.png', None],
        [ID_RESOURCE_PERSPECTIVE, "Resource", 'resource_persp.png', None],
        [wx.NewIdRef(), "SVN Repository Exploring", 'svn_perspective.png', None],
        [wx.NewIdRef(), "Team Synchronizing", 'synch_synch.png', None],
        [wx.NewIdRef(), "Web", 'web_perspective.png', None],
        [wx.NewIdRef(), "XML", 'xml_perspective.png', None],
    ]

_treeList1 = [
    ("General", [
        ("Appearance", [
                ("Colors and Fonts"),
                ("Label Decorations")
            ]
        ),
        ("Capabilities"),
        ("Compare/Patch"),
        ("Content Types"),
        ("Editors", [
            ("Autosave"),
            ("File Associations"),
            ("Structured Text Editors"),
            ]
        ),
        ("Error Reporting"),
        ("Globalization"),
        ("Keys"),
        ("Network Connections", [
            ("Cache"),
            ("SSH2")
            ]
         )
        ]
    ),
    ("Ant", [
        ("Editor", [
                ("Colors and Fonts"),
                ("Label Decorations")
            ]
        ),
        ("Runtime")
        ]
    ),
    ("Cloud Foundry", [
        ("HTTP Tracing")
        ]
    ), ("Code Recommenders", [
        ("Advisors"),
        ("Completions", [
            ("Calls"),
            ("Chains"),
            ("Constructors"),
            ("Overrides"),
            ("Statics"),
            ("Subwords"),
            ]),
        ("Models"),
        ]
    ),
    ("Data Management", [
        ("Connectivity", [
            ("Database Connection Profile"),
            ("Driver Definitions"),
            ("Open Data Access", [
                ("XML Data Set")
                ]),
            ]),
        ("Label Decorations"),
        ("SQL Development", [
            ("Execution Plan View Options"),
            ("General"),
            ("Schema Object Editor Configuration"),
            ("SQL Editor", [
                ("Code Assist"),
                ("SQL Files/Scrapbooks"),
                ("Syntax Coloring"),
                ("Templates"),
                ]),
            ]),
        ]
    ),
    ("Gradle"),
    ("Help", [("Content")]),
    (
     "Install/Update", [
            ('Automatic Updates'),
            ('Available plugins')
        ]
     ),
    ("Java", [("Appearance", [("Members Sort Order"), ("Type Filters")]),
             ("Build Path", [("Classpath Variables"), ("User Liberaries")]),
             ("Code Coverage"),
             ("Code Style", [("Clean Up"), ("Code Templates"), ("Formatter"), ("Organize Imports")]),
             ("Compiler", [("Building"), ("Errors/Warning"), ("Javadoc"), ("Task Tags")]),
             ("Debug", [("Detail Formatters"), ("Heap Walking"), ("Logical Structures"), ("Premitive Display Options"), ("Step Filtering")]),
             ("Editor", [("Content Assist"), ("Folding"), ("Hovers"), ("Mark Occurrences"), ("Save Actions"), ("Syntax Coloring"), ("Templates"), ("Typing")]),
             ("Installed JREs", [("Execution Environments")]),
             ("JUnit"),
             ("Properties Files Editor"),

             ]),
    ("Java EE"),
    ("Java Persistence"),
    ("JavaScript"),
    ("JSON", [("JSON Catalog"), ("JSON Files", [("Editor", [("Content Assist"), ("Syntax Coloring"), ("Templates")]), ("Validation")])]),
    ("Maven", [("Archetypes"), ("Discovery"), ("Errors/Warning"), ("Installations"), ("Java EE Integration"), ("Lifecycle Mappings"), ("Source Lookup"), ("Templates"), ("User Interface"), ("User Settings")]),
    ("Python", [("Builders"),
               ("Debug", [("Source Locator")]),
               ("Editor", [("Auto Imports")]),
               ("Code Analysis", [("PyLint")]),
               ("Code Completion (ctx insensitive and common tokens)"),
               ("Code Folding"), ("Code Style", [("Block Comments"), ("Code Formatter"), ("Docstrings"), ("File types"), ("Imports")]),
               ("Editor caption/icon"), ("Hover"), ("Mark Occurrences"), ("Overview Ruler Minimap")
               ]),
    ("Remote Systems"),
    ("Run/Debug"),
    ("Server"),
    ("Team", [("File Content"), ("Git", [
        ("Committing"), ("Configuration"), ("Confirmation and Warning"), ("Date Format"), ("History"), ("Label Decorations"), ("Projects"), ("Staging View"), ("Synchronize"), ("Window Cache"),
        ]),
        ("Ignored Resources"), ("Models")
    ]),
    ("Terminal", [("Local Terminal")]),
    ("Validation"),
    ("Web", [
        ("CSS Files", [("Editor", [("Content Assist"), ("Syntax Coloring"), ("Templates")])]),
        ("HTML Files", [("Editor", [("Content Assist"), ("Syntax Coloring"), ("Templates"), ("Typing")]), ("Validation")]),
        ("JavaServer Faces Tools", [("FacesConfig Editor"), ("Validation"), ("Views", [("JSP Tag Registry")])]),
        ("JSP Files", [("Editor", [("Content Assist"), ("Syntax Coloring"), ("Templates")])]),

    ]),
    ("Web Services", [("Axis Emitter"), ("Axis2 Preferences")]),
    ("XML"),
]

_treeList = [
    # new stuff
    (
     'General', [
        'Appearance',
        'Search',
        'Workspace',
        'Keys'
        ]
     ),
    (
     'Sharing', [
        'Email book',
        'Open cloud',
        'Configure device',
        ]
     ),
    (
     'Account', [
        'Email book',
        'Open cloud',
        'Configure device',
        ]
     ),

    ('Check out the samples dir too', []),

]


class OtherPerspectiveTreeFrame(wx.Dialog):

    def __init__(self, parent, title, size=(313, 441),
                 style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.SUNKEN_BORDER | wx.STAY_ON_TOP):
        style = style & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, parent, -1, title, size=size,
                          style=style)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.SetMinSize((100, 100))
        self.fileOperations = FileOperations()
        # set frame icon
        icon = wx.Icon()
        icon.CopyFromBitmap(self.fileOperations.getImageBitmap(imageName='eclipse16.png'))
        self.SetIcon(icon)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonPanel = CreateButtonPanel(self)
        ####################################################################

        self.OtherPerspectiveTreePanel = OtherPerspectiveTreePanel(self)
        ####################################################################

        sizer.Add(self.OtherPerspectiveTreePanel, 1, wx.EXPAND)
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


class OtherPerspectiveTreePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
#         self.fileOperations = FileOperations()
        self.connDict = dict()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.treeMap = {}
        self.tree = OtherViewBaseTreePanel(self)

        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter search text")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
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
        sizer.Add(vBox, 1, wx.EXPAND , 0)
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

        for category, items in _treeList:
            self.searchItems[category] = []
            for childItem in items:
#                 if SearchDemo(childItem, value):
                self.searchItems[category].append(childItem)

        wx.EndBusyCursor()
        self.RecreateTree()

    #---------------------------------------------
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
        self.root = self.tree.AddRoot("Other View")
        self.tree.SetItemImage(self.root, self.tree.iconsDictIndex['other_view.png'])
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

        def constructNode(parent=None, treeData=None):
            logger.debug(treeData)
            for idx, items in enumerate(treeData):
                logger.debug(items)
#                 itemText = None
#                 image = 1
#                 if isinstance(items, tuple):
#                     itemText = items[1]
#                     image = self.tree.iconsDictIndex['folder.png']
#                 else:
#                     itemText = items
#                     image = self.tree.iconsDictIndex['fileType_filter.png']
                itemText = items[1]
                if items[2]:
                    image = self.tree.iconsDictIndex[items[2]]
                else:
                    image = self.tree.iconsDictIndex['fileType_filter.png']
                child = self.tree.AppendItem(parent, itemText, image=image)
#                 self.tree.SetItemFont(child, catFont)
                self.tree.SetItemData(child, count)
#                 if isinstance(items, tuple) and len(items) > 1:
#                     constructNode(parent=child, treeData=items[1])

        constructNode(parent=self.root, treeData=perspectiveList)
#         for category, items in _treeList:
#             category, items
#             count += 1
#             if filter:
#                 if fullSearch:
#                     items = self.searchItems[category]
#                 else:
#                     items = [item for item in items if filter.lower() in item.lower()]
#             if items:
#                 child = self.tree.AppendItem(self.root, category, image=count)
#                 self.tree.SetItemFont(child, catFont)
#                 self.tree.SetItemData(child, count)
#                 if not firstChild: firstChild = child
#                 for childItem in items:
#                     image = count
# #                     if DoesModifiedExist(childItem):
# #                         image = len(_demoPngs)
#                     theDemo = self.tree.AppendItem(child, childItem, image=image)
#                     self.tree.SetItemData(theDemo, count)
#                     self.treeMap[childItem] = theDemo
#                     if current and (childItem, category) == current:
#                         selectItem = theDemo

#         self.tree.Expand(self.root)
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
    def RecreateTree1(self, evt=None):
        # Catch the search type (name or content)
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
        self.root = self.tree.AddRoot("Preferences")
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
        self.tree.SetItemFont(self.root, treeFont)

        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0

        for category, items in _treeList:
            category, items
            count += 1
            if filter:
                if fullSearch:
                    items = self.searchItems[category]
                else:
                    items = [item for item in items if filter.lower() in item.lower()]
            if items:
                child = self.tree.AppendItem(self.root, category, image=count)
                self.tree.SetItemFont(child, catFont)
                self.tree.SetItemData(child, count)
                if not firstChild: firstChild = child
                for childItem in items:
                    image = count
#                     if DoesModifiedExist(childItem):
#                         image = len(_demoPngs)
                    theDemo = self.tree.AppendItem(child, childItem, image=image)
                    self.tree.SetItemData(theDemo, count)
                    self.treeMap[childItem] = theDemo
                    if current and (childItem, category) == current:
                        selectItem = theDemo

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
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item and item == self.tree.GetSelection():
            print(self.tree.GetItemText(item) + " Overview")
        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):
#         if self.dying or not self.loaded or self.skipLoad:
#             return

#         self.StopDownload()

        item = event.GetItem()
        itemText = self.tree.GetItemText(item)
        logger.debug(itemText)
        opalPreference = self.GetTopLevelParent()
        if opalPreference:
    #         rightPanel=opalPreference.rightPanelItem.GetParent()
    #         opalPreference.rightPanelItem.Hide()
    #         opalPreference.rightPanelItem.Hide()
    #         opalPreference.rightPanelItem=opalPreference.getPreferencePanelObj(rightPanel,preferenceName=itemText)
    #         opalPreference.rightPanelItem.Show(True)
    #         opalPreference.rightPanelItem.Layout()
            for pnl in opalPreference.pnl.GetChildren():
    #             print(pnl)
                if pnl.GetName() == 'rightPanel':
                    opalPreference = self.GetTopLevelParent()
                    for child in pnl.GetChildren():
#                         if 'preference' in child.name.lower():
                        child.Hide()
    #                     break
    #                     child.opalPreference.getPreferencePanelObj(pnl,preferenceName=itemText)
                    rightPanelItem = opalPreference.getPreferencePanelObj(pnl, preferenceName=itemText)
                    opalPreference.addPanel(rightPanelItem)
                    pnl.Layout()
                    pnl.Refresh()
                    pnl.Fit()
            opalPreference.Layout()
    #         print(opalPreference.GetChildrenCount())
    #         opalPreference.GetChildrenCount().rightpanel.Refresh()

            opalPreference.mgr.Update()


#         self.UpdateNotebook(preferenceName=itemText)
class OtherViewBaseTreePanel(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in preferences page
    '''

    def __init__(self, parent):

        TreeCtrl.__init__(self, parent, style=wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE |
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
                          'java.png', 'python_module.png', 'xml.png', "other_view.png", 'gitrepository.png', 'jperspective.png',
                           'javaee_perspective.png', 'python_perspective.png', 'database.png', 'resource_persp.png', 'debug_persp.png',
                           'jpa.png', 'web_perspective.png', 'javascript_perspective.png', 'plugin_perspecitve.png', 'svn_perspective.png',
                           'remote_perspective.png', 'browse_persp.png', 'perspective-planning.png', 'database_debug_perspective.png',
                           'java_type_hierarchy.png','xml_perspective.png', 'synch_synch.png', ]:
            self.ImageList.Add(self.fileOperations.getImageBitmap(imageName=imageName))
            self.iconsDictIndex[imageName] = count
            count += 1

    def GetItemIdentity(self, item):
        return self.GetItemData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(OtherViewBaseTreePanel, self).Freeze()

    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(OtherViewBaseTreePanel, self).Thaw()


if __name__ == '__main__':
    app = wx.App(False)
    frame = OtherPerspectiveTreeFrame(None, 'Open Perspective')
    frame.Show()
    app.MainLoop()
