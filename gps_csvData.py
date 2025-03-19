import socket
import json

HOST = "0.0.0.0" #ecoute partout
PORT = 5000
FILENAME = "gps_data.csv"
	
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #on établit la connection en IPv4 (INET) et via le protocole TCP (STREAM)
print("test1")
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("test2")
server.bind((HOST, PORT))
print("test3")
server.listen(5)
print(f"server en attente sur le port {PORT}.")


with open(FILENAME, "w") as file:
	file.write("timestamp, latitude, longitude\n")
conn, addr = server.accept()

while(True):
	print(f"connexionrecue de {addr}")
	
	data = conn.recv(1024)
	if not data:
		print(f"aucune data recue")
		conn.close()
		break
		
	timestamp, latitude, longitude = json.loads(data.decode())
	with open (FILENAME, "a") as file:
		file.write(f"{timestamp}, {latitude}, {longitude}\n")
	print(f"data enregistrees : {timestamp}, {latitude}, {longitude}")
	
		
		
conn.close()
