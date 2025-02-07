import socket

send_adress = "B8:27:EB:85:58:B8"   

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) #on établit la communicatio avec le protocole bluetooth (AF_BLUETOOTH) via le protocole TCP (SOCK_STREAM) et le protocole bluetooth RFCOMM (BTPROTO_RFCOMM)
client.connect((send_adress, 4))

try:
    message = "Lancer programme"
    client.send(message.encode())
    data = client.recv(1024)
    print("Received message:"+data.decode())
    data = client.recv(1024)
    print("Received message:"+data.decode())
except OSError as e:
    pass


client.close()
