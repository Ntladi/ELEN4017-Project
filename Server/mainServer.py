from ServerPI import ServerPI

server1 = ServerPI("127.0.0.1",12000)

server1.open_connection()

server1.running()