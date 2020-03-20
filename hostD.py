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
            if("D"==fields[0]):
                print("port d is: ", fields[2])
                return int(fields[2],10)

creds = "../data_files/attendance.csv"

def verify(us):
    # print("veri")
    with open(creds, 'r') as database: 
        # print("876t")
        csvreader = csv.reader(database) 
        next(csvreader)
        for fields in csvreader:
            if(us==fields[1]):
                pres=0
                for dat in fields:
                    if dat=="Done":
                        pres=pres+1
                tot=len(fields)-2
                percentage=pres/tot*100
                print(pres,tot,percentage)
                if percentage>=80:
                    return " and you have exclusive access due to better attendance "
                else:
                    return " no exclusive access, attendance below minimum "

                
    # print("veridone")

def communicate(conn):
    data=conn.recv(1024)
    username=data.decode()
    result=verify(username)
    conn.send(result.encode())



server=socket.socket()
server.bind(('',get_port()))
server.listen(5)

while True:
    conn,address=server.accept()
    print("new connection from ", address)
    communicate(conn)
    conn.close()