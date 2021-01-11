from ServerPI import ServerPI

server = ServerPI("127.0.0.1", 12000)
server.open_connection()
server.running()
