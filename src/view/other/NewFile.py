from wx import TreeCtrl
from src.view.util.FileOperationsUtil import FileOperations
import logging.config
import wx, os
import stat
from src.view.constants import LOG_SETTINGS, keyMap
from src.view.views.file.explorer._filetree import FileTree
import time
from src.view.util.common.eclutil import Freezer
from pathlib import Path
from pubsub import pub
from src.view.views.editor.EditorManager import EditorWindowManager
from src.view.util.osutil import GetWindowsDriveType, RemovableDrive, CDROMDrive

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
##################################################


class NewFileFrame(wx.Frame):
    '''
    This is for new file and new folder.
    '''

    def __init__(self, parent, title, selectedPath=None, size=(350, 420),
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
        self.newFileFrame = NewFilePanel(self, title=title, selectedPath=selectedPath)
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
        try:
            self.parent.refreshNode()
        except Exception as e:
            logger.error(e)
        self.Destroy()

    def OnSize(self, event):
        hsize = event.GetSize()
        logger.debug(hsize)


class NewFilePanel(wx.Panel):

    def __init__(self, parent, *args, title=None, selectedPath='', **kw):
        wx.Panel.__init__(self, parent, id=-1)
#         self.parent = parent
        self.title = title
        vBox = wx.BoxSizer(wx.VERTICAL)

        v1 = wx.BoxSizer(wx.VERTICAL)
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        h2 = wx.BoxSizer(wx.HORIZONTAL)
        ###################################3333333333
        self.parentFolderText = selectedPath
            
        self.fileNameText = ''

        parentFolderLabel = wx.StaticText(self, -1, "Enter or select parent folder:")
        self.parentFolderCtrl = wx.TextCtrl(self, id=-1, name=title, size=(400, -1))

        fileLabel = ''
        if title == 'New File':
            fileLabel = "File name:"
        elif title == 'New Folder':
            fileLabel = "Folder name:"
        fileNameLabel = wx.StaticText(self, -1, fileLabel)
        self.fileNameCtrl = wx.TextCtrl(self, -1, self.fileNameText, size=(400, -1) , style=wx.TE_PROCESS_ENTER)
        self.fileNameCtrl.SetFocus()
        self.Bind(wx.EVT_TEXT , self.onEnteredText, self.fileNameCtrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnterButtonPressed, self.fileNameCtrl)

        self.folderExplorerTreePanel = FolderExplorerTreePanel(self)
        self.buttons = CreateButtonPanel(self)
        ####################################################################
        v1.Add(parentFolderLabel, 0, wx.ALL, 2)
        v1.Add(self.parentFolderCtrl, 0, wx.ALL, 2)
        h2.Add(fileNameLabel, 0, wx.ALL, 2)
        h2.Add(self.fileNameCtrl, 0, wx.ALL, 2)

        ####################################################################

        vBox1 = wx.BoxSizer(wx.VERTICAL)
        vBox1.Add(v1, 0, wx.EXPAND , 0)
        vBox.Add(vBox1, 0, wx.EXPAND, 0)
        vBox.Add(self.folderExplorerTreePanel, 1, wx.EXPAND , 0)
        vBox.Add(h2, 0, wx.EXPAND , 0)
        vBox.Add(self.buttons, 0, wx.EXPAND , 0)
        self.SetSizer(vBox)
        self.SetAutoLayout(True)

    def onEnterButtonPressed(self, event):
        text = event.GetString()
        logger.debug(f'onEnterButtonPressed: {text}')
        self.buttons.onFinishClicked(event)

    def onEnteredText(self, event):
        text = event.GetString()
        logger.debug(f'fileName: {text}')
        if text.strip() != '':
            self.buttons.finishButton.Enable(enable=True)
            self.buttons.finishButton.SetFocus()
            self.fileNameCtrl.SetFocus()

    def setFindText(self, findText):
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                self.findTextCtrl.SetValue(do.GetText())

    def onChooseBtn(self):
        logger.debug('onChooseBtn')


class CreateButtonPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):

        wx.Panel.__init__(self, parent, id=-1)

#         self.parent = parent
        self.fileOperations = FileOperations()
        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.onCancelClicked, self.cancelButton)
#         self.cancelButton.SetDefault()

        self.finishButton = wx.Button(self, -1, "Finish")
        self.Bind(wx.EVT_BUTTON, self.onFinishClicked, self.finishButton)
        self.finishButton.Disable()

        hbox1.Add(self.finishButton)
        hbox1.Add(self.cancelButton)

#         sizer.Add(cancelButton, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM)
        sizer.Add(hbox1, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox2, 0, wx.ALIGN_RIGHT | wx.RIGHT , 5)
        sizer.Add(hbox3, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

    def onCancelClicked(self, event):
        logger.debug('onCancelClicked: ')
        self.GetTopLevelParent().Close()

    def onFinishClicked(self, event):
        logger.debug('onFinishClicked')
        logger.debug(self.GetParent().parentFolderCtrl.GetValue())
        logger.debug(self.GetParent().fileNameCtrl.GetValue())
        try:
            parentDir = self.GetParent().parentFolderCtrl.GetValue()
            fname = self.GetParent().fileNameCtrl.GetValue()
            if self.GetParent().title == 'New File':
                os.makedirs(parentDir, mode=511, exist_ok=True)
                os.chdir(parentDir)
                Path(os.path.join(parentDir, fname)).touch(mode=0o777, exist_ok=True)
            elif self.GetParent().title == 'New Folder':
                os.makedirs(os.path.join(parentDir, fname), mode=511, exist_ok=True)
        except Exception as e:
            logger.error(e)
#         os.makedirs(self.GetParent().parentFolderCtrl.GetValue(), mode=511, exist_ok=False)
        self.GetTopLevelParent().Close()

#     def onReplaceAllClicked(self, event):
#         logger.debug('onReplaceAllClicked')


class FolderExplorerTreePanel(FileTree):

    def __init__(self, parent, size=wx.DefaultSize):
        self.iconManager = FolderIconManager()
        super().__init__(parent)
        self._mw = None
        self.isClosing = False
        self.syncTimer = wx.Timer(self)
        self._cpath = None
#         self.sqlExecuter = SQLExecuter()

        self.menu = None
        self.fileOperations = FileOperations()
        # Setup
        self.SetupImageList()
        self.initProjects()
#         self.Bind(wx.EVT_CONTEXT_MENU, self._OnMenu)

    def initProjects(self):
        
        try:

            for project in setting.activeWorkspace.projects:
                self.AddWatchDirectory(project=project)
        except Exception as e:
            logger.error(e)

    def onDelete(self, evt):
        logger.debug('onDelete')
        item = evt.GetItem()

    def onSelectionChange(self, event):
        logger.debug(f'onSelectionChange {self}')
#         self.LogKeyEvent('KeyDown', event.GetKeyEvent())
        keypress = self.GetKeyPress(event)
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
        logger.debug(f'onSelectionChange keycode: {keycode}  keypress: {keypress} keyname: {keyname}')

        nodes = self.GetSelections()
        files = [ self.GetPyData(node) for node in nodes ]
#         files = self.GetSelectedFiles()
        logger.debug(files)
        if files and len(files) > 0:
            self.showFileSelected(selectedFilePath=files[0])
#         logger.debug(keypress == 'WXK_F2')
#
# #         if keypress == 'Ctrl+C':
# #             pass
# #             self.onTreeCopy(event)
#         if keypress == 'WXK_F2':
#             self.onF2KeyPress(event)
#         elif keypress == 'WXK_DELETE':
#             self.onDeleteKeyPress(event)
        event.Skip()

    def setSelectedDirPath(self, selectedPath=None):
        logger.debug(f'setSelectedFilePath: {selectedPath}')
        # TODO : need to be implement

    def showFileSelected(self, selectedFilePath=None):
        logger.debug(f'showFileSelected: {selectedFilePath}')
        self.GetParent().parentFolderCtrl.SetValue(selectedFilePath)

    def onTreeKeyDown(self, event):
        logger.debug(f'onTreeKeyDown {self}')
#         self.LogKeyEvent('KeyDown', event.GetKeyEvent())
        keypress = self.GetKeyPress(event)
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
        logger.debug(f'onTreeKeyDown keycode: {keycode}  keypress: {keypress} keyname: {keyname}')
        nodes = self.GetSelections()
        files = [ self.GetPyData(node) for node in nodes ]
#         files = self.GetSelectedFiles()
        logger.debug(files)
#         logger.debug(keypress == 'WXK_F2')
#
# #         if keypress == 'Ctrl+C':
# #             pass
# #             self.onTreeCopy(event)
#         if keypress == 'WXK_F2':
#             self.onF2KeyPress(event)
#         elif keypress == 'WXK_DELETE':
#             self.onDeleteKeyPress(event)
        event.Skip()

    def AddWatchDirectory(self, project=None):
        """Add a directory to the controls top level view
        @param dname: directory path
        @return: TreeItem or None
        @todo: add additional api for getting already existing nodes based
               on path.

        """
        logger.debug('AddWatchDirectory')
#         assert os.path.exists(dname), "Path(%s) doesn't exist!" % dname
        childNode = None

#         dname = r"c:\1\sql_editor"
        if project.projectPath not in self._watch:

            self._watch.append(project.projectPath)
            childNode = self.AppendFileNode(self.RootItem, project=project)
            return childNode

    def AppendFileNode(self, item, project=None):
        """Append a child node to the tree
        @param item: TreeItem parent node
        @param path: path to add to node
        @return: new node

        """
        logger.debug('AppendFileNode')
        img = self.DoGetFileImage(project.projectPath)
        name = os.path.basename(project.projectPath)
        if not name:
            name = project.projectPath
        child = self.AppendItem(item, name, img)
        self.SetItemData(child, project.projectPath)
        if os.path.isdir(project.projectPath):
            self.SetItemHasChildren(child, True)
        return child

    def DoOnActivate(self, active):
        """Handle activation of main window that this
        tree belongs too.
        @param active: bool

        """
        # Suspend background checks when window is not active
        if active and self.IsShown():
            self.SuspendChecks(False)  # Resume
        elif not active:
            self.SuspendChecks(True)  # Suspend

    def DoOnDestroy(self):
        """Clean up resources and message handlers"""
        self._menu.Clear()
#         ed_msg.Unsubscribe(self.OnPageChange)
#         ed_msg.Unsubscribe(self.OnPageClosing)
#         ed_msg.Unsubscribe(self.OnThemeChanged)
#         ed_msg.Unsubscribe(self.OnConfig)
        if self.syncTimer.IsRunning():
            self.syncTimer.Stop()

    def SuspendChecks(self, suspend=True):
        """Suspend/Continue background monitoring"""
        self._monitor.Suspend(suspend)

    #--- FileTree interface methods ----#

    def DoSetupImageList(self):
        """Setup the image list for this control"""
        self.iconManager.PopulateImageList(self.ImageList)

#         super().DoSetupImageList()

    def DoGetFileImage(self, path):
        """Get the image for the given item"""
        return self.iconManager.GetImageIndex(path)

    def DoGetToolTip(self, item):
        """Get the tooltip to show for an item
        @return: string or None

        """
        tip = None
#         if self.GetItemImage(item) == self.iconManager.IMG_NO_ACCESS:
#             tip = _("Access Denied")
#        elif item: # Slightly annoying on GTK disable for now
#            tip = self.GetPyData(item)
        return tip

    def DoItemActivated(self, item):
        """Override to handle item activation
        @param item: TreeItem

        """
        logger.debug('DoItemActivated')
        filePathWithIconList = self.GetSelectedFilesWithImage()
        self.OpenFiles(self.GetSelectedFilesWithImage())
        for filePathWithIcon in filePathWithIconList:
            pub.sendMessage('addFileToHistory', path=filePathWithIcon[0])

    def DoItemCollapsed(self, item):
        """Handle when an item is collapsed"""
        d = self.GetPyData(item)
#         if d:
#             self._monitor.RemoveDirectory(d)
        super().DoItemCollapsed(item)
        self.SetItemImage(item, self.iconManager.GetImageIndex(d, False))

    def ShouldDisplayFile(self, path):
        """Check if the given file should be displayed based on configuration
        @param path: file path
        @return: bool

        """

        shouldDisplay = True
        dname = os.path.split(path)[-1]
        if os.path.isfile(path) or dname.startswith('.') or dname in ['__pycache__' , 'build', 'dist'] or '.egg-info' in dname :
            shouldDisplay = False
        return shouldDisplay

#     def ShouldDisplayFile(self, path):
#         """Check if the given file should be displayed based on configuration
#         @param path: file path
#         @return: bool
#
#         """
#         showHidden = fbcfg.GetFBOption(fbcfg.FB_SHF_OPT, False)
#         if not showHidden and ebmlib.IsHidden(path):
#             return False
#         name = os.path.basename(path)
#         filters = fbcfg.GetFBOption(fbcfg.FB_FILTER_OPT,
#                                     fbcfg.FB_DEFAULT_FILTERS)
#         if filter(lambda x: fnmatch.fnmatchcase(name, x), filters):
#                 return False
#         return True

#     def FilterFileList(self, paths):
#         """Filter a list of files returning only the ones that are valid to
#         display in the tree. Optimized for large lists of paths.
#         @param paths: list of paths
#         @return: filtered list
#
#         """
#         showHidden = True
# #         showHidden = fbcfg.GetFBOption(fbcfg.FB_SHF_OPT, False)
#         filters = fbcfg.GetFBOption(fbcfg.FB_FILTER_OPT,
#                                     fbcfg.FB_DEFAULT_FILTERS)
#         isHidden = IsHidden
#         rval = list()
#         rAdd = rval.append
#         getBase = os.path.basename
#         for path in paths:
#             if not showHidden and isHidden(path):
#                 continue
#             name = getBase(path)
#             if filter(lambda x: fnmatch.fnmatchcase(name, x), filters):
#                 continue
#             rAdd(path)
#         return rval

    def DoItemExpanding(self, item):
        """Handle when an item is expanding to display the folder contents
        @param item: TreeItem

        """
        logger.debug('DoItemExpanding')
        cursor = wx.BusyCursor()  # can take a few seconds on big directories

        d = None
        try:
            d = self.GetPyData(item)
        except wx.PyAssertionError:
            logger.debug("[FileBrowser][err] FileBrowser.DoItemExpanding")
            return

        if d and os.path.exists(d) and os.access(d, os.R_OK) and self.ShouldDisplayFile(d):
            contents = self.GetDirContents(d)
            if contents and  len(contents) > 0:
                t1 = time.time()
                with Freezer(self) as _tmp:
                    self.AppendFileNodes(item, contents)
                    self.SortChildren(item)
                logger.info("Tree expand time: %f" % (time.time() - t1))
            else:
                self.SetItemHasChildren(item, hasChildren=False)
#             if not self._monitor.AddDirectory(d):
#                 self.SetItemImage(item, self.iconManager.IMG_NO_ACCESS)
#                 return

        # Update tree image
        self.SetItemImage(item, self.iconManager.GetImageIndex(d, True))
        # mark item has children or not here
        del cursor

    def GetDirContents(self, directory):
        """Get the list of files contained in the given directory"""
        logger.debug('GetDirContents')
        assert os.path.isdir(directory)
        files = list()
        try:
#             joinPath = os.path.join
#             fappend = files.append
            # fs_encoding = sys.getfilesystemencoding()
            for p in os.listdir(directory):
                logger.debug(p)
                fullpath = os.path.join(directory, p)

                if self.ShouldDisplayFile(fullpath):
#                 if type(fullpath) != types:
#                     fullpath = fullpath.decode(fs_encoding)
                    files.append(fullpath)
        except OSError:
            pass
        return files

    def DoBeginEdit(self, item):
        """Handle when an item is requested to be edited"""
        d = None
        try:
            d = self.GetPyData(item)
        except wx.PyAssertionError:
            logger.debug("[FileBrowser][err] FileBrowser.DoItemExpanding")
#             util.Log("[FileBrowser][err] FileBrowser.DoItemExpanding")
            return False
        if d and not os.access(d, os.W_OK) or os.path.ismount(d):
            return False
        return True

    def DoEndEdit(self, item, newlabel):
        """Handle after a user has made changes to a label"""
        editOk = False
        path = self.GetPyData(item)
        # TODO: check access rights and validate input
#         if path:
#             newpath = os.path.join(os.path.dirname(path), newlabel)
#             try:
#                 dobjs = TakeSnapshots([path,])
#                 os.rename(path, newpath)
#                 editOk = True
#                 if dobjs:
#                     self.RefreshView(dobjs)
#             except OSError:
#                 editOk = False # TODO: notify user of error
        return editOk

#     def DoShowMenu(self, item):
#         """Show context menu"""
#         logger.debug('DoShowMenu')
#         # Check if click was in blank window area
#         activeNode = None
#         try:
#             activeNode = self.GetPyData(item)
#             if not self.menu:
#                 self.menu = wx.Menu()
#                 items = [
#                     [ID_NEW, 'New', None ],
#                     [],
#                     [wx.NewIdRef(), 'Copy', "copy_edit.png"],
#                     [wx.NewIdRef(), 'Paste', "paste_edit.png"],
#                     [ID_DELETE_PROJECT, 'Delete', "delete_obj.png"],
#                     [wx.NewIdRef(), 'Move', None],
#                     [wx.NewIdRef(), 'Rename', None],
#                     [],
#                     [ID_IMPORT, 'Import', "import_prj.png"],
#                     [ID_EXPORT, 'Export', "export.png"],
#                     [],
#                     [wx.NewIdRef(), 'Refresh', "refresh.png"],
#                     [ID_CLOSE_PROJECT, 'Close Project', None],
#                     [wx.NewIdRef(), 'Close Unreleated Projects', None],
#                     [wx.NewIdRef(), 'Run As', "run_exc.png"],
#                     [wx.NewIdRef(), 'Debug As', "debug_exc.png"],
#                     [],
#                     [ID_PROJECT_PROPERTIES, 'Properties', "project_properties.png"],
#                     ]
#                 #
#                 for mi_tup in items:
#                     if len(mi_tup) > 0:
#                         if mi_tup[0] == ID_NEW:
#                             sm = wx.Menu()
#                             for menuItemName in menuItemList[self.GetTopLevelParent().selectedPerspectiveName]:
#                                 if len(menuItemName) > 1:
#                                     menuItem = wx.MenuItem(sm, menuItemName[0], menuItemName[1])
#                                     if menuItemName[2]:
#                                         menuItem.SetBitmap(self.fileOperations.getImageBitmap(imageName=menuItemName[2]))
#                                     sm.Append(menuItem)
#                                 else:
#                                     sm.AppendSeparator()
#                             self.menu.Append(mi_tup[0], mi_tup[1], sm)
#                         else:
#                             mitem = wx.MenuItem(self.menu, mi_tup[0], mi_tup[1])
#                             if mi_tup[2] is not None:
#                                 mitem.SetBitmap(self.fileOperations.getImageBitmap(imageName=mi_tup[2]))
#                             self.menu.Append(mitem)
#                             self.Bind(wx.EVT_MENU, self.onRightClickMenu, id=mi_tup[0])
#                     else:
#                         self.menu.AppendSeparator()
# #                         bmp = wx.ArtProvider.GetBitmap(str(mi_tup[2]), wx.ART_MENU)
# #                         mitem.SetBitmap(bmp)
#         except Exception as e:
#             logger.error(e)
#             pass
#
#         self.PopupMenu(self.menu)

    #---- End FileTree Interface Methods ----#
#     def onRightClickMenu(self, event):
#         logger.debug('onRightClickMenu')
#         if event.Id == ID_PROJECT_PROPERTIES:
#             logger.debug('ID_PROJECT_PROPERTIES')
#         if event.Id == ID_CLOSE_PROJECT:
#             logger.debug('ID_CLOSE_PROJECT')
#         if event.Id == ID_DELETE_PROJECT:
#             logger.debug('ID_DELETE_PROJECT')
#             for project in setting.activeWorkspace.projects:
#                 for node in self.GetSelections():
# 
#                     if project.projectDirName == self.GetItemText(node):
#                         setting.activeWorkspace.projects.remove(project)
#                     self.Delete(node)
# #                     self.initProjects()
# #                     self.RemoveWatchDirectory(dname)
#         if event.Id == ID_IMPORT:
#             logger.debug('ID_IMPORT')

    def OpenFiles(self, filesWithImage=[]):
        """Open the list of files in Editra for editing
        @param files: list of file names

        """
        to_open = list()
        for fileWithImage in filesWithImage:
            fname = fileWithImage[0]
            try:
                res = os.stat(fname)[0]
                # isRegularFile or IsDirectory
                if stat.S_ISREG(res):
                    to_open.append(fileWithImage)

                elif  stat.S_ISDIR(res):
                    # TODO: need to think on it.
                    pass
            except (IOError, OSError) as msg:
                logger.debug("[filebrowser][err] %s" % str(msg))

        # TODO : Need to work on it.
        if hasattr(self.GetTopLevelParent(), '_mgr'):

            for fileWithImage in to_open:
                filePath = fileWithImage[0]
                fileName = os.path.split(fileWithImage[0])[-1]
                file_ext = fileName.split('.')[-1]
                window = EditorWindowManager().getWindow(self, filePath)
#                 mainStc = MainStc(self, text=FileOperations().readFile(filePath=fileWithImage[0]))
#                 mainStc.SetFileName(filePath)
#                 mainStc.SetModTime(os.path.getmtime(filePath))
# #                 mainStc.SetText(FileOperations().readFile(filePath=fileWithImage[0]))
#                 mainStc.ConfigureLexer(file_ext)
#                 mainStc.SetModified(False)
#                 mainStc.SetSavePoint()
                imageName = self.iconManager.getFileImageNameByExtension(file_ext)
                (name, captionName) = self.getTitleString(window=window, path=fileWithImage[0])
                icon = fileWithImage[1]
#                     imageName=self.iconsDictIndex[extensionName]
                self.GetTopLevelParent()._mgr.addTabByWindow(window=window, icon=icon, imageName=imageName, name=f'{name}-{captionName}', captionName=name, tabDirection=5)
#                     centerPaneTab.window.addTab(name='openFileLoad'+fileName, worksheetPanel=stc)

#         win = wx.GetApp().GetActiveWindow()
#         if win:
#             win.GetNotebook().OnDrop(to_open)

    def getTitleString(self, window=None, path=None):
        """Get the title string to display in the MainWindows title bar
        @return: (unicode) string

        """
#         fname = self.GetFileName()
        title = os.path.split(path)[-1]

        # Its an unsaved buffer
        if not len(title):
            title = path = self.GetTabLabel()

        if window.GetModify() and not title.startswith(u'*'):
            title = u"*" + title
        return title, path

    def OnCompareItems(self, item1, item2):
        """Handle SortItems"""
        data = self.GetPyData(item1)
        if data is not None:
            path1 = int(not os.path.isdir(data))
        else:
            path1 = 0
        tup1 = (path1, data.lower())

        data2 = self.GetPyData(item2)
        if data2 is not None:
            path2 = int(not os.path.isdir(data2))
        else:
            path2 = 0
        tup2 = (path2, data2.lower())

        if tup1 < tup2:
            return -1
        elif tup1 == tup2:
            return 0
        else:
            return 1

    def OnFilesChanged(self, added, deleted, modified):
        """DirectoryMonitor callback - synchronize the view
        with the filesystem.
        @param added: list of paths added
        @param deleted: list of paths removed
        @param modified: list of paths modified

        """
        nodes = self.GetExpandedNodes()
        visible = list()
        for node in nodes:
            visible.extend(self.GetChildNodes(node))

        # Remove any deleted file objects
        for fobj in deleted:
            for item in visible:
                path = self.GetPyData(item)
                if fobj.Path == path:
                    self.Delete(item)
                    visible.remove(item)
                    break

        # Add any new file objects to the view
        pathCache = dict()
        needsort = list()
        for fobj in added:
            # apply filters to any new files
#             if not self.ShouldDisplayFile(fobj.Path):
#                 continue
            dpath = os.path.dirname(fobj.Path)
            for item in nodes:
                path = self.GetPyData(item)
                if path == dpath:
                    # prevent duplicates from being added
                    if path not in pathCache:
                        pathCache[path] = self.GetNodePaths(item)
                        if fobj.Path in pathCache[path]:
                            continue

                    self.AppendFileNode(item, fobj.Path)
                    if item not in needsort:
                        needsort.append(item)
                    break

        # Re-sort display
        for item in needsort:
            self.SortChildren(item)

    def OnMenu(self, evt):
        """Handle the context menu events for performing
        filesystem operations

        """
        logger.debug(f'OnMenu{ evt.Id}')
        e_id = evt.Id

#         path = self._menu.GetUserData('active_node')
#         paths = self._menu.GetUserData('selected_nodes')

        def Opener(paths):
            """File opener job
            @param paths: list of paths

            """
#             for fname in paths:
#                 subprocess.call([FILEMAN_CMD, fname])
#                 time.sleep(.25)
#
#         if e_id == ID_EDIT:
#             self.OpenFiles(paths)
#         elif e_id == ID_OPEN:
#             ed_thread.EdThreadPool().QueueJob(Opener, paths)
#         elif e_id == ID_REVEAL:
#             dpaths = [os.path.dirname(fname) for fname in paths]
#             dpaths = list(set(dpaths))
#             ed_thread.EdThreadPool().QueueJob(Opener, dpaths)
#         elif e_id == wx.ID_REFRESH:
#             # Refresh the view
#             self.RefreshView()
#         elif e_id == ID_SEARCH_DIR:
#             if len(paths):
#                 path = paths[0] # Go off of the first selected item
#                 if not os.path.isdir(path):
#                     path = os.path.dirname(path)
#                 mdata = dict(mainw=self._mw, lookin=path)
#                 ed_msg.PostMessage(ed_msg.EDMSG_FIND_SHOW_DLG, mdata)
#         elif e_id == ID_GETINFO:
#             last = None
#             for fname in paths:
#                 info = ed_mdlg.EdFileInfoDlg(self.TopLevelParent, fname)
#                 if last is None:
#                     info.CenterOnParent()
#                 else:
#                     lpos = last.GetPosition()
#                     info.SetPosition((lpos[0] + 14, lpos[1] + 14))
#                 info.Show()
#                 last = info
#         elif e_id == ID_RENAME:
#             item = self._menu.GetUserData('item_id')
#             self.EditLabel(item)
#         elif e_id == ID_NEW_FOLDER:
#             name = wx.GetTextFromUser(_("Enter folder name:"), _("New Folder"),
#                                       parent=self.TopLevelParent)
#             if name:
#                 dobjs = TakeSnapshots([path,])
#                 err, msg = ebmlib.MakeNewFolder(path, name)
#                 if not err:
#                     wx.MessageBox(msg, _("Failed to create folder"),
#                                   style=wx.OK|wx.CENTER|wx.ICON_ERROR)
#                 else:
#                     self.RefreshView(dobjs)
#         elif e_id == ID_NEW_FILE:
#             name = wx.GetTextFromUser(_("Enter file name:"), _("New File"),
#                                       parent=self.TopLevelParent)
#             if name:
#                 dobjs = TakeSnapshots([path,])
#                 err, msg = ebmlib.MakeNewFile(path, name)
#                 if not err:
#                     wx.MessageBox(msg, _("Failed to create file"),
#                                   style=wx.OK|wx.CENTER|wx.ICON_ERROR)
#                 else:
#                     self.RefreshView(dobjs)
#         elif e_id == ID_DUPLICATE:
#             dobjs = TakeSnapshots(paths)
#             for fname in paths:
#                 DuplicatePath(fname)
#             self.RefreshView(dobjs)
#         elif e_id == ID_ARCHIVE:
#             dobjs = TakeSnapshots([path,])
#             MakeArchive(path)
#             self.RefreshView(dobjs)
#         elif e_id == ID_DELETE:
#             dobjs = TakeSnapshots(paths)
#             MoveToTrash(paths)
#             self.RefreshView(dobjs)
#         else:
#             evt.Skip()
#             return

    def OnThemeChanged(self, msg):
        """Update the icons when the icon theme has changed
        @param msg: Message Object

        """
        self.iconManager.RefreshImageList(self.ImageList)

    def OnConfig(self, msg):
        """Handle updates for filebrowser preference updates"""
        # TODO: refresh tree for hidden files on/off
        pass

#     @ed_msg.mwcontext
    def OnPageClosing(self, msg):
        self.isClosing = True

#     @ed_msg.mwcontext
    def OnPageChange(self, msg):
        """Synchronize selection with the notebook page changes
        @param msg: MessageObject
        @todo: check if message is from a page closing and avoid updates

        """
        if self.isClosing:
            self.isClosing = False
            return

#         if not fbcfg.GetFBOption(fbcfg.FB_SYNC_OPT, True):
#             return

        nbdata = msg.GetData()
        if not nbdata[0]:
            return

        pg_count = nbdata[0].GetPageCount()
        if nbdata[1] > pg_count  or nbdata[1] < 0:
            # Page is out of range, something has changed since the
            # message was sent.
            return

        page = nbdata[0].GetPage(nbdata[1])
        if page:
            path = getattr(page, 'GetFileName', lambda: u"")()
            if len(path) and os.path.exists(path):
                # Delay selection for smoother operation when many
                # page change events are received in a short time.
                if self.syncTimer.IsRunning():
                    self.syncTimer.Stop()
                self._cpath = path
                self.syncTimer.Start(500, True)

#     @refreshAfter
#     def OnTimer(self, evt):
#         """Handle tab synchronization"""
#         if self._cpath:
#             self.SelectFile(self._cpath)

    def RefreshView(self, paths=None):
        """Refresh file view of monitored directories"""
        self._monitor.Refresh(paths)

    def GetMainWindow(self):
        """Get the main window, needed by L{ed_msg.mwcontext}"""
        return self._mw

    def SetMainWindow(self, mainw):
        """Set the main window this browser belongs to.
        @param mainw: MainWindow or None

        """
        self._mw = mainw


class FileBrowserMimeManager():

    def __init__(self):
        self.fileOperations = FileOperations()
        self.fileImageExtensionDict = {
#             '.exe':'exe.png',
            '.xml':'xml.png',
            '.java':'java.png',
            '.py':'python_module.png',
            '.html':'web.png',
            '.md':'markdown.png',
            '.jar':'jar_file.png',
            '.yaml':'yaml.png',
            '.yml':'yaml.png',
            '.spec':'spec.png',
            }
        pass

    def PopulateImageList(self, imglist):
        """Populate an ImageList with the icons for the file tree
        @param imglist: wx.ImageList instance (16x16)

        """
        imglist.RemoveAll()
        self.iconsDictIndex = {}
        count = 0
        for extensionName in ['.pdf', '.zip', '.xlsx', '.xls', '.doc', '.ppt', '.7z', '.png', '.md', '.json',
                              '.docx', '.css', '.js', '.bat', '.csv', '.txt', '.emf', '.rtf', '.chm', '.odt', '.ini',
                              '.rar', '.msi', '.avi', '.mp4', '.mov', '.flv', '.mpg', '.gif', '.spec',
                              '.wma', '.mp3', '.wav', '.aac', '.m4a', '.dmg', '.tar', '.gz', ]:
            try:
                icon = self.getIconByExtension(extensionName)
                if icon:
                    imglist.Add(icon)
                    self.iconsDictIndex[extensionName] = count
                    self.fileImageExtensionDict[extensionName] = extensionName
                    count += 1
                    wx.LogNull()
            except Exception as e:
                logger.error(e, exc_info=True)
        for imageName in ['fileType_filter.png', 'folder.png', 'folder_view.png', 'harddisk.png', 'usb.png', 'stop.png',
                          'java.png', 'python_module.png', 'xml.png', 'python.png', 'java.png', 'jar_file.png', 'markdown.png',
                          'yaml.png', 'spec.png', 'web.png' ]:
            imglist.Add(self.fileOperations.getImageBitmap(imageName=imageName))
            self.iconsDictIndex[imageName] = count
            count += 1

    def getIconByExtension(self, extension=".txt"):
        '''
        @param extension:
        @return icon
        '''
        icon = None
        noLog = wx.LogNull()
        logger.debug(extension)
        fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)

        if fileType is None:
            logger.debug("File extension not found.")
        else:
            try:
                icon, file, idx = fileType.GetIconInfo()
                if icon.IsOk():
                    icon = icon
            except :
                logger.error('some error :' + extension)
#        This is to supress warning
        del noLog
        return icon

    def GetImageIndex(self, path, expanded=False):
        """Get the appropriate file index for the given path
        @param path: file name or path

        """
        imageName = 'fileType_filter.png'
        if not os.access(path, os.R_OK):
            imageName = 'stop.png'
        elif os.path.ismount(path):
            imageName = 'harddisk.png'
            if wx.Platform == '__WXMSW__':
                dtype = GetWindowsDriveType(path)
                if isinstance(dtype, RemovableDrive):
                    imageName = 'usb.png'
                elif isinstance(dtype, CDROMDrive):
                    imageName = 'cdrom.png'
        elif os.path.isdir(path):
            if expanded:
                imageName = 'folder_view.png'
            else:
                imageName = 'folder.png'
        elif os.path.isfile(path):
            filename, fileExtension = os.path.splitext(path)
            fileExtension = fileExtension.lower()
            if fileExtension and self.getFileImageNameByExtension(fileExtension):
                imageName = self.getFileImageNameByExtension(fileExtension)

        return self.iconsDictIndex[imageName]

    def getFileImageNameByExtension(self, fileExtension=None):
        if fileExtension:
            if '.' not in fileExtension:
                fileExtension = '.' + fileExtension
        imageName = None

        if fileExtension in self.fileImageExtensionDict.keys():
            imageName = self.fileImageExtensionDict[fileExtension]

        return imageName

#     def IsDevice(self, path):
#         """Is the path some sort of device"""
#         if os.path.ismount(path):
#             self._ftype = FBMimeMgr.IMG_HARDDISK
#             if wx.Platform == '__WXMSW__':
#                 dtype = GetWindowsDriveType(path)
#                 if isinstance(dtype, RemovableDrive):
#                     self._ftype = FBMimeMgr.IMG_USB
#                 elif isinstance(dtype, CDROMDrive):
#                     self._ftype = FBMimeMgr.IMG_CD
#         rval = self._ftype != FBMimeMgr.IMG_FILE
#         return rval
# class FBMimeMgr(object):
#     """Manager class for managing known file types and icons"""
#     IMAGES = range(18)
#     IMG_COMPUTER, \
#     IMG_FLOPPY, \
#     IMG_HARDDISK, \
#     IMG_CD, \
#     IMG_USB, \
#     IMG_FOLDER, \
#     IMG_FOLDER_OPEN, \
#     IMG_NO_ACCESS, \
#     IMG_BIN, \
#     IMG_FILE, \
#     IMG_PYTHON, \
#     IMG_BOO, \
#     IMG_CSS, \
#     IMG_HTML, \
#     IMG_JAVA, \
#     IMG_PHP, \
#     IMG_RUBY, \
#     IMG_SHELL = IMAGES
#     IMGMAP = { IMG_COMPUTER : ID_COMPUTER,
#                IMG_FLOPPY  : ID_FLOPPY,
#                IMG_HARDDISK : ID_HARDDISK,
#                IMG_CD      : ID_CDROM,
#                IMG_USB     : ID_USB,
#                IMG_FOLDER  : ID_FOLDER,
#                IMG_FOLDER_OPEN : ID_OPEN,
#                IMG_NO_ACCESS : ID_STOP,
#                IMG_BIN     : ID_BIN_FILE,
#                IMG_FILE    : ID_FILE,
#                IMG_PYTHON  : ID_LANG_PYTHON,
#                IMG_BOO     : ID_LANG_BOO,
#                IMG_CSS     : ID_LANG_CSS,
#                IMG_HTML    : ID_LANG_HTML,
#                IMG_JAVA    : ID_LANG_JAVA,
#                IMG_PHP     : ID_LANG_PHP,
#                IMG_RUBY    : ID_LANG_RUBY,
#                IMG_SHELL   : ID_LANG_BASH }
#     def __init__(self):
#         super(FBMimeMgr, self).__init__()
#
#         # Attributes
#         self._ftype = FBMimeMgr.IMG_FILE
#
#     @classmethod
#     def PopulateImageList(cls, imglist):
#         """Populate an ImageList with the icons for the file tree
#         @param imglist: wx.ImageList instance (16x16)
#
#         """
#         imglist.RemoveAll()
#         for img in FBMimeMgr.IMAGES:
#             imgid = FBMimeMgr.IMGMAP[img]
#             bmp = wx.ArtProvider.GetBitmap(str(imgid), wx.ART_MENU)
#             if bmp.IsOk():
#                 imglist.Add(bmp)
#
#     @classmethod
#     def RefreshImageList(cls, imglist):
#         """Refresh all icons from the icon manager"""
#         for idx, img in enumerate(FBMimeMgr.IMAGES):
#             imgid = FBMimeMgr.IMGMAP[img]
#             bmp = wx.ArtProvider.GetBitmap(str(imgid), wx.ART_MENU)
#             if bmp.IsOk():
#                 imglist.Replace(idx, bmp)
#
#     def GetImageIndex(self, path, expanded=False):
#         """Get the appropriate file index for the given path
#         @param path: file name or path
#
#         """
#         self._ftype = FBMimeMgr.IMG_FILE
#         if not os.access(path, os.R_OK):
#             self._ftype = FBMimeMgr.IMG_NO_ACCESS
#         elif self.IsDevice(path):
#             pass
#         elif os.path.isdir(path):
#             if expanded:
#                 self._ftype = FBMimeMgr.IMG_FOLDER_OPEN
#             else:
#                 self._ftype = FBMimeMgr.IMG_FOLDER
#         elif self.IsKnownTextFile(path):
#             pass
#         elif self.IsKnownBinType(path):
#             pass
#         return self._ftype
#
#     def IsKnownTextFile(self, path):
#         """Is a known text file type
#         @param path: file path / name
#
#         """
#         tpath = os.path.basename(path)
#         ext = GetFileExtensions(tpath)
# #         etype = GetIdFromExt(ext)
#         tmap = { ID_LANG_PYTHON : FBMimeMgr.IMG_PYTHON,
#                  ID_LANG_BOO : FBMimeMgr.IMG_BOO,
#                  ID_LANG_CSS : FBMimeMgr.IMG_CSS,
#                  ID_LANG_HTML : FBMimeMgr.IMG_HTML,
#                  ID_LANG_JAVA : FBMimeMgr.IMG_JAVA,
#                  ID_LANG_PHP : FBMimeMgr.IMG_PHP,
#                  ID_LANG_RUBY : FBMimeMgr.IMG_RUBY,
#                  ID_LANG_BASH : FBMimeMgr.IMG_SHELL }
# #         self._ftype = tmap.get(etype, FBMimeMgr.IMG_FILE)
#         return self._ftype != FBMimeMgr.IMG_FILE
#
#     def IsKnownBinType(self, path):
#         """Is a known binary file type
#         @param path: file path / name
#
#         """
#         ext = GetFileExtension(path)
#         if ext in ('exe', 'dll', 'so'): # TODO better mapping
#             self._ftype = FBMimeMgr.IMG_BIN
#         else:
#             return False
#         return True
#
#     def IsDevice(self, path):
#         """Is the path some sort of device"""
#         if os.path.ismount(path):
#             self._ftype = FBMimeMgr.IMG_HARDDISK
#             if wx.Platform == '__WXMSW__':
#                 dtype = GetWindowsDriveType(path)
#                 if isinstance(dtype, RemovableDrive):
#                     self._ftype = FBMimeMgr.IMG_USB
#                 elif isinstance(dtype, CDROMDrive):
#                     self._ftype = FBMimeMgr.IMG_CD
#         rval = self._ftype != FBMimeMgr.IMG_FILE
#         return rval


class FolderIconManager():

    def __init__(self):
        self.fileOperations = FileOperations()
        self.fileImageExtensionDict = {
#             '.exe':'exe.png',
            '.xml':'xml.png',
            '.java':'java.png',
            '.py':'python_module.png',
            '.html':'web.png',
            '.md':'markdown.png',
            '.jar':'jar_file.png',
            '.yaml':'yaml.png',
            '.yml':'yaml.png',

            }
        pass

    def PopulateImageList(self, imglist):
        """Populate an ImageList with the icons for the file tree
        @param imglist: wx.ImageList instance (16x16)

        """
        imglist.RemoveAll()
        self.iconsDictIndex = {}
        count = 0
        for extensionName in ['.pdf', '.zip', '.xlsx', '.xls', '.doc', '.ppt', '.7z', '.png', '.md', '.json',
                              '.docx', '.css', '.js', '.bat', '.csv', '.txt', '.emf', '.rtf', '.chm', '.odt', '.ini',
                              '.rar', '.msi', '.avi', '.mp4', '.mov', '.flv', '.mpg', '.gif',
                              '.wma', '.mp3', '.wav', '.aac', '.m4a', '.dmg', '.tar', '.gz', ]:
            try:
                icon = self.getIconByExtension(extensionName)
                if icon:
                    imglist.Add(icon)
                    self.iconsDictIndex[extensionName] = count
                    self.fileImageExtensionDict[extensionName] = extensionName
                    count += 1
                    wx.LogNull()
            except Exception as e:
                logger.error(e, exc_info=True)
        for imageName in ['fileType_filter.png', 'folder.png', 'folder_view.png', 'harddisk.png', 'usb.png', 'stop.png',
                          'java.png', 'python_module.png', 'xml.png', 'python.png', 'java.png', 'jar_file.png', 'markdown.png',
                          'yaml.png', 'package_obj.png', 'web.png' ]:
            imglist.Add(self.fileOperations.getImageBitmap(imageName=imageName))
            self.iconsDictIndex[imageName] = count
            count += 1

    def getIconByExtension(self, extension=".txt"):
        icon = None
        noLog = wx.LogNull()
        logger.debug(extension)
        fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)

        if fileType is None:
            logger.debug("File extension not found.")
        else:
            try:
                icon, file, idx = fileType.GetIconInfo()
                if icon.IsOk():
                    icon = icon
            except :
                logger.error('some error :' + extension)
#        This is to supress warning
        del noLog
        return icon

    def GetImageIndex(self, path, expanded=False):
        """Get the appropriate file index for the given path
        @param path: file name or path

        """
        imageName = 'fileType_filter.png'
        if not os.access(path, os.R_OK):
            imageName = 'stop.png'

        elif os.path.isdir(path):
            if expanded:
                imageName = 'folder_view.png'
            else:
                imageName = 'folder.png'
        elif os.path.isfile(path):
            filename, fileExtension = os.path.splitext(path)
            fileExtension = fileExtension.lower()
            if fileExtension and self.getFileImageNameByExtension(fileExtension):
                imageName = self.getFileImageNameByExtension(fileExtension)

        return self.iconsDictIndex[imageName]

    def getFileImageNameByExtension(self, fileExtension=None):
        imageName = None

        if fileExtension in self.fileImageExtensionDict.keys():
            imageName = self.fileImageExtensionDict[fileExtension]

        return imageName


if __name__ == '__main__':
    app = wx.App(False)
    frame = NewFileFrame(None, 'New File', selectedPath="c:\work\python-project")
    frame.Show()
    app.MainLoop()
