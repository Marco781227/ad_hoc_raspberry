import socket
import time

sauvegarde_index = "index_reception.txt"  # Fichier pour suivre l'avancement
MAX_ITER = 30

def get_index():
    try:
        with open(sauvegarde_index, "r") as f:
            return int(f.read())
    except Exception:
        return 0 

def save_index(index):
    with open(sauvegarde_index, "w") as f:
        f.write(str(index))

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as serversocket : 
    serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    serversocket.bind(('', 5000))  
    serversocket.listen(1) 

    client_socket, client_address = serversocket.accept()

    with open('programme.py', "wb") as f: 
        segment_index = get_index()
        nb_iter = 0
        while True and nb_iter < MAX_ITER:
            data = client_socket.recv(10) 
            if data.decode() == "finish":
                break
            if not data:
                print("Perte de connection... Tentative de reconnection.")
                nb_iter += 1
                time.sleep(1)
            else:   
                f.write(data)  
                print(f"Reçu segment {segment_index}")
                ack = str(segment_index).encode()
                client_socket.send(ack)
                segment_index += 1  
                save_index(segment_index)

print("Fichier reçu ")
client_socket.close()
serversocket.close()
