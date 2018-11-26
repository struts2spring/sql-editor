
"""

Base class control for displaying a file system in a hierarchical manor.

"""

# Imports
import os
import wx

import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.util.FileOperationsUtil import FileOperations
from src.view.util.osutil import GetWindowsDrives
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class FileTree(wx.TreeCtrl):
    """Simple base control for displaying directories and files in a
    hierarchical view.

    """
    def __init__(self, parent):
        super(FileTree, self).__init__(parent,
                                       style=wx.TR_HIDE_ROOT|
                                             wx.TR_FULL_ROW_HIGHLIGHT|
                                             wx.TR_LINES_AT_ROOT|
                                             wx.TR_HAS_BUTTONS|
                                             wx.TR_MULTIPLE|
                                             wx.TR_EDIT_LABELS)

        # Attributes
        self._watch = list() # Root directories to watch
        self._il = None
        self._editlabels = True

        # Setup
        self.SetupImageList()
        self.AddRoot('root')
        self.SetItemData(self.RootItem, "root")

        # Event Handlers
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self._OnGetToolTip)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._OnItemActivated)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self._OnItemCollapsed)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self._OnItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self._OnMenu)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self._OnBeginEdit)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self._OnEndEdit)

    def _OnBeginEdit(self, evt):
        logger.debug('_OnBeginEdit')
        if not self._editlabels:
            evt.Veto()
        else:
            item = evt.GetItem()
            if self.DoBeginEdit(item):
                evt.Skip()
            else:
                evt.Veto()

    def _OnEndEdit(self, evt):
        logger.debug('_OnEndEdit')
        if self._editlabels:
            item = evt.GetItem()
            newlabel = evt.GetLabel()
            if self.DoEndEdit(item, newlabel):
                evt.Skip()
                return
        evt.Veto()

    def _OnGetToolTip(self, evt):
#         logger.debug('_OnGetToolTip')
        item = evt.GetItem()
        tt = self.DoGetToolTip(item)
        if tt:
            evt.ToolTip = tt
        else:
            evt.Skip()

    def _OnItemActivated(self, evt):
        logger.debug('_OnItemActivated')
        item = evt.GetItem()
        self.DoItemActivated(item)
        evt.Skip()

    def _OnItemCollapsed(self, evt):
        logger.debug('_OnItemCollapsed')
        item = evt.GetItem()
        self.DoItemCollapsed(item)
        evt.Skip()

    def _OnItemExpanding(self, evt):
        logger.debug('_OnItemExpanding')
        item = evt.GetItem()
        self.DoItemExpanding(item)
        evt.Skip()

    def _OnMenu(self, evt):
        logger.debug('_OnMenu')
        try:
            item = evt.GetItem()
            self.DoShowMenu(item)
        except:
            pass

    #---- Properties ----#

    SelectedFiles = property(lambda self: self.GetSelectedFiles())

    #---- Overridable methods ----#

    def DoBeginEdit(self, item):
        logger.debug('DoBeginEdit')
        """Overridable method that will be called when
        a user has started to edit an item.
        @param item: TreeItem
        return: bool (True == Allow Edit)

        """
        return False

    def DoEndEdit(self, item, newlabel):
        logger.debug('DoEndEdit')
        """Overridable method that will be called when
        a user has finished editing an item.
        @param item: TreeItem
        @param newlabel: unicode (newly entered value)
        return: bool (True == Change Accepted)

        """
        return False

    def DoGetToolTip(self, item):
        """Get the tooltip to show for an item
        @return: string or None

        """
#         logger.debug('DoGetToolTip')
        data = self.GetItemData(item)
        return data

    def DoItemActivated(self, item):
        """Override to handle item activation
        @param item: TreeItem

        """
        logger.debug('DoItemActivated')
        pass

    def DoItemCollapsed(self, item):
        """Handle when an item is collapsed
        @param item: TreeItem

        """
        logger.debug('DoItemCollapsed')
        
        self.DeleteChildren(item)

    def DoItemExpanding(self, item):
        """Handle when an item is expanding
        @param item: TreeItem

        """
        logger.debug('DoItemExpanding')
        d = self.GetPyData(item)
        if d and os.path.exists(d):
            contents = FileTree.GetDirContents(d)
            for p in contents:
                self.AppendFileNode(item, p)

    def DoShowMenu(self, item):
        """Context menu has been requested for the given item.
        @param item: wx.TreeItem

        """
        logger.debug('DoShowMenu')
        pass

    def DoSetupImageList(self):
        """Add the images to the control's ImageList. It is guaranteed
        that self.ImageList is valid and empty when this is called.

        """
        logger.debug('DoSetupImageList')
        self.fileOperations = FileOperations()
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_MENU, (16,16))
        self.ImageList.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_MENU, (16,16))
        self.ImageList.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_MENU, (16,16))
        self.ImageList.Add(bmp)
        
        iconsPresent=self.getExtensionWithBmp()
        logger.debug(iconsPresent)
        count=3
        self.iconsDictByIndex={}
        self.iconsDictByExtension={}
        for iconInfo in iconsPresent:
            self.ImageList.Add(iconInfo[1])
            iconInfo.append(count)
            self.iconsDictByExtension[iconInfo[0][0]]=iconInfo
            self.iconsDictByIndex[count]=iconInfo
            count =count+1
        logger.debug(self.iconsDictByIndex)

    def DoGetFileImage(self, path):
        """Get the index of the image from the image list to use
        for the file.
        @param path: Absolute path of file
        @return: long

        """
        # TODO: image handling
        logger.debug('DoGetFileImage')
        if not os.access(path, os.R_OK):
            img = 2
        else:
            if os.path.isdir(path):
                img = 0 # Directory image
            else:
                filename, file_extension = os.path.splitext(path)
                if file_extension in self.iconsDictByExtension.keys():
                    iconInfo=self.iconsDictByExtension[file_extension]
                    if iconInfo:
                        img =iconInfo[3]
                else:
                    img = 1 # Normal file image
#                 self.getMimeType()
        return img

    def getIconByExtension(self, file_extension=".txt"):
        fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(file_extension)
        bmp = wx.Bitmap(16,16) 
        if fileType is None:
            logger.debug("File extension not found.")
        else:
            icon, file, idx = fileType.GetIconInfo()
            if icon.IsOk():
                bmp.CopyFromIcon(icon) 
                bmp = bmp.ConvertToImage() 
                # Rescale it, usually it's not 16x16 
                bmp.Rescale(16,16) 
                bmp = wx.BitmapFromImage(bmp) 
        return bmp
    
    def getExtensionWithBmp(self):
        # Locate all file types 
        mtypes = wx.TheMimeTypesManager.EnumAllFileTypes() 
        
        iconsPresent=[]
        iconsNotPresent=[]
        for mt in mtypes: 
        
            # Loop over all file types 
            fileType = wx.TheMimeTypesManager.GetFileTypeFromMimeType(mt) 
            
            if fileType is not None: 
                # Get the icon information for that file extension 
                nntype = fileType.GetIconInfo() 
        
                if nntype is not None: 
                    # Get the icon for that file extension 
                    icon, file, idx = nntype 
        
                    if icon.IsOk():
                        bmp = wx.Bitmap(16,16) 
                        bmp.CopyFromIcon(icon) 
                        bmp = bmp.ConvertToImage() 
                        # Rescale it, usually it's not 16x16 
                        bmp.Rescale(16,16) 
                        bmp = wx.Bitmap(bmp) 
                        iconsPresent.append([fileType.GetExtensions(), bmp, file])
                    else:
                        iconsNotPresent.append(nntype)
                else:
                    iconsNotPresent.append(fileType)
            else:
                iconsNotPresent.append(mt)
        return iconsPresent
    #---- End Overrides ----#

    #---- Properties ----#

    WatchDirs = property(lambda self: self._watch)

    #---- FileTree Api ---#

    def AddWatchDirectory(self, dname):
        """Add a directory to the controls top level view
        @param dname: directory path
        @return: TreeItem or None
        @todo: add additional api for getting already existing nodes based
               on path.

        """
        logger.debug('AddWatchDirectory')
        assert os.path.exists(dname), "Path(%s) doesn't exist!" % dname
        if dname not in self._watch:
            self._watch.append(dname)
            return self.AppendFileNode(self.RootItem, dname)

    def RemoveWatchDirectory(self, dname):
        """Remove a directory from the watch list
        @param dname: directory path

        """
        logger.debug('RemoveWatchDirectory')
        if dname in self._watch:
            self._watch.remove(dname)
            nodes = self.GetChildNodes(self.RootItem)
            for node in nodes:
                data = self.GetPyData(node)
                if dname == data:
                    self.Delete(node)
                    break

    def SetupImageList(self):
        """Setup/Refresh the control's ImageList.
        Override DoSetupImageList to customize the behavior of this method.

        """
        logger.debug('SetupImageList')
        if self._il:
            self._il.Destroy()
            self._il = None
        self._il = wx.ImageList(16, 16)
        self.SetImageList(self._il)
        self.DoSetupImageList()

    def AppendFileNode(self, item, path):
        """Append a child node to the tree
        @param item: TreeItem parent node
        @param path: path to add to node
        @return: new node

        """
        logger.debug('AppendFileNode')
        img = self.DoGetFileImage(path)
        name = os.path.basename(path)
        if not name:
            name = path
        child = self.AppendItem(item, name, img)
        self.SetItemData(child, path)
        if os.path.isdir(path):
            self.SetItemHasChildren(child, True)
        return child

    def AppendFileNodes(self, item, paths):
        """Append a list of child node to the tree. This
        method can be used instead of looping on AppendFileNode
        to get slightly better performance for large sets.
        @param item: TreeItem parent node
        @param paths: list of file paths
        @return: None

        """
        logger.debug('AppendFileNodes')
        getBaseName = os.path.basename
        isDir = os.path.isdir
        getImg = self.DoGetFileImage
        appendNode = self.AppendItem
        setData = self.SetPyData
        for path in paths:
            img = getImg(path)
            name = getBaseName(path)
            if not name:
                name = path
            child = appendNode(item, name, img)
            setData(child, path)
            if isDir(path):
                self.SetItemHasChildren(child, True)

    def GetChildNodes(self, parent):
        """Get all the TreeItemIds under the given parent
        @param parent: TreeItem
        @return: list of TreeItems

        """
        logger.debug('GetChildNodes')
        rlist = list()
        child, cookie = self.GetFirstChild(parent)
        if not child or not child.IsOk():
            return rlist

        rlist.append(child)
        while True:
            child, cookie = self.GetNextChild(parent, cookie)
            if not child or not child.IsOk():
                return rlist
            rlist.append(child)
        return rlist

    def GetExpandedNodes(self):
        """Get all nodes that are currently expanded in the view
        this logically corresponds to all parent directory nodes which
        are expanded.
        @return: list of TreeItems

        """
        logger.debug('GetExpandedNodes')
        def NodeWalker(parent, rlist):
            """Recursively find expanded nodes
            @param parent: parent node
            @param rlist: list (outparam)

            """
            children = self.GetChildNodes(parent)
            for node in children:
                if self.IsExpanded(node):
                    rlist.append(node)
                    NodeWalker(node, rlist)

        nodes = list()
        NodeWalker(self.RootItem, nodes)
        return nodes

    def GetSelectedFiles(self):
        """Get a list of the selected files
        @return: list of strings

        """
        logger.debug('GetSelectedFiles')
        nodes = self.GetSelections()
        files = [ self.GetPyData(node) for node in nodes ]
        return files

    def EnableLabelEditing(self, enable=True):
        """Enable/Disable label editing. This functionality is
        enabled by default.
        @keyword enable: bool

        """
        logger.debug('EnableLabelEditing')
        self._editlabels = enable

    def SelectFile(self, filename):
        """Select the given path
        @param filename: full path to select
        @return: bool

        """
        bSelected = False
        # Find the root
        for node in self.GetChildNodes(self.RootItem):
            dname = self.GetPyData(node)
            if not os.path.isdir(dname):
                dname = os.path.dirname(dname)
            if not dname.endswith(os.sep):
                dname += os.sep
            if filename.startswith(dname):
                filename = filename[len(dname):].split(os.sep)
                if not self.IsExpanded(node):
                    self.Expand(node)
                folder = node
                try:
                    while filename:
                        name = filename.pop(0)
                        for item in self.GetChildNodes(folder):
                            if self.GetItemText(item) == name:
                                if not self.IsExpanded(item):
                                    self.Expand(item)
                                folder = item
                                continue
                except:
                    pass

                self.UnselectAll()
                self.EnsureVisible(folder)
                self.SelectItem(folder)
                break

    #---- Static Methods ----#

    @staticmethod
    def GetDirContents(directory):
        """Get the list of files contained in the given directory"""
        logger.debug('GetDirContents')
        assert os.path.isdir(directory)
        files = list()
        try:
            joinPath = os.path.join
            fappend = files.append
            #fs_encoding = sys.getfilesystemencoding()
            for p in os.listdir(directory):
                fullpath = joinPath(directory, p)
#                 if type(fullpath) != types:
#                     fullpath = fullpath.decode(fs_encoding)
                fappend(fullpath)
        except OSError:
            pass
        return files

    def GetNodePaths(self, dirNode):
        """Get a list of paths contained below the given
        directory node.
        @param dirNode: wx.TreeItemId
        @return: list of paths

        """
        logger.debug('GetNodePaths')
        paths = list()
        if self.ItemHasChildren(dirNode):
            append = paths.append
            getData = self.GetPyData
            for node in self.GetChildNodes(dirNode):
                try:
                    append(getData(node))
                except wx.PyAssertionError:
                    pass
        return paths

    def GetPyData(self, item):
        """Get data from given tree item
        @param item: TreeItemId

        """
        logger.debug('GetPyData')
        data = None
        # avoid assertions in base class when retrieving data...
        if item and item.IsOk():
            try:
                data = super(FileTree, self).GetItemData(item)
            except wx.PyAssertionError:
                pass
        return data

    def SortParentDirectory(self, item):
        """Sort the parent directory of the given item"""
        logger.debug('SortParentDirectory')
        parent = self.GetItemParent(item)
        if parent.IsOk():
            self.SortChildren(parent)

    #-----------------------------------------------------------------------------#
# Test
if __name__ == '__main__':
    app = wx.App(False)
    f = wx.Frame(None)
    ft = FileTree(f)
    drives=GetWindowsDrives()
#     d = wx.GetUserHome()
    for drive in drives:
        try:
            logger.debug(drive)
            ft.AddWatchDirectory(drive.Name)
        except:
            pass
#         break
    f.Show()
    app.MainLoop()
