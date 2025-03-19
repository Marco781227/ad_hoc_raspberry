import socket 
import os 
server = socket.socket(socket.AF_BLUETOOTH , socket.SOCK_STREAM , socket.BTPROTO_RFCOMM )
server.bind(("B8:27:EB:85:58:B8",4))
server.listen(1)
client,addr = server.accept()
try :
	while True : 
		data = client.recv(1024)
		if not data : break 
		print(f"Message : {data.decode('utf-8')}")
		message = "Ok lancement de la fusee"  
		client.send(message.encode("utf-8"))

		os.system("python3 blabla.py")
		client.send(("Fichier exécutable ").encode("utf-8")) 
except OSError as e :
	pass
client.close()
server.close()
