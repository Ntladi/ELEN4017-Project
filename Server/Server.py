import socket
import os
import sys

class Server():
	def __init__(self, connectionSocket, addr, serverName):
		self.user = '' # Used for USER
		self.validUser = False # Used for PASS
		self.cmdConn = connectionSocket # Used to estalish commands connection
		self.serverName = serverName # Keep the servername closeby
		self.dataConn = None # Used to establish data connection
		self.clientAddr = addr # Stores the client's IP Address (Probably) 
		self.isConnActive = True # boolean for if the connection is still active
		self.bufferSize = 8192 # The file transfer buffer size

	def run(self):
		print("Connected to: " + str(self.clientAddr) + "\r\n")
		self.sendResponse("220 Successful FTP Connection\r\n") # Tell client their connection was successful

		while self.isConnActive:
			clientTransmission = self.cmdConn.recv(1024).decode() # Receive client transmission
			command = clientTransmission[:4].strip() # Get command from transmission 
			argument = clientTransmission[4:].strip() # Get argument from transmission
			self.executeCommand(command,argument)

	def executeCommand(self,command,argument):
		possibleCommands = ['USER', 'PORT', 'RETR', 'STOR', 'QUIT'] # List of implemented FTP Commands

		if command in possibleCommands:
			ftpFunction = getattr(self, command)
			if argument == '':
				ftpFunction()
			else:
				ftpFunction(argument)
		elif command not in possibleCommands:
				self.sendResponse("502 Command Not Implemented\r\n")

	def sendResponse(self,response):
		print(response)
		self.cmdConn.send(response.encode())
		return

	def USER(self, userName):
		possibleUsers = ['Ntladi', 'Gerald', 'Learn', 'Tshepo'] # List of Users Registered to the FTP Server

		if userName in possibleUsers:
			self.validUser = True
			self.user = userName
			self.sendResponse("230 Welcome " + userName + "\r\n")
		else:
			self.validUser = False
			self.sendResponse("530 Invalid User \r\n")

	def PORT(self,dataAddr):
		# dataAddr = h1,h2,h3,h4,p1,p2 and we must split it
		splitAddr = dataAddr.split(',')
		portNumber = splitAddr[-2:]
		clientIP = '.'.join(splitAddr[:4]) # Join h1,h2,h3,h4
		hostPort = int(portNumber[0]) + int(portNumber[1]) # Join p1,p2

		# Here we establish the data connection
		self.dataConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.dataConn.connect((clientIP,hostPort))
			self.sendResponse("225 Establishing Active Data Connection\r\n")
		except:
			self.sendResponse("425 Unable to Establish Active Data Connection\r\n")

	def RETR(self,filename):
		filename = "UserFiles/" + self.user + "/" + filename
		file = open(filename,'rb')
		readingFile = file.read(1024)

		while readingFile:
			self.dataConn.send(readingFile)
			readingFile = file.read(1024)

		self.sendResponse("266 Data Transfer Complete\r\n")
		self.dataConn.close()
		file.close()

	def STOR(self, argument):
		message = "STOR is still a work in progress also the argument is: " + argument + "\r\n"
		self.sendResponse(message)

	def QUIT(self):
		self.isConnActive = False
		self.sendResponse("221 Terminating Command Connection\r\n")
		self.cmdConn.close()
