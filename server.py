import socket
import threading

HOST = '0.0.0.0'  # Nasłuchuj na wszystkich interfejsach
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []

def handle_client(client_socket, client_address):
    print(f"Connected: {client_address}")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            print(f"{client_address[0]}: {message}")
            broadcast(message)
        except:
            break

    print(f"Disconnected: {client_address}")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client)

print("Waiting for connections...")
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
