import socket
import Command

def open_command():
	serverIP = '127.0.0.1'
	cmdPort = 12000 # Sets server port number
	commandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the client socket (IPv4, TCP)

	try:
		commandSocket.connect((serverIP,cmdPort)) # Initiates TCP connection
		Command.receiveResponse(commandSocket)
	except:
		print("Unable to connect to server")
		return

	return commandSocket

def close_command(commandSocket):
	Command.sendCommand('QUIT',commandSocket)
	commandSocket.close() # Closes TCP connection

def open_data(commandSocket):
	clientIP = '127.0.0.1'
	dataPortUpper = 24000 # Sets server port number
	dataPortLower = 250
	dataPort = dataPortUpper + dataPortLower

	clientAddr = clientIP.split(".")
	clientAddr = ','.join(clientAddr)
	clientAddr = clientAddr + "," + str(dataPortUpper) + "," + str(dataPortLower)

	dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the client socket (IPv4, TCP)
	dataSocket.bind((clientIP,dataPort))
	dataSocket.listen(1)

	Command.port(clientAddr,commandSocket)

	print("Data Connection Successful\r\n")

	dataSocket.accept()
	
	return dataSocket

def close_data(dataSocket):
	dataSocket.close()

