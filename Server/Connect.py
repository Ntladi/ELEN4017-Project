import socket

def open_command():
	serverPort = 12000 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the server socket (IPv4, TCP)
	s.bind((socket.gethostname(),serverPort)) # Assigns the port number to server socket
	s.listen(1) # Server listens for TCP connection requests from client (at least one connection)
	print ('The server is ready to receive. Type \"stop\" to terminate data exchange.')
	return s

def close_command(connectionSocket):
	connectionSocket.close()