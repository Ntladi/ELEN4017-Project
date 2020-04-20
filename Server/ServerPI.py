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
		self.possibleCommands = ["USER","PASS","PASV","PORT","SYST","RETR","STOR","QUIT",
		"NOOP","STRU","MODE","PWD","MKD","TYPE"]
		self.noUserCommands = ["USER","NOOP","QUIT","PASS"]
		self.possibleUsers = ["Ntladi","Gerald","Learn","Tshepo"]
		self.current_mode = "S"
		self.current_type = "I"

	def __send(self,message):
		print(message)
		self.cmdConn.send(message.encode())

	def __execute_command(self,command,argument):
		ftpFunction = getattr(self,command)
		if argument == "":
			ftpFunction()
		else:
			ftpFunction(argument)

	def __command_length(self,clientMessage):
		space_pos = clientMessage.find(" ")
		messageSize = 0

		if space_pos == -1:
			messageSize = len(clientMessage) - 2
		else:
			messageSize = space_pos

		return messageSize

	def running(self):
		while self.isCmdActive:
			clientMessage = self.cmdConn.recv(1024).decode()
			cmdLen = self.__command_length(clientMessage)
			command = clientMessage[:cmdLen].strip().upper()
			argument = clientMessage[cmdLen:].strip()

			if not self.validUser and command not in self.noUserCommands:
				self.__send("530 Please log in\r\n")
				continue

			if command in self.possibleCommands:
				self.__execute_command(command,argument)
			else:
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

	def USER(self,userName):
		if userName in self.possibleUsers:
			self.user = userName
			self.serverDTP.set_user(self.user)
			self.__send("331 Please enter password " + userName + "\r\n")
		else:
			self.validUser = False
			self.__send("332 Invalid user\r\n")

	def PASS(self,password = "phrase"):
		if self.user == "":
			self.__send("530 Please log in\r\n")
			return

		if self.serverDTP.is_password_valid(password):
			self.validUser = True
			self.__send("230 Welcome " + self.user + "\r\n")
		else:
			self.validUser = False
			self.__send("501 Invalid password\r\n")


	def PASV(self):
		dataPort = self.serverDTP.generate_data_port()
		hostAddress = (self.serverName,dataPort[0])
		serverAddress = self.serverDTP.generate_server_address(self.serverName,dataPort[1],dataPort[2])

		# try:
		# 	self.dataConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 	self.dataConn.bind(hostAddress)
		# 	self.dataConn.listen(1)
		self.__send("227 Entering Passive connection mode " + serverAddress + "\r\n")

		# except socket.error:
		# 	self.__send("425 Cannot open PASV data connection")

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

	def SYST(self):
		self.__send("215 MACOS\r\n")

	def RETR(self,fileName):
		if self.serverDTP.does_file_exist(fileName):
			self.__send("150 Sending " + fileName + " to client\r\n")
			self.serverDTP.begin_download(fileName)
			self.serverDTP.close_data()
			self.__send("226 Data transfer complete " + fileName + " sent to client\r\n")
		else:
			self.__send("666 Unable to send file\r\n")
			self.serverDTP.close_data()

	def STOR(self,fileName):
		self.__send("150 Receiving " + fileName + " from client\r\n")
		self.serverDTP.begin_upload(fileName)
		self.serverDTP.close_data()
		self.__send("226 Data transfer complete " + fileName + " sent to client\r\n")

	def QUIT(self):
		self.__send("221 Terminating control connection\r\n")
		self.isCmdActive = False
		self.cmdConn.close()

	def NOOP(self):
		if self.isCmdActive:
			self.__send("200 Control connection OK\r\n")

	def TYPE(self,argument):
		argument = argument.upper()
		possibleArguments = ["A","I"]

		if argument in possibleArguments:
			if argument == "I":
				self.current_type = "I"
				self.__send("200 Binary (I) Type selected\r\n")
			else:
				self.current_type = "A"
				self.__send("200 ASCII (A) Type selected\r\n")
		else:
			self.__send("501 Invalid Type selected\r\n")

	def STRU(self,argument):
		argument = argument.upper()
		possibleArguments = ["F","R","P"]

		if argument in possibleArguments:
			if argument == "F":
				self.__send("200 File structure selected\r\n")
			else:
				self.__send("504 Only file structure supported\r\n")
		else:
			self.__send("501 Not a possible file structure\r\n")

	def MODE(self,argument):
		argument = argument.upper()
		possibleArguments = ["S","B","C"]

		if argument in possibleArguments:
			self.current_mode = "S"
			if argument == "S":
				self.__send("200 Stream mode selected\r\n")
			else:
				self.__send("504 Only stream mode supported\r\n")
		else:
			self.__send("501 Not a possible mode\r\n")

	def PWD(self):
		directory = "\"" + self.serverDTP.current_directory() + "\""
		self.__send("200 " + "Current Working Directory: " + directory + "\r\n")
