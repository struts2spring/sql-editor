import os
import subprocess
import sys
from src.view.views.calibre.book.browser.epub.opal_epub_worker import EpubBook

import traceback
import rarfile

import logging
from PIL import Image as Img
import platform
logger = logging.getLogger('extensive')


class BookImage():

    def __init__(self):
        pass



    def getPdfBookImage(self, name=None):
        # Converting first page into JPG
#         with Image(filename=sourcePdf) as img:
#             img.save(filename=destImg)
        if platform.system() == 'Windows':
            path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','bin','pdftocairo.exe')
#             os.chdir(path)
            cmd=f'''{path} -f 1 -l 1 -jpeg "{name}.pdf" "{name}.jpg"'''
        else:
            cmd = 'convert -background white -alpha remove "' + name + '.pdf[0]' + '" "' + name + '.jpg' + '"'
            
        print(cmd)
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
            self.getPdfBookImage(name)
#             self.convert(os.path.join(filePath,name))

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
