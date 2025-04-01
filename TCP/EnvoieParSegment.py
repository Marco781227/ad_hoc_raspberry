import socket
import sys
import time

ip = sys.argv[1]
port = 5000
fichier = sys.argv[2]  # Nom du fichier envoyer
taille_seg = 10
sauvegarde_index = "index.txt"  # Fichier pour suivre l'avancement


def creation_seg():  # On divise le fichier avec la taille des segments définit .
    segments = []
    with open(fichier, "rb") as f:  # Ouverture mode binaire
        while True:
            data = f.read(taille_seg)  # On lit que taille seg a chaque fois
            if not data:
                break
            segments.append(data)
    return segments


def get_index():  # On recupere l'index dans le fichier index .
    try:
        with open(sauvegarde_index, "r") as f:
            return int(f.read())
    except Exception:  # Au cas ou il n'y a pas de fichier .
        return 0


def save_index(index):  # On sauvegarde l'index dans le fichier
    with open(sauvegarde_index, "w") as f:  # ouverture ecriture
        f.write(str(index))


def envoie():
    segments = creation_seg()
    last_index = get_index()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket IPV4 / TCP
    client.settimeout(
        30
    )  # Si jamais on reste +30s sur recv sans message , on termine sans erreur
    client.connect((ip, port))
    i = last_index
    while i < len(segments):  # On envoie tout les segments
        client.send(segments[i])
        try:
            ack = client.recv(1024)  # On attend le ack de reçus
            if ack.decode() == str(i):
                print(f"ACK reçu pour segment {i}")
                i = i + 1
                save_index(i)
            elif (
                ack
            ):  # Si on reçois un ack mais que c'est pas le bon = On est pas synchro donc on reset l'envoie
                print("ACK incorrect, Reset ")
                client.send(b"reset")  # On signale a l'autre que on doit reset .
                i = 0
                save_index(i)
            time.sleep(0.1)
        except Exception as e:
            print(e)
            exit(1)

    client.send(b"finish")  # Envoie de la fin de l'envoie
    print("Fichier envoyé")
    save_index(0)
    client.close()


envoie()
