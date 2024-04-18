# Import socket module
from socket import *
# import system module
import sys
# import threading module
from threading import *

# checks if correct amount of arguments were passed
if len(sys.argv) != 2:
    print("Usage: python3 client.py <svr_port>")
    sys.exit(1)

# init server_port from argument
server_port = int(sys.argv[1])


def client_receive(server_socket):
    # message received from server
    while True:
        try:
            data = server_socket.recv(1024)
            print('Received from the server : ', str(data.decode('ascii')))
        except:
            print("Error")
            server_socket.close()
            break
        if not data:
            print("Disconnecting")
            server_socket.close()
            break

    sys.exit(1)


def client_send(server_socket):
    # message sent to server
    while True:
        command = input()
        server_socket.send(command.encode("ascii"))


def main():
    # server host
    host = 'ecs-coding1.csus.edu'

    # creating socket and connecting to server
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((host, server_port))

    # creating threads
    send_thread = Thread(target=client_send, args=(server_socket,))
    recv_thread = Thread(target=client_receive, args=(server_socket,))
    send_thread.start()
    recv_thread.start()

    # IGNORE COMMENTS BELOW THIS
    # ask the client whether he wants to continue
    # resp = input('\nDo you want to continue(y/n) :')
    # if resp == 'y':
    #     continue
    # else:
    #     break


if __name__ == '__main__':
    main()