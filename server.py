# import socket programming library
from socket import *
# import thread module
from threading import *
#  system module
import sys

# checks if right amount of arguments were passed
if len(sys.argv) != 2:
    print("Usage: python3 server.py <svr_port>")
    sys.exit(1)

# server port set from argument
server_port = int(sys.argv[1])

# init dicts
active_users = {}

# thread function
def threaded(client_socket):
    # loops until break
    while True:
        # data received from client
        data = client_socket.recv(1024)
        data = str(data.decode('ascii'))

        # checks the command
        if len(data.split()) > 1:
            command = data.split()[0]
        else:
            command = data

        # if no data returned this disconnect
        if not data:
            print('Disconnecting')
            if client_socket in active_users:
                del active_users[client_socket]
            # lock released on exit
            # print_lock.release()
            break

        # checks and validates the join command
        if command == "JOIN":
            username = data.split()[1]
            if client_socket in active_users:
                message = "Client can't have multiple users"
            elif username in active_users.values():
                message = "Username already in use"
            elif len(active_users) >= 10:
                message = "Too many users"
            else:
                active_users[client_socket] = username
                message = f"You have joined as {username}"
                print(f"{username} Joined the Chatroom")

            client_socket.send(message.encode("ascii"))

        # send the users in chatroom if client is a user currently in the chatroom
        if command == "LIST":
            if client_socket in active_users:
                message = "Users in Chatroom:\n "
                for username in active_users.values():
                    message += f"{username}\n"
            else:
                message = "Only Users can use the LIST command"

            client_socket.send(message.encode("ascii"))

    # connection closed
    client_socket.close()

def main():
    # binding the socket
    host = ""
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, server_port))
    print("Socket binded to port", server_port)

    # put the socket into listening mode
    server_socket.listen(5)
    print("Socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        client_socket, addr = server_socket.accept()
        address = f"{addr[0]} : {addr[1]}"
        print(f"Connected to : {address}")

        # lock acquired by client
        # print_lock.acquire()

        # Start a new thread and return its identifier
        thread = Thread(target=threaded, args=(client_socket,))
        # receive_thread = threading.Thread(target=receive,args=(nickname, client_socket,))
        thread.start()

    # closes socket
    server_socket.close()


if __name__ == '__main__':
    main()
