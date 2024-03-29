#----------------------------------------------------------------------
# Name:        wx.lib.embeddedimage
# Purpose:     Defines a class used for embedding PNG images in Python
#              code. The primary method of using this module is via
#              the code generator in wx.tools.img2py.
#
# Author:      Anthony Tuininga
#
# Created:     26-Nov-2007
# RCS-ID:      $Id: embeddedimage.py 51067 2008-01-07 09:01:14Z CJP $
# Copyright:   (c) 2007 by Anthony Tuininga
# Licence:     wxWindows license
#----------------------------------------------------------------------

import base64
import wx
from _io import StringIO, BytesIO

class PyEmbeddedImage(object):
    """
    PyEmbeddedImage is primarily intended to be used by code generated
    by img2py as a means of embedding image data in a python module so
    the image can be used at runtime without needing to access the
    image from an image file.  This makes distributing icons and such
    that an application uses simpler since tools like py2exe will
    automatically bundle modules that are imported, and the
    application doesn't have to worry about how to locate the image
    files on the user's filesystem.

    The class can also be used for image data that may be acquired
    from some other source at runtime, such as over the network or
    from a database.  In this case pass False for isBase64 (unless the
    data actually is base64 encoded.)  Any image type that
    wx.ImageFromStream can handle should be okay.
    """

    def __init__(self, data, isBase64=True):
        self.data = data
        self.isBase64 = isBase64

    def GetBitmap(self):
        return wx.Bitmap(self.GetImage())

    def GetData(self):
        return self.data

    def GetIcon(self):
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(self.GetBitmap())
        return icon

    def GetImage(self):
        data = self.data
        if self.isBase64:
            data = base64.b64decode(self.data)
        stream = BytesIO(data)
        return wx.Image(stream)

    # added for backwards compatibility
    getBitmap = GetBitmap
    getData = GetData
    getIcon = GetIcon
    getImage = GetImage

    # define properties, for convenience
    Bitmap = property(GetBitmap)
    Icon = property(GetIcon)
    Image = property(GetImage)

