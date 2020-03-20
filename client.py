import socket
import sys
import os
import hashlib 
from objects import *



def create_sockets(ip1,port1,ip2,port2):
	sockets=[]
	socket1=socket.socket()
	try:
		socket1.connect((ip1,port1))
		result,reply=just_recieve(socket1)
		if result:
			print("initial handshake socket1: ",reply)
			sockets.append(socket1)
	except Exception as e: 
		print(e)
		print("socket 1 failed")
	# print("===========================")
	socket2=socket.socket()
	try:
		socket2.connect((ip2,port2))
		result,reply=just_recieve(socket2)
		if result:
			print("initial handshake socket2",reply)
			sockets.append(socket2)
	except Exception as e:
		print(e)
		print("socket 2 failed")
	return sockets


def complete_authentication(sockets,username,password):
	# sockets=list()
	delete=[]
	for server in sockets:        
		result=just_send(server,username)
		if not result:
			server.close()
			delete.append(server)
			# sockets.remove(server)
			continue
			# return False
		result,reply=just_recieve(server)
		if not result:
			server.close()
			delete.append(server)
			# sockets.remove(server)
			continue
		print(reply)

		result=just_send(server,password)
		if not result:
			server.close()
			sockets.remove(server)
			continue
		result,reply=just_recieve(server)
		if not result:
			server.close()
			delete.append(server)
			# sockets.remove(server)
			continue
		print("verification result ", reply)

		if reply.startswith("False"):
			server.close()
			delete.append(server)
			# sockets.remove(server)
			continue
	for server in delete:
		sockets.remove(server)
	if len(sockets)==0:
		return False
	return True

def split_data(file, frame_size):
	while True:
		data = file.read(frame_size)
		if not data:
			break
		yield data

# def create_frame(data,frame_number):
# 	print(data,frame_number)
# 	data=str(frame_number)+data
# 	data=data.encode()
# 	checksum=hashlib.md5(data)
# 	data=data+checksum
# 	return data
		

def send_frame(sockets,frame):
	if len(sockets)==0:
		return False,""
	for i in range(len(sockets)):
		result,reply=send_wait_receive(sockets[i],frame)
		if not result:
			continue
		if result and reply=="1":
			sockets.reverse()
			return True,"1"
		if result and reply=="0":
			return True,"0"
	sockets.reverse()
	return False

# max_time=5
# frame_size=1024
# max_attempts=4

utility(max_attempts,frame_size)

# ip1=input("Enter the ip address of server 1: ")
ip1="localhost"
porttemp="300"
port1=input("Enter the port of server 1: ")
port1=int(porttemp+port1,10)
# ip2=input("Enter the ip address of server 2: ")
# port2=input("Enter the port of server 2: ")
# port2=int(port2,10)
port2=port1


sockets=create_sockets(ip1,port1,ip1,port2)
if len(sockets)==0:
	print("No connection were found")
	exit()
# starting connection
#()()
username="nikhil"
password="password"
# username=input("Enter the username: ")
# password=input("Enter the password: ")
result=complete_authentication(sockets,username,password)
if not result:
	print("Verification unsucessfull")
	exit()

print("verification sucessfull, initiating file transfer")

''''''


for conn in sockets:
	conn.settimeout(rttime)

filename=input("Enter the file path: ")
frame_number=0

with open(filename, 'rb') as f:
	while 1:
		data = f.read(frame_size)
		if not data:
			break
		# print(byte_s)
		print("Read in client: ",data)
		frame_number+=1
		frame=frame_blueprint(content=data,frame_number=frame_number)
		while True:
			result,reply=send_frame(sockets,frame.to_string())
			if not result:
				print("File not sent")
				exit()
			elif reply=="1":
				break		

with open(filename) as file:

	for data in split_data(file,frame_size):
		frame_number+=1
		frame=frame_blueprint(data,frame_number)
		while True:
			result,reply=send_frame(sockets,frame.to_string())
			if not result:
				print("File not sent")
				exit()
			elif reply=="1":
				break			

print("File uploaded")
for conn in sockets:
	conn.close()

			






# def send(data):
#     global sockets,retry_threshold,frame_number
#     if len(sockets)==0:
#         return False
#     client=sockets[0]

#     ## sending
#     for i in range(retry_threshold):
#         try:
#             client.sendall(data)
#         except:
#             if len(sockets)==1:
#                 return False
#             print("server connection failed, retrying with other server")
#             sockets.reverse()
#             return send(data)

#         ## recieving
#         try:
#             reply=client.recv(1024)
#             frame_number=reply
#         except:
#             print("ack not recieved, retrying for ",i," th time")
#             continue

#         print("frame successfully sent")        
#         sockets.reverse()
#         return True
#     print("Frame was not sent")
#     return False

# def authentication_request():    
#     username=input("enter the username: ")
	
#     for sockets 
#     client.send(username.encode())
#     data=client.recv(1024)
#     data=data.decode()
#     if data!="true":
#         print(" some issues, closing connection ")
#         return False
#     password=input("enter the password: ")
#     client.send(password.encode())
#     data=client.recv(1024)
#     data=data.decode()
#     if data=="Verified":
#         return True
#     else:
#         return False




# config_connections()
# create_socket()

# filename=input("Enter the path to the file: ")
# frame_size=input("Enter the frame size(in KB) :")
# frame_size=int(frame_size)

# frame_number=0
# try:
#     with open(filename) as file:

#         for data in split_data(file,frame_size):
#             frame_number+=1
#             data=create_frame(data,frame_number)
#             result=send(data)
#             if not result:
#                 print("File not sent")
#                 exit
			

		


