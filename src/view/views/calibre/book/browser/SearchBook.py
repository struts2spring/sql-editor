import os
from src.dao.BookDao import CreateDatabase
from src.logic.BookShellOperation import BookTerminal


class FindingBook():
    '''
    This class searches book detail in Opal database.this database would be created in workspace(Opal library).
    '''
    def __init__(self,libraryPath=None):
        self.libraryPath=libraryPath
        self.createDatabase = CreateDatabase(libraryPath=libraryPath)
        pass

    def searchingBook(self, searchText=None, exactSearchFlag=False):
        '''
        This method return list of books matching with search text.
        @param searchText: may be a book name 
        '''
        books = list()
        if searchText != None and searchText != '':
            os.chdir(self.libraryPath)
            if exactSearchFlag:
                books = self.createDatabase.findByBookName(searchText)
            else:
                books = self.createDatabase.findBySimlarBookName(searchText)
        else:
            books = self.findAllBooks()
        return books
    
    def countAllBooks(self):
        bookCount = self.createDatabase.countAllBooks()
        return bookCount
    def findBookByNextMaxId(self, bookId=None):
        return self.createDatabase.findBookByNextMaxId(bookId)
    def findBookByPreviousMaxId(self, bookId=None):
        return self.createDatabase.findBookByPreviousMaxId(bookId)
    
    def findAllBooks(self, pageSize=None):
        '''
        This method will give all the books list in book library.
        '''
        books = list()
        os.chdir(self.libraryPath)
        books = self.createDatabase.findAllBook(pageSize=pageSize)
        return books

    def findBookByIsbn(self, isbn_13):
        bs = self.createDatabase.findBookByIsbn(isbn_13)
        return bs

    def getMaxBookId(self):
        os.chdir(self.libraryPath)
    
    def deleteBook(self, book):
        '''
        removing book from database and files.
        @param book: book object 
        '''
        bookPath = book.bookPath
        isSuccessfulDatabaseDelete = self.createDatabase.removeBook(book)
        if isSuccessfulDatabaseDelete:
            BookTerminal().removeBook(bookPath=bookPath)
            
    def findFolderWithoutBook(self):
        '''
        this method will find all the folder without book.
        '''
        directory_name = self.libraryPath
        os.chdir(directory_name)
        listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
        if listOfDir:
            listOfDir.sort(key=int)
        defaulterList = list()
        for dir in listOfDir:
            lst = list()
            levelOne = os.path.join(directory_name, dir)
            for sName in os.listdir(levelOne):
                if os.path.isfile(os.path.join(levelOne, sName)):
                    lst.append(sName.split('.')[-1:][0])
#             if 'pdf' not in lst:
#                 defaulterList.append(levelOne)
            if len(lst) < 3:
                defaulterList.append(levelOne)
#         print defaulterList
if __name__ == '__main__':
#     print 'hi'
    findingBook = FindingBook()
    findingBook.findFolderWithoutBook()
