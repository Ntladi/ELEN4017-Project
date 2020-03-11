import socket

serverPort = 12000 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the server socket (IPv4, TCP)
s.bind((socket.gethostname(),serverPort)) # Assigns the port number to server socket
s.listen(1) # Server listens for TCP connection requests from client (at least one connection)
print ('The server is ready to receive. Type \"stop\" to terminate data exchange.')
sentence = ''
connectionSocket, addr = s.accept() # Creates a new socket for transfer of data
 
while 1: 
	binarySentence = connectionSocket.recv(1024) # Receives text from client
	sentence = binarySentence.decode("utf-8") # Decodes text from binary to ASCII
	if sentence == 'stop':
		break
	print(sentence)
	connectionSocket.send(bytes("From Server: Received.", "utf-8"))

connectionSocket.send(bytes("From Server: Closing TCP connection.", "utf-8"))
connectionSocket.close()