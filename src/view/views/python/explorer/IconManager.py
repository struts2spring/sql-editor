'''
Created on Feb 28, 2019

@author: xbbntni
'''
from src.view.util.FileOperationsUtil import FileOperations
import logging.config
from src.view.constants import LOG_SETTINGS
import wx
import os
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class PythonExplorerIconManager():

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
                          'yaml.png', 'package_obj.png' ]:
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
if __name__ == '__main__':
    pass
