import socket
import select
import sys
import Joueur as joueur
import time as t 

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
    "La molécule d'eau ?" : "h2o"
    
   }
"""
"Le nombre planettes du système solaire ?" : "8",
    "La vitesse de la lumière en km/s (arondir)? " : "300000",
    "Le nombre de continents ? " :"7",
    "Pi ? ": "3.14",
    "Le plus grands pays au monde ?" : "russie",
    "la première planette du système solaire ?" : "mercure",
    "5*6-31+1 = ":"0",
    "Le meilleur manga de tous les temps ? " :"one piece"
"""
    
# liste des joueurs 
joueurs = []
time_out = 30 

def get_gamer(soc): 
    i = 0 
    for x in joueurs :
        if x.soc == soc : 
            return i 
        i = i + 1     


def quiz(): 
    for j in joueurs :
        j.soc.send("Vous avez 30s par question, c'est parti ...".encode('utf8'))   
    for q,r in questions.items() :
        #sockets of all gamers 
        s=[]                                          
        for j in joueurs :
                j.soc.send(q.encode('utf8')) 
                s.append(j.soc)
        #time.time() return the current time with seconds         
        now = t.time()
        time_over = False  
        while not time_over :
            #before select 
            rep,_,_ = select.select(s,[],[], time_out - (t.time() - now )   )
            #after select
            temps_restant  =  time_out - (t.time() - now )                                                 
            for p in  rep : 
            
                i = get_gamer(p) 
        
                if str(p.recv(10).decode('utf8')) == r :
                    p.send(str("Bonne réponse "+ joueurs[i].nom +" " +joueurs[i].prenom+"\n" ).encode('utf8'))
                    joueurs[i].add_score()
                    print(joueurs[i].score)
                    time_over = True 
                else : 
                    p.send(str("Mauvaise réponse "+ j.nom + " "+j.prenom+" il vous reste "+str(int(temps_restant))+"s  pour repondre à la question !" ).encode('utf8'))     
            #get out from the  while loop and pass to another question     
            if temps_restant <= 0 : 
                time_over = True  

    # display results 
    max = 0 
    nom =''
    prenom =''
    for j in joueurs  :
        j.etat = 'waiting' 
        print(j.score)
        if j.score > max :
            nom = j.nom 
            print(nom)
            prenom = j.prenom
            max = j.score
            print(max)
    for j in joueurs  : 
        j.soc.send(str("Le gagnant est "+nom +" "+prenom +" avec un score de "+str(max)+ "\n Renvoyez 'start' pour rejouer à nouveau & 'stop' pour quitter. "). encode('utf8'))  
    # ask every gamer he wont to replay 
    while True :              
        reponses =  True 
        nouvelle_partie =[]
        nouvelle_partie,_,_ = select.select([x.soc for x in joueurs], [],[])
        for p in nouvelle_partie : 
            j = get_gamer(p)
            if p.recv(10).decode('utf8') ==  'start' :
                j.etat = 'start'
                for x in joueurs :
                    if x.etat == 'waiting' :
                        reponses = False     
                        p.send("En attente de réponse des autres joueurs ".encode('utf8'))
            elif p.recv(10).decode('utf8') ==  'stop' :
                print("been here ")
                joueurs.remove(joueurs[i])
        if reponses : 
            return True  

        if len(joueurs) == 0 : 
            return False     






replay =  True 

while True:
    
        clients_a_lire = []
        try:
            # waiting any events about connexion_principal all any socket traying to connect to our server 
            clients_a_lire, _, _ =select.select(sockets,[], [] )
            
            for client in clients_a_lire:
                        if client ==  connexion_principale : 
                             connexion_avec_client, infos_connexion =connexion_principale.accept()
                             print("Nouveau Joueur connecté !")

                             nom, prenom = tuple(connexion_avec_client.recv(1000).decode('utf8').split(','))
                             for j in joueurs : 
                                 j.soc.send(str("Nouveau joueur connecté : "+nom+" "+prenom).encode('utf8'))
                             print("info connexion : "+ str(infos_connexion))
                             connexion_avec_client.send(str("Bienvenue au quiz "+prenom) .encode('utf8'))
                             
                             p = joueur.Joueur(nom, prenom , infos_connexion[0], infos_connexion[1], connexion_avec_client, 0 ,'waiting')
                             print(p)
                             joueurs.append(p)
                             if len(joueurs) >=2 : 
                                for x in joueurs : 
                                    x.soc.send("Envoyez 'start' pour lancer le jeu ...".encode("utf8") )
                             elif len(joueurs) == 1 : 
                                  p.soc.send("Veuillez patienter que au moins 2 joueurs se connectent... ".encode("utf8")) 

                             sockets.append(connexion_avec_client)
                             #to exit the server safly 
                        elif client == sys.stdin : 
                             s  = input()
                             if s == 'fin' : 
                                    get_out = True 
                        else  :
                            if client.recv(1024).decode ('utf8') == 'start' :
                               b = False 
                               for x in joueurs : 
                                   if x.soc == client : 
                                      x.etat = 'start'
                                   # if there is even one gamer didnt send 'start' yet     
                                   if x.etat == 'waiting':
                                        b = True   
                               if b :
                                    client.send("Ok,Veuillez patienter que d'autres joueurs envoient 'start', tennez vous pret ...".encode('utf8'))
                                # if all gamers sent 'start' 
                               else : 
                                    #child 
                                      while replay :
                                         replay = quiz() 
                                      get_out = True 



        except select.error:
                pass

             
        if get_out : 
            break
           
      
           
print("Fermeture des connexions")
for client in sockets:
    client.close()
