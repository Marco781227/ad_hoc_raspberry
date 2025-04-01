import socket
import sys

# Instanciation du socket Bluetooth (AF_BLUETOOTH), avec comme protocole de transport TCP (SOCK_STREAM) et comme protocole de liaison de données RFCOMM (BTPROTO_RFCOMM)
server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

# Le socket écoute l'adresse MAC sur le port 4
server.bind((sys.argv[1], 4))
server.listen(1)
client, addr = server.accept()
try:
    data = client.recv(1024)
    print(f"Received message : {data.decode('utf-8')}")
    reply = "Bien recu"
    client.send(reply.encode("utf-8"))

except Exception as e:
    print(e)
client.close()
