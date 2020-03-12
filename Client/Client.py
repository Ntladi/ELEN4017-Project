import Connect
import Retrieve

commandSocket = Connect.open_command()

sentence = ''

while sentence != 'QUIT':
	sentence = input('Please input command: ') # Prompts user for input
	commandSocket.send(bytes(sentence, "utf-8"))
	response = (commandSocket.recv(1024)).decode("utf-8")
	Retrieve.retrieve(response)

Connect.close_command(commandSocket)