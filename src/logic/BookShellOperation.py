import os
import shutil


class BookTerminal():
    '''
    This class has been written to deal with all the terminal operation on book directory 
    '''
    def __init__(self):
        pass
    
    def removeBook(self,bookPath=None):
        '''
        this function remove book directory from workspace. Method returns True if success. 
        '''
        isDirRemoved=False
        try:
            if bookPath and os.path.exists(bookPath):
                shutil.rmtree(bookPath)
                isDirRemoved=True
        except:
            isDirRemoved=False
        return isDirRemoved