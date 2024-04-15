# Import socket module
from socket import *
import sys

if len(sys.argv) != 2:
    print("Usage: python3 client.py <svr_port>")
    sys.exit(1)

server_port = int(sys.argv[1])


def main():
    # local host IP '127.0.0.1'
    host = 'ecs-coding1.csus.edu'

    # Define the port on which you want to connect
    # port = 12345

    server_socket = socket(AF_INET, SOCK_STREAM)

    # connect to server on local computer
    server_socket.connect((host, server_port))

    # message you send to server
    message = "Hello, this is threading program"
    while True:

        command = input("Enter Command ")
        message = command
        # message sent to server
        server_socket.send(message.encode('ascii'))

        # message received from server
        data = server_socket.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
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

