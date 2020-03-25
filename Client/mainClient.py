from ClientClass import Client

client1 = Client("127.0.0.1","12000","24250")

client1.open_command()

username = input('Please input Username: ')

if client1.user(username):
	client1.download_file("transferData.txt")
	client1.download_file("somethingElse.txt")

client1.close_command()