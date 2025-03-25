import socket
import time
import os 
import sys


ip = sys.argv[1] 
port = 5000
fichier = sys.argv[2]
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
    client.settimeout(30)
    client.connect((ip, port))
    i = last_index 
    while i < len(segments) :
        client.send(segments[i]) 
        try : 
            ack = client.recv(1024) 
            if ack.decode() == str(i): 
                print(f"ACK reçu pour segment {i}")
                i = i + 1 
                save_index(i)
            elif ack :
                print(f"ACK incorrect, Reset ")
                client.send(b'reset')
                i = 0
                save_index(i)
            time.sleep(0.1)
        except Exception as e :
            print(e)
            exit(1)
            
    client.send(b'finish' ) 
    print("Fichier envoyé")
    save_index(0)        
    client.close()

envoie()
