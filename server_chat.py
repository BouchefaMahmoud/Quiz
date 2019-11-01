import socket
import select
import sys
import os 
import Joueur as j


hote = 'localhost'
port = 12003
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(20)
print("Le serveur écoute à présent sur le port {}" .format(port))
#serveur_lance = True
sockets = [connexion_principale, sys.stdin]
get_out =  False 

questions = {
    "La molécule d'eau ?" : "h2o",
    
    "Le nombre planettes du système solaire ?" : "8",
    "La vitesse de la lumière en km/s (arondir)? " : "300000",
    "Le nombre de continents ? " :"7",
    "Pi ? ": "3.14",
    "Le meilleur manga de tous les temps ? " :"one piece"
}


def quez(client) : 
    compteur  = 0 
    for q,r in questions.items() : 
        response = []
        client.send(q.encode("utf8"))
        response,_,_ = select.select([client],[],[],30) 
        
        if response  != [] : 
            rep = client.recv(1024).decode('utf8')

            if r == rep : 
                compteur= compteur + 1
                client.send("Bonne réponse ! \n ".encode("utf8"))
            else  : 
                client.send("Mauvaise réponse ! \n ".encode("utf8"))

    
# liste des joueurs 
joueurs = []

while True:
    
        clients_a_lire = []
        try:
            # waiting any events about connexion_principal all any socket traying to connect to server 
            clients_a_lire, _, _ =select.select(sockets,[], [] )
            
            for client in clients_a_lire:
                        if client ==  connexion_principale : 
                             connexion_avec_client, infos_connexion =connexion_principale.accept()
                             print("Nouveau Joueur connecté !")
                             nom, prenom = tuple(connexion_avec_client.recv(1000).decode('utf8').split(','))
                             print("info connexion : "+ str(infos_connexion))
                             connexion_avec_client.send(str("Bienvenue au quiz  "+prenom) .encode('utf8'))
                             
                             p =  j.Joueur(nom, prenom , infos_connexion[0], infos_connexion[1], connexion_avec_client, 0 ,'waiting')
                             print(p)
                             joueurs.append(p)
                             if len(joueurs) >=2 : 
                                for x in joueurs : 
                                    x.soc.send("Envoyez 'start' pour lancer le jeu ...".encode("utf8") )
                             elif len(joueurs) == 1 : 
                                  print("been here ?")
                                  joueurs[0].soc.send("Veuillez patienter que au moins 2 joueurs se connectent ...".encode("utf8")) 

                             sockets.append(connexion_avec_client)
                        elif client == sys.stdin : 
                             s  = input()
                             print("i'm here")
                             if s == 'fin' : 
                                    get_out = True 
                        else  :
                            #child
                            if (os.fork() ==  0 ) :     
                                if client.recv(1024).decode ('utf8') == 'start' :
                                   b = False 
                                   for x in joueurs : 
                                       if x.soc == client : 
                                          x.etat = 'start'
                                       if x.etat = 'waiting':
                                            b = True   
                                    if b :
                                        client.send("Ok,Veuillez patienter que d'autres joueurs envoient start, tennez vous pret ...".encode('utf8'))
                                    else : 
                                        # if all gamers sent 'start' 
                                            

                    
        except select.error:
                pass

             
        if get_out : 
            break
           
      
           
print("Fermeture des connexions")
for client in sockets:
    client.close()
