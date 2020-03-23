import socket
import Command

def open_command(serverName):
	cmdPort = 12000 # Sets server port number
	commandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the client socket (IPv4, TCP)

	try:
		commandSocket.connect((serverName,cmdPort)) # Initiates TCP connection
		Command.receiveResponse(commandSocket)
	except:
		print("Unable to connect to server")
		return

	return commandSocket

def close_command(commandSocket):
	Command.sendCommand('QUIT',commandSocket)
	commandSocket.close() # Closes TCP connection

def open_data():
	clientHost = '127.0.0.1'
	dataPort = 24000 # Sets server port number
	dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the client socket (IPv4, TCP)
	dataSocket.connect((serverName,dataPort)) # Initiates TCP connection
	return dataSocket

def close_data(dataSocket):
	dataSocket.close()

