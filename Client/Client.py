import Connect
import Command
import socket

commandSocket = Connect.open_command('localhost')

sentence = ''

while sentence != 'QUIT':
	sentence = input('Please input command: ') # Prompts user for input
	commandSocket.send(sentence.encode())
	Command.retrieve(commandSocket)

Connect.close_command(commandSocket)