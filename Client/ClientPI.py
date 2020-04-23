import socket
from ClientDTP import ClientDTP

class ClientPI():
	def __init__(self,serverIP,cmdPort):
		self.clientDTP = ClientDTP()
		self.username = None
		self.serverIP = serverIP
		self.clientIP = "127.0.0.1"
		self.cmdSocket = None
		self.cmdPort = int(cmdPort)
		self.cmdIsActive = False
		self.userIsValid = False

	# Private Functions for sending and receiving commands
###################################################################################
	def __receive_command(self):
		response = self.cmdSocket.recv(1024).decode()
		print(response)
		return response

	def __send_command(self,command,partial = True):
		if self.__is_CMD_active():
			print(command)
			self.cmdSocket.send(command.encode())
			response = self.__receive_command() 
			if partial:
				response = response[:3].strip()
			return response
		else:
			print("No control connection\r\n")
			return "000"

	# Private Functions for managing connections
###################################################################################
	def __active_mode(self):
		if not self.clientDTP.is_data_established():
			self.clientDTP.listen_active(self.clientIP)
			response = self.__send_command("PORT " + 
			self.clientDTP.client_address_active(self.clientIP) + "\r\n")
			if response == "225":
				self.clientDTP.accept_connection_active()
			else:
				pass # Stop listening

	def __passive_mode(self):
		if not self.clientDTP.is_data_established():
			response = self.__send_command("PASV\r\n",False)
			if response[:3] == "227":
				self.clientDTP.make_connection_passive(response)
			else:
				pass

	def __data_connection(self):
		if self.clientDTP.is_passive():
			self.__passive_mode()
		else:
			self.__active_mode()

	def __is_CMD_active(self):
		if self.cmdIsActive:
			return True
		else:
			print("Control connection not active\r\n")
			return False

	# Private Functions for managing user login
###################################################################################
	def __is_password_valid(self,password):
		response = self.__send_command("PASS " + password + "\r\n")
		if response == "230":
			return True
		else:
			return False

	# Public Functions for managing connections (set functions)
###################################################################################
	def open_connection(self):
		try:
			self.cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.cmdSocket.connect((self.serverIP,self.cmdPort))
			response = self.__receive_command()
			if response[:3] == "220":
				self.cmdIsActive = True
			else:
				self.cmdIsActive = False
		except:
			print("Unable to establish control connection\r\n")

	def data_mode(self,mode):
		if mode == "active":
			self.clientDTP.data_mode(False)
			print("Now transferring in active mode\r\n")
		elif mode == "passive":
			self.clientDTP.data_mode(True)
			print("Now transfering in passive mode\r\n")
		else:
			print("Invalid mode")

	def close_connections(self):
		self.__send_command("QUIT\r\n")
		self.cmdSocket.close()
		self.clientDTP.close_data()
		self.cmdIsActive = False
		self.userIsValid = False

	# Public Functions for qurying connections (get functions)
###################################################################################
	def which_mode(self):
		if self.clientDTP.is_passive():
			print("Passive mode\r\n")
		else:
			print("Active mode\r\n")

	def check_control(self):
		self.__send_command("NOOP\r\n")

	# Private Functions for managing user login
###################################################################################
	def login(self,username,password):
		if not self.userIsValid:
			response = self.__send_command("USER " + username + "\r\n")
			if response == "331":
				self.username = username
				if self.__is_password_valid(password):
					self.userIsValid = True
			else:
				self.username = None
				self.userIsValid = False
		else:
			print("User is already logged in\r\n")

	# Public Functions for transfering files
###################################################################################
	def download(self,fileName):
		self.__data_connection()
		if self.clientDTP.is_data_established():
			response = self.__send_command("RETR " + fileName + "\r\n")
			if response == "125":
				self.clientDTP.from_server(fileName)
				self.clientDTP.close_data()
				self.__receive_command()

	def upload(self,fileName):
		if not self.clientDTP.does_file_exist(fileName):
			print("Invalid file name\r\n")
			return
		self.__data_connection()
		if self.clientDTP.is_data_established():
			response = self.__send_command("STOR " + fileName + "\r\n")
			if response == "125":
				self.clientDTP.to_server(fileName)
			self.clientDTP.close_data()
			if response != "000":
				self.__receive_command()

	# Public Functions for managing the server
###################################################################################
	def change_structure(self,structure):
		self.__send_command("STRU " + structure + "\r\n")
			
	def change_mode(self,mode):
		self.__send_command("MODE " + mode + "\r\n")

	# Public Functions for querying the server
###################################################################################
	def current_directory(self):
		self.__send_command("PWD\r\n")

	def directory_list(self, path = ""):
		self.__data_connection()
		if self.clientDTP.is_data_established():
			response = self.__send_command("LIST " + path + "\r\n")
			if response == "125":
				# self.clientDTP.get_list()
				self.clientDTP.close_data()
				self.__receive_command()

	def server_os(self):
		self.__send_command("SYST\r\n")
