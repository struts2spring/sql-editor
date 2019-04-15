'''
Created on 30-Jul-2016

@author: vijay
'''

import logging
import sys, time, math, os, os.path

import wx
import wx.richtext
from src.view.views.calibre.book.browser.SearchBook import FindingBook
from src.view.views.calibre.book.browser.BookDescriptionPanel import RichTextPanel

logger = logging.getLogger('extensive')

class PropertyPhotoPanel(wx.Panel):

    def __init__(self, parent=None, book=None):
        wx.Panel.__init__(self, parent, id=-1)
        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.parent = parent
        self.bitmap = None
        self.currentBook = book
        
    def OnContextMenu(self, event):
        logger.debug("OnContextMenu\n")

        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity. 
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1, "Copy book cover")
#         bmp = images.Smiles.GetBitmap()
#         item.SetBitmap(bmp)
        menu.AppendItem(item)
        # add some other items
        menu.Append(self.popupID2, "Download book cover")
        menu.Append(self.popupID3, "Generate book cover")
        menu.Append(self.popupID4, "Open book")
        
        
        self.Bind(wx.EVT_MENU, self.OnCopyToClipboard, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.downloadCover, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.generateCover, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.openBook, id=self.popupID4)
        
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
    def downloadCover(self, event):
        logger.debug( 'downloadCover')
    def generateCover(self, event):
        logger.debug( 'generateCover')
    def openBook(self, event):
        logger.debug( 'openBook'  )      
        
    def OnCopyToClipboard(self, event):
        logger.debug( 'OnCopyToClipboard')

        d = wx.BitmapDataObject(self.bitmap)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(d)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
            logger.debug("Image copied to cliboard.\n")
        else:
            logger.debug("Couldn't open clipboard!\n")  
              
    def OnSize(self, event):
        self.changeBitmapWorker()
        logger.debug( 'onsize')

    def OnPaint(self, evt):
        if self.bitmap != None:
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            dc.DrawBitmap(self.bitmap, 0, 0)
        else:
            pass
    def changeBitmapWorker(self):
#         relevant_path = "/docs/LiClipse Workspace/img/wallpaper"
#         imgFileName=self.getImgFileName(relevant_path)
#         imgFilePath=os.path.join(relevant_path,imgFileName[0] )
        imgFilePath = os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName)
#         img2 =  imgFilePath=os.path.join(relevant_path,imgFileName[1] )
        logger.debug( 'PropertyPhotoPanel GetSize', self.GetSize())
        NewW, NewH = self.GetSize()
        if  NewW > 0 and NewH > 0:
            img = wx.Image(imgFilePath, wx.BITMAP_TYPE_ANY)
            img = img.Scale(NewW, NewH)
            self.bitmap = wx.Bitmap(img)
            self.Refresh()


class BookPropertyPanel(wx.Panel):

    def __init__(self, parent, book):
        wx.Panel.__init__(self, parent)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.currentBook = book
        
        self.photoPanel = PropertyPhotoPanel(self, book=self.currentBook)
#         self.rt = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        self.rt=RichTextPanel(self,book)
#         img1 = wx.Image(os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
#         img=wx.Bitmap(os.path.join(book.bookPath, book.bookImgName))
        logger.debug( 'BookPropertyPanel size: %s', self.GetParent().GetSize())
        img1 = self.scale_bitmap()
        img = wx.Image(240, 240)
#         self.imageCtrl = wx.StaticBitmap(self.photoPanel, wx.ID_ANY, wx.BitmapFromImage(img))
#         self.imageCtrl = wx.StaticBitmap(self.photoPanel, wx.ID_ANY, img1, name="anotherEmptyImage")
#         self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.onImageClick)
        
        
        topsizer = wx.BoxSizer(wx.VERTICAL)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
#         self.pg = self.createPropetyGrid(self.currentBook)
        
        vBox= wx.BoxSizer(wx.VERTICAL)
#         vBox.Add(self.pg, 1, wx.EXPAND, 2)
        vBox.Add(self.rt, 1, wx.EXPAND, 1)
        hBox.Add(self.photoPanel, 2, wx.EXPAND, 5)
        hBox.Add(vBox, 3, wx.EXPAND, 5)
        
        topsizer.Add(hBox, 3, wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        next = wx.Button(self.panel, -1, "Next")
        previous = wx.Button(self.panel, -1, "Previous")
        cancel = wx.Button(self.panel, -1, "Cancel")
        ok = wx.Button(self.panel, -1, "Ok")
        downloadMetadata = wx.Button(self.panel, -1, "Download metadata")
        downloadCover = wx.Button(self.panel, -1, "Download cover")
        generateCover = wx.Button(self.panel, -1, "Generate cover")
        
#         next.Bind(wx.EVT_BUTTON, self.onNext)
#         previous.Bind(wx.EVT_BUTTON, self.onPrevious)
#         ok.Bind(wx.EVT_BUTTON, self.onOk)
#         cancel.Bind(wx.EVT_BUTTON, self.onCancel)
#         downloadMetadata.Bind(wx.EVT_BUTTON, self.onDownloadMetadata)
#         downloadCover.Bind(wx.EVT_BUTTON, self.onDownloadCover)
#         generateCover.Bind(wx.EVT_BUTTON, self.onGenerateCover)
        
        
        
#         rowsizer.Add(previous, 1)
#         rowsizer.Add(next, 1)
#         rowsizer.Add(cancel, 1)
#         rowsizer.Add(ok, 1)
#         rowsizer.Add(downloadMetadata, 1)
#         rowsizer.Add(downloadCover, 1)
#         rowsizer.Add(generateCover, 1)
        topsizer.Add(rowsizer, 0, wx.EXPAND)


        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.sizer.Fit(self)
        self.SetSizer(self.sizer)
#         self.SetAutoLayout(True)

    #----------------------------------------------------------------------
    

        
    def scale_bitmap(self, width=None, height=None):
        bitmap = wx.Image(os.path.join(self.currentBook.bookPath, self.currentBook.bookImgName), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image = bitmap.ConvertToImage()
        if width and height:
            image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result

class BookPropertyFrame(wx.Frame):
    def __init__(self, parent, book):
        wx.Frame.__init__(self, parent, -1, title='Edit Book Metadata', size=(1100, 650))
        self.panel = BookPropertyPanel(self, book)
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
#         self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Show()
    # Makes sure the user was intending to quit the application
    def OnCloseFrame(self, event):
        self.OnExitApp(event)
        
    # Destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        self.Destroy()
if __name__ == '__main__':
    books = FindingBook(libraryPath=r'C:\new\library').findAllBooks()
    book = None
    for b in books:
        book = b
        break
#     print book
    app = wx.App(0)
    frame = BookPropertyFrame(None, book)
    app.MainLoop() 
