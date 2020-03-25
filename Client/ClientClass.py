import socket
import os

class Client():
	def __init__(self,ip,cmdPort,dataPort):
		#
		# Constructor to initialize class member variables
		#
		self.username = '' # Stores the username of the client when they log in
		self.ip = ip # Stores the IP Address of the server
		self.cmdSocket = None # The TCP Connection for sending commands and responses
		self.dataSocket = None # The TCP Connection for sending files
		self.cmdPort = int(cmdPort) # The TCP Port number for the commands/responses connection 
		self.dataPortUpper = dataPort[:2] + "000" # The higher order digits of data connection TCP port number
		self.dataportLower = dataPort[-3:] # The lower order digits of the data connection TCP port number
		self.dataPort = int(self.dataPortUpper) + int(self.dataportLower) # The full TCP port number of the data connection 
		self.cmdIsActive = False # Boolean for if the command connection is active
		self.dataIsActive = False # Boolean for if a data connection is active
		self.userIsValid = False # Boolean for if a valid user is logged in
		self.bufferSize = 8192 # Buffer size fro transering files
		self.downloadsFolder = "FromServer" # Downloads folder directory

	def __send_command(self,command):
		#
		# This private method sends FTP commands to the server and returns the response code
		#
		self.cmdSocket.send(command.encode())
		return self.__receive_command()

	def __receive_command(self):
		#
		# This private method receives FTP response codes and messages from an FTP server
		#
		response = self.cmdSocket.recv(1024).decode()
		print(response) # Print response code and response response messages
		response = response[:3].strip()
		return response # Returns only the response code

	def __get_client_address(self):
		#
		# This private method puts the client address in
		# the form (h1,h2,h3,h4,p1,p2) for establishing a data connection
		#
		clientAddr = self.ip.split(".")
		clientAddr = ",".join(clientAddr)
		clientAddr = clientAddr + "," + self.dataPortUpper + "," + self.dataportLower
		return clientAddr

	def __open_data(self):
		#
		# This private method establishes an active TCP connection with the server
		# in order to perform a file transfer
		# 
		dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dataSocket.bind((self.ip,self.dataPort))
		dataSocket.listen(1)
		self.__send_command("PORT " + self.__get_client_address())
		self.dataSocket,dataIP = dataSocket.accept()
		self.dataIsActive = True

	def __close_data(self):
		# 
		# This private method closes the data connection once a file transer is complete
		# 
		self.dataSocket.close()
		self.dataIsActive = False
		print("Closing data connection\r\n")

	def open_command(self):
		# 
		# This public method attempts to establish a TCP command connection with the server
		# 
		if not self.cmdIsActive:
			self.cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			try:
				self.cmdSocket.connect((self.ip,self.cmdPort))
				if self.__receive_command() == "220":
					self.cmdIsActive = True
					return True
			except:
				print("Unable to connect to server\r\n")
				self.cmdIsActive = False
				return False

		else:
			print("Command connection already open\r\n")
			return False

	def close_command(self):
		# 
		# This public method attemps to ask the server to close the command connection
		# 
		if self.cmdIsActive:
			self.__send_command("QUIT")
			self.cmdSocket.close()
			self.cmdIsActive = False
			self.userIsValid = False

	def user(self,username):
		# 
		# This methos attempts to log a user into the server
		# 
		if self.cmdIsActive and not self.userIsValid:
			response = self.__send_command("USER " + username)

			if response == "230":
				self.username = username
				self.userIsValid = True
				return True
			else:
				return False

		elif not self.cmdIsActive:
			print("Please establish a connection\r\n")
			return False
		elif self.userIsValid:
			print("Already logged in as " + self.username + "\r\n")
			return False


	def download_file(self,fileName):
		# 
		# This method is used to doenload files from the server
		# 
		if self.cmdIsActive and self.userIsValid and not self.dataIsActive:
			self.__open_data()
			response = self.__send_command("RETR" + fileName + "\r\n")
			if not os.path.exists(self.downloadsFolder):
				os.makedirs(self.downloadsFolder)

			data = self.dataSocket.recv(self.bufferSize)
			file = open(self.downloadsFolder + "/" + fileName,"wb")

			while data:
				file.write(data)
				data = self.dataSocket.recv(self.bufferSize)

			self.__close_data()
			file.close()
			if response == "266":
				return True
			return False

		elif not self.cmdIsActive:
			print("Please establish connection")
			return False

		elif self.dataIsActive:
			print("File transfer aleady in progress")
			return False

