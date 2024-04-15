# Import socket module
from socket import *
# import system module
import sys

# checks if correct amount of arguments were passed
if len(sys.argv) != 2:
    print("Usage: python3 client.py <svr_port>")
    sys.exit(1)

# init server_port from argument
server_port = int(sys.argv[1])


def main():
    # server host
    host = 'ecs-coding1.csus.edu'

    # creating socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # connect to server on local computer
    server_socket.connect((host, server_port))

    # loops forever
    while True:
        command = input("Enter Command ")
        message = command
        # message sent to server
        server_socket.send(message.encode('ascii'))

        # message received from server
        data = server_socket.recv(1024)

        # print the received message
        print('Received from the server :', str(data.decode('ascii')))

        # ask the client whether he wants to continue
        resp = input('\nDo you want to continue(y/n) :')
        if resp == 'y':
            continue
        else:
            break
            # close the connection
        server_socket.close()


if __name__ == '__main__':
    main()

