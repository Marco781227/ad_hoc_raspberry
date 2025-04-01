import json
import socket
import sys
import time

HOST = "0.0.0.0"  # Le serveur écoute sur toutes les interfaces réseau
PORT = int(sys.argv[1])  # Le port est passé en argument lors de l'exécution du script
FILENAME = "gps_data.csv"  # Nom du fichier CSV qui contiendra les données GPS

server = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # on établit la connection en IPv4 (INET) et via le protocole TCP (STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(
    (HOST, PORT)
)  # Liaison du socket à l'adresse et au port spécifiés (HOST et PORT)
server.listen(5)
print(f"server en attente sur le port {PORT}.")


with open(FILENAME, "w") as file:
    file.write(
        "timestamp,latitude,longitude\n"
    )  # Ecriture des data dan sle fichier csv
conn, addr = (
    server.accept()
)  # Attente de la connexion d'un client et récupération de la connexion et de l'adresse du client

while True:
    print(f"connexionrecue de {addr}")  # Affichage de l'adresse du client connecté

    data = conn.recv(46)  # Taille d'une trame GPS
    if not data:
        print("aucune data recue")
        conn.close()
        break

    print(len(data))
    timestamp, latitude, longitude = json.loads(
        data.decode()
    )  # Décodage des données reçues depuis bytes vers string, puis conversion du JSON en une liste ou tuple
    with open(FILENAME, "a") as file:
        file.write(f"{timestamp},{latitude},{longitude}\n")
        time.sleep(1)
    print(f"data enregistrees : {timestamp},{latitude},{longitude}")


conn.close()
