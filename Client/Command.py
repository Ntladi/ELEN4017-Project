import Connect

def receiveResponse(commandSocket):
	response = commandSocket.recv(1024).decode()
	print(response)
	response = response[:3].strip()
	return response

def sendCommand(message,commandSocket):
	commandSocket.send(message.encode())
	return receiveResponse(commandSocket)

def user(username,commandSocket):
	command = 'USER ' + username
	response = sendCommand(command,commandSocket)

	if response != '230':
		return False

	return True

def port(addr,commandSocket):
	command = 'PORT ' + addr
	response = sendCommand(command,commandSocket)

	if response != '530':
		return False

	return True
