
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, UnicodeText, func, \
    Column, Integer, String, Column, Integer, String, create_engine, create_engine
from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.sql.schema import UniqueConstraint


Base = declarative_base()
engine = create_engine('sqlite:///better_calibre.sqlite')


class Book(Base):
    __tablename__ = 'book'
    """A Book class is an entity having database table."""
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bookName = Column('book_name', String(convert_unicode=True), nullable=False)  # bookName
    subTitle = Column('sub_title', String)  # Title
    isbn_10 = Column(String)  # isbn_10
    isbn_13 = Column(String, unique=True)  # isbn_13
    series = Column(String)  # series
    dimension = Column(String)  # dimension
    customerReview = Column('customer_review', String)  # customerReview
    bookDescription = Column('book_description', String)  # bookDescription
    editionNo = Column('edition_no', String)  # editionNo
    publisher = Column(UnicodeText)  # publisher
    bookFormat = Column("book_format", String)  # bookFormat
    fileSize = Column('file_size', String)  # fileSize
    numberOfPages = Column('number_of_pages', Integer)  # numberOfPages
    inLanguage = Column('in_language', String)  # inLanguage
    publishedOn = Column('published_on', DateTime)
    hasCover = Column('has_cover', String)  # hasCover
    hasCode = Column('has_code', String)  # hasCode
    bookPath = Column('book_path', String)  # bookPath
    rating = Column('rating', String)  # rating
    uuid = Column('uuid', String)  # uuid
    tag = Column('tag', String)  # a comma separated list of subjects
    bookFileName = Column('book_file_name', String)
    bookImgName = Column('book_img_name', String) # a comma separated list of images for the book
    wishListed = Column('wish_listed', String)  # this is an indicator that book is not available in workspace.
    itEbookUrlNumber=Column(String)
    createdOn = Column('created_on', DateTime, default=func.now())
#     authors = relationship(
#         "Author",
#         backref="teachers",
#         secondary=AuthorBoo
#     )

    authors = relationship(
        'Author',
        secondary='author_book_link'
    )


#     __table_args__ = (UniqueConstraint('isbn_13', 'location_code', name='_customer_location_uc'),)
