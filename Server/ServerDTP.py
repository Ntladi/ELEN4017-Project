import socket
import random
import os

class ServerDTP():
	def __init__(self):
		self.dataConn = None
		self.dataSocket = None
		self.files = None
		self.user = None
		self.currentDirectory = None
		self.rootDirectory = None
		self.dataPort = None
		self.dataPortUpper = None
		self.dataportLower = None
		self.isConnOpen = False
		self.isConnPassive = False
		self.bufferSize = 1024

	# Functions for establishing an passive data connection
###################################################################################
	def __generate_data_port_passive(self):
		self.dataPortUpper = str(random.randint(20,30))
		self.dataportLower = str(random.randint(0,255))
		self.dataPort = (int(self.dataPortUpper) * 256) + int(self.dataportLower)

	def server_address_passive(self,hostName):
		serverAddress = hostName.split(".")
		serverAddress = ",".join(serverAddress)
		serverAddress = "(" + serverAddress + "," + self.dataPortUpper + "," + self.dataportLower + ")"
		return serverAddress

	def listen_passive(self,hostName):
		self.__generate_data_port_passive()
		self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dataSocket.bind((hostName,self.dataPort))
		self.dataSocket.listen(1)

	def accept_connection_passive(self):
		self.dataConn,dataAddr = self.dataSocket.accept()
		self.isConnOpen = True
		self.isConnPassive = True
		print("Successful passive data connection\r\n")

	# Functions for establishing an active data connection
###################################################################################
	def __extract_client_ip_active(self,dataAddr):
		splitAddr = dataAddr.split(',')
		clientIP = '.'.join(splitAddr[:4])
		return clientIP

	def __extract_client_port_active(self,dataAddr):
		splitAddr = dataAddr.split(',')
		portNumber = splitAddr[-2:]
		self.dataPort = (int(portNumber[0]) * 256) + int(portNumber[1])
		return self.dataPort

	def make_connection_active(self,dataAddr):
		ip = self.__extract_client_ip_active(dataAddr)
		port = self.__extract_client_port_active(dataAddr)
		self.dataConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dataConn.connect((ip,port))
		self.isConnOpen = True
		self.isConnPassive = False

	# Functions for managing a data connection
###################################################################################
	def data_connection(self,dataConn):
		self.isConnOpen = True
		self.dataConn = dataConn

	def close_data(self):
		if self.isConnOpen and self.dataConn != None:
			self.dataConn.close()
			print("Terminating data connection\r\n")

	# Functions for querying file system info (get functions)
###################################################################################
	def does_file_exist(self,fileName):
		filePath = self.rootDirectory + self.currentDirectory + fileName

		if os.path.isfile(filePath):
			return True
		return False

	def does_directory_exist(self,dirPath):
		directoryPath = self.rootDirectory + dirPath

		if os.path.isdir(directoryPath):
			return True
		return False

	def is_password_valid(self,password):
		passwordPath = "UserFiles/" + self.user + "/Phrase.txt"
		file = open(passwordPath,"r")
		data = file.readlines()
		file.close()

		if password in data:
			return True
		else:
			return False

	def current_directory(self):
		return self.currentDirectory

	# Functions for changing file system info (set functions)
###################################################################################
	def set_user(self,userName):
		self.user = userName
		self.rootDirectory = "UserFiles/" + self.user + "/Files"
		self.currentDirectory = "/"

	def change_directory(self,dirPath):
		if does_directory_exist(dirPath):
			self.currentDirectory = dirPath

	# Functions for data transfer
###################################################################################
	def begin_download(self,fileName):
		fileName = self.rootDirectory + self.currentDirectory + fileName
		file = open(fileName,"rb")
		readingFile = file.read(self.bufferSize)

		while readingFile:
			self.dataConn.send(readingFile)
			readingFile = file.read(self.bufferSize)

		file.close()

	def begin_upload(self,fileName):
		fileName = self.rootDirectory + self.currentDirectory + fileName
		file = open(fileName,"wb")
		writingFile = self.dataConn.recv(self.bufferSize)

		while writingFile:
			file.write(writingFile)
			writingFile = self.dataConn.recv(self.bufferSize)
		
		file.close()

	def send_list(self,dirPath):
		pass

