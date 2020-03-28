import socket
from ServerDTP import ServerDTP

class ServerPI():
	def __init__(self, serverName, serverPort):
		self.serverDTP = ServerDTP()
		self.user = ""
		self.validUser = False
		self.cmdConn = None
		self.dataConn = None
		self.serverName = serverName
		self.cmdPort = serverPort
		self.isCmdActive = False
		self.possibleCommands = ["USER","PORT","RETR","STOR","QUIT","NOOP"]
		self.possibleUsers = ["Ntladi","Gerald","Learn","Tshepo"]

	def __send(self,message):
		print(message)
		self.cmdConn.send(message.encode())

	def __execute_command(self,command,argument):
		ftpFunction = getattr(self,command)
		if argument == "":
			ftpFunction()
		else:
			ftpFunction(argument)

	def running(self):
		while self.isCmdActive:
			clientMessage = self.cmdConn.recv(1024).decode()
			command = clientMessage[:4].strip()
			argument = clientMessage[4:].strip()

			if command in self.possibleCommands:
				self.__execute_command(command,argument)
			else:
				self.isCmdActive = False
				self.__send("502 Command not implemented\r\n")

	def open_connection(self):
		cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cmdSocket.bind((self.serverName,self.cmdPort))
		cmdSocket.listen(1)
		print("Server is listening for client\r\n")
		self.cmdConn, addr = cmdSocket.accept()
		print("Connected to: " + str(addr) + "\r\n")
		self.isCmdActive = True
		self.__send("220 Successful control connection\r\n")

	def NOOP(self):
		self.__send("200 Control connection OK\r\n")

	def USER(self,userName):
		if userName in self.possibleUsers:
			self.validUser = True
			self.user = userName
			self.__send("230 Welcome " + userName + "\r\n")
		else:
			self.validUser = False
			self.__send("530 Invalid user\r\n")

	def PORT(self,dataAddr):
		splitAddr = dataAddr.split(',')
		portNumber = splitAddr[-2:]
		clientIP = '.'.join(splitAddr[:4])
		hostPort = int(portNumber[0]) + int(portNumber[1])
		dataConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			dataConn.connect((clientIP,hostPort))
			self.__send("225 Active data connection established\r\n")
			self.serverDTP.data_connection(dataConn)
		except:
			self.__send("425 Unable to establish active data connection\r\n")
			self.serverDTP.close_data()

	def RETR(self,fileName):
		filePath = self.user + "/" + fileName

		if self.serverDTP.does_file_exist(filePath):
			self.__send("150 Sending " + fileName + " to client\r\n")
			self.serverDTP.begin_download(filePath)
			self.serverDTP.close_data()
			self.__send("226 Data transfer complete " + fileName + " sent to client\r\n")
		else:
			self.__send("666 Unable to send file\r\n")
			self.serverDTP.close_data()

	def STOR(self,fileName):
		filePath = self.user + "/" + fileName
		self.__send("150 Receiving " + fileName + " from client\r\n")
		self.serverDTP.begin_upload(filePath)
		self.serverDTP.close_data()
		self.__send("226 Data transfer complete " + fileName + " sent to client\r\n")

	def QUIT(self):
		self.isCmdActive = False
		self.__send("221 Terminating control connection\r\n")
		self.cmdConn.close()
