import socket
import threading
from time import sleep

ss= socket.socket()#sending socet

print("Sending Socket created for client")

rs = socket.socket() # recieving socket

print("Receiving Socket created for client")

port= 9900
#1)---
#we should on which port number and IP address our server
#-is binded to


def is_correct(username):
	for character in username:
		if ord(character)>=65 and ord(character)<=90 or ord(character)>=97 and ord(character)<=122 or ord(character)>=48 and ord(character)<=57:
			continue
		else :	
			return False

	return True

username = input("ENTER USERNAME - ")#username input taken
#2)-----
#username check is also happening at client why to bother server for it
#only alphabet - lower and upper and numberical value 
while(is_correct(username)!=True):
	print("ERROR 100 Malformed username\n \n")
	username = input("ENTER USERNAME - ")


print("USERNAME IS VALID")


rtsm= "REGISTER TOSEND " + username + '\n\n'
rtrm ="REGISTER TORECV " + username + '\n\n'


love= input("Press ENTER TO REGISTER-")
while love!="":
	print("ERROR 101 No user registered \n \n")
	print("ERROR: REGISTER BEFORE SENDING MESSAGES")
	love= input("Press ENTER TO REGISTER-")

#3)----------------------
#at client only ERROR message of REGISTRATION IS NOT COMPLETED YET
#sender is not sending the the error message why to bother server for this
# this problem will be solved at client part only na..

ss.connect(('127.0.0.1',port))
ss.send(bytes(rtsm, 'utf-8'))
love=ss.recv(1024).decode()

print("Sending socket Registered Succesfullly")

rs.connect(('127.0.0.1' ,port))
rs.send(bytes(rtrm , 'utf-8'))
print(rs.recv(1024).decode())

print("Receiving  socket Registered Succesfullly")

print("REGISTRATION DONE SUCCESSFULLY")
print("READY TO SEND AND RECIEVE")

        
def do_something():
	
	while True:
		name= input("")
		while name.find("@")== -1 or name.find(" ") ==-1 or name.find("@")>name.find(" "): 
		#if input line don't have @ adn " " ask him to write again 
		#or space position come before @ position
			print("TYPE INPUT CORRCTLY")
			name= input(" ")
				
		reciptname= name[1:name.find(" ")]
		reciptmessage=name[name.find(" ")+1: ]
		messagelen=len(name) -name.find(" ")-1
			
		name= "SEND {}\n Content Length:{}\n\n{}".format(reciptname , messagelen,reciptmessage)
			
		ss.send(bytes(name, 'utf-8'))
	
		
def do_something1():
	
	while True:
		name=rs.recv(1024).decode()#forwarded message form server
		#5)------
		#reciving buffer is of size 1024
		sleep(1)
				
		if name.find("FORWARD")!=-1:
				
			if name.find("Content Length")==-1 :#my response(as a recipt response)
				rs.send(bytes("ERROR 103 Header Incomplete\n\n", 'utf-8'))
			else: 
				print("Forwarded message : " ,name)
				receivedmessage= "RECIEVED "+name[name.find(" ")+1 :name.find('\n')]+'\n\n'
				rs.send(bytes(receivedmessage,'utf-8' ))
				
		else:
			print("Aknowledgement messeage: " ,name)
			if name== "ERROR 103 Header Incomplete\n\n":
				print("CLOSING THE CONNECTION PLEASE MAKE NEW CONNECTION......")
				break
				#4)---------
				#recived this  when Content Length flag is missing in our--
				#--SEND messsage to server
				#so server send this message and close the connection from server side
				#so we terminate thread2 but can't terminate thread1 so whole program
				#-- is still running
		
t1=threading.Thread(target=do_something)#Thread1 - Sending thread
t2=threading.Thread(target=do_something1)#Thread2 - Sending thread

t1.start()
t2.start()

t1.join()
t2.join()


