import socket
import threading
from  time import sleep

s= socket.socket()

dictsc ={}

dictrc={}

port= 9900
s.bind(('127.0.0.1',port))
#1)---
#we have to bind our server to availble port number
#we have bind to IP address 127.0.0.1 'local host'


print("Waiting for connection....")

s.listen(5)
#2)----
#at server I am listening to 5 clients 

def do_something(sc1,rc1):
		   	
	while True:         #first it will send the packet and wait for its acknowledment
		name=sc1.recv(1024).decode()
		print("CLIENT : ",name)
					
		content_length= int(name[name.find(":")+1:name.find('\n\n')])				
		reciptname= name[name.find(" ")+1: name.find('\n')]
		reciptmessage=name[name.find('\n\n')+1:]
		messagelen=len(reciptmessage)-1#actual message length is it		
		forwardmessage= "FORWARD {}\n Content Length :{}\n\n{}".format(reciptname , messagelen,reciptmessage)
															     
		if name.find("Content Length")==-1 :#Content length field not found
			rc1.send(bytes("ERROR 103 Header Incomplete\n\n", 'utf-8'))
			for a in dictrc :
				if dictrc[a]==rc1 :
					dictrc.pop(a)
					dictsc.pop(a)
					print("CLOSING CONNECTION... FOR USERNAME -", a)
					sc1.close()
					rc1.close()
					break
			break
		elif content_length!=messagelen:#content_length != actual message length
			rc1.send(bytes("ERROR 100 Malformed username(content length not equal to message lenth)\n \n", 'utf-8'))	
		
		
		elif reciptname=="ALL" :#send to all
			for a in dictrc :
				if dictrc[a]!=rc1 :
					dictrc[a].send(bytes(forwardmessage ,'utf-8')) #send it to recipt 
					reciptresponse= dictrc[a].recv(1024).decode() #record response f recipt
					rc1.send(bytes(reciptresponse, 'utf-8')) 
					
			#4)-----
			#forwarded packet come from recieve socket from some other thread and here send
			#- send RECIEVE packet along recieve socket and to that thread only
									
			#when sending to ALL send to a recipt wait for response and then send 
			#-to other recipt after reciving response(Acknowlegment) from it                      
												
		elif dictrc.get(reciptname, -1)== -1 : #reicpt not found
			rc1.send(bytes("ERROR 102 Unable to send(recipt user not found)\n\n" , 'utf-8'))	
									     
		else :
			dictrc[reciptname].send(bytes(forwardmessage ,'utf-8')) #send it to recipt 
			reciptresponse= dictrc[reciptname].recv(1024).decode() # record response from reicpt
			rc1.send(bytes(reciptresponse, 'utf-8')) #send the response form recipt to original sender			#3)-----
			#forwarded packet come from recieve socket from some other thread and here send
			#- send RECIEVE packet along recieve socket and to that thread only
						
while True:
	sc,addr1= s.accept() #accepti1ng the sender socket of client1
	temp=sc.recv(1024).decode()	
		
	sc.send(bytes(temp, 'utf-8'))
	dictsc[temp[16:temp.find('/n/n')-1]]= sc
	print("Connected with Sending socket of client 1" , addr1 , temp[16:temp.find('/n/n')-1])

	rc,addr2= s.accept()#accepting the reciever socket of client1
	temp=rc.recv(1024).decode()
	
	rc.send(bytes(temp, 'utf-8'))
	dictrc[temp[16:temp.find('/n/n')-1]]= rc
	print("Connected with Reciving socket of client 1" , addr2, temp[16:temp.find('/n/n')-1])

	t=threading.Thread(target=do_something, args=[sc,rc])
	t.start()#starting thread at server for this client with sc, rc as sending and reciving socket
	#5)-----
	#here we are not using another thread to add username and socket into the dictionary
	#this is done by main thread only
	

