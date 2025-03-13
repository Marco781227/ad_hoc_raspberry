import gpsd
import time
import socket

gpsd.connect()
FILENAME = "gps_data.txt"
SERVER_IP = "192.168.1.1"
PORT = 5000

# Enregistrement des données GPS
with open(FILENAME, "w") as file:
    file.write("timestamp,latitude,longitude,altitude\n")

    try:
        while True:
            packet = gpsd.get_current()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            latitude, longitude = packet.position()
            altitude = packet.altitude()

            file.write(f"{timestamp},{latitude},{longitude},{altitude}\n")
            file.flush()
            print(f"Enregistré : {timestamp} - {latitude}, {longitude}, Altitude: {altitude}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Arrêt de l'enregistrement GPS")

# Envoi automatique du fichier
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    with open(FILENAME, "rb") as f:
        data = f.read()
        client.sendall(data)

    client.shutdown(socket.SHUT_WR)
    response = client.recv(1024)
    print("Réponse du serveur :", response.decode())

    client.close()
except Exception as e:
    print(f"Erreur lors de l'envoi : {e}")
