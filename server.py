# import dependencies and packages
import threading
import socket

# declares the port and ip address for the server (5 lines of code)
host = '127.0.0.1' # localhost
port = 12700

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
# server infinitely listens for a new connection
server.listen()

# creates a variable list of connected usernames in the chatroom server
clients = []
nicknames = []

# broadcasts a message from a user for all connected users to see in the chatroom
def broadcast(message):
    for client in clients:
        client.send(message)

# the handler for the client
# removes a client from the server if the connection becomes severed
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat! Press F to pay respects :)'.encode('ascii'))
            nicknames.remove(nickname)
            break

# handler for the client
# adds a client
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat~'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening... Give it a whirl~")
receive()
