import socket
import sys
import os
from port_availibility import checkHost as isOpen

connections=list()
server_toggle=0

def config_connections():    

    global connections

    ip=input("Enter server 1 IP address: ")
    port=input("Enter the port 1 number: ")
    port=int(port,10)
    connections.append((ip,port))

    ip=input("Enter server 2 IP address: ")
    port=input("Enter the port 2 number: ")
    port=int(port,10)
    connections.append((ip,port))

def config_socket():
    global server_toggle

    ip,port=connections[server_toggle]

    if not isOpen(ip,port):
        print("Server ",server_toggle," is down, trying the other")
        server_toggle+=1
        server_toggle=server_toggle%1

    ip,port=connections[server_toggle]

    if not isOpen(ip,port):
        print("Both the server are down, retry after some time")
    

    if not isOpen(ip,port):
        return None

    client=socket.socket()
    client.connect((ip,port))
    return client






def communicate(client):
    username=input("enter the username: ")
    client.send(username.encode())
    data=client.recv(1024)
    data=data.decode()
    if data!="true":
        print(" some issues, closing connection ")
        return
    password=input("enter the password: ")
    client.send(password.encode())
    data=client.recv(1024)
    data=data.decode()
    print(data)
    return
    



client=config_socket()
if client is None:
    print(" Atleast on of server connection not possible ")

try:

    client=config_socket(client,args[1],int(args[2],10))
    data=client.recv(1024)
    data=data.decode()
    print(data)
    print("connection established")
    communicate(client)
    print("Voluntarily exiting the socket")
    client.close()
    # while True:
    #     data=client.recv(1024)
    #     if not data:
    #         break
    #     print(data)

except:
    print("connection broke ")

