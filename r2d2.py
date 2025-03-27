import sys
import socket 
import json

with socket.socket(socket.AF_INET , socket.SOCK_STREAM ) as serversocket :
	serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
	serversocket.bind(('',5000))  
	serversocket.listen(1)
	
	(clientsocket,adress) = serversocket.accept()
	
	with open('blabla.py',"wb") as f : 
		while True :
			data = clientsocket.recv(1024)
			if not data :
				break
			f.write(data)

clientsocket.send(b"hohohohoo")
print("Fichier reçus ")
clientsocket.close()
serversocket.close()
