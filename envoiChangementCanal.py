import sys 
import socket 
import time
import os

MAX_ITER = 30

def send_channel(ip, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip,port))
            s.settimeout(10)
            s.send(data.encode())
            s.shutdown(socket.SHUT_WR) #fermeture du socket en ecriture
            response = s.recv(1024)
            print(response)
            time.sleep(1)
            s.close()
            return 0
        except OSError:
            print(e)
            return 1
  
def main():
    port = 5001
    receivers_ip = ['192.168.1.1','192.168.1.3']
    bestChannel = sys.argv[1]

    for ip in receivers_ip :
        ip_not_ok = send_channel(ip, bestChannel)
        nb_iter = 0
        while(ip_not_ok and nb_iter < MAX_ITER):
            time.sleep(5)
            ip_not_ok = send_channel(ip, bestChannel)
            nb_iter += 1

        if (ip_not_ok):
            print(f"Après {MAX_ITER} essais, la connection n'a pas pu être établie)")
            exit(1)
        else:
            print(f"Connection to {ip} ok") 

    os.system(f"/home/marco/Documents/tp_rsf/ad_hoc_startup.sh {bestChannel}")
    print("Changement de cannal effectué")


if __name__ == '__main__' :
    main()
