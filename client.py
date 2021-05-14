# import all necessary dependencies & libraries
import socket
import threading

# Gives the operator the ability to use an identifier for the chatroom server
nickname = input("Choose a nickname: ")

# connects the client to the server at the specified ip address and port (4 lines of code)
host = '127.0.0.1' # localhost
port = 12700

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12700))

# starts an infinite loop to attempt to recieve information from the server
def receive():
    while True:
        try:
            # recieves a message and decodes the message and unique identifiers
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# starts an infinite loop to send information to the server
# information is assigned identifiers, encoded, then transmitted
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# execute receive
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# execute send
write_thread = threading.Thread(target=write)
write_thread.start()
