'''
Created on 02-Dec-2015

@author: vijay
'''

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    Column, Integer, String, Column, Integer, String, create_engine, create_engine
from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import os
import sys
import sqlalchemy
from src.dao.Author import Author
from src.dao.AuthorBookLink import AuthorBookLink
import json
from src.dao.Book import Base, Book
# from src.dao.Book import engine
import shutil
import traceback
# from src.static.constant import Workspace
import datetime
# from src.static.SessionUtil import SingletonSession

import logging

logger = logging.getLogger('extensive')

# if os.path.exists(Workspace().libraryPath):
#     os.chdir(Workspace().libraryPath)
#     listOfDir = os.listdir(Workspace().libraryPath)
#     

 
class CreateDatabase():

    def __init__(self, libraryPath=None, databaseFileName='_opal.sqlite'):
        '''
        Creating database for library.
        '''
        logger.debug('CreateDatabase')
        databasePath = os.path.join(libraryPath, databaseFileName)
        self.libraryPath = libraryPath
        isDatabaseExist = os.path.exists(databasePath)

        databaseFilePath = f'sqlite:///{databasePath}'
        self.engine = create_engine(databaseFilePath , echo=True, connect_args={'check_same_thread': False})
        Session = sessionmaker(autoflush=True, autocommit=False, bind=self.engine)
        self.session = Session()
        
        os.makedirs(libraryPath, exist_ok=True)
        if not isDatabaseExist:
#             os.mkdir(libraryPath)
            self.creatingDatabase()
        os.chdir(libraryPath)

    def creatingDatabase(self):
        logger.debug('creatingDatabase')
        os.chdir(self.libraryPath)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        logger.debug('database created blank')

    def addSingleBookData(self, dirName):
        '''
        Using this method you can update single book info into database.
        '''
        logger.debug('addSingleBookData')
        try:
            single = {}
            duplicate = {}
            os.chdir(self.libraryPath)
            duplicateBooks = list()
            addDatabase = True
            b = self.readJsonFile(dirName=dirName)
            if b:
                book = self.createBookFromJson(bookJson=b)
                book.bookPath = os.path.join(self.libraryPath , dirName)
                if book.isbn_13: 
                    if not single.has_key(book.isbn_13):
                        single[book.isbn_13] = book
                        
                    else:
                        duplicate[book.isbn_13] = book
                        addDatabase = False
                        duplicateBooks.append(duplicate)
                if addDatabase:
                    self.session.add(book)
                self.session.commit()
        except Exception as e:
            logger.error(e, exc_info=True)
            self.session.rollback();
            
    def addingData(self):
        logger.debug('addingData')
        directory_name = self.libraryPath
        os.chdir(directory_name)
        listOfDir = list()
#         listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
        for name in os.listdir(directory_name):
            if os.path.isdir(os.path.join(directory_name, name)) :
                try:
                    if int(name):
                        listOfDir.append(name)
                except Exception as e:
                    logger.error(e, exc_info=True)
        if listOfDir:
            listOfDir.sort(key=int)
        one = ''
       
        try:    
            single = {}
            duplicate = {}
            self.duplicateBooks = list()
            for dirName in listOfDir:
                addDatabase = True
                b = self.readJsonFile(dirName=dirName)
                book = self.createBookFromJson(bookJson=b)
                book.bookPath = os.path.join(directory_name , dirName)
                if book.isbn_13: 
                    if not single.has_key(book.isbn_13):
                        single[book.isbn_13] = book
                        
                    else:
                        duplicate[book.isbn_13] = book
                        addDatabase = False
                        self.duplicateBooks.append(duplicate)
                if addDatabase:
                    self.session.add(book)
            self.session.commit()
            logger.debug('number of duplicateBooks: %s', len(self.duplicateBooks))
    
        except Exception as e:
            logger.error(e, exc_info=True)
            self.session.rollback();
        logger.debug('data loaded') 
    
    def createBookFromJson(self, bookJson=None):
        logger.debug('createBookFromJson') 
        book = Book()
        for k in bookJson:
            if not isinstance(bookJson[k], list):
                if k in ['publishedOn', 'createdOn']:
                    if bookJson[k]:
                        book.__dict__[k] = datetime.datetime.strptime(bookJson[k][0:19], "%Y-%m-%d %H:%M:%S")
                else:
                    book.__dict__[k] = bookJson[k]

            else:
                authorList = list()
                for a in bookJson[k]:
                    author = Author()
                    for aKey in a:
                        author.__dict__[aKey] = a[aKey]
                        authorList.append(author)
                book.authors = authorList
        return book
    
    def readJsonFile(self, dirName=None):
        logger.debug('readJsonFile') 
#         print 'readJsonFile----->', os.path.join(Workspace().libraryPath, dirName , 'book.json')
        bookJsonFile = None
        b = None
        try:
            if os.path.exists(os.path.join(self.libraryPath, dirName , 'book.json')):
                bookJsonFile = open(os.path.join(self.libraryPath, dirName , 'book.json'), 'r')
                rep = ''
                for line in bookJsonFile:
                    rep = rep + line
                bookJsonFile.close
                try:
                    b = json.loads(rep)
                except Exception as e:
                    logger.error(e, exc_info=True)
            elif os.path.exists(os.path.join(self.libraryPath, dirName)):
                os.removedirs(os.path.join(self.libraryPath, dirName)) 
        except Exception as e:
            logger.debug(os.path.join(self.libraryPath, dirName))
            logger.error(e, exc_info=True)

#             print rep
        return b

    def saveAuthorBookLink(self, authorBookLink):
        logger.debug('saveAuthorBookLink') 
        self.session.add(authorBookLink)
        self.session.commit()

    def saveBook(self, book):
        self.session.add(book)
        try:
            self.session.commit()
        except Exception as e:
            logger.error(e, exc_info=True)
            self.session.rollback()
            raise

    def countAllBooks(self):
        logger.debug('countAllBooks')
        bookCount = 0
        try:
            bookCount = self.session.query(Book).count()
        except Exception as e:
            logger.error(e, exc_info=True)
        return bookCount
    
    def findAllBook(self, pageSize=None):
        logger.debug('findAllBook pageSize: %s', pageSize)
        bs = self.pagination(limit=pageSize, offset=0)
        return bs
    
    def pagination(self, limit=0, offset=0):
        logger.debug('pagination limit : %s , offset: %s', limit, offset)
        if limit:
            query = self.session.query(Book).limit(limit).offset(offset)
        else:
            query = self.session.query(Book)
        bs = None
        try:    
            bs = query.all()
        except Exception as e:
            logger.error(e, exc_info=True)
        return bs
    
    def findBookByIsbn(self, isbn_13):
        logger.debug('findBookByIsbn : %s', isbn_13)
        bs = self.session.query(Book).filter(Book.isbn_13 == isbn_13).first()
        return bs

    def findBookByNextMaxId(self, bookId):
        logger.debug('findBookByNextMaxId bookId: %s', bookId)
        bs = self.session.query(Book).filter(Book.id > bookId).order_by(Book.id.asc()).first()
        return bs

    def findBookByPreviousMaxId(self, bookId):           
        logger.debug('findBookByPreviousMaxId bookId: %s', bookId)
        bs = self.session.query(Book).filter(Book.id < bookId).order_by(Book.id.desc()).first()
        return bs      
      
    def removeBook(self, book=None):
        '''
        This method removes entry from database. 
        '''
        isBookDeleted = False
        try:
            if book:
                query = self.session.query(Book).filter(Book.id == book.id)
                session_book = query.first()
#                 print book
#                 book = books[0]
                
                author_id_lst = []
                for author in session_book.authors:
                    author_id_lst.append(author.id)
                    self.session.delete(author)
                    
#                 query = self.session.query(AuthorBookLink).filter(AuthorBookLink.bookId == book.id)
#                 authorBookLinks = query.all()
                self.session.delete(session_book)
#                 for authorBook in authorBookLinks:
#                     self.session.delete(authorBook)
                
#                 query = self.session.query(Author).filter(Author.id.in_(author_id_lst))
#                 authors = query.all()
#                 for author in authors:
#                     self.session.delete(author)
#                 self.session.delete(book)
                self.session.commit()
                
#                 path = book.bookPath
#                 if path and os.path.exists(path):
#                     shutil.rmtree(path)
#                     print 'deleting path'
                isBookDeleted = True
        except Exception as e:
            logger.error(e, exc_info=True)
            self.session.flush()
            self.session.close()
            isBookDeleted = False

        return isBookDeleted

    def findByBookName(self, bookName=None, limit=50, offset=0):
        '''
        This method provide search of book name IGNORECASE .
        '''
        logger.debug('findByBookName')
        try:
            if bookName:
                query = self.session.query(Book).filter(func.lower(Book.bookName) == func.lower(bookName)).limit(limit).offset(offset)
#                 .order_by(Book.id.desc())
                books = query.all()
                return books
        except Exception as e:
            logger.error(e, exc_info=True)
            
    def findBySimlarBookName(self, bookName=None, limit=50, offset=0):
        '''
        This method provide search of book name IGNORECASE and similar result like.
        '''
        logger.debug('findBySimlarBookName bookName: %s', bookName)
        try:
            if bookName:
                query = self.session.query(Book).filter(Book.bookName.ilike('%' + bookName + '%')).limit(limit).offset(offset)
#                 .order_by(Book.id.desc())
                books = query.all()
                return books
        except Exception as e:
            logger.error(e, exc_info=True)

    def findByIsbn_13Name(self, isbn_13=None):
        logger.debug('findBySimlarBookName isbn_13: %s', isbn_13)
        if isbn_13:
            query = self.session.query(Book).filter(Book.isbn_13.ilike('%' + isbn_13 + '%'))
            books = query.all()
            return books

    def findDuplicateBook(self):
        logger.debug('findDuplicateBook ')
        books = self.session.query(Book).group_by(Book.isbn_13).having(func.count(Book.isbn_13) > 1).order_by(Book.isbn_13.desc())
        return books
    
    def findBookByFileName(self, bookFileName):
        logger.debug('findBySimlarBookName bookFileName: %s', bookFileName)
        if bookFileName:
            query = self.session.query(Book).filter(Book.bookFileName.ilike('%' + bookFileName + '%'))
            books = query.all()
            return books
        
    def findBook(self, book=None):
        '''
        This method will find the book in database . It will return true.If book present.

        '''
        logger.debug('findBook')
        books = None
        if book.isbn_13:
            query = self.session.query(Book).filter(Book.isbn_13.ilike('%' + book.isbn_13 + '%'))
            books = query.all()
        if book.bookName:
            query = self.session.query(Book).filter(Book.bookName.ilike('%' + book.bookName + '%'))
            books = query.all()
        return books

    def getMaxBookID(self, book=None):
        '''
        This method will find the book in database . It will return true.If book present.

        '''
        books = None
#         maxBookId = self.session.query(func.max(Book.id)).one()
        length = len(self.libraryPath) + 2
        logger.debug('length: %s', length)
        sql = 'select max(substr(book_path,' + str(length) + '), id) from book order by id desc'
        logger.debug('getMaxBookID sql: %s ', sql)
        maxBookId = self.session.execute(sql).first()
        if maxBookId == None:
            maxBookId = [0]
        logger.debug('maxBookId: %s', int(maxBookId[0]))
        return int(maxBookId[0])


if __name__ == '__main__':
#     session = CreateDatabase().creatingDatabase()
#     CreateDatabase().addingData()

#     books = CreateDatabase().findByBookName("java")
    libraryPath = r'/docs/new/library'
    if not os.path.exists(libraryPath):
        print('no workspace')
        
    try:
        createdb = CreateDatabase(libraryPath=libraryPath)
#         createdb.creatingDatabase()
#         createdb.addingData()
        x = createdb.getMaxBookID()
        page = createdb.pagination(10, 10)
        logger.debug(page)
#         createdb.findAllBook()
    except Exception as e:
        print(e)
#     for b in books:
#         print b.isbn_13, b.id

#         createdb.removeBook(b)

    pass
