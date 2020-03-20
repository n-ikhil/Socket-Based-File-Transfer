import socket
import sys
import csv 
import threading
from objects import *
from constants import *


rtl="localhost.rtl"

buffers={}

def get_port():
    with open(rtl, 'r') as database: 
        # print("876t")
        csvreader = csv.reader(database) 
        next(csvreader)
        for fields in csvreader:
            if("A"==fields[0]):
                print("port a is: ", fields[2])
                return int(fields[2],10)

creds = "ha.csv"

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

def write_to_file(filname,username):
    
    global buffers
    # print(username,buffers)
    if username not in buffers:
        return True
    buf=buffers[username]
    try :
        f=open(filname+".txt","w") 
        size=len(buf)
        for i in range(size):
            frame_number=i+1
            for item in buf:
                number=int(item.header,10)
                # print(number,frame_number,item.content)
                if number==frame_number:
                    data=item.content
                    # print(data,type(data))
                    # data=str()
                    # data.decode('ascii')
                    
                    f.write(data)
        del buffers[username]
        f.close()
        return True
    except Exception as e:
        print(e)
        return False


def communicate(conn,address):
    global buffers
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
    #----------------------------------------
    if not result or check.startswith("False"):
        conn.close()
        return False
    ## further exchanging
    recieving=True
    # buffers[username]=[]
    if username not in buffers:
        buffers[username]=[]
    buf=buffers[username]
    while recieving:
        result,data=just_recieve(conn)
        if not result:
            conn.close()
            return
        if data=="":
            continue
        inframe=frame_blueprint(content=data)
        # print(inframe.content,buf)
        if inframe.valid:
            msg="1"
            # frame_number=int(inframe.header,10)
            # s
            if inframe.content==flag:
                result=write_to_file(filname=username,username=username)
                if not result:
                    msg="3"
                    print("some error writing file")
                    recieving=False
                else:
                    print("successfully wrote file")
                    msg="4"
                    recieving=False
                    # conn.close()
                # server.close()
            else:
                buf.append(inframe)
        else:
            msg="0"
        # print(inframe.content,buf,msg)
        result=just_send(conn,msg)
        if msg=="3" or msg=="4":
            conn.close()
        if not result:
            return

    
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