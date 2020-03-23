import socket

# We'll use a class so that threading is easier to implement later.
# I'll start slow so that the changes aren't overwhelming.
# I'll do a lot of commits so the changes are easy to follow

class Server():
	def __init__(self, connectionSocket, addr, serverName): # __init__() is how a constructor is done in python
		# These are some of the member variables we'll use in this class more may be added later
		self.user = ' ' # Used for USER
		self.validUser = False # Used for PASS
		self.cmdConn = connectionSocket # Used to estalish commands connection
		self.serverName = serverName # Keep the servername closeby
		self.dataConn = None # Used to establish data connection
		self.clientAddr = addr # Stores the client's IP Address (Probably) 
		self.isConnActive = True # boolean for if the connection is still active

	def run(self):
		# The next 3 commands tel the client their connection was successful
		print("Connected to: ", str(self.clientAddr))
		self.sendResponse("220 Successful FTP Connection")

		while self.isConnActive:

			# Below are the base minimum FTP Commands some are missing like NOOP and STRU but we'll deal with those later
			possibleCommands = ['USER', 'PORT', 'RETR', 'STOR', 'QUIT']

			clientTransmission = self.cmdConn.recv(1024).decode()
			command = clientTransmission[:4].strip() # The first 4 charachers are the command
			argument = clientTransmission[4:].strip() # Everything else is the argument
			# Clever way of turning the command into a function call
			# Basically turning 'USER' into USER() for example
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

	def USER(self, username):
		self.sendResponse("230 Welcome " + username + "\r\n")
		# 430 if chowed

	def PORT(self,dataAddr):
		# dataAddr = h1,h2,h3,h4,p1,p2 and we must split it

		# Here we recombine hi.h2.h3.h4
		dataAddr = dataAddr.split(',')
		hostIP = '.'.join(dataAddr[:4])

		# Here we recombine p1 and p2
		portNumber = dataAddr[-2:]
		hostPortUpper = int(portNumber[0])*256
		hostPortLower = portNumber[1]
		hostPort = int(hostPortUpper + hostPortLower)

		# Here we establish the data connection
		self.dataConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.dataConn.connect((hostIP,hostPort))
			self.sendResponse("225 Establishing Active Data Connection\r\n")
		except:
			self.sendResponse("425 Unable to Establish Active Data Connection\r\n")

	def RETR(self):
		message = "RETR is still a work in progress\r\n"
		self.sendResponse(message)

	def STOR(self, argument):
		message = "STOR is still a work in progress also the argument is: " + argument + "\r\n"
		self.sendResponse(message)

	def QUIT(self):
		self.isConnActive = False
		self.sendResponse("221 Terminating Command Connection\r\n")
		self.cmdConn.close()
