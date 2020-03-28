import socket
import random
import os

class ClientDTP():
	def __init__(self):
		self.dataConn = None # The TCP Connection for the data connection
		self.dataSocket = None #
		self.dataPortUpper = None # The higher order digits of data connection TCP port number
		self.dataportLower = None # The lower order digits of the data connection TCP port number
		self.dataPort = None # The full TCP port number of the data connection
		self.__generate_port()
		self.dataIsActive = False # Boolean for if a data connection is active
		self.bufferSize = 1024 # Buffer size for transering files
		self.downloadsFolder = "FromServer/" # Downloads folder directory
		self.uploadsFolder = "ToServer/" # Uploads folder directory

	def __generate_port(self):
		self.dataPortUpper = str(random.randint(12500,32000))
		self.dataportLower = str(random.randint(0,255))
		self.dataPort = int(self.dataPortUpper) + int(self.dataportLower)

	def listen(self,ip):
		self.__generate_port()
		self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dataSocket.bind((ip,self.dataPort))
		self.dataSocket.listen(1)

	def port(self):
		return [self.dataPortUpper,self.dataportLower]

	def does_file_exist(self,fileName):
		filePath = self.uploadsFolder + fileName

		if os.path.isfile(filePath):
			return True
		return False

	def accept_connection(self):
		self.dataConn,dataIP = self.dataSocket.accept()
		self.dataIsActive = True

	def close_data(self):
		self.dataConn.close()
		self.dataIsActive = False

	def fromServer(self,fileName):
		file = open(self.downloadsFolder + fileName,"wb")
		data = self.dataConn.recv(self.bufferSize)

		while data:
			file.write(data)
			data = self.dataConn.recv(self.bufferSize)

		file.close()

	def toServer(self,fileName):
		file = open(self.uploadsFolder + fileName,"rb")
		data = file.read(self.bufferSize)

		while data:
			self.dataConn.send(data)
			data = file.read(self.bufferSize)

		file.close()
