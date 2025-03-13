import socket
import time
import os 


ip = '192.168.1.2'  
port = 5000
fichier = "reçois.py"  
taille_seg = 10  
sauvegarde_index = "index.txt"  # Fichier pour suivre l'avancement

def creation_seg():
    segments = []
    with open(fichier, "rb") as f:
        while True:
            data = f.read(taille_seg)
            if not data:
                break
            segments.append(data)
    return segments

def get_index():
    try:
        with open(sauvegarde_index, "r") as f:
            return int(f.read())
    except Exception:
        return 0 

def save_index(index):
    with open(sauvegarde_index, "w") as f:
        f.write(str(index))

def envoie():
    segments = creation_seg()
    last_index = get_index()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    i = last_index 
    while i < len(segments) :
        client.send(segments[i]) 

        ack = client.recv(1024) 
        if ack.decode().strip() == str(i): 
            print(f"ACK reçu pour segment {i}")
            save_index(i + 1)
            i = i + 1 
        else:
            print(f"ACK incorrect, re-envoi du segment {i}")

        time.sleep(0.1) 
        
    client.send(b'finish' ) 
    print("Fichier envoyé")
    save_index(0)        
    client.close()

envoie()
