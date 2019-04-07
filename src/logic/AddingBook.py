'''
Created on Jan 1, 2016

@author: vijay
'''
from PyPDF2.pdf import PdfFileReader
import copy
from datetime import datetime
import json
import os
import shutil

from src.dao.Author import Author
from src.dao.AuthorBookLink import AuthorBookLink
from src.dao.Book import Book
from src.dao.BookDao import CreateDatabase
from src.logic.BookImages import BookImage
from src.view.views.calibre.book.browser.epub.opal_epub_worker import EpubBook

from src.view.views.calibre.book.browser.util.remove import Util
import logging.config
from src.view.constants import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')
# from src.static.constant import Workspace
# from src.util.remove import Util
# import traceback
# from src.ui.view.epub.opal_epub_worker import EpubBook
import uuid
# import logging

# logger = logging.getLogger('extensive')


class AddBook():
    '''
    This class have been written to add book to Opal workspace library.
    '''
    
    def __init__(self, libraryPath=None):
        self.book = Book()
        self.book.uuid = str(uuid.uuid4())
        self.book.tag = None
        self.book.authors = list()
        self.libraryPath=libraryPath
        self.createDatabase = CreateDatabase(libraryPath=libraryPath)

    def addingBookToWorkspace(self, sourcePath=None):

        '''
        This function will be creating a new dir. Get the max of id in Book table. Create the folder name with max of id plus one.
        @param sourcePath: This is the path of selected book.
        -1. Check if database present in workspace. There is possibility of a new workspace.
        0. Check if book already present in workspace.
        1. Create a folder with max_book_id+1 . 
        2. Copy the book file in the directory.
        3. Create metadata i.e. (book.json)
        4. Make an entry in database.
        '''

        if sourcePath:
            maxBookId = self.createDatabase.getMaxBookID()
            
            if maxBookId == None:
                maxBookId = 0
#             workspacePath = Workspace().libraryPath
            self.book.bookPath = os.path.join(self.libraryPath, str(maxBookId + 1))

            head, tail = os.path.split(sourcePath)
            self.book.bookFileName = tail
            
            self.book.inLanguage = 'English'
            self.book.hasCover = 'Y'
            
            splited_name = tail.split(".")
            self.book.bookFormat = splited_name[-1:][0]
            splited_name.remove(self.book.bookFormat)
            book_file_name = '.'.join(splited_name)
            self.book.bookName = book_file_name
            self.book.wishListed = 'No'
            
            if not self.findingSameBook():
            
                self.book.bookPath = os.path.join(self.libraryPath, str(maxBookId + 1))
                if not os.path.exists(self.book.bookPath):
                    os.makedirs(self.book.bookPath)
                
                dest = os.path.join(self.book.bookPath, tail)
                if sourcePath != dest:
                    shutil.copy (sourcePath, dest)
                
                if 'pdf' == self.book.bookFormat :
                    self.getPdfMetadata(sourcePath)
                if 'epub' == self.book.bookFormat:
                    self.getEpubMetadata(sourcePath)
                    pass
                
                os.chdir(self.book.bookPath)
                self.book.bookImgName = book_file_name + '.jpg'
                BookImage().getBookImage(self.book.bookPath, book_file_name, self.book.bookFormat)
                
                book_copy1 = copy.deepcopy(self.book)
                self.writeBookJson(self.book.bookPath, book_copy1)
                self.addingBookInfoInDatabase(self.book)

    def findingSameBook(self):
        '''
        This method will allow you to find the same book available in workspace already.
        1. check for same book name.
        2. check for isbn.
        
        '''
        logger.debug('findingSameBook')
        isSameBookPresent = False
        books = self.createDatabase.findBookByFileName(self.book.bookFileName)
        logger.debug('len(books): %s', len(books))
        if len(books) > 0:
            isSameBookPresent = True
        return isSameBookPresent

    def addingBookInfoInDatabase(self, book):
        '''
        This method will add new book info in database.
        '''
        logger.debug('addingBookInfoInDatabase')
        self.createDatabase.saveBook(book)

    def writeBookJson(self, newDirPath=None, book=None):
        '''
        This function will write book.json (metadata) of the newly added book in workspace.
        '''
        logger.debug('writeBookJson newDirPath: %s', newDirPath)
        f = open(os.path.join(newDirPath , 'book.json'), 'w')
        row2dict = dict(book.__dict__)
        authors = []
        try:
            for a in row2dict['authors']:
                author = {}
                if type(a) == str:
                    author['authorName'] = a
                else:
                    author = a.__dict__
                if '_sa_instance_state' in author:
                    del author['_sa_instance_state']
                if 'book_assoc' in author:
                    del author['book_assoc']
                authors.append(author)
            if '_sa_instance_state' in row2dict:
                del row2dict['_sa_instance_state']
            if 'authors' in row2dict:   
                del row2dict['authors']
            if 'book_assoc' in row2dict:  
                del row2dict['book_assoc']
    
            row2dict['authors'] = authors
            row2dict['publishedOn'] = str(datetime.now())
            row2dict['createdOn'] = str(datetime.now())
        except Exception as e:
            logger.error(e)
#             print newDirPath
#             print row2dict
        f.write(json.dumps(row2dict, sort_keys=True, indent=4))

        f.close()

    def getEpubMetadata(self, path=None):
        logger.debug('getEpubMetadata')
        os.chdir(self.book.bookPath)
        file_name = self.book.bookName + '.epub'
        epubBook = EpubBook()
        epubBook.open(file_name)
    
        epubBook.parse_contents()
        
        authorList = list()
        for authorName in epubBook.get_authors():
            
            author = Author()
            author.authorName = authorName
            author.aboutAuthor = 'aboutAuthor'
            authorList.append(author)
        self.book.authors = authorList
        
        self.book.tag = epubBook.subjectTag
        epubBook.extract_cover_image(outdir='.')
        self.book.createdOn = datetime.now()
    
    def getPdfMetadata(self, path=None):
        '''
        This method will get the pdf metadata and return book object.
        '''
        logger.debug('getPdfMetadata path: %s', path)

        if path:
            try:
                input = PdfFileReader(open(path, "rb"))
                logger.debug('getIsEncrypted : %s ', input.getIsEncrypted())
            except Exception as e:
                logger.error(e, exc_info=True)
            pdf_info = None
            try:
                pdf_toread = PdfFileReader(open(path, "rb"))
                if pdf_toread.isEncrypted:
                    try:
                        pdf_toread.decrypt('')
                    except Exception as e:
                        logger.error(e, exc_info=True)
            except Exception as e:
                logger.error(e, exc_info=True)
            try:
                pdf_info = pdf_toread.getDocumentInfo()
                logger.debug('NumPages:%s', pdf_toread.getNumPages())
                self.book.numberOfPages = pdf_toread.getNumPages()
                #             value = pdf_info.subject
                subject=None
                if pdf_info.subject and type(pdf_info.subject) == str:
                    # Ignore errors even if the string is not proper UTF-8 or has
                    # broken marker bytes.
                    # Python built-in function unicode() can do this.
                    subject = pdf_info.subject
                    
#                 else:
#                     # Assume the value object has proper __unicode__() method
#                     value = unicode(pdf_info.subject)
#                     print 'else'
                if not self.book.tag and subject :
                    self.book.tag = subject
                elif self.book.tag and subject:
                    self.book.tag = self.book.tag + '' + subject
            except Exception as e:
                logger.error(e, exc_info=True)
            try:
                if pdf_info.title != None and pdf_info.title.strip() != '':
                    self.book.bookName = str(pdf_info.title)
            except Exception as e:
                logger.error(e, exc_info=True)
            
            try:
                if pdf_info.creator:
                    self.book.publisher = str(pdf_info.creator.encode('utf-8'))
            except Exception as e:
                logger.error(e, exc_info=True)
            self.book.createdOn = datetime.now()
            try:
#                 print str(pdf_info['/CreationDate'])[2:10]
                date = datetime.strptime(str(pdf_info['/CreationDate'])[2:10] , '%Y%m%d')
                self.book.publishedOn = date
            except Exception as e:
                logger.error(e, exc_info=True)
                logger.error('CreationDate not found')
            
            logger.debug(Util().convert_bytes(os.path.getsize(path)))
            self.book.fileSize = Util().convert_bytes(os.path.getsize(path))

#             if 'ISBN'.lower() in str(pdf_info['/Subject']).lower():
#                 self.book.isbn_13 = str(pdf_info['/Subject'])[6:]

            author = Author()
            val = 'Unknown'
            try:
                if pdf_info.author != None and pdf_info.author.strip() != '':
                    val = pdf_info.author
#                     val = val.encode("utf8", "ignore")
            except Exception as e:
                logger.error(e, exc_info=True)
            author.authorName = val

            authorList = list()
            authorList.append(author)
            self.book.authors = authorList


if __name__ == '__main__':
#     sourcePath='C:\\Users\\vijay\\Downloads\\ST-52900095-16911.pdf'
#     sourcePath = 'C:\\Users\\vijay\\Downloads\\Head First Rails.pdf'
#     sys.set
#     sourcePath = '/home/vijay/Downloads/1389095365492.pdf'
#     AddBook().addingBookToWorkspace(sourcePath)
    path = "/home/vijay/Downloads/9781784398224-FUNCTIONAL_PROGRAMMING_IN_JAVASCRIPT.pdf"
    addBook = AddBook()
#     path = "/media/vijay/Seagate Backup Plus Drive/vijay/books/English Grammar - A function-based introduction/English Grammar - A function-based introduction. Volume I.pdf"
#     path = "/media/vijay/Seagate Backup Plus Drive/vijay/books/Apress.Venture.Capitalists.at.Work.Nov.2011/Apress.Venture.Capitalists.at.Work.Nov.2011.pdf"
     
    addBook.getPdfMetadata(path)
    newDirPath = '/docs/new/library/1'
    addBook.writeBookJson(newDirPath, addBook.book)
    pass
