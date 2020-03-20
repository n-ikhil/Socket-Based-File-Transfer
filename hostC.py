import socket
import sys
import csv 
import threading
from objects import *

rtl="localhost.rtl"

def get_port():
    with open(rtl, 'r') as database: 
        # print("876t")
        csvreader = csv.reader(database) 
        next(csvreader)
        for fields in csvreader:
            if("C"==fields[0]):
                print("port c is: ", fields[2])
                return int(fields[2],10)

creds = "hc.csv"

def verify(us,ps):
    # print("veri")
    with open(creds, 'r') as database: 
        # print("876t")
        csvreader = csv.reader(database) 
        next(csvreader)
        for fields in csvreader:
            if(us==fields[0]):
                if(ps==fields[1]):
                    return "True verified"
        return "False , not correct"
    # print("veridone")

def communicate(conn,address):
    ''' copied'''
    msg="connection accepted by host-a"+str(address)+"\n send username"
    result=just_send(conn,msg)
    if not result :
        conn.close()
        return False
    result,reply=just_recieve(conn)
    if not result:
        conn.close()
        return False
    username=reply
    print("username is ",username)
    msg="request password"
    result=just_send(conn,msg)
    if not result:
        conn.close()
        return False
    result,reply=just_recieve(conn)
    if not result:
        conn.close()
        return False
    password=reply
    print("Password is : ", password)
    ''''''
    
    check=verify(username,password)

    result=just_send(conn,check)
    # conn.close()
    if not result or check.startswith("False"):
        conn.close()
        return False
    ## further exchanging
    
    return True


# args=sys.argv
server=socket.socket()
server.bind(('',get_port()))
server.listen(5)
max_listen=100
threads=[None]*max_listen
counter=0

while True:    
    # remote=custom_socket( server.accept())
    remote,address=server.accept()
    print("new connection from ", address)    
    threads[counter]=threading.Thread(target=communicate, args=(remote,address))
    threads[counter].start()
    counter+=1
    counter=counter%100