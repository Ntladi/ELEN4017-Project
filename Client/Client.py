import socket

serverName = '10.203.39.28'
serverPort = 12000 # Sets server port number

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the client socket (IPv4, TCP)
clientSocket.connect((serverName,serverPort)) # Initiates TCP connection

sentence = ''

while sentence != 'stop':
	sentence = input('Input text:') # Prompts user for input
	clientSocket.send(bytes(sentence, "utf-8")) # Sends text through socket into TCP connection
	response = (clientSocket.recv(1024)).decode("utf-8") # Recieves data from server
	print(response + "\n") # Prints response

clientSocket.close() # Closes TCP connection