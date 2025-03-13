import os
import socket
import time
import sys


def receive_data(server_socket):
    try:
        (client_socket, _) = server_socket.accept()
        data = client_socket.recv(1024)
        client_socket.send(b"Bien recu")
        print("Nouveau channel bien reçu")
        client_socket.close()
        return 0, data.decode()
    except Exception as e:
        print(e)
        return 1, ""


def main():
    my_ip = sys.argv[1]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.settimeout(30)
    server_socket.bind(("", 5001))
    server_socket.listen(1)

    reception_not_ok, best_channel = receive_data(server_socket)

    if reception_not_ok:
        print("La connection a échoué, le cannal reste le même")
        exit(1)
    else:
        reception_not_ok, change_data = receive_data(server_socket)
        if change_data:
            print(f"Changement du cannal actuel pour {best_channel}")
            os.system(f"/home/marco/Documents/tp_rsf/ad_hoc_startup.sh {best_channel} {my_ip}")
            time.sleep(1)
        else:
            print("Une ou plusieurs machines n'ont pas pu être joignable, pas de changement de cannal")

    server_socket.close()
