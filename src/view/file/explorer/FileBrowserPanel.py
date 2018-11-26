
import logging.config
import os
import stat
import time

import wx

from src.view.constants import LOG_SETTINGS
from src.view.file.explorer._filetree import FileTree
from src.view.file.explorer.eclutil import Freezer

from src.view.util.FileOperationsUtil import FileOperations
from src.view.util.osutil import GetWindowsDrives, GetWindowsDriveType, \
    RemovableDrive, CDROMDrive

# from src.view.syntax.syntax import GetIdFromExt
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class FileBrowser(FileTree):
    
    """FileExplorer Tree"""

    def __init__(self, parent):
        self._mime = FileBrowserMimeManager()

        super(FileBrowser, self).__init__(parent)

        # Attributes
        self._mw = None
#         self._menu = ebmlib.ContextMenuManager()
#         self._monitor = ebmlib.DirectoryMonitor(checkFreq=-1) # manual refresh...
#         self._monitor.SubscribeCallback(self.OnFilesChanged)
#         self._monitor.StartMonitoring()
        self.isClosing = False
        self.syncTimer = wx.Timer(self)
        self._cpath = None

        # Setup
        self.SetupImageList()
        if wx.Platform == '__WXMSW__':
            for dname in GetWindowsDrives():
                if os.path.exists(dname.Name):
                    self.AddWatchDirectory(dname.Name)
        else:
            self.AddWatchDirectory("/")

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnMenu)

#         self.Bind(wx.EVT_TIMER, self.OnTimer)
#         ed_msg.Subscribe(self.OnThemeChanged, ed_msg.EDMSG_THEME_CHANGED)
#         ed_msg.Subscribe(self.OnPageChange, ed_msg.EDMSG_UI_NB_CHANGED)
#         ed_msg.Subscribe(self.OnPageClosing, ed_msg.EDMSG_UI_NB_CLOSING)
#         ed_msg.Subscribe(self.OnConfig, ed_msg.EDMSG_PROFILE_CHANGE + (fbcfg.FB_PROF_KEY,))
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
        self._mime.PopulateImageList(self.ImageList)
        
#         super().DoSetupImageList()

    def DoGetFileImage(self, path):
        """Get the image for the given item"""
        return self._mime.GetImageIndex(path)

    def DoGetToolTip(self, item):
        """Get the tooltip to show for an item
        @return: string or None

        """
        tip = None
#         if self.GetItemImage(item) == self._mime.IMG_NO_ACCESS:
#             tip = _("Access Denied")
#        elif item: # Slightly annoying on GTK disable for now
#            tip = self.GetPyData(item)
        return tip

    def DoItemActivated(self, item):
        """Override to handle item activation
        @param item: TreeItem

        """
        self.OpenFiles(self.GetSelectedFiles())

    def DoItemCollapsed(self, item):
        """Handle when an item is collapsed"""
        d = self.GetPyData(item)
#         if d:
#             self._monitor.RemoveDirectory(d)
        super(FileBrowser, self).DoItemCollapsed(item)
        self.SetItemImage(item, self._mime.GetImageIndex(d, False))

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
        busy = wx.BusyCursor()  # can take a few seconds on big directories

        d = None
        try:
            d = self.GetPyData(item)
        except wx.PyAssertionError:
            logger.debug("[FileBrowser][err] FileBrowser.DoItemExpanding")
            return

        if d and os.path.exists(d) and os.access(d, os.R_OK):
            contents = FileBrowser.GetDirContents(d)
            t1 = time.time()
            with Freezer(self) as _tmp:
                self.AppendFileNodes(item, contents)
                self.SortChildren(item)
            logger.debug("[FileBrowser][info] Tree expand time: %f" % (time.time() - t1))
 
#             if not self._monitor.AddDirectory(d):
#                 self.SetItemImage(item, self._mime.IMG_NO_ACCESS)
#                 return

        # Update tree image
        self.SetItemImage(item, self._mime.GetImageIndex(d, True))

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

    def DoShowMenu(self, item):
        """Show context menu"""
        # Check if click was in blank window area
        activeNode = None
        try:
            activeNode = self.GetPyData(item)
        except wx.PyAssertionError:
            pass

#         if not self._menu.Menu:
#             self._menu.Menu = wx.Menu()
#             # TODO: bother with theme changes ...?
#             items = [(ID_EDIT, _("Edit"), None),
#                      (ID_OPEN, _("Open with " + FILEMAN), ID_OPEN),
#                      (ID_REVEAL, _("Reveal in " + FILEMAN), None),
#                      (wx.ID_SEPARATOR, '', None),
#                      (wx.ID_REFRESH, _("Refresh"), ID_REFRESH),
#                      (wx.ID_SEPARATOR, '', None),
#                      (ID_MARK_PATH, _("Bookmark Selected Path(s)"),
#                       ID_ADD_BM),
#                      (wx.ID_SEPARATOR, '', None),
#                      (ID_SEARCH_DIR, _("Search in directory"), ID_FIND),
#                      (wx.ID_SEPARATOR, '', None),
#                      (ID_GETINFO, _("Get Info"), None),
#                      (ID_RENAME, _("Rename"), None),
#                      (wx.ID_SEPARATOR, '', None),
#                      (ID_NEW_FOLDER, _("New Folder"), ID_FOLDER),
#                      (ID_NEW_FILE, _("New File"), ID_NEW),
#                      (wx.ID_SEPARATOR, '', None),
#                      (ID_DUPLICATE, _("Duplicate"), None),
#                      (ID_ARCHIVE, _("Create Archive of \"%s\"") % '', None),
#                      (wx.ID_SEPARATOR, '', None),
#                      (ID_DELETE, TrashString(), ID_DELETE),
#                     ]
# 
#             for mi_tup in items:
#                 mitem = wx.MenuItem(self._menu.Menu, mi_tup[0], mi_tup[1])
#                 if mi_tup[2] is not None:
#                     bmp = wx.ArtProvider.GetBitmap(str(mi_tup[2]), wx.ART_MENU)
#                     mitem.SetBitmap(bmp)
# 
#                 self._menu.Menu.AppendItem(mitem)

        # Set contextual data
        self._menu.SetUserData('item_id', item)
        self._menu.SetUserData('active_node', activeNode)
        self._menu.SetUserData('selected_nodes', self.GetSelectedFiles())

        # Update Menu
#         mitem = self._menu.Menu.FindItemById(ID_ARCHIVE)
#         if mitem != wx.NOT_FOUND:
#             path = self._menu.GetUserData('active_node')
#             mitem.SetText(_("Create Archive of \"%s\"") % \
#                           path.split(os.path.sep)[-1])
#         for mitem in (ID_DUPLICATE,):
#             self._menu.Menu.Enable(mitem, len(self.GetSelections()) == 1)

        self.PopupMenu(self._menu.Menu)

    #---- End FileTree Interface Methods ----#

    @staticmethod
    def OpenFiles(files):
        """Open the list of files in Editra for editing
        @param files: list of file names

        """
        to_open = list()
        for fname in files:
            try:
                res = os.stat(fname)[0]
                if stat.S_ISREG(res) or stat.S_ISDIR(res):
                    to_open.append(fname)
            except (IOError, OSError) as msg:
                logger.debug("[filebrowser][err] %s" % str(msg))

        win = wx.GetApp().GetActiveWindow()
        if win:
            win.GetNotebook().OnDrop(to_open)

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
        e_id = evt.Id
        path = self._menu.GetUserData('active_node')
        paths = self._menu.GetUserData('selected_nodes')

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
        self._mime.RefreshImageList(self.ImageList)

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
            '.py':'python.png',
#             '.cpp':'cpp.png',
            
            }
        pass
    
    def PopulateImageList(self, imglist):
        """Populate an ImageList with the icons for the file tree
        @param imglist: wx.ImageList instance (16x16)
 
        """
        imglist.RemoveAll()
        self.iconsDictIndex = {}
        count = 0
        for imageName in ['fileType_filter.png', 'folder.png', 'folder_view.png', 'harddisk.png', 'usb.png', 'stop.png',
                          'java.png', 'python_module.png', 'xml.png']:
            imglist.Add(self.fileOperations.getImageBitmap(imageName=imageName))
            self.iconsDictIndex[imageName] = count
            count += 1

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
            if fileExtension and self.getFileImageNameByExtension(fileExtension):
                imageName = self.getFileImageNameByExtension(fileExtension)
        return self.iconsDictIndex[imageName]
    
    def getFileImageNameByExtension(self, fileExtension=None):
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


# Test
if __name__ == '__main__':
    app = wx.App(False)
    f = wx.Frame(None)
    ft = FileBrowser(f)

    f.Show()
    app.MainLoop()
