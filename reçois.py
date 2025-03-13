import sys
import socket 
import json

with socket.socket(socket.AF_INET , socket.SOCK_STREAM ) as serversocket :
    serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    serversocket.bind(('',5000))
    serversocket.listen(1)
    print("test1")
    (clientsocket,adress) = serversocket.accept()
    print("test2")
    while True:
        data = clientsocket.recv(1024)
        if not data :
            break
        print(json.loads(data.decode()))    
        clientsocket.send(b'hohohohoo')
print("Fichier reçus ")
