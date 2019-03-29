'''
Created on Mar 1, 2019

@author: xbbntni
'''
import wx
from src.view.views.editor.pandoc.PandocPanel import CreatingPandocPanel
from src.view.views.file.MainStcPanel import MainStc
from src.view.util.FileOperationsUtil import FileOperations
import os


class EditorWindowManager():
    
    def __init__(self):
        pass

    def getWindow(self, attachTo, filePath=None):
        window = wx.Panel()
        fileExtension = filePath.split('.')[-1]
        if fileExtension == 'md':
            window = CreatingPandocPanel(attachTo, filePath=filePath)
#             window.markdownSourcePanel.stc.LoadFile(path=filePath)
            window.markdownSourcePanel.stc.SetFileName(filePath)
            window.markdownSourcePanel.stc.SetModTime(os.path.getmtime(filePath))
#                 mainStc.SetText(FileOperations().readFile(filePath=fileWithImage[0]))
            window.markdownSourcePanel.stc.ConfigureLexer(fileExtension)
            window.markdownSourcePanel.stc.SetModified(False)
#             imageName = self.iconManager.getFileImageNameByExtension(fileExtension)
#             (name, captionName) = self.getTitleString(stc=mainStc, path=fileWithImage[0])
            window.markdownSourcePanel.stc.SetSavePoint()
        else:
            window = MainStc(attachTo, text=FileOperations().readFile(filePath=filePath))
            window.SetFileName(filePath)
            window.SetModTime(os.path.getmtime(filePath))
#                 mainStc.SetText(FileOperations().readFile(filePath=fileWithImage[0]))
            window.ConfigureLexer(fileExtension)
            window.SetModified(False)
#             imageName = self.iconManager.getFileImageNameByExtension(fileExtension)
#             (name, captionName) = self.getTitleString(stc=mainStc, path=fileWithImage[0])
            window.SetSavePoint()
        return window 
    

if __name__ == '__main__':
    pass
