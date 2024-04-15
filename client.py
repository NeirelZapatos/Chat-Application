# Import socket module
import socket


def main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    serv_sock.connect((host, port))

    # message you send to server
    message = "Hello, this is threading program"
    while True:

        # message sent to server
        serv_sock.send(message.encode('ascii'))

        # message received from server
        data = serv_sock.recv(1024)

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
    serv_sock.close()


if __name__ == '__main__':
    main()
