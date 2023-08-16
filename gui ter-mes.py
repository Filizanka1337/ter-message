import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class SimpleChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chat Client")

        self.server_ip_label = tk.Label(root, text="Server IP:")
        self.server_ip_label.grid(row=0, column=0, padx=5, pady=3, sticky="e")

        self.server_ip_entry = tk.Entry(root)
        self.server_ip_entry.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        self.server_port_label = tk.Label(root, text="Server Port:")
        self.server_port_label.grid(row=0, column=2, padx=5, pady=3, sticky="e")

        self.server_port_entry = tk.Entry(root)
        self.server_port_entry.grid(row=0, column=3, padx=5, pady=3, sticky="w")

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=0, column=4, padx=5, pady=3)

        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect_from_server, state=tk.DISABLED)
        self.disconnect_button.grid(row=0, column=5, padx=5, pady=3)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_chat)
        self.clear_button.grid(row=0, column=6, padx=5, pady=3)

        self.client_socket = None
        self.receive_thread = None

        self.chat_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.grid(row=1, column=0, columnspan=7, padx=5, pady=5, sticky="nsew")

        self.message_entry = tk.Entry(root)
        self.message_entry.grid(row=2, column=0, padx=5, pady=3, columnspan=5, sticky="nsew")
        self.message_entry.bind("<Return>", self.send_message_event)
        self.message_entry.bind("<KeyRelease>", self.update_send_button_state)

        self.send_button = tk.Button(root, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=2, column=5, padx=5, pady=3, sticky="nsew")

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)
        root.grid_columnconfigure(4, weight=1)
        root.grid_columnconfigure(5, weight=1)

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get()
        server_port = int(self.server_port_entry.get())

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, server_port))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the server:\n{str(e)}")
            return

        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def disconnect_from_server(self):
        self.client_socket.close()

        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.client_socket.send(f"{socket.gethostname()}: {message}".encode('utf-8'))
            self.message_entry.delete(0, tk.END)
        self.update_send_button_state()

    def send_message_event(self, event):
        self.send_message()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_text.config(state=tk.NORMAL)
                self.chat_text.insert(tk.END, message + '\n')
                self.chat_text.config(state=tk.DISABLED)
            except:
                break

    def clear_chat(self):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def update_send_button_state(self, event=None):
        if self.client_socket:
            message = self.message_entry.get().strip()
            if message:
                self.send_button.config(state=tk.NORMAL)
            else:
                self.send_button.config(state=tk.DISABLED)
        else:
            self.send_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleChatClientGUI(root)
    root.mainloop()
