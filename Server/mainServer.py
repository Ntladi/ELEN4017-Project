from Server import Server
import socket

#Everything up to line 8 is the same as the open_command() from the old Connect.py
serverPort = 12000
serverName = 'localhost'
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the server socket (IPv4, TCP)
serverSocket.bind((serverName,serverPort)) # Assigns the port number to server socket
serverSocket.listen(1) # Server listens for TCP connection requests from client (at least one connection)
print("Server is listening for client")
connectionSocket, addr = serverSocket.accept() # Creates a new socket for transfer of data

# This is us running the server
server1 = Server(connectionSocket, addr, serverName)
server1.run()