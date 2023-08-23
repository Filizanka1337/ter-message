import socket
import threading
import cmd

class SimpleChatClientCLI(cmd.Cmd):
    intro = "Welcome to ter-mes Client. Type 'connect' to connect to a server.\n"
    prompt = "(ter-mes) "
    
    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.receive_thread = None
        self.selected_name = socket.gethostname()
        
    def do_connect(self, args):
        """Connect to a server. Usage: connect <server_ip> <server_port>"""
        try:
            server_ip, server_port = args.split()
            server_port = int(server_port)
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, server_port))
            
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
            
            print("Connected to the server.")
            
        except Exception as e:
            print(f"Failed to connect to the server: {str(e)}")
            
    def do_send(self, message):
        """Send a message to the server. Usage: send <message>"""
        if self.client_socket:
            message_with_name = f"{self.selected_name}: {message}"
            self.client_socket.send(message_with_name.encode('utf-8'))
        else:
            print("Not connected to a server.")
            
    def do_disconnect(self, args):
        """Disconnect from the server."""
        if self.client_socket:
            self.client_socket.close()
            print("Disconnected from the server.")
        else:
            print("Not connected to a server.")
            
    def do_nickname(self, new_name):
        """Change your nickname. Usage: nickname <new_name>"""
        if new_name:
            self.selected_name = new_name
            print(f"Nickname changed to '{new_name}'.")
        else:
            print("Please provide a new nickname.")
            
    def do_exit(self, args):
        """Exit the client."""
        if self.client_socket:
            self.client_socket.close()
        print("Exiting.")
        return True
        
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                print(message)
            except:
                break

if __name__ == "__main__":
    cli = SimpleChatClientCLI()
    cli.cmdloop()
