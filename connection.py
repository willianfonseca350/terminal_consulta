import socket
import time
from terminal import await_terminal_query, check_terminal_alive, set_always_on

from commands import Receive_Cmd, Send_Cmd
from rich import print


# Create a server socket
ip_server = "192.168.1.33"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_server, 6500))
server.listen()
print(f'Listening: {ip_server}:6500')

# Accept a connection from a client
client = server.accept()[0]

# Send a command to the client
client.send(Send_Cmd.OK.value)
time.sleep(0.5)

# Receive a response from the client
response = client.recv(255)
response = response.decode("ascii")

if response.find('|'):
    if Receive_Cmd(response.split('|')[0][0:3]) == Receive_Cmd.RESPONSE_OK:
        print('Client connected')
        check_terminal_alive(client)
        set_always_on(client)
        await_terminal_query(client)
        print('fim')

