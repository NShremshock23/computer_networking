import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
from tcp_packet import TCPPacket

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address and port number
# Currently local host, change to IP of device on network so 
# that any device on the network can connect
SERVER_HOST = "0.0.0.0" 
SERVER_PORT = 5002
separator_token = "<COL>" # we will use this to separate the client name & message

# initialize TCP socket
client_socket = socket.socket()
print(f"### Attempting to connect to {SERVER_HOST}:{SERVER_PORT}")
# connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("+ Connected to server.")
# Name for the client
name = input("Enter name: ")

def listen_for_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print("\n" + message)

# create thread that will listen for messages
client_thread = Thread(target=listen_for_messages)
# runs in background and ends with main program
client_thread.daemon = True
# start
client_thread.start()

while True:
    # get input to send as message
    to_send = input()
    # exit the program
    if to_send.lower() == 'q':
        break
    # add the date and time, name of the client and what color to use
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # create the packet
    pkt = TCPPacket(
        '0.0.0.0',
        20,
        SERVER_HOST, # Server IP
        SERVER_PORT, # Server Port
        to_send.encode(), # Encode the message to be sent
        0b000101001
    )
    pkt_built = pkt.build() # build the packet structure
    client_socket.sendto(pkt_built, (SERVER_HOST, SERVER_PORT)) # send the pacet to the server

# close the socket being used
client_socket.close()