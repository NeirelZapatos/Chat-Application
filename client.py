from socket import *
import sys
from threading import Thread

# List to store registered clients
registered_clients = []

# Function to register a user by adding the username to the list of registered clients
def register_user(username):
    registered_clients.append(username) # Append username to list of registered clients
    print(f"{username} has registered successfully.") # Print message

# Function to relay a message from a sender to a recipient if the recipient is registered.
def relay_message(sender, recipient, message, server_socket):
    if recipient not in registered_clients: # If not registered print Unknown Recipient
        print("Unknown Recipient")
        server_socket.send("Unknown Recipient".encode('ascii')) # Encode message to ascii and send to server
    else:
        server_socket.send(f"{sender} says: {message}".encode('ascii')) # Encode message to ascii and send to server

# Function to broadcast a message from a sender to all registered clients except the sender.
def broadcast_message(sender, message, server_socket):
    for client in registered_clients: # Stepping through the list of registered clients
        if client != sender: # If the client is not the sender
            server_socket.send(f"{sender} broadcasts: {message}".encode('ascii')) # Encode message/send

# Function to connect to the server using the given host and port.
def connect_to_server(host, server_port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((host, server_port))
    return server_socket

# Function to process the register command
def process_register_command(command):
    username = parse_register_command(command)
    register_user(username)

# Function to process the relay message
def process_relay_command(command, server_socket):
    sender, recipient, message = parse_message_command(command)
    relay_message(sender, recipient, message, server_socket)

# Function to process the broadcast command
def process_broadcast_command(command, server_socket):
    sender, message = parse_broadcast_command(command)
    broadcast_message(sender, message, server_socket)

# Function to parse the register command and extract the username
def parse_register_command(command):
    return command.split(' ')[1]

# Function to parse the message command and extract the sender, recipient, and message
def parse_message_command(command):
    parts = command.split(' ')
    sender = parts[1]
    recipient = parts[2]
    message = ' '.join(parts[3:])
    return sender, recipient, message

# Function to parse the broadcast command and extract the sender and message
def parse_broadcast_command(command):
    parts = command.split(' ')
    sender = parts[1]
    message = ' '.join(parts[2:])
    return sender, message

# Function to handle the received command
def handle_received_command(command, server_socket):
    if command.startswith('REG'):
        process_register_command(command)
    elif command.startswith('MESG'):
        process_relay_command(command, server_socket)
    elif command.startswith('BCST'):
        process_broadcast_command(command, server_socket)

# Function to receive messages from the server
def client_receive(server_socket):
    while True:
        try:
            data = server_socket.recv(1024)
            print('Received from the server:', str(data.decode('ascii')))
            command = data.decode('ascii')
            handle_received_command(command, server_socket)
        except:
            print("Error")
            server_socket.close()
            break

# Function to send messages to the server
def client_send(server_socket):
    while True:
        command = input()
        server_socket.send(command.encode("ascii"))

# Function to set up connection to the server and start send/receive threads
def setup_connection(server_port):
    # Server host
    host = 'ecs-coding1.csus.edu'
    # Creating socket and connecting to server
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((host, server_port))
    # Creating threads for sending and receiving messages
    send_thread = Thread(target=client_send, args=(server_socket,))
    recv_thread = Thread(target=client_receive, args=(server_socket,))
    # Starting threads
    send_thread.start()
    recv_thread.start()

# Function to check command line arguments and start the connection
def check_args_and_start():
    if len(sys.argv) != 2: #If arguments not 2
        print("Usage: python3 client.py <svr_port>") #Print usage statement
        sys.exit(1) #Exit

    server_port = int(sys.argv[1]) #Assign port based on command line argument
    setup_connection(server_port) #Start connection

if __name__ == '__main__':
    check_args_and_start() #Check arguments and start connection
