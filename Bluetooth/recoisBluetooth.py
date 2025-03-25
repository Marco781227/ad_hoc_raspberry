import socket 
import os
import sys 
server = socket.socket(socket.AF_BLUETOOTH , socket.SOCK_STREAM , socket.BTPROTO_RFCOMM )
server.bind((sys.argv[1],4))
server.listen(1)
client,addr = server.accept()
try :
	while True : 
		data = client.recv(1024)
		if not data : break 
		print(f"Received message : {data.decode('utf-8')}")
		reply = "Bien recu"
		client.send(reply.encode("utf-8"))

except Exception as e :
	pass
client.close()
