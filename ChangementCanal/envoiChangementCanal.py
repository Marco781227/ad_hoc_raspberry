import os
import socket
import sys
import time

MAX_ITER = 10  # Nombre maximal de tentatives de connexion
CONFIRMATION = "CHANGEMENT_OK"  # Message de confirmation envoyé après le changement de canal



def send_data(ip, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(
                10
            )  # Définit un timeout de 10 secondes pour éviter les blocages
            s.connect(
                (ip, port)
            )  # Connexion à la machine cible sur l'IP et le port spécifiés
            s.send(data.encode())  # Envoi des données encodées en bytes
            s.shutdown(
                socket.SHUT_WR
            )  # Fermeture en écriture pour pouvoir recevoir un message sur le même socket
            response = s.recv(1024)  # Attend une réponse de confirmation
            print(response.decode())  # Affiche la réponse reçue
            time.sleep(1)  
            s.close()  
            return 0
        except Exception as e:
            print(e)  
            return 1  # Échec de l'envoi


def send_to_servers(receivers_ip, port, data):
    for ip in receivers_ip:
        ip_not_ok = send_data(ip, port, data)
        nb_iter = 1

        # Réessaie MAX_ITER fois si l'envoi échoue
        while ip_not_ok and nb_iter < MAX_ITER:
            time.sleep(1)  # Attente avant de réessayer
            ip_not_ok = send_data(ip, port, data)
            nb_iter += 1

        if ip_not_ok:
            print(f"Après {MAX_ITER} essais, la connexion n'a pas pu être établie")
            return 1  # Échec après le maximum de tentatives
        else:
            print(f"Connexion à {ip} réussie")  # Succès de la connexion
    return 0  


def main():
    port = 5001  
    receivers_ip = ["192.168.1.1", "192.168.1.3"]  
    best_channel = sys.argv[1]  
    my_ip = sys.argv[2]  
    file_path = sys.argv[3] + "/ad-hoc-startup.sh"  # Chemin du script de configuration Ad Hoc

    print(f"Tentative de connexion au canal {best_channel}")

    # Envoi du meilleur canal à toutes les machines du réseau
    channel_not_sent = send_to_servers(receivers_ip, port, best_channel)

    if channel_not_sent:
        print(
            "La connexion n'a pas pu être établie avec toutes les machines, le canal reste le même"
        )
        exit(1) 

    # Envoi d'un message de confirmation après la modification du canal
    confirmation_not_sent = send_to_servers(receivers_ip, port, CONFIRMATION)

    if confirmation_not_sent:
        print(
            "La confirmation n'a pas pu être envoyée à toutes les machines, le canal reste le même"
        )
        exit(2)  

    # Exécution du script de changement de canal avec les paramètres
    os.system(f"{file_path} {best_channel} {my_ip}")
    print("Changement de canal effectué")
    time.sleep(1)


if __name__ == "__main__":
    main()  

