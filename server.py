"""
Server Program Header

Authors: Phillip Harris, Jenil Shingala, Neirel Zapatos

Course Section: CSC-138-04

Date: 4/19/2024

Description: This server program receives message and command requests from the client side. If the server receives  JOIN  request, 
the server will validate the user by checking to see if the username exists already.  Also, the server checks if there are more than 
10 active users in the chat room. Server will not allow the user to proceed until they are assigned a username.  Once a user successfully 
joins the chatroom, the server will send a message to all users in the chatroom that a new user has joined and a message to the user that 
they have joined the chatroom.  The server also checks if the user is a registered user before allowing for the use of the commands.  LIST 
command provides a list of active users in the chatroom.  MESG command allows users to send messages to other users in the chatroom.  BCST 
command allows users to broadcast messages to all users in the chatroom.  QUIT comman allows users to exit the chatroom.  The server program 
receives and processes the response from the client and, relays the message to the client side.  Once 5 users have joined the chatroom, the 
server will broadcast message.

"""
# import socket programming library
from socket import *
# import thread module
from threading import *
# system module
import sys

# checks if the right amount of arguments were passed
if len(sys.argv) != 2:
    print("\nUsage: python3 server.py <svr_port>\n")
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


        # checks and validates the join command
        if command == "JOIN":
            test_username = data.split()[1] #Splits users in the string
            if client_socket in active_users:
                message = "\nClient can't have multiple users"
            elif test_username in active_users.values():
                message = "\nUsername already in use"
            elif len(active_users) >= 10:
                message = "\nToo many users"
            else:
                username = test_username #Username = split up string
                active_users[client_socket] = username #pinpointing user and assigning split string
                message = f"\n{username} Joined! Connected to server!\n"
                print(f"\n{username} Joined the Chatroom")
                for user_socket, user in active_users.items():  # Added to broadcast message user Joined!
                    if user_socket != client_socket:
                        user_socket.send(f"{username} joined!\n".encode("ascii"))

            client_socket.send(message.encode("ascii")) #Send encoded message

        elif command == "LIST":
            if client_socket in active_users:
                message = "\nUsers in Chatroom: "
                user_list = list(active_users.values()) #Creating user_list string
                if user_list:
                    message += ', '.join(user_list) + "\n" # joins each user in list by comma and space
            else:
                message = "\nOnly Users can use the LIST command\n"

            client_socket.send(message.encode("ascii")) #Sending encoded message

        # send messages to individual clients
        elif command == "MESG":
            if client_socket in active_users:
                recipient = data.split()[1]  #Splits recipients in string
                message = ' '.join(data.split()[2:]) #Joins the words of the input data

                #Checking if recipient is an active user
                if recipient in active_users.values():
                    for user_socket, mesg_user in active_users.items(): #Steps through active users
                        if mesg_user == recipient:  #If message sent by user send messages
                            user_socket.send(f"Message from {username}: {message}\n".encode("ascii"))
                            client_socket.send(f"\nSent MESG to {mesg_user}\n".encode("ascii"))
                else: #Else send encoded message "Recipient not found"
                    client_socket.send("\nRecipient not found\n".encode("ascii"))
            else: #Else send encoded message "Only Users can use the MESG command"
                client_socket.send("\nOnly Users can use the MESG command\n".encode("ascii"))

        # sends messages to all users
        elif command == "BCST":
           if client_socket in active_users:
               message = ' '.join(data.split()[1:])  # Joins the words in the message
               for user_socket in active_users.keys():  # For each User in the database send message
                   if user_socket == client_socket:  # Check if the user_socket is not equal to client_socket
                       client_socket.send(f"\n{username} is sending a Broadcast\n".encode("ascii"))
                   else:
                       user_socket.send(f"{username} : {message}\n".encode("ascii"))
           else:
                client_socket.send("\nOnly Users can use the BCST command\n".encode("ascii"))

        # disconnects user
        elif command == "QUIT":
            if client_socket in active_users:
                username = active_users[client_socket] #Assign user to active users
                print(f'\n{username} left the chat server')
                # Message for the user who is quitting
                user_quit_message = f"\n{username} is quitting the chat server\n"
                client_socket.send(user_quit_message.encode("ascii"))
                message = f"{username} left\n"
                if client_socket in active_users:
                    del active_users[client_socket] #Delete user
                for user_socket in active_users.keys(): #Broadcast message that user has left
                    user_socket.send(message.encode("ascii"))
                client_socket.close() #Close the client socket

                break
            else: #Else send/encode invalid user message
                client_socket.send("\nOnly Users can use the QUIT command\n".encode("ascii"))

        # command not possible
        else:
            client_socket.send("\nThat is not a Valid Command\n".encode("ascii"))

    # connection closed
    client_socket.close()


def main():
    # binding the socket
    host = ""
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, server_port))
   # print("Socket binded to port", server_port)

    # put the socket into listening mode
    server_socket.listen(5)
    print("\nThe Chat Server Started")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        client_socket, addr = server_socket.accept()
        if len(active_users) < 10:
            client_socket.send("Enter JOIN followed by your username: ".encode("ascii"))
            address = f"('{addr[0]}' , {addr[1]})"
            print(f"\nConnected with  {address}")

            # lock acquired by client
            # print_lock.acquire()

            # Start a new thread and return its identifier
            thread = Thread(target=threaded, args=(client_socket,))
            thread.start()
        else:
            client_socket.send("\nToo Many Users\n".encode("ascii"))

    # closes the socket
    server_socket.close()


if __name__ == '__main__':
    main()
