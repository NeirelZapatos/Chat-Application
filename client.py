from socket import *
import sys
from threading import Thread


# Function to connect to the server using the given host and port.
def connect_to_server(host, server_port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((host, server_port))
    return server_socket


# Function to receive messages from the server
def client_receive(server_socket):
    while True:
        try:
            data = server_socket.recv(1024)
            print('Received from the server:', str(data.decode('ascii')))
        except:
            print("Error")
            server_socket.close()
            break
        if not data:
            print("Disconnecting")
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

    # Initial message for user to enter username
    print("Enter JOIN followed by your username:")

    return server_socket


# Function to handle command line arguments, set up the connection, and start the chat threads
def check_args_and_start():
    if len(sys.argv) != 3:  #If arguments not 2
        print("Usage: python3 client.py <host> <svr_port>")  #Print usage statement
        sys.exit(1)  #Exit

    server_port = int(sys.argv[2])  #Assign port based on command line argument
    server_socket = setup_connection(server_port)  #Start connection
    start_chat_threads(server_socket)  # Start chat threads


# Function to start the chat threads for sending and receiving messages
def start_chat_threads(server_socket):
    # Creating threads for sending and receiving messages
    send_thread = Thread(target=client_send, args=(server_socket,))
    recv_thread = Thread(target=client_receive, args=(server_socket,))
    # Starting threads
    send_thread.start()
    recv_thread.start()


if __name__ == '__main__':
    check_args_and_start()  #Check arguments and start connection
