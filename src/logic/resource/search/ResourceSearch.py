

import  os, fnmatch
import logging.config
from src.view.constants import LOG_SETTINGS
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')


class ResourceSearchLogic():

    def __init__(self):
        self.resultDict = {}

    def clearLastResult(self):
        self.resultDict.clear()

    def getFiles(self, basePath='/docs/work/python_project', projectDirName='sql_editor', searchText="*.txt"):
#         directory = f"{basePath}/{projectDirName}/"
        directory = os.path.join(basePath, projectDirName)

#         directory="/docs/work/python_project/sql_editor/src"
#         os.chdir("/docs/work/python_project/sql_editor/src")
#         for file in glob.glob(searchText):
#             print(file)
        try:
            for root, dirs, files in os.walk(directory):
                if len(self.resultDict) < 100:
                    for file in files:
                        if file.endswith(searchText):
                            self.resultDict[len(self.resultDict)] = [file, root.split(basePath)[1][1:], root]
                            filePath=os.path.join(root,file)
                            print(filePath)
                            if len(self.resultDict) > 100:
                                break

#             fileiter = (os.path.join(root, f)
#                 for root, _, files in os.walk(dir)
#                 for f in files)
#             txtfileiter = (f for f in fileiter if os.path.splitext(f)[1] == '.py')
#             for txt in txtfileiter:
#                 print(txt)
        except Exception as e:
            logger.error(e)
        return self.resultDict


if __name__ == "__main__":
    resourceSearchLogic = ResourceSearchLogic()
    resultDict = resourceSearchLogic.getFiles(basePath='/docs/work/python_project', projectDirName='sql_editor',searchText='.py')
    print(resultDict)
