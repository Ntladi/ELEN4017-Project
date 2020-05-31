import getpass
from ClientPI import ClientPI
from ClientUI import ClientUI

serverAddress = "127.0.0.1" #input("Server Address: ")
serverPort = "12000"#input("Port: ")
client = ClientPI(serverAddress, int(serverPort))

if client.is_CMD_active():
	userName = "Ntladi"#input("User Name: ")
	password = "SomeSecureShit"#getpass.getpass()
	client.login(userName, password)
if client.is_user_valid():
	ui = ClientUI()
	ui.initilise_client(client)
	ui.cmdloop()