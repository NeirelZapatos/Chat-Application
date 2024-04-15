# import socket programming library
import socket
# import thread module
import threading


# thread function
def threaded(cli_sock):
    while True:
        # data received from client
        data = cli_sock.recv(1024)
        if not data:
            print('Disconnecting')

            # lock released on exit
            # print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        cli_sock.send(data)

    # connection closed
    cli_sock.close()


def main():
    host = ""

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind((host, port))
    print("Socket binded to port", port)

    # put the socket into listening mode
    serv_sock.listen(5)
    print("Socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        cli_sock, addr = serv_sock.accept()

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        t1 = threading.Thread(target=threaded, args=(cli_sock,))
        # receive_thread = threading.Thread(target=receive,args=(nickname, client_socket,))
        t1.start()
    serv_sock.close()


if __name__ == '__main__':
    main()
