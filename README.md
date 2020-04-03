## ELEN4017-Network Fundamentals
# File Transfer Protocol Project

1. To run the server, run the following command: __python3 mainServer.py__
  * _Note start the server before starting the client_

2. To run the client, start the python shell and __import mainClient.py__
  * To login, use __mainClient.client.login("_username_")__

  * To logout, use __mainClient.client.logout()__

  * To download use __mainClient.client.download("_filename.extention_")__

  * To upload use __mainClient.client.upload("_filename.extention_")__

  * To noop use __mainClient.client.check_control()__

  * To change mode use __mainClient.client.change_mode("*mode*")__
  
  * To change structure use __mainClient.client.change_structure("*structure*")__ 