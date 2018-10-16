import os

import logging

logger = logging.getLogger('extensive')


class FileOperations:

	def __init__(self):
		pass
	
	def removeFile(self, filename=None):
		isFileRemoved = False
		if os.path.exists(filename):
			try:
				os.remove(filename)
				isFileRemoved = True
			except Exception as e:
				logger.error(filename)
				logger.error(e, exc_info=True)
		else:  
			logger.error("Sorry, I can not find %s file." % filename)
		return isFileRemoved
	
	def readFile(self, filePath=None):
		htmlDoc = ''
		if os.path.exists(filePath):
			try:
				with open(filePath, 'r') as htmlFile:
					for line in htmlFile:
						htmlDoc += line
			except Exception as ex:
				logger.error(ex, exc_info=True)
		return htmlDoc	

			
if __name__ == "__main__":
	fileOperations = FileOperations()
# 	isFileRemoved = fileOperations.removeFile(r'C:\soft\sample db\4.sqlite')
# 	print(isFileRemoved)
	htmlDoc = fileOperations.readFile()
	print(htmlDoc)
