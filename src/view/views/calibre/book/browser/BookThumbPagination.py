
import wx
import logging.config
from src.view.constants import LOG_SETTINGS
from src.view.views.calibre.book.browser.BookThumbCrtl import ThumbnailCtrl, NativeImageHandler
import os
from src.view.views.calibre.book.browser.SearchBook import FindingBook
from src.view.util.FileOperationsUtil import FileOperations
from src.view.constants import ID_FIRST_RESULT, ID_LAST_RESULT, ID_PREVIOUS_RESULT, ID_NEXT_RESULT
from re import search
from src.logic.AddingBook import AddBook
from src.view.other.debounce import debounce
from src.dao.BookDao import CreateDatabase
from pubsub import pub

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD


class TransparentText(wx.StaticText):

    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TRANSPARENT_WINDOW, name=''):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_paint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)

        font_face = self.GetFont()
        font_color = self.GetForegroundColour()

        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def on_size(self, event):
        self.Refresh()
        event.Skip()


class Page():

    def __init__(self, searchText='', pageSize=30, pages=100, pageData=None, total=0, offset=0, currentPage=0):
        self.pageSize = pageSize  # the number of items to be displayed on a page.
        self.pages = pages  # The total number of pages
        self.total = total  # the total number of items matching the query
        self.pageData = pageData  # the items for the current page
        self.offset = offset
        self.currentPage = currentPage
        self.searchText = searchText
#         self.hasNext = False  # True if a next page exists.
#         self.hasPrevious = False  # True if a previous page exists
    
    def hasNext(self):
        next = False
        if self.currentPage + 1 < self.pages:
            next = True
        return next

    def hasPrevious(self):
        previous = False
        if -1 < self.currentPage - 1:
            previous = True
        return previous
    
    def getNextPageNumber(self):
        if self.hasNext():
            self.currentPage = self.currentPage + 1
        return self.currentPage
        
    def getPreviousPageNumber(self):
        if self.hasPrevious():
            self.currentPage = self.currentPage - 1
        return self.currentPage

    def getFirstPageNumber(self):
        self.currentPage = 0
        return self.currentPage

    def getLastPageNumber(self):
        self.currentPage = self.pages - 1
        return self.currentPage


class ThumbnailCtrlPaginationPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        pub.subscribe(self.reloadingDatabase, 'reloadingDatabase')
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.libraryPath = r'C:\new\library'
        self.fileDropTarget = FileDropTarget(self, libraryPath=self.libraryPath)
        self.fileOperations = FileOperations()
        self.search = wx.SearchCtrl(self, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.search.ShowSearchButton(1)
        self.search.ShowCancelButton(1)
        self.search.SetMenu(None)
        self.search.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.search.Bind(wx.EVT_TEXT, self.OnSearch)
                
        self.thumbnailCtrl = ThumbnailCtrl(self, -1, imagehandler=NativeImageHandler)
        self.thumbnailCtrl.EnableToolTips(enable=True)
        self.thumbnailCtrl.SetDropTarget(self.fileDropTarget)
#         self.thumbnailCtrl.ShowDir(r'/home/vijay/Pictures')
#         findingBook = FindingBook(libraryPath=r'/docs/new/library')
#         books = findingBook.searchingBook(searchText='head')
        self.page = Page()
        self.loadingBook()
        self.paginationBar = self.constructTopToolBar()
        ####################################################################
        vBox.Add(self.search , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.thumbnailCtrl , 1, wx.EXPAND | wx.ALL)
        vBox.Add(self.paginationBar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)

    @debounce(1)
    def OnSearch(self, event):
        logger.debug('onSearch')
        self.loadingBook(searchText=self.search.GetValue())

    def loadingBook(self, searchText=None):
        
        books = None
        if os.path.exists(self.libraryPath):
            findingBook = FindingBook(libraryPath=self.libraryPath)
            if searchText:
                books = findingBook.searchingBook(searchText=searchText)
            else:
                books = findingBook.findAllBooks(pageSize=50)
            self.page.pageData = books
            self.page.searchText = searchText
            self.thumbnailCtrl.ShowBook(books)        

    def constructTopToolBar(self):

        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, (10, 10), agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)

#         tb1.SetToolBitmapSize(wx.Size(16, 16))
        # id, name, image, name, method, kind
        pageSizeText = TransparentText(tb1, -1, "Page Size")
#         tb1.AddControl(pageSizeText)
        pageNumber = [f'{pageNum}' for pageNum in range(10, 101, 20)]       
        self.pageSizeCtrl = wx.Choice(tb1, 10, (-1, -1), (50, 25), pageNumber, style=0)
        self.pageSizeCtrl.SetSelection(0)
        
        pageNumbers = [f'{1+pageNum}' for pageNum in range(self.page.pages)]            
        self.pageNumberCtrl = wx.Choice(tb1, 11, (-1, -1), (50, 25), pageNumbers, style=0)
        self.pageNumberCtrl.SetSelection(0)
        pageNumbersCount = TransparentText(tb1, -1, f"/{len(pageNumbers)}")
#         tb1.AddControl(choice)
        tools = [
            ('control', pageSizeText),
            ('control', self.pageSizeCtrl),
            (ID_FIRST_RESULT, "First", "resultset_first.png", 'First', lambda e:self.onToolButtonClick(e), wx.ITEM_NORMAL),
            (ID_PREVIOUS_RESULT, "Previous", "resultset_previous.png", 'Previous', lambda e:self.onToolButtonClick(e), wx.ITEM_NORMAL),
            ('control', self.pageNumberCtrl),
            ('control', pageNumbersCount),
            (ID_NEXT_RESULT, "Next", "resultset_next.png", 'Next', lambda e:self.onToolButtonClick(e), wx.ITEM_NORMAL),
            (ID_LAST_RESULT, "Last", "resultset_last.png", 'Last', lambda e:self.onToolButtonClick(e), wx.ITEM_CHECK),
            
#             (ID_REFRESH_ROW, "Result refresh", "resultset_refresh.png", 'Result refresh \tF5', self.onRefresh),
#             (ID_ADD_ROW, "Add a new row", "row_add.png", 'Add a new row', self.onAddRow),
#             (ID_DUPLICATE_ROW, "Duplicate selected row", "row_copy.png", 'Duplicate selected row', self.onDuplicateRow),
#             (ID_DELETE_ROW, "Delete selected row", "row_delete.png", 'Delete selected row', self.onDeleteRow),
            ]
        for tool in tools:
            if len(tool) == 0:
                tb1.AddSeparator()
            elif len(tool) == 2:
                tb1.AddControl(tool[1])
            else:
                logger.debug(tool)
                toolItem = tb1.AddSimpleTool(tool[0], tool[1], self.fileOperations.getImageBitmap(imageName=tool[2]), kind=tool[5], short_help_string=tool[3])
                
                if tool[4]:
                    self.Bind(wx.EVT_MENU, tool[4], id=tool[0])

#         tb1.AddControl(choice)
        self.Bind(wx.EVT_CHOICE, self.onPageNumberCtrl, self.pageNumberCtrl)
        self.Bind(wx.EVT_CHOICE, self.onPageSizeCtrl, self.pageSizeCtrl)
        tb1.Realize()

        return tb1

    def onPageNumberCtrl(self, event):
        logger.debug('onPageNumberCtrl')
        self.page.currentPage = int(event.GetString()) - 1

    def onPageSizeCtrl(self, event):
        logger.debug('onPageSizeCtrl')
        self.page.pageSize = int(event.GetString())

    def onToolButtonClick(self, e):
        if e.Id == ID_FIRST_RESULT:
            logger.debug('ID_FIRST_RESULT')
            self.pageNumberCtrl.SetSelection(self.page.getFirstPageNumber())
            self.paginationBar.EnableTool(ID_FIRST_RESULT, False)
            self.paginationBar.EnableTool(ID_PREVIOUS_RESULT, False)
            self.paginationBar.EnableTool(ID_NEXT_RESULT, True)
        if e.Id == ID_PREVIOUS_RESULT:
            
            logger.debug('ID_PREVIOUS_RESULT')
            if self.page.hasPrevious():
                self.paginationBar.EnableTool(ID_NEXT_RESULT, True)
                self.paginationBar.EnableTool(ID_LAST_RESULT, True)
                self.pageNumberCtrl.SetSelection(self.page.getPreviousPageNumber())
            else:
                self.paginationBar.EnableTool(ID_PREVIOUS_RESULT, False)
                self.paginationBar.EnableTool(ID_FIRST_RESULT, False)
                
        if e.Id == ID_NEXT_RESULT:
            logger.debug('ID_NEXT_RESULT')
            if self.page.hasNext():
                self.paginationBar.EnableTool(ID_PREVIOUS_RESULT, True)
                self.paginationBar.EnableTool(ID_FIRST_RESULT, True)
                self.pageNumberCtrl.SetSelection(self.page.getNextPageNumber())
            else:
                self.paginationBar.EnableTool(ID_NEXT_RESULT, False)
                self.paginationBar.EnableTool(ID_LAST_RESULT, False)
                
        if e.Id == ID_LAST_RESULT:
            logger.debug('ID_LAST_RESULT')
            self.pageNumberCtrl.SetSelection(self.page.getLastPageNumber())
            self.paginationBar.EnableTool(ID_LAST_RESULT, False)
            self.paginationBar.EnableTool(ID_NEXT_RESULT, False)
            self.paginationBar.EnableTool(ID_FIRST_RESULT, True)
            self.paginationBar.EnableTool(ID_PREVIOUS_RESULT, True)

    def reloadingDatabase(self, event):
        logger.debug('reloadingDatabase')
        self.createDatabase = CreateDatabase(libraryPath=self.libraryPath)
        self.createDatabase.creatingDatabase()
        self.createDatabase.addingData()
        self.loadingBook(searchText=self.search.GetValue())


class FileDropTarget(wx.FileDropTarget):
    """ This object implements Drop Target functionality for Files """

    def __init__(self, obj, libraryPath=None):
        """ Initialize the Drop Target, passing in the Object Reference to
            indicate what should receive the dropped files """
        # Initialize the wxFileDropTarget Object
        wx.FileDropTarget.__init__(self)
        # Store the Object Reference for dropped files
        self.obj = obj
        self.libraryPath = libraryPath
    
    def OnDropFiles(self, x, y, filenames):
        """ Implement File Drop """
        # For Demo purposes, this function appends a list of the files dropped at the end of the widget's text
        # Move Insertion Point to the end of the widget's text
        logger.debug('OnDropFiles')
#         self.obj.SetInsertionPointEnd()
        # append a list of the file names dropped
        logger.debug (f"{len(filenames)} file(s) dropped at {x}, {y}:\n")
        for file in filenames:
            self.selectedFilePath = file
            logger.debug ('file: %s' , file)
            if file:
                AddBook(libraryPath=self.libraryPath).addingBookToWorkspace(file)
        logger.debug('drop book completed.')
        return True
#         text = self.obj.searchCtrlPanel.searchCtrl.GetValue()
#         self.obj.searchCtrlPanel.doSearch(text)


#         self.obj.WriteText('\n')
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    try:
        panel = ThumbnailCtrlPaginationPanel(frame)
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
