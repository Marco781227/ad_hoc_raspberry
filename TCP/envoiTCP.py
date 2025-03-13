import socket
import sys

port = 5000 #on établit le port d'envoi qui sera le même que celui de reception"
ip = '192.168.1.2' #on établit l'ip de la machine cible"
filename = sys.argv[1]

def send_data():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #on établit la connection en IPv4 (INET) et via le protocole TCP (STREAM)
    client.connect((ip,port)) #on se connecte au socket avec l'ip et le port
    with open(filename, "rb") as f : #on ouvre le fichier à envoyer en lecture et en binaire pour directement l'envoyer sur le socket
        data = f.read() 
        if data:
            client.send(data) #envoi du contenu du script
    client.shutdown(socket.SHUT_WR) #fermeture du socket en ecriture
    response = client.recv(1024) #reception du message
    print(response.decode())
    client.close()

send_data()
