import socket 
import select 
import sys
import random
from fractions import gcd

def is_prime(n):
    if n==2 or n==3: return True
    if n%2==0 or n<2: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n%i==0:
            return False    

    return True

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

def generate_keys(p, q):
    if(is_prime(p) == False or is_prime(q) == False):
        print("Both numbers must be prime.")
        initialize()
    else:
        n = p * q
        phi = (p-1)*(q-1)
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = gcd(e, phi)       

        d = multiplicative_inverse(e, phi)
        
        return ((e, n), (d, n))        

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


def initialize():

    print("                        _    _____ _           _   ")
    print("                       | |  / ____| |         | |  ")
    print(" ___  ___  ___ _ __ ___| |_| |    | |__   __ _| |_ ")
    print("/ __|/ _ \\/ __| '__/ _ \\ __| |    | '_ \\ / _` | __|")
    print("\\__ \\  __/ (__| | |  __/ |_| |____| | | | (_| | |_ ")
    print("|___/\\___|\\___|_|  \\___|\\__|\\_____|_| |_|\\__,_|\\__|")
    print("      MA464 Project: Cadets Wasaff and Benden      ")
    print("                     CLIENT                        ")


    p = int(raw_input("Enter a prime number: "))
    q = int(raw_input("Enter a different prime number: "))
    public, private = generate_keys(p, q)
    print "Public key: ", public ," Private key is: ", private
    username = raw_input("Enter your username: ")
    print("")
    print("Commands: ")
    print("K-ALL --------------- add all connected users' public keys to your local cache")
    print("KEYREQ!<username> --- add a specific user's public key to your local cache")
    print("CACHE --------------- view your local cache")
    print("To send a message use: <to>`<message> ")
    print("")
    return username, public, private




username, public, private = initialize() 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print("Correct usage: script, IP address, port number")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
server.send("PUBLIC KEY!" + username + "!" + str(public))

keyCache = {}

while True: 
  
    sockets_list = [sys.stdin, server] 

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

    for socks in read_sockets: 
        #READ
        if socks == server: 
            message = socks.recv(2048)
            if("KEY!" in message):
                keyMsg = message.split("!")
                publicKey = keyMsg[1]
                to = keyMsg[2]
                print(to + "'s public key is " + publicKey)
                sys.stdout.flush()
                keyCache[to] = publicKey

            elif("`" in message):
                split = message.split("`")
                fromUser = split[0]
                ciphertext = split[1].strip()
                ciphertext = ciphertext.replace(" ", "")
                ciphertext = ciphertext.replace("L","")
                ciphertext = ciphertext.replace("[", "")
                ciphertext = ciphertext.replace("]", "")
                ciphertext = ciphertext.split(",")
                cipherString = [int(i) for i in ciphertext]
                plaintext = decrypt(private, cipherString)
                print("From: " + fromUser + " Message: " + plaintext)

            else:
                print(message)

        #WRITE
        else:
            message = sys.stdin.readline()
            if("KEYREQ" in message):
                server.send(message)
                message = message.split("!")
                sys.stdout.write("You key requested ") 
                sys.stdout.write(message[1]) 
                sys.stdout.flush() 

            elif("K-ALL" in message):
                server.send(message)
                print("You key requested everyone") 
                sys.stdout.flush()

            elif("CACHE" in message):
                if not keyCache:
                    print("Key cache is empty.")
                else:
                    for x,y in keyCache.items():
                        print("User: " + x + " Public Key: " + y)
                sys.stdout.flush()

            else:
                #send with `. format: to`message
                if "`" not in message:
                    print("ERROR: Format: <to>`<message>")
                    sys.stdout.flush()
                else:
                    splitMsg = message.split("`")
                    to = splitMsg[0]
                    plaintext = splitMsg[1]
                    if to not in keyCache:
                        print("Request " + to + "'s key with <KEYREQ!" + to + ">")
                        sys.stdout.flush()

                    else:
                        publicKey = keyCache.get(to)
                        publicKey = publicKey.split(",")
                        a = publicKey[0]
                        a = int(a[1::])
                        b = publicKey[1].strip()
                        b = int(b[:-1])
                        ciphertext = to + "`" + str(encrypt((a,b), plaintext))
                        server.send(ciphertext) 
                        sys.stdout.write("You: ") 
                        sys.stdout.write(message) 
                        sys.stdout.flush()


server.close() 

