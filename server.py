import socket
from threading import Thread

# server's IP address and port number
# Currently local host, change to IP of device on network so 
# that any device on the network can connect
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>" # we will use this to separate the client name & message

# Start list of client sockets connected to the server
client_sockets_list = set()
# create a TCP socket for the client
s = socket.socket()
# set options for the socket so that it is reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the server IP and port
s.bind((SERVER_HOST, SERVER_PORT))
# listen for connections from starting a client
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

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
            print(f"[!] Error: {e}")
            client_sockets.remove(client_socket)
        else:
            # if receive a message, replace the <SEP> 
            # token with ": "
            msg = msg.replace(separator_token, ": ")
        # iterate connected sockets and send the message to each
        for client_socket in client_sockets:
            client_socket.send(msg.encode())


while True:
    # listen for new socket connections from new clients
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new socket to list of connected clients
    client_sockets_list.add(client_socket)
    # Spin up a new thread for each new connected client
    t = Thread(target=listen_for_client, args=(client_socket,))
    # Thread runs in background and closes with end of main program
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for client_socket in client_sockets_list:
    client_socket.close()
# close server socket
s.close()