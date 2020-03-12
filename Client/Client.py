import Connect

commandSocket = Connect.open_command()

sentence = ''

while sentence != 'stop':
	sentence = input('Input text: ') # Prompts user for input
	commandSocket.send(bytes(sentence, "utf-8")) # Sends text through socket into TCP connection
	response = (clientSocket.recv(1024)).decode("utf-8") # Recieves data from server
	print(response + "\n") # Prints response

Connect.close_command(commandSocket)