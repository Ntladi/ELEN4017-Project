import Connect

# We'll use a class so that threading is easier to implement later.
# I'll start slow so that the changes aren't overwhelming.
# I'll do a lot of commits so the changes are easy to follow

class Server():
	def __init__(self, connectionSocket, addr): # __init__() is how a constructor is done in python
		# These are some of the member variables we'll use in this class more may be added later
		self.user = ' ' # Used for USER
		self.validUser = False # Used for PASS
		self.cmdConn = connectionSocket # Used to estalish commands connection
		self.dataConn = None # Used to establish data connection
		self.clientAddr = addr # Stores the client's IP Address (Probably) 
		self.isConnActive = True # boolean for if the connection is still active

	def run(self):
		# The next 3 commands tel the client their connection was successful
		print("Connected to: ", str(self.clientAddr)) 
		reply = "220 Successful FTP Connection"
		self.cmdConn.send(reply.encode())

		while self.isConnActive:

			# Below are the base minimum FTP Commands some are missing like NOOP and STRU but we'll deal with those later
			possibleCommands = ['USER', 'PASS', 'RETR', 'STOR', 'QUIT']

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
				reply = "502 command not implemented\r\n"
				self.cmdConn.send(reply.encode())


	def USER(self, username):
		print("Welcome ", username)

	def PASS(self, password):
		print("Your Password is: ", password)

	def RETR(self):
		print("RETR is still a work in progress")

	def STOR(self, argument):
		print("STOR is still a work in progress also the argument is: ", argument)

	def QUIT(self):
		self.isConnActive = False
		reply = "221 Goodbye\r\n"
		self.cmdConn.send(reply.encode())
		self.cmdConn.close()
