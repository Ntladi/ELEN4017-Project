import sys
import socket
from ServerPI import ServerPI

clients = int(sys.argv[1])
connections = []

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("127.0.0.1", 12000))
print("Awaiting clients\r\n")

for i in range(1, clients + 1):
	try:
		serverSocket.listen(1)
		conn, addr = serverSocket.accept()
		server = ServerPI(f"Connection-{i}", "127.0.0.1", 12000, conn, addr)
		server.start()
		connections.append(server)
	except:
		print("Failed to create socket for Connection-" + str(i) + "\r\n")

for connection in connections:
	connection.join()

print("All connections closed \r\n")