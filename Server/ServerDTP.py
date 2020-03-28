import socket
import os

class ServerDTP():
	def __init__(self):
		self.dataConn = None
		self.files = "UserFiles/"
		self.bufferSize = 8192

	def data_connection(self,dataConn):
		self.dataConn = dataConn

	def close_data(self):
		self.dataConn.close()

	def does_file_exist(self,filePath):
		filePath = self.files + filePath

		if os.path.isfile(filePath):
			return True
		return False

	def begin_download(self,filePath):
		filePath = self.files + filePath
		file = open(filePath,"rb")
		readingFile = file.read(self.bufferSize)

		while readingFile:
			self.dataConn.send(readingFile)
			readingFile = file.read(self.bufferSize)

		file.close()

	def begin_upload(self,fileName):
		fileName = self.files + fileName
		file = open(fileName,"wb")
		writingFile = self.dataConn.recv(self.bufferSize)

		while writingFile:
			file.write(writingFile)
			writingFile = self.dataConn.recv(self.bufferSize)
		
		file.close()
