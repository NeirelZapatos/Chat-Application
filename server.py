# import socket programming library
from socket import *
# import thread module
from threading import *
# system module
import sys

# checks if the right amount of arguments were passed
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
            username = active_users[client_socket]
            print(f'Disconnecting {username}')
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
                # Needed for the user joining server side
                client_socket.send(f"{username} joined! Connected to server!".encode("ascii"))
                for client_sock, user in active_users.items():  # Added to broadcast message user Joined!
                    if client_sock != client_socket:
                        client_sock.send(f"{username} joined!".encode("ascii"))

            client_socket.send(message.encode("ascii"))

        elif command == "LIST":
            if client_socket in active_users:
                message = "Users in Chatroom: "
                user_list = list(active_users.values())
                if user_list:
                    message += ', '.join(user_list)
            else:
                message = "Only Users can use the LIST command"

            client_socket.send(message.encode("ascii"))

        # send messages to individual clients
        elif command == "MESG":
            if client_socket in active_users:
                recipient = data.split()[1]
                message = ' '.join(data.split()[2:])
                if recipient in active_users.values():
                    for user_socket, mesg_user in active_users.items():
                        if mesg_user == recipient:
                            user_socket.send(f"Message from {username}: {message}".encode("ascii"))
                else:
                    client_socket.send("Recipient not found".encode("ascii"))
            else:
                client_socket.send("Only Users can use the MESG command".encode("ascii"))

        # sends messages to all users
        elif command == "BCST":
            if client_socket in active_users:
                message = ' '.join(data.split()[1:])
                for client_socket in active_users.keys():
                    client_socket.send(f"{username} : {message}".encode("ascii"))
            else:
                client_socket.send("Only Users can use the BCST command".encode("ascii"))

        # disconnects user
        elif command == "QUIT":
            if client_socket in active_users:
                username = active_users[client_socket]
                print(f'Disconnecting {username}')
                message = f"{username} has Disconnected"
                if client_socket in active_users:
                    del active_users[client_socket]
                for user_socket in active_users.keys():
                    user_socket.send(message.encode("ascii"))
                break
            else:
                client_socket.send("Only Users can use the QUIT command".encode("ascii"))

        # command not possible
        else:
            client_socket.send("That is not a Valid Command".encode("ascii"))

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
        thread.start()

    # closes the socket
    server_socket.close()


if __name__ == '__main__':
    main()
