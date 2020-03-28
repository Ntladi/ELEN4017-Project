import socket
from ClientDTP import ClientDTP

class ClientPI():
	def __init__(self,serverIP,cmdPort):
		self.clientDTP = ClientDTP() # This directly accesses files on the system and handles data connections
		self.username = '' # Stores the username of the client when they log in
		self.serverIP = serverIP # Stores the IP address of the server
		self.clientIP = "127.0.0.1" # Stores the IP address of the client
		self.cmdSocket = None # The TCP Connection for the control connection
		self.cmdPort = int(cmdPort) # The TCP Port number for the control connection
		self.cmdIsActive = False # Boolean for if the command connection is active
		self.userIsValid = False # Boolean for if a valid user is logged in

	def __receive_command(self):
		response = self.cmdSocket.recv(1024).decode() # Receive Response from server
		print(response) # Print the response code and message
		response = response[:3].strip()
		return response # Returns only the response code

	def __client_address(self):
		ip = self.clientIP.split(".")
		ip = ",".join(ip)
		dataPort = self.clientDTP.port()
		ip = ip + "," + dataPort[0] + "," + dataPort[1]
		return ip 

	def __send_command(self,command):
		if self.cmdIsActive:
			print(command)
			self.cmdSocket.send(command.encode()) # Send command to server
			return self.__receive_command() # Receive response
		else:
			print("No control connection\r\n")

	def __begin_download(self,fileName):
		response = self.__send_command("RETR " + fileName + "\r\n")

		if response == "150":
			self.clientDTP.fromServer(fileName)
			self.clientDTP.close_data()
			self.__receive_command()
		else:
			self.clientDTP.close_data()

	def __begin_upload(self,fileName):
		response = self.__send_command("STOR " + fileName + "\r\n")

		if response == "150":
			self.clientDTP.toServer(fileName)
			
		self.clientDTP.close_data()
		self.__receive_command()

	def open_connection(self):
		self.cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.cmdSocket.connect((self.serverIP,self.cmdPort)) # Attempt a control connection to the host server
		response = self.__receive_command() # Get a response from the host

		if response == "220":
			self.cmdIsActive = True
		else:
			self.cmdIsActive = False

	def close(self):
		self.__send_command("QUIT\r\n")
		self.cmdSocket.close()
		self.cmdIsActive = False
		self.userIsValid = False

	def check_control(self):
		self.__send_command("NOOP\r\n")

	def login(self,username):
		if not self.userIsValid:
			response = self.__send_command("USER " + username + "\r\n")

			if response == "230":
				self.username = username
				self.userIsValid = True
			else:
				self.username = ""
				self.userIsValid = False
		else:
			print("User is already logged in\r\n")

	def download(self,fileName):
		if self.cmdIsActive and self.userIsValid:
			self.clientDTP.listen(self.clientIP)
			response = self.__send_command("PORT " + self.__client_address() + "\r\n")

			if response == "225":
				self.clientDTP.accept_connection()
				self.__begin_download(fileName)

	def upload(self,fileName):
		if not self.clientDTP.does_file_exist(fileName):
			print("Invalid file name\r\n")
			return

		if self.cmdIsActive and self.userIsValid:
			self.clientDTP.listen(self.clientIP)
			response = self.__send_command("PORT " + self.__client_address() + "\r\n")

			if response == "225":
				self.clientDTP.accept_connection()
				self.__begin_upload(fileName)
