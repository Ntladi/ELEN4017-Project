import socket
import random
import os

class ServerDTP():
	def __init__(self):
		self.dataConn = None
		self.files = None
		self.bufferSize = 8192
		self.user = None
		self.currentDirectory = None

	def generate_data_port(self):
		dataPortUpper = str(random.randint(12500,32000))
		dataportLower = str(random.randint(0,255))
		dataPort = int(dataPortUpper) + int(dataportLower)
		return (dataPort,dataPortUpper,dataportLower)

	def generate_server_address(self,hostName,dataPortUpper,dataportLower):
		serverAddress = hostName.split(".")
		serverAddress = ",".join(serverAddress)
		serverAddress = "(" + serverAddress + "," + dataPortUpper + "," + dataportLower + ")"
		return serverAddress

	def data_connection(self,dataConn):
		self.dataConn = dataConn

	def close_data(self):
		self.dataConn.close()

	def does_file_exist(self,filePath):
		filePath = self.files + filePath

		if os.path.isfile(filePath):
			return True
		return False

	def current_directory(self):
		return self.currentDirectory

	def set_user(self,userName):
		self.user = userName
		self.currentDirectory = self.user + "/"
		self.files = "UserFiles/" + self.currentDirectory

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