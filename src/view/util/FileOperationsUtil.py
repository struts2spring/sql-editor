import os

import logging.config
import csv
from src.view.constants import LOG_SETTINGS

logger = logging.getLogger('extensive')
logging.config.dictConfig(LOG_SETTINGS)


class FileOperations():

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
	
	def readCsvFile(self, filePath=None, columnNameFirstRow=False, delimiter=',', quotechar='|'):
		data = {}
		if os.path.exists(filePath):
			try:
				with open(filePath, newline='', encoding='utf-8') as csvfile:
					spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
					idKey = 1
					if columnNameFirstRow:
						idKey = 0
					for row in spamreader:
						data[idKey] = tuple(row)
						idKey += 1
					if not columnNameFirstRow:
						colName = list()
						for idx, rowdata in enumerate(data[1]):
							colName.append("Col_{}".format(idx))
						data[0] = tuple(colName)
# 						logger.info(', '.join(row))
			except Exception as ex:
				logger.error(ex, exc_info=True)		
		return data

	def createTableScript(self, tableName=None, columnHeader=None):
		logger.info("createTableScript")

		partialSql = "CREATE TABLE IF NOT EXISTS '{}' ( ".format(tableName)
		for column in columnHeader:
			partialSql += "'{}' TEXT ,".format(column)
		partialSql =partialSql[:-1]
		partialSql += ");"	
		return partialSql

	def sqlScript(self, tableName=None, data=None):

		logger.info("insertScript")

		sqlList=list()
		sqlList.append(self.createTableScript(tableName, columnHeader=data[0]))
		for row in data.items():
			partialSql="INSERT INTO '{}' (".format(tableName)
			for column in data[0]:
				partialSql += "'{}' ,".format(column)
			partialSql =partialSql[:-1]
			partialSql +=") VALUES ("
			for dataRow in row[1]:
				partialSql += "'{}' ,".format(dataRow)
			partialSql =partialSql[:-1]
			partialSql +=");"
			sqlList.append(partialSql)
		return sqlList
if __name__ == "__main__":
# 	print(".".join("Book1_csv.csv".split(sep=".")[:-1]))
	fileOperations = FileOperations()
	data = fileOperations.readCsvFile(filePath=r"C:\soft\Book1_csv.csv", columnNameFirstRow=True, delimiter=",", quotechar='|')
	# print(len(data))	
	# print(data)
	script = fileOperations.createTableScript(tableName="ABCd", columnHeader=data[0])
	print(script)
	sqlList = fileOperations.sqlScript(tableName="ABCd", data=data)
	print(sqlList)
# 	isFileRemoved = fileOperations.removeFile(r'C:\soft\sample db\4.sqlite')
# 	print(isFileRemoved)
# 	htmlDoc = fileOperations.readFile()
# 	print(htmlDoc)

