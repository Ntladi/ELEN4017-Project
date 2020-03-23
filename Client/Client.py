import Connect
import Command
import socket

commandSocket = Connect.open_command()

message = input('Please input Username: ') # Prompts user for input

if Command.user(message,commandSocket):
	print('Success\r\n')
else:
	print('Failure\r\n')

Connect.open_data(commandSocket)

Connect.close_command(commandSocket)