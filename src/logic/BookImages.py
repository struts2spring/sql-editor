import os
import subprocess
import sys
from src.view.views.calibre.book.browser.epub.opal_epub_worker import EpubBook

import traceback
import rarfile

import logging
import uuid
import numpy as np
import glob
from PIL import Image as Img
import wand
import minecart
logger = logging.getLogger('extensive')


class BookImage():

    def __init__(self):
        pass

#     def convert(self, filepdf):
#         # used to generate temp file name. so we will not duplicate or replace anything
#         uuid_set = str(uuid.uuid4().fields[-1])[:5]
#         try:
#             # now lets convert the PDF to Image
#             # this is good resolution As far as I know
#             with wand.image.Image(filename=filepdf, resolution=200) as img:
#                 # keep good quality
#                 img.compression_quality = 80
#                 # save it to tmp name
#                 logger.debug(os.getcwd())
#                 img.save(filename="temp/temp%s.jpg" % uuid_set)
#         except Exception as err:
#             logger.error(err)
#             # always keep track the error until the code has been clean
#             # print err
#             return False
#         else:
#             """
#             We finally success to convert pdf to image. 
#             but image is not join by it self when we convert pdf files to image. 
#             now we need to merge all file
#             """
#             pathsave = []
#             try:
#                 # search all image in temp path. file name ends with uuid_set value
#                 list_im = glob.glob("temp/temp%s*.jpg" % uuid_set)
#                 list_im.sort()  # sort the file before joining it
#                 imgs = [Img.open(i) for i in list_im]
#                 # now lets Combine several images vertically with Python
#                 min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
#                 imgs_comb = np.vstack(
#                     (np.asarray(i.resize(min_shape)) for i in imgs))
#                 # for horizontally  change the vstack to hstack
#                 imgs_comb = Img.fromarray(imgs_comb)
#                 pathsave = "MyPdf%s.jpg" % uuid_set
#                 # now save the image
#                 imgs_comb.save(pathsave)
#                 # and then remove all temp image
#                 for i in list_im:
#                     os.remove(i)
#             except Exception as err:
#                 # print err 
#                 return False
#         logger.debug(pathsave)
#         return pathsave

    def getPdfImage(self, filePath):
        pdffile = open(filePath, 'rb')
        doc = minecart.Document(pdffile)
        page = doc.get_page(1)
    def getPdfBookImage(self, name=None):
        # Converting first page into JPG
#         with Image(filename=sourcePdf) as img:
#             img.save(filename=destImg)

        cmd = 'convert -background white -alpha remove "' + name + '.pdf[0]' + '" "' + name + '.jpg' + '"'
        subprocess.call(cmd, shell=True)
        
    def getDjuvBookImage(self, name=None):
        cmd = 'ddjvu -page=1 -format=pnm "' + name + '.djvu" 1.pnm && pnmtojpeg 1.pnm > "' + name + '.jpg" && rm *.pnm'
        subprocess.call(cmd, shell=True)
        
    def getChmBookImage(self, name=None):
        pass

#         print 'getChmBookImage'
    def getCbrBookImage(self, name=None):
        
        logger.info('getCbrBookImage')
        rar = rarfile.RarFile(name + ".cbr")
        nameList = rar.namelist()
        nameList.sort()
        try:
            cmd = '''
            unrar e -v "''' + name + '''.cbr" "''' + nameList[0] + '''"
            mv "''' + nameList[0] + '''" "''' + name + '''.jpg"
            '''
            logger.info(cmd)
            subprocess.call(cmd, shell=True)
        except:
            traceback.print_exc()

    def getBookImage(self, filePath=None, name=None, bookFormat=None):

        '''
        @name book_file_name
        convert -size 30x32 cbr.png cbr.png 
        convert cbr.png -resize 50% cbr.png
        convert -thumbnail x300 -background white -alpha remove input_file.pdf[0] output_thumbnail.png
        convert azw.png -resize 16% azw3.png
        '''
        os.chdir(filePath)
        if 'pdf' == bookFormat:
#             self.getPdfBookImage(name)
            self.convert(os.path.join(filePath,name))

        elif 'djvu' == bookFormat:
            self.getDjuvBookImage(name)
            
        elif 'chm' == bookFormat:
            self.getChmBookImage(name)
            
        elif 'epub' == bookFormat:
            file_name = name + '.epub'
            epubBook = EpubBook()
            epubBook.open(file_name)
        
            epubBook.parse_contents()
            epubBook.extract_cover_image(name + '.jpg', outdir='.',)
        elif 'cbr' == bookFormat:
            logger.info('bookFormat:' + bookFormat)
            self.getCbrBookImage(name)    
        elif 'mobi' == bookFormat:
            print('work in progress')
        print('getBookImage completed')


if __name__ == "__main__":
    filePath = None
    if sys.platform == 'win32':
        filePath = r'C:\new\library\4'
    else:
#         filePath = '/docs/new_1/3'
        filePath = '/docs/github/Opal/src/viewer/cbr/'

    name = 'linux-insides.pdf'
#     print 'started'
#     pdfFilePath=os.path.join(filePath, name+'.pdf')
#     imageFilePath=os.path.join(filePath, name+'.jpg')
    BookImage().getBookImage(filePath, name, bookFormat='pdf')
#     print 'e'
    pass
