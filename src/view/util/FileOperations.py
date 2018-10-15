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
			
			
if __name__ == "__main__":
	fileOperations = FileOperations()
	isFileRemoved = fileOperations.removeFile(r'C:\soft\sample db\4.sqlite')
	print(isFileRemoved)
