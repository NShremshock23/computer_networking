import socket
from threading import Thread

# server'server_socket IP address and port number
# Currently local host, change to IP of device on network so 
# that any device on the network can connect
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<COL>" # we will use this to separate the client name & message

# Start list of client sockets connected to the server
client_sockets_list = set()
# create a TCP socket for the client
server_socket = socket.socket()
# set options for the socket so that it is reusable
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the server IP and port
server_socket.bind((SERVER_HOST, SERVER_PORT))
# listen for connections from starting a client
server_socket.listen(5)
print(f"### {SERVER_HOST}:{SERVER_PORT} listening...")

def listen_for_client(client_socket):
    """
    :param client_socket: socket for client
    This function listens for packets from the client socket.
    When a message is received, send it to all connected clients.
    """
    while True:
        try:
            # listen for packets from passed in socket
            orig_msg = client_socket.recv(1024).split(b'\x00')[-1]
            msg = orig_msg.decode() # decode the received message
        except Exception as e:
            # Exception occurs if client is not connected anymore.
            # in this case remove the client from the list
            print(f"Error: {e}")
            client_sockets.remove(client_socket)
        else:
            # if receive a message, replace the <COL> 
            # token with ": "
            msg = msg.replace(separator_token, ": ")
        # iterate connected sockets and send the message to each
        for client_socket_entry in client_sockets_list:
            client_socket_entry.send(msg.encode())


while True:
    # listen for new socket connections from new clients
    client_socket, client_address = server_socket.accept()
    print(f"+ {client_address} connected.")
    # add the new socket to list of connected clients
    client_sockets_list.add(client_socket)
    # Spin up a new thread for each new connected client
    server_thread = Thread(target=listen_for_client, args=(client_socket,))
    # Thread runs in background and closes with end of main program
    server_thread.daemon = True
    # start the thread
    server_thread.start()

# close client sockets
for client_socket_entry in client_sockets_list:
    client_socket_entry.close()
# close server socket
server_socket.close()