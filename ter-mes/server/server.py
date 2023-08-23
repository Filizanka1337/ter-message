import socket
import threading
import subprocess
import os

HOST = '0.0.0.0'
PORT = 12345
WEBSITE_PORT = 12346

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []

uploaded_dir = os.path.join(os.getcwd(), "uploaded")
os.makedirs(uploaded_dir, exist_ok=True)

def handle_client(client_socket, client_address):
    print(f"Connected: {client_address}")
    clients.append(client_socket)
    
    if client_address[0] != '127.0.0.1':
        send_website_message(client_socket, client_address)
    
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

def send_website_message(client_socket, client_address):
    website_message = f"if you wanna share files then share it on website of this server, the URL to this site is http://{client_address[0]}:{WEBSITE_PORT}"
    client_socket.send(website_message.encode('utf-8'))

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client)

subprocess.Popen(["python", "start-html.py"])

print("Waiting for connections...")
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
