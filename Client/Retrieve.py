
# RETR
def retrieve(response):
	if response == '200':
		print('OK')
	elif response == '503':
		print('Unrecognized Command')
	elif response == '201':
		print('Service Closing Control Connection')
