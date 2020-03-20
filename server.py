import socket
import sys
import csv 
import threading
from objects import *

creds = "../data_files/login_credentials.csv"

success="True , "
failure="False , "

secondary_servers=[]
wait_time=10
max_attempts=2


sock=[0,0,0,0]
ip=[0,0,0,0]




rtl="localhost.rtl"



def get_port():
    global sock,ip,secondary_servers
    with open(rtl, 'r') as database: 
        # print("876t")
        csvreader = csv.reader(database) 
        next(csvreader)
        for fields in csvreader:
            if("A"==fields[0]):
                # print("port a is: ", fields[2])
                # return int(fields[2],10)
                sock[0]=int(fields[2],10)
                ip[0]=fields[1]
                secondary_servers.append((ip[0],sock[0]))
            elif("B"==fields[0]):
                # print("port a is: ", fields[2])
                # return int(fields[2],10)
                sock[1]=int(fields[2],10)
                ip[1]=fields[1]
                secondary_servers.append((ip[1],sock[1]))
            elif("C"==fields[0]):
                # print("port a is: ", fields[2])
                # return int(fields[2],10)
                sock[2]=int(fields[2],10)
                ip[2]=fields[1]
                secondary_servers.append((ip[2],sock[2]))
            elif("D"==fields[0]):
                # print("port a is: ", fields[2])
                # return int(fields[2],10)
                sock[3]=int(fields[2],10)
                ip[3]=fields[1]
                # attendance_server=(ip[3],sock[3])
                # secondary_servers.append((ip[3],sock[3]))
        for s in sock:
            print(s)

def verify(username,password):

    global secondary_servers
    

    for item in secondary_servers:
        try:
            socket_conn=socket.socket()
            socket_conn.connect((item[0],item[1]))
            result,reply=just_recieve(socket_conn)
            if not result:
                socket_conn.close()
                continue
            print(reply)
            result=just_send(socket_conn,username)
            if not result:
                socket_conn.close()
                continue
            result,reply=just_recieve(socket_conn)
            if not result:
                continue
            print(reply)
            result=just_send(socket_conn,password)
            if not result:
                socket_conn.close()
                continue
            result,reply=just_recieve(socket_conn)
            if not result:
                socket_conn.close()
                continue
            print(reply)
            
            if reply.startswith("True"):
                return True,socket_conn
            socket_conn.close()
        except Exception as e:
            print(e)
            print("error")

    return False,None

def check_attendance(username):
    global ip
    attendance=socket.socket()
    attendance.connect((ip[3],sock[3]))
    result,reply=send_and_wait(attendance,username)
    attendance.close()
    if not result:
        return False    
    return result,reply

def get_and_forward(conn,hsocket):
    result,frame_incoming=just_recieve(conn)
    if not result:
        return 0
    print(frame_incoming)
    result,reply=send_wait_receive(hsocket,frame_incoming)
    if reply=="0":
        return 1
    




def communicate(conn,address):

    ''' below is section for simple starting communication '''

    msg="connection accepted by layer1 server a"+str(address)+"\n send username"
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
    ''' username and password are now obtained '''
    
    result,hsocket=verify(username,password)
    # result=True
    if not result:
        msg="False"
        result=just_send(conn,msg)
        conn.close()
        return False
    
    msg="True"
    result=just_send(conn,msg)

    # frame_input=get_frame(conn,hsocket)
    print("waiting to recieve file data")
    '''initiate data transfer'''

    recieving=True

    while recieving:
        result,data=just_recieve(conn)
        if not result:
            conn.close()
            hsocket.close()
            recieving=False
            return
        if data=="":
            continue
        ''''''
        result,reply=send_wait_receive(hsocket,data)
        if not result:
            msg="3"
            just_send(conn,msg)
            conn.close()
            hsocket.close()
            recieving=False
            return

        result=just_send(conn,reply)
        if not result:
            hsocket.close()
            conn.close()
            recieving=False
            return
        

        inframe=frame_blueprint(content=data)
        print(inframe.content)
        if inframe.valid:
            msg="1"
        else:
            msg="0"
        result=just_send(conn,msg)

        if not result:
            recieving=False
    return
    #  while recieving:
    #         result,data=just_recieve(conn)
    #     if not result:
    #         conn.close()
    #     if data=="":
    #         continue
    #     inframe=frame_blueprint(content=data)
    #     print(inframe.content)
    #     if inframe.valid:
    #         msg="1"
    #     else:
    #         msg="0"
    #     result=just_send(conn,msg)

    #     if not result:
    #         return

    # while recieving:
        # recieving,data=get_and_forward(conn,hsocket)
    # result,reply=just_recieve(hsocket)
    # print(reply)
    

    # return True
    # result=True
    # reply="True"
    # hsocket=""
    # login=reply
    # msg="False"
    # if not result:
    #     just_send(conn,msg)
    #     conn.close()
    #     return False
    # msg="True"
    # just_send(conn,msg)
    # # attendance=check_attendance(username)

    # reply="Yes at"
    # attendance=reply
    # msg="False"
    # if not result:
    #     just_send(conn,msg)
    #     conn.close()
    #     return False
    
    # msg=login + attendance
    # result=just_send(conn,msg)

    # conn.close()
    # if result:
    #     return True
    # return False
    

get_port()
server=socket.socket()
# ()()
porttemp="300"
port=input("Enter the port to open : ")
port=int(porttemp+port,10)
server.bind(('',port))
server.listen(5)
print("Server created")
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
    
    # thread.start_ communicate(new_conn)
    

