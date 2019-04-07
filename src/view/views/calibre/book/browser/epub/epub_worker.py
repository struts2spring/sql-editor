import Image
from bs4 import BeautifulSoup as BS
from bs4 import Tag
import cStringIO
from zipfile import ZipFile as ZP


class EpubWorker():
    def open_epub(self, in_file):
        theEpub = ZP(in_file)
        return theEpub
    
    def get_epub_content_soup(self, _ePub):
        try:
            the_container = _ePub.read('META-INF/container.xml')
        except AttributeError, e:
            print 'Error encountered: %s' % e
            return
    
        cSoup = BS(the_container)
        rootfile = cSoup.find('rootfile')
    
        try:
            the_content = rootfile.attrs['full-path']
        except KeyError, e:
            print 'Error encountered: Key %s does not exist!' % e
            return
    
        try:
            mSoup = BS(_ePub.read(the_content))
        except:
        # All encompassing except, this will be changed.
            raise
    
        return mSoup
    
    def get_epub_general_info(self, content_soup):
        meta_info = {}
    
        for s in ['title', 'language', 'creator', 'date', 'identifier',
                  'publisher', 'source', 'description']:
            try:
                meta_info[s] = content_soup.findAll('dc:%s' % s)[0].text
            except IndexError:
                meta_info[s] = content_soup.find('dc:%s' % s)
        return meta_info
    
    def get_epub_content_lists(self, content_soup):
        spine_list = []
        img_list = []
        text_list = []
        css_list = []
        for item in content_soup.spine.findAll('itemref'):
            spine_list.append(item.attrs['idref'])
    
        the_manifest = content_soup.manifest.findAll('item')
    
        for item_id in spine_list:
            for item in the_manifest:
                if item_id == item.attrs['id']:
                    if item.attrs['media-type'].startswith('application'):
                        text_list.append(item.attrs['href'])
    
        for item in the_manifest:
            if item.attrs['media-type'].endswith('css', -3):
                css_list.append(item.attrs['href'])
            if item.attrs['media-type'].startswith('image'):
                img_list.append(item.attrs['href'])
    
        return img_list, text_list, css_list
    
    def get_epub_section(self, _ePub, section):
        try:
            content = BS(_ePub.read(section))
            return content
        except KeyError:
            for item in _ePub.namelist():
                if section in item:
                    content = BS(_ePub.read(item))
                    return content
        except:
            print 'Received an error from the "get_epub_section" function.'
            return
    
    def preprocess_image(self, _ePub, image):
        try:
            _image = _ePub.read(image)
        except KeyError:
            for item in _ePub.namelist():
                if image in item:
                    _image = _ePub.read(item)
        imgData = cStringIO.StringIO(_image)
        im_img = Image.open(imgData)
        return im_img
    
    def clean_convert_links(self, in_page):
        
        '''Adjust internal links so that the point to memory instead
        of the ePub file. We start with images.'''
        orig_link = None
        pSoup = in_page
        for image in pSoup.findAll('img'):
            new_link = image.attrs['src'].strip('../')
            image.attrs['src'] = 'memory:%s' % new_link
    
        for image in pSoup.findAll('image'):
            try:
                image_link = image.attrs['xlink:href']
                src_tag = Tag(pSoup, name='img')
                src_tag.attrs['src'] = 'memory:%s' % image_link
                image.replaceWith(src_tag)
            except:
                raise
        # Conversions for other types of links will be added at a later time.
        # This is to help ensure we don't convert the wrong links.
        return pSoup.prettify('latin-1')
    
