import socket

def open_command():
	serverName = 'localhost'
	serverPort = 12000 # Sets server port number
	commandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the client socket (IPv4, TCP)
	commandSocket.connect((serverName,serverPort)) # Initiates TCP connection
	return commandSocket

def close_command(commandSocket):
	commandSocket.close() # Closes TCP connection

def open_data():
	serverName = '10.203.3.14'
	serverPort = 12001 # Sets server port number
	dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the client socket (IPv4, TCP)
	dataSocket.connect((serverName,serverPort)) # Initiates TCP connection
	return dataSocket

def close_data(dataSocket):
	dataSocket.close()

