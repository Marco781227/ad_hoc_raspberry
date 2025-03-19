"""
import gps

session = gps.gps(mode=gps.WATCH_ENABLE)
#gpsd.connect()


try :
	while True :
		report = session.next()
		if report['class']=='TPV':
			latitude = getattrr(report, 'lat', "N/A")
			longitude = getattrr(report, 'lon', "N/A")
			altitude = getattrr(report, 'alt', "N/A")
			print(f"Latitude : {latitude}, Longitude : {longitude}, Altitude : {altitude}")
except KeyboardInterrupt:
	print("Arrêt du script GPS")
"""
import gpsd
import time
import socket
import sys
import json

gpsd.connect()

port = 5000 #on établit le port d'envoi qui sera le même que celui de reception"
ip = '127.0.0.1' #on établit l'ip de la machine cible"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #on établit la connection en IPv4 (INET) et via le protocole TCP (STREAM)
print("test1")
client.connect((ip,port)) #on se connecte au socket avec l'ip et le port
print("test2")	

i=0


while(True):
    packet = gpsd.get_current()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    latitude, longitude = packet.position()

    coordonnees = json.dumps([timestamp, latitude, longitude])
    time.sleep(1)
    client.send(coordonnees.encode())
    print(f"data envoyée : {timestamp}, {latitude}, {longitude}")
    
    time.sleep(1)
else :
    print(f"aucune donnée GPS reçue")
    


client.close()			






	
