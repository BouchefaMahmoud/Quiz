class Joueur :

    def __init__(self, nom, prenom, ip , port, soc,  score, etat ) : 
            self.nom = nom 
            self.prenom = prenom 
            self.ip = ip 
            self.score = score 
            self.port = port
            self.soc = soc 
            #waiting ,  gaming 
            self.etat =  etat 


    

    def gamer(slef) :
        return  'ip = ' + str(self.ip) + ', port = '+ str(self.port)

    
    def __str__(self):
        return self.nom+' '+self.prenom+' Score='+str(self.score)    

    def add_score(self) : 
        self.score = self.score + 1 
