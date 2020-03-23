
# RETR
def retrieve(commandSocket):
	response = (commandSocket.recv(1024)).decode("utf-8")
	print(response)
