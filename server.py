import socket 
import select 
import sys 
from thread import *
import random
  

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 
  
IP_address = str(sys.argv[1]) 
  
Port = int(sys.argv[2]) 

server.bind((IP_address, Port))   

server.listen(100) 

print("                        _    _____ _           _   ")
print("                       | |  / ____| |         | |  ")
print(" ___  ___  ___ _ __ ___| |_| |    | |__   __ _| |_ ")
print("/ __|/ _ \\/ __| '__/ _ \\ __| |    | '_ \\ / _` | __|")
print("\\__ \\  __/ (__| | |  __/ |_| |____| | | | (_| | |_ ")
print("|___/\\___|\\___|_|  \\___|\\__|\\_____|_| |_|\\__,_|\\__|")
print("      MA464 Project: Cadets Wasaff and Benden      ")
print("                     SERVER                        ")


list_of_clients = [] 
  
def clientthread(conn, username, publicKey, addr): 
	while True: 
			try: 
				message = conn.recv(2048)
				if("KEYREQ" in message):
					message = message.strip()
					message = message.split("!")
					keyRequest = message[1].strip()

					print("KEY REQUEST: " +  keyRequest + " FROM: " + username)

					keyMsg = ""
					for user in list_of_clients:
						if(user[1] == keyRequest):
							publicKey = user[2]
							keyMsg = "KEY!" + publicKey + "!" + keyRequest
					if(keyMsg == ""):
						print("FAILED KEY REQ: " + keyRequest)
						conn.send("No such user named " + keyRequest)
					else:
						conn.send(keyMsg)

				elif("K-ALL" in message):
					for user in list_of_clients:
						publicKey = user[2]
						keyMsg = "KEY!" + publicKey +  "!" + user[1]
						conn.send(keyMsg)
						print(keyMsg)

					print("^^KEY REQUESTS ALL FROM " + username)

				elif message: 
					split = message.split("`")
					to = split[0]
					for user in list_of_clients:
						if(user[1] == to):
							message = username + "`" + split[1]
							user[0].send(message)
							print("MESSAGE " + username + " -> " + to + "; encrypted message: " + split[1])


				else:
					remove(conn)   
			except: 
				continue
  
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 
  
while True: 
  	conn, addr = server.accept() 

	message = conn.recv(2048)
	if("PUBLIC" in message):
		message = message.split("!")
		username = message[1]
		publicKey = message[2]
		

	client = [conn, username, publicKey, addr]
	list_of_clients.append(client)
	print("NEW CONNECTION: " + username + " connected to server. Public Key: " + publicKey)

	start_new_thread(clientthread,(conn, username, publicKey, addr))     
  
conn.close() 
server.close() 