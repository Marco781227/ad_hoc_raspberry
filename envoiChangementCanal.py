import sys 
import socket 

port = 5001
receivers_ip = ['192.168.1.1','192.168.1.3']
bestChannel = sys.argv[1]

def send_channel()
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
