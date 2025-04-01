import socket
import sys

filename = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
    )  # on établit la connection en IPv4 (INET) et via le protocole TCP (STREAM)
    serversocket.bind(("", 6000)) # On écoute sur le port 6000 au niveau de toutes les interfaces du réseau
    serversocket.listen(1)

    (clientsocket, adress) = serversocket.accept()

    with open(filename, "wb") as f:
        while True:
            data = clientsocket.recv(1024)
            if not data:
                break
            f.write(data)

clientsocket.send(b"Reception ok")
print("Fichier reçu ")
clientsocket.close()
serversocket.close()
