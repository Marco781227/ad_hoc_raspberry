import socket
import time
import sys

sauvegarde_index = "index_reception.txt"  # Fichier pour suivre l'avancement
file_name = sys.argv[1] # Nom que on attribue au fichier reçus . 

def get_index(): #Recuperation de l'index 
    try:
        with open(sauvegarde_index, "r") as f: 
            return int(f.read())
    except Exception:
        return 0 

def save_index(index):
    with open(file_name, "w") as f:
        f.write(str(index))

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as serversocket :
    serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    serversocket.bind(('', 5000))  # On ecoute sur l'adresse local et au port 5000
    serversocket.listen(1) # socket en mode écoute , avec une connexion max en file
    # On ouvre avec un with pour fermer automatiquement a la fin la socket , evite les erreurs 
    client_socket, client_address = serversocket.accept()
    client_socket.settimeout(30) # On attend 30s avant de fermer la connexion avec timeout

    with open(file_name, "ab") as f: # Ouverture en mode ajout binaire . 
        segment_index = get_index() # On recupere notre numéro de segment actuel 
        while True :
            try:
                data = client_socket.recv(10) 
                if data.decode() == "finish": 
                    break
                elif data.decode() == "reset" : # On reset, met a jours l'index et le fichier
                    print("Erreur de synchronisation, relancement de la communication")
                    segment_index = 0
                    save_index(segment_index)
                    with open(file_name, "w") as nf: # On écrase ce qu'on avait ecrit 
                        pass
                elif data : # On ecrit et envoie le ack de bien reçus puis on incremente l'index
                    f.write(data)  
                    print(f"Reçu segment {segment_index}")
                    ack = str(segment_index).encode()
                    client_socket.send(ack)
                    segment_index += 1  
                    save_index(segment_index)
            except Exception as e: # Gestion erreur timeout
                print(e)
                exit(1)                                          

print("Fichier reçu ")
save_index(0)
client_socket.close()
serversocket.close()
