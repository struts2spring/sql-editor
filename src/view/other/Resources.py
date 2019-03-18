'''
Created on 30-Dec-2018

@author: vijay
'''

import wx
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.util.FileOperationsUtil import FileOperations
from src.logic.resource.search.ResourceSearch import ResourceSearchLogic
import logging.config
from src.view.constants import LOG_SETTINGS, ID_JAVA_EE_PERSPECTIVE, \
    ID_JAVA_PERSPECTIVE, ID_DEBUG_PERSPECTIVE, ID_GIT_PERSPECTIVE, \
    ID_PYTHON_PERSPECTIVE, ID_DATABASE_PERSPECTIVE, ID_RESOURCE_PERSPECTIVE
from src.view.views.editor.EditorManager import EditorWindowManager
import os

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


class ResourceFrame(wx.Frame):

    def __init__(self, parent, title, size=(413, 441),
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
        self.resourcePanel = ResourcePanel(self, parent)
        ####################################################################

        sizer.Add(self.resourcePanel, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
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


class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):

        wx.Panel.__init__(self, parent, id=-1)

        self.parent = parent
        self.fileOperations = FileOperations()
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.openWithButton = wx.Button(self, wx.NewIdRef(), "Open Wit&h", size=(95, 26))
        self.showInButton = wx.Button(self, wx.NewIdRef(), "Show In", size=(95, 26))
        okButton = wx.Button(self, wx.NewIdRef(), "Open", size=(90, 26))
        okButton.SetToolTip("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onOkClick, okButton)
        self.Bind(wx.EVT_BUTTON, self.onOpenWithButton, self.openWithButton)
        self.Bind(wx.EVT_BUTTON, self.onShowInButton, self.showInButton)

        cancelButton = wx.Button(self, wx.NewIdRef(), "Cancel", size=(90, 26))
        cancelButton.SetToolTip("Execute script to create table.")
        self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, cancelButton)

        self.openWithButton.SetBitmap(self.fileOperations.getImageBitmap(imageName='button_menu.png'),
#                     wx.LEFT    # Left is the default, the image can be on the other sides too
                    wx.RIGHT
                    # wx.TOP
                    # wx.BOTTOM
                    )
        self.showInButton.SetBitmap(self.fileOperations.getImageBitmap(imageName='button_menu.png'),
#                     wx.LEFT    # Left is the default, the image can be on the other sides too
                    wx.RIGHT
                    # wx.TOP
                    # wx.BOTTOM
                    )
        hbox.Add(self.showInButton)
        hbox.Add(self.openWithButton)
        hbox.Add(okButton)
        hbox.Add(cancelButton)
#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

    def onShowInButton(self, event):
        logger.debug('showInButton')
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Menu Item 1")
        menu.Append(wx.ID_ANY, "Menu Item 2")
        menu.Append(wx.ID_ANY, "Menu Item 3")
        w, h = self.showInButton.GetSize()
        x, y = self.showInButton.GetPosition()
        self.PopupMenu(menu, (x, y + h))

    def onOpenWithButton(self, event):
        logger.debug('openWithButton')
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Menu Item 1")
        menu.Append(wx.ID_ANY, "Menu Item 2")
        menu.Append(wx.ID_ANY, "Menu Item 3")
        self.openWithButton
        w, h = self.openWithButton.GetSize()
        x, y = self.openWithButton.GetPosition()
        self.PopupMenu(menu, (x, y + h))

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


class ResourcePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
#         self.fileOperations = FileOperations()
        self.connDict = dict()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.resourceSearchLogic = ResourceSearchLogic()
        self.enterLabel = wx.StaticText(self, -1, "Enter resource name prefix, path prefix or pattern(?, * or camel case):")
        self.matchingItemLabel = wx.StaticText(self, -1, "Matching items:")
        self.treeMap = {}
#         self.tree = OtherViewBaseTreePanel(self)
        self.resourceSearchResultListCtrl = ResourceSearchResultListCtrl(self)

        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter search text")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.OnSearch)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

#         self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
#         self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
#         self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
#         self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
#         self.tree.SelectItem(self.root)

        searchMenu = wx.Menu()
        item = searchMenu.AppendRadioItem(-1, "Full search")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        item = searchMenu.AppendRadioItem(-1, "Sample Content")
        self.Bind(wx.EVT_MENU, self.OnSearchMenu, item)
        self.filter.SetMenu(searchMenu)
#         self.RecreateTree()
        ####################################################################
        vBox.Add(self.enterLabel, 0, wx.EXPAND | wx.ALL, 5)
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.matchingItemLabel, 0, wx.EXPAND | wx.ALL, 5)
        vBox.Add(self.resourceSearchResultListCtrl , 1, wx.EXPAND | wx.ALL)
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
#         if not value:
#             self.RecreateTree()
#             return

        wx.BeginBusyCursor()
        logger.debug(value)
        self.resourceSearchLogic.clearLastResult()
        projects = [
            ('c:\work\python_project', 'sql-editor'),
            ('c:\work\python_project', 'Phoenix'),
            ]
        for x in projects:
            self.searchResult = self.resourceSearchLogic.getFiles(basePath=x[0], projectDirName=x[1], searchText=value)

        self.resourceSearchResultListCtrl.loadData(self.searchResult)
#         for category, items in _treeList:
#             self.searchItems[category] = []
#             for childItem in items:
# #                 if SearchDemo(childItem, value):
#                 self.searchItems[category].append(childItem)

        wx.EndBusyCursor()
#         self.RecreateTree()

    #---------------------------------------------


#         self.UpdateNotebook(preferenceName=itemText)
import wx.lib.mixins.listctrl as listmix


class ImprovedListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class ResourceSearchResultListCtrl(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.searchResult = {
#             1 : ["abc1.py", r"c:\1\asdf"],
#             2 : ["abc2.java", r"c:\1\asdf"],
#             3 : ["abcasdfasdfa3.java", r"c:\1\asdf"],
#             4 : ["abc4.java", r"c:\1\asdf"],
#             5 : ["abc5.properties", r"c:\1\asdf"],
#             6 : ["abc5.md", r"c:\1\asdf"],
#             7 : ["abc5.txt", r"c:\1\asdf"],
        }

        self.fileOperations = FileOperations()
        self.list = ImprovedListCtrl(self, wx.NewIdRef(),
                                style=wx.LC_REPORT
                                # | wx.BORDER_SUNKEN
                                | wx.BORDER_NONE
                                | wx.LC_EDIT_LABELS
                                # | wx.LC_SORT_ASCENDING    # disabling initial auto sort gives a
                               | wx.LC_NO_HEADER  # better illustration of col-click sorting
                                | wx.LC_VRULES
                                | wx.LC_HRULES
                                | wx.LC_SINGLE_SEL
                                )
        self.setImageList()
        self.loadData(items={})
        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.list)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.list)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnEndEdit, self.list)

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        logger.debug('OnItemSelected')
        self.currentItem = event.Index
        logger.debug(f"OnItemSelected: {self.currentItem}, {self.list.GetItemText(self.currentItem)}, {self.getColumnText(self.currentItem, 1)}")

#         if self.currentItem == 10:
#             logger.debug("OnItemSelected: Veto'd selection\n")
#             # event.Veto()  # doesn't work
#             # this does
#             self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

        event.Skip()

    def OnItemDeselected(self, event):
        logger.debug('OnItemDeselected')

    def OnItemActivated(self, event):
        logger.debug('OnItemActivated')
        self.currentItem = event.Index
        logger.debug(f"OnItemActivated: {self.list.GetItemText(self.currentItem)} TopItem: {self.list.GetTopItem()}")
        logger.debug(self.searchResult[self.currentItem])
        fileName, relateName, fileDirPath = self.searchResult[self.currentItem]
        captionName = fileName
        window = EditorWindowManager().getWindow(self.GetTopLevelParent().Parent, os.path.join(fileDirPath, fileName))
#         icon = self.list.OnGetItemImage(self.currentItem)
        self.GetTopLevelParent().Parent._mgr.addTabByWindow(window=window, icon=None, name=f'{relateName}-{captionName}', captionName=captionName, tabDirection=5)
        self.GetTopLevelParent().Destroy()

    def OnItemDelete(self, event):
        logger.debug('OnItemDelete')

    def OnColClick(self, event):
        logger.debug('OnColClick')

    def OnColRightClick(self, event):
        logger.debug('OnColRightClick')

    def OnColBeginDrag(self, event):
        logger.debug('OnColBeginDrag')

    def OnColDragging(self, event):
        logger.debug('OnColDragging')

    def OnColEndDrag(self, event):
        logger.debug('OnColEndDrag')

    def OnBeginEdit(self, event):
        logger.debug('OnBeginEdit')

    def OnEndEdit(self, event):
        logger.debug('OnEndEdit')

    def OnDoubleClick(self, event):
        logger.debug('OnDoubleClick')

    def OnRightDown(self, event):
        logger.debug('OnRightDown')

    def OnRightClick(self, event):
        logger.debug('OnRightClick')

    def setImageList(self):
        self.il = wx.ImageList(16, 16)

        self.imageList = {
            '_':['_', 'fileType_filter.png'],
            'py':['py', 'python_module.png'],
            'java':['java', 'jcu_obj.png'],
            'md':['md', 'markdown.png'],
            'txt':['txt', 'text.png'],
        }
        for imageExtension, item in self.imageList.items():
            imageExtension, imageName = item[0], item[1]
            item.append(self.il.Add(self.fileOperations.getImageBitmap(imageName=imageName)))

        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

    def getExtension(self, fileName=None):
        return fileName.split('.')[-1]

    def loadData(self, items={}):
        logger.debug('loadData')
        self.list.ClearAll()
        self.list.InsertColumn(0, "Name")
        self.list.InsertColumn(1, "Path")
        self.searchResult = items
#         items = self.searchResult.items()
        for key, data in items.items():
            index = self.list.InsertItem(self.list.GetItemCount(), data[0], self.getImageIndex(extention=self.getExtension(fileName=data[0])))
            self.list.SetItem(index, 1, data[1])
#             self.list.SetItem(index, 2, data[2])
            self.list.SetItemData(index, key)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def clearData(self):
        logger.debug('clearData')
        self.list.ClearAll()

    def getImageIndex(self, extention='txt'):
        imageIndex = 0
        try:
            if self.imageList[extention]:
                imageIndex = self.imageList[extention][2]
        except:
            pass
        return imageIndex


if __name__ == '__main__':
    app = wx.App(False)
    frame = ResourceFrame(None, 'Open Resource')
    frame.Show()
    app.MainLoop()
