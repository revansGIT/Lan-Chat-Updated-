import socket
import threading

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to all available interfaces and a port
server_ip = '0.0.0.0'
port = 12345  # Reserve a port for your service

try:
    # Bind the socket to the IP address and port
    server_socket.bind((server_ip, port))
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{port}")
except socket.error as e:
    print(f"Error binding to {server_ip}:{port}: {e}")
    server_socket.close()
    exit()

# List to store client connections
clients = []
# Dictionary to store client usernames
usernames = {}

def broadcast(message, sender_client):
    """Broadcasts a message to all clients except the sender."""
    for client in clients:
        if client != sender_client:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def send_private_message(message, sender_client, recipient_username):
    """Sends a private message to a specific user."""
    recipient_client = None
    for client, username in usernames.items():
        if username == recipient_username:
            recipient_client = client
            break
    
    if recipient_client:
        try:
            recipient_client.send(f"Private from {usernames[sender_client]}: {message}".encode('utf-8'))
        except:
            recipient_client.close()
            clients.remove(recipient_client)
    else:
        sender_client.send(f"User {recipient_username} not found.".encode('utf-8'))

def handle_client(client):
    """Handles a single client connection."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                if message.startswith('/'):
                    handle_command(message, client)
                else:
                    username = usernames[client]
                    broadcast(f"{username}: {message}", client)
        except:
            if client in clients:
                clients.remove(client)
            username = usernames.pop(client, None)
            client.close()
            if username:
                broadcast(f"{username} has left the chat.", client)
            break

def handle_command(command, client):
    """Handles commands from clients."""
    parts = command.split(' ', 2)
    cmd = parts[0]
    
    if cmd == '/users':
        client.send(f"Connected users: {', '.join(usernames.values())}".encode('utf-8'))
    elif cmd == '/pm' and len(parts) > 2:
        recipient_username = parts[1]
        private_message = parts[2]
        send_private_message(private_message, client, recipient_username)
    else:
        client.send("Unknown command or incorrect usage.".encode('utf-8'))

# Accept incoming connections
print("Waiting for connections...")
try:
    while True:
        client, addr = server_socket.accept()
        print(f"Got connection from {addr}")
        client.send('Connected to the Group Chat Server!'.encode('utf-8'))

        username = client.recv(1024).decode('utf-8')
        usernames[client] = username
        clients.append(client)

        print(f"Username of the client is {username}")
        broadcast(f"{username} has joined the chat.", client)
        client.send('You are now connected!'.encode('utf-8'))

        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
except KeyboardInterrupt:
    print("Server is shutting down...")
    server_socket.close()
    for client in clients:
        client.close()
