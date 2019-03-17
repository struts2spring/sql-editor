

import  os,fnmatch
import logging.config
from src.view.constants import LOG_SETTINGS
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

class ResourceSearchLogic():

    def __init__(self):
        pass
    
    def getFiles(self, basePath='/docs/work/python_project', projectPath='sql_editor', searchText="*.txt"):
        directory = f"{basePath}/{projectPath}/"
#         directory="/docs/work/python_project/sql_editor/src"
#         os.chdir("/docs/work/python_project/sql_editor/src")
#         for file in glob.glob(searchText):
#             print(file)
        resultDict={}
        try:
            for root, dirs, files in os.walk(directory):
                if len(resultDict)<100:
                    for file in files:
                        if file.endswith(searchText):
                            resultDict[len(resultDict)]=[file, root.replace(f'{basePath}/',''),root]
                            print(f'{root}/{file}')   
                            if len(resultDict)>100:
                                break

#             fileiter = (os.path.join(root, f)
#                 for root, _, files in os.walk(dir)
#                 for f in files)
#             txtfileiter = (f for f in fileiter if os.path.splitext(f)[1] == '.py')
#             for txt in txtfileiter:
#                 print(txt)
        except Exception as e:
            logger.error(e)
            pass
        return resultDict
if __name__ == "__main__":
    resourceSearchLogic = ResourceSearchLogic()
    resultDict=resourceSearchLogic.getFiles(searchText='.py')
    print(resultDict)
