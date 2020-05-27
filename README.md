# ELEN4017-Network Fundamentals
## File Transfer Protocol Project

1. To run the server, run the following command: 
``` bash 
python3 mainServer.py
```
  * _Note start the server before starting the client_

2. To run the client, start the python shell and run:
``` bash
import mainClient.py
```
  * To login, use `mainClient.client.login("username","password")`

  * To logout, use `mainClient.client.close_connections()`

  * To download use `mainClient.client.download("filename.extention")`

  * To upload use `mainClient.client.upload("filename.extention")`

  * To noop use `mainClient.client.check_control()`

  * To change mode use `mainClient.client.change_mode("mode")`
  
  * To change structure use `mainClient.client.change_structure("structure")` 

  __*Note that only the default states for structure (f) and mode (s) have been implemented__