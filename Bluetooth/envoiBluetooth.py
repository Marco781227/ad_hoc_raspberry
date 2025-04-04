import socket
import sys

address_gps_receiver = "B8:27:EB:C9:02:3B"
address_gps_sender =  "B8:27:EB:85:58:B8"

# Instanciation des sockets Bluetooth (AF_BLUETOOTH), avec comme protocole de transport TCP (SOCK_STREAM) et comme protocole de liaison de données RFCOMM (BTPROTO_RFCOMM)

# Socket déstiné au futur émetteur Wi-Fi
client_gps_sender = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) 

#Socket destiné au futur récepteur Wi-Fi
client_gps_receiver = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) 

try:
    #Récuperation du port et de l'ip à envoyer
    port = int(sys.argv[1])
    receiver_ip = sys.argv[2]

    # Connection aux adresses MAC des périphériques cibles sur le port 4
    client_gps_sender.connect((address_gps_sender, 4))
    client_gps_receiver.connect((address_gps_receiver, 4))
    
    message_receiver = f"Listen for coordinates from port: {port}"
    message_sender = f"Send coordinates to: {receiver_ip} at port: {port}"
    client_gps_receiver.send(message_receiver.encode())
    client_gps_sender.send(message_sender.encode())

    receiver_reply = client_gps_receiver.recv(1024)
    sender_reply = client_gps_sender.recv(1024)
    print("Received message from receiver:"+receiver_reply.decode())
    print("Received message from sender:"+sender_reply.decode())
except Exception as e:
    print(e)
    exit(1)


client_gps_sender.close()
client_gps_receiver.close()
