# secretChat
Two-way RSA-encrypted messaging application in Python  

Usage:  
+ Server: `python server.py <IP addr> <port>`  
+ Client: `python client.py <IP addr> <port>`  
  
*Example* `python server.py 'localhost' 8081`  
  
Commands:  
+ `KEYREQ!<username>` to request a specific user's public key from the server username-key cache.  
+ `K-ALL` to recieve the server's entire username-key cache.  
+ ``<username>`<message>`` to send an encrypted message to a user.
  
