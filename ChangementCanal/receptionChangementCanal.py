import os
import socket
import time
import sys


def receive_data(server_socket, message):
    try:
        (client_socket, _) = server_socket.accept()  # Accepte une connexion entrante
        data = client_socket.recv(1024)  # Reçoit les données envoyées par le client
        client_socket.send(message)  # Envoie un message de confirmation au client
        client_socket.close()  
        return 0, data.decode()  # Retourne le statut de succès et les données reçues
    except Exception as e:
        print(e)  
        return 1, ""  # Echec de la réception


def main():
    my_ip = sys.argv[1]  
    file_path = sys.argv[2] + "/ad-hoc-startup.sh"  # Chemin du script de configuration du mode Ad Hoc

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création du socket serveur en IPv4 et TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permet de réutiliser l'adresse même sans fermuture du socket
    server_socket.settimeout(20)  # Définit un timeout de 20 secondes pour éviter un blocage
    server_socket.bind(("", 5001))  # Lie le socket à toutes les interfaces sur le port 5001
    server_socket.listen(1)  # Met le socket en écoute pour une connexion entrante

    # Réception du canal optimal depuis un client
    reception_not_ok, best_channel = receive_data(server_socket, b"Canal recu")

    if reception_not_ok:
        print("La connexion a échoué, le canal reste le même")
        exit(1)  
    else:
        # Réception de la confirmation du changement de canal
        reception_not_ok, change_data = receive_data(server_socket, b"Confirmation recue")
        if change_data == "CHANGEMENT_OK":
            print(f"Changement du canal actuel pour {best_channel}")
            os.system(f"{file_path} {best_channel} {my_ip}")  # Exécute le script avec le nouveau canal
            time.sleep(1)
        else:
            print("Une ou plusieurs machines n'ont pas pu être jointes, pas de changement de canal")

    server_socket.close()  


main()
