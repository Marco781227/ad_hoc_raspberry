import socket

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as serversocket : 
    serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    serversocket.bind(('', 5000))  
    serversocket.listen(1) 

    client_socket, client_address = serversocket.accept()

    with open('programme.py', "wb") as f: 
        segment_index = 0 
        while True:
            data = client_socket.recv(1024) 
            if not data:
                break  

            f.write(data)  
            print(f"Reçu segment {segment_index}")

            ack = str(segment_index).encode()
            client_socket.send(ack)
            segment_index += 1  

print("Fichier reçu ")
client_socket.close()
serversocket.close()
