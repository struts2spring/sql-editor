'''
Enhanced File History - Provides more consistent behavior than wxFileHistory
'''


class FileHistoryTracker():
    
    def __init__(self):
        self._history = []
        
    def addFileToHistory(self, fileName:str):
        self._history.append(fileName)

    def removeFileFromHistory(self, index:int):
        if len(self.getCount()) > index:
            self._history.pop(index)
            
    def getCount(self):
        """Get the number of files in the history
        @return: int

        """
        return len(self._history)


if __name__ == '__main__':
    fileHistoryTracker = FileHistoryTracker()
    fileHistoryTracker.addFileToHistory("a")
    
