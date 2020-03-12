import Connect

connectionSocket, addr = Connect.open_command().accept() # Creates a new socket for transfer of data
sentence = ''
while sentence != "QUIT": 
	binarySentence = connectionSocket.recv(1024) # Receives text from client
	sentence = binarySentence.decode("utf-8") # Decodes text from binary to ASCII
	if sentence == "RETR":
		connectionSocket.send(bytes("200", "utf-8"))
	elif sentence == 'STOR':
		connectionSocket.send(bytes("200", "utf-8"))
	elif sentence == 'NOOP':
		connectionSocket.send(bytes("200", "utf-8"))
	elif sentence == "QUIT":
		connectionSocket.send(bytes("201", "utf-8"))
	elif sentence[0:4] == "USER":
		print("The user is " + sentence[5:])
		connectionSocket.send(bytes("200", "utf-8"))
	else:
		connectionSocket.send(bytes("503", "utf-8"))

Connect.close_command(connectionSocket)

