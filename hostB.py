import socket
import sys
import csv 
import threading

rtl="localhost.rtl"

def get_port():
    with open(rtl, 'r') as database: 
        # print("876t")
        csvreader = csv.reader(database) 
        next(csvreader)
        for fields in csvreader:
            if("B"==fields[0]):
                print("port b is: ", fields[2])
                return int(fields[2],10)

creds = "hb.csv"

def verify(us,ps):
    # print("veri")
    with open(creds, 'r') as database: 
        # print("876t")
        csvreader = csv.reader(database) 
        next(csvreader)
        for fields in csvreader:
            if(us==fields[0]):
                if(ps==fields[1]):
                    return "authorization was successfull"
        return "authorization failed"
    # print("veridone")

def communicate(conn):
    data=conn.recv(1024)
    username=data.decode()
    # print(username,123)
    conn.send(creds.encode())
    data=conn.recv(1024)
    
    password=data.decode()
    # print(password,456)
    result=verify(username,password)
    conn.send(result.encode())


# args=sys.argv
server=socket.socket()
server.bind(('',get_port()))
server.listen(5)

while True:
    conn,address=server.accept()
    print("new connection from ", address)
    communicate(conn)
    conn.close()