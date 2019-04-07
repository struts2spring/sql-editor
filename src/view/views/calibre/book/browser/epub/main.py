from src.ui.view.epub.epubtag import EpubBook



if __name__=='__main__':
    f='issue106_en.epub'
    book = EpubBook()
    book.open(f)

    book.parse_contents()
    book.extract_cover_image(outdir='.')
    
    pass