import Connect
import Command
import socket

commandSocket = Connect.open_command('localhost')

message = input('Please input Username: ') # Prompts user for input

if Command.user(message,commandSocket):
	print('Success')
else:
	print('Failure')

Connect.close_command(commandSocket)