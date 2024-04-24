"""

Client Program Header

Authors: Phillip Harris, Jenil Shingala, Neirel Zapatos

Course Section: CSC-138-04

Date: 4/19/2024

Description: This client program allows users to connect to a server via TCP to join a chatroom, send message requests to the respective server, 
as well as command requests such as LIST, JOIN, MESG, and BCST. The client program receives and processes the response from the server and, and 
prints the server response.  Client program will not allow the user to proceed until they are assigned a username. Program also checks for proper
usage of the terminal commands and assigns variables based on usage input.  

"""

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
            print( str(data.decode('ascii')))
        except:
            server_socket.close()
            sys.exit(0)  # Exit the client process
        if not data:
            print("Disconnecting")
            server_socket.close()
            sys.exit(0)  # Exit the client process

# Function to send messages to the server
def client_send(server_socket):
    while True:
        command = input()
        if command == "QUIT":
            server_socket.send(command.encode("ascii")) #Send message to server
            server_socket.close()  # Close the server socket
            sys.exit(0)  # Exit the client process
        else:
            server_socket.send(command.encode("ascii"))

# Function to set up connection to the server and start send/receive threads
def setup_connection(server_port):
    # Server host
    host = 'ecs-coding1.csus.edu'
    # Creating socket and connecting to server
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((host, server_port))

    return server_socket


# Function to handle command line arguments, set up the connection, and start the chat threads
def check_args_and_start():
    if len(sys.argv) != 3:  # If arguments not 2
        print("\nUsage: python3 client.py <host> <svr_port>\n")  # Print usage statement
        sys.exit(1)  # Exit

    server_port = int(sys.argv[2])  # Assign port based on command line argument
    server_socket = setup_connection(server_port)  # Start connection
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
    check_args_and_start()  # Check arguments and start connection
