import socket
import time
import sys

sauvegarde_index = "index_reception.txt"  # Fichier pour suivre l'avancement
file_name = sys.argv[1]

def get_index():
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
    serversocket.bind(('', 5000))  
    serversocket.listen(1) 

    client_socket, client_address = serversocket.accept()
    client_socket.settimeout(30)

    with open('programme.py', "ab") as f: 
        segment_index = get_index()
        while True :
            try:
                data = client_socket.recv(10) 
                if data.decode() == "finish":
                    break
                elif data.decode() == "reset" : # On reset 
                    print("Erreur de synchronisation, relancement de la communication")
                    segment_index = 0
                    save_index(segment_index)
                    with open('programme.py', "w") as nf: 
                        pass
                elif data :   
                    f.write(data)  
                    print(f"Reçu segment {segment_index}")
                    ack = str(segment_index).encode()
                    client_socket.send(ack)
                    segment_index += 1  
                    save_index(segment_index)
            except Exception as e:
                print(e)
                exit(1)                                          

print("Fichier reçu ")
save_index(0)
client_socket.close()
serversocket.close()
