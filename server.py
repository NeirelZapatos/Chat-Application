# import socket programming library
from socket import *
# import thread module
from threading import *
import sys

if len(sys.argv) != 2:
    print("Usage: python3 server.py <svr_port>")
    sys.exit(1)

server_port = int(sys.argv[1])

active_users = {}
stored_threads = {}


# thread function
def threaded(client_socket):
    while True:
        # data received from client
        data = client_socket.recv(1024)
        data = str(data.decode('ascii'))
        command = data.split()[0]

        if not data:
            print('Disconnecting')
            # lock released on exit
            # print_lock.release()
            break

        if command == "JOIN":
            username = data.split()[1]
            if client_socket in active_users:
                message = "Client can't have multiple users"
                client_socket.send(message.encode("ascii"))
            elif username in active_users.values():
                message = "Username already in use"
                client_socket.send(message.encode("ascii"))
            elif len(active_users) >= 10:
                message = "Too many users"
                client_socket.send(message.encode("ascii"))
            else:
                active_users[client_socket] = username
                message = f"You have joined as {username}"
                client_socket.send(message.encode("ascii"))
                print(f"{username} Joined the Chatroom")
            # print(active_users)
    # connection closed
    client_socket.close()


def main():
    host = ""

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    # port = 12345

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

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        address = f"{addr[0]} : {addr[1]}"

        # Start a new thread and return its identifier
        if address not in stored_threads:
            thread = Thread(target=threaded, args=(client_socket,))
            # receive_thread = threading.Thread(target=receive,args=(nickname, client_socket,))
            stored_threads[address] = thread
            thread.start()

    server_socket.close()


if __name__ == '__main__':
    main()
