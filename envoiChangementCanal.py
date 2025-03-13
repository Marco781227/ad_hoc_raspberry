import os
import socket
import sys
import time

MAX_ITER = 10
CONFIRMATION = "yes"


def send_data(ip, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(10)
            s.connect((ip, port))
            s.send(data.encode())
            s.shutdown(socket.SHUT_WR)  # fermeture du socket en ecriture
            response = s.recv(1024)
            print(response)
            time.sleep(1)
            s.close()
            return 0
        except Exception as e:
            print(e)
            return 1


def send_to_servers(receivers_ip, port, data):
    for ip in receivers_ip:
        ip_not_ok = send_data(ip, port, data)
        nb_iter = 0
        while ip_not_ok and nb_iter < MAX_ITER:
            time.sleep(1)
            ip_not_ok = send_data(ip, port, data)
            nb_iter += 1

        if ip_not_ok:
            print(f"Après {MAX_ITER} essais, la connection n'a pas pu être établie)")
            return 1
        else:
            print(f"Connection to {ip} ok")
    return 0


def main():
    port = 5001
    receivers_ip = ["192.168.1.1", "192.168.1.3"]
    best_channel = sys.argv[1]
    my_ip = sys.argv[2]

    channel_not_sent = send_to_servers(receivers_ip, port, best_channel)

    if channel_not_sent:
        print(
            "La connection n'a pas pu être établie avec toutes les machines, le cannal reste le même"
        )
        exit(1)

    confirmation_not_sent = send_to_servers(receivers_ip, port, CONFIRMATION)

    if confirmation_not_sent:
        print(
            "La confirmation n'a pas pu être envoyée à toutes les machines, le cannal reste le même"
        )
        exit(2)

    os.system(f"/home/marco/Documents/tp_rsf/ad_hoc_startup.sh {best_channel} {my_ip}")
    print("Changement de cannal effectué")
    time.sleep(1)


if __name__ == "__main__":
    main()
