import socket 
import select
import sys


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) 
soc.connect(('localhost',12003))

print("Veuillez entrer votre nom : ") 
nom = input(">")
print("Veuillez entrer votre prénom : ") 
prenom = input(">")
#send nom concat prenom 
soc.send( str(nom+','+prenom).encode('utf8'))


while True : 
    # bloqué en attente d'event 
    readers, _, _ =  select.select([sys.stdin, soc],[],[]) 
    for reader in readers : 
        
        if reader is soc : 
            msg= soc.recv(1000).decode('utf8')
            if msg != "" :
               print(msg)
        else :
            msg= input(">")
            soc.send(msg.encode('utf8'))
            print('message envoyé '+msg)



