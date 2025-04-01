import json
import socket
import sys
import time

import gpsd  # Récupérer les données du GPS.

gpsd.connect()

port = int(
    sys.argv[1]
)  # on établit le port d'envoi qui sera le même que celui de reception"
ip = sys.argv[2]  # on établit l'ip de la machine cible"

client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # on établit la connection en IPv4 (INET) et via le protocole TCP (STREAM)
client.connect((ip, port))  # on se connecte au socket avec l'ip et le port

i = 0

try:
    while True:
        try:
            packet = gpsd.get_current()  # Récupère le paquet de données GPS actuel
            timestamp = time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )  # Formate l'heure actuelle en chaîne de caractères
            latitude, longitude = (
                packet.position()
            )  # Extrait la latitude et la longitude du paquet
        except Exception as _:
            print("aucunes donnees gps captées")

        coordonnees = json.dumps(
            [timestamp, latitude, longitude]
        )  # Convertit les données en JSON
        time.sleep(1)  # Pause d'une seconde
        client.send(
            coordonnees.encode()
        )  # Envoie les données (après encodage en bytes) via le socket
        print(
            f"data envoyée : {timestamp}, {latitude}, {longitude}"
        )  # Affiche les données envoyées
        time.sleep(1)  # Pause d'une seconde avant de recommencer

except KeyboardInterrupt:
    print("\nInterruption. Fermeture du socket...")
    client.close()
