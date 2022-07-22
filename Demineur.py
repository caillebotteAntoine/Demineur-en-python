
import random as r
import math
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN

"""Ce Jeu doit etre lancer avec python 2.7 et pygame 1.9.1"""
pygame.init()

Image = {"B":(100,0,20,20),"X":(60,0,20,20),'0':(100,100,100), '1':(0,128,255),'2':(0,200,64),'3':(255,0,0),'4':(0,64,128),'5':(0,128,64),'6':(128,0,0),'7':(0,64,32),'8':(64,0,0),'9':(0,0,0)}
#=============================================#
class Bouton:

    def __init__(self,rang,nom, Visu): #initialisation de l objet Bouton utilise comme une case
        self.w = 20
        self.h = 20
        self.x = rang%NbrColone*self.w
        self.y = rang//NbrColone*self.h
        self.nom = nom # = type d objet etant sur la case//Bouton
        self.Visu = Visu # l utilisateur peut-il voir la case
        self.Fleche = 0


    def __getattr__(self): # gestion des erreurs POO
         print("il n'y a pas d'attribut {} dans la class Bouton !".format(self.nom))

    def __del__(self):
        # gestion de la destruction des objets
        self.nom = ""

    def dclic(self, xs, ys):#fonction qui detecte si le curseur est dans le bouton

        if xs >= self.x+self.w or xs <= self.x or ys >= self.y+self.h or ys <= self.y :#On detecte quand le curseur n est pas dans les boutons
            return -1
        else :
            return self.x//self.w+ self.y//self.h* NbrColone 
        
    def affichage(self, ecran, Sprite):
         #fonction d affichage des boutons
         #en fonction de self.Visu et de self.nom
        
        if self.Visu :
            ecran.blit(Sprite,(self.x, self.y),(0,0,20,20))
            line = self.nom #affichage des nombres
            if self.nom in Image.keys() :
                if len(Image[self.nom]) == 4 :
                    ecran.blit(Sprite,(self.x, self.y),Image[self.nom])
                    line = ""#affiche une image
                else :
                    fg = Image[self.nom]#affiche un chiffre avec une couleur
            else :
                fg = (0,0,0)
            

            if line != "" : #affichage de texte
                bg = (5,5,5)
                sur = font.render(line, 0, fg,bg )
                sur.set_colorkey(bg)
                ecran.blit(sur,(self.x+4,self.y-1))

        elif self.Fleche == 1 :
            ecran.blit(Sprite,(self.x, self.y),(40,0,20,20))
        elif self.Fleche == 2 :
            ecran.blit(Sprite,(self.x, self.y),(80,0,20,20))

        else :
            ecran.blit(Sprite,(self.x, self.y),(20,0,20,20))

        

def clic(ListeBouton,xs,ys):#Detecte a chaque clic les clics si le curseur est dans le bouton
    for i in ListeBouton :
        back = i.dclic(xs,ys)
        if back!= -1 :
            return back
    return -1 

def BoutonAjout(ListeBouton, rang ,nom, Visu):#Pour les boutons
    New = Bouton(rang,nom, Visu)#Creer un nouveau bouton
    ListeBouton.append(New)#Placer les boutons dans un liste de boutons
    return ListeBouton
    #=============================================#
def Wait(Temps): #fonction servant a faire attendre le programme tout en gardant la gestion des events
    for i in range(Temps):
        pygame.time.wait(1)
        for event in pygame.event.get():
            if event.type == QUIT :
                return -1
            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1:
                    return 1
#=============================================#
def Affichage(Sprite): #affiche tous les objets
    for i in Table :
        i.affichage(ecran, Sprite)
    pygame.display.flip() #actualisation de l ecran

#=============================================#
def Clic(x,y): #permet de rendre visible tous les 0, ou savoir si l'utilisateur a clicer sur une bombe
    if Table[x+y*NbrColone].nom !=  "X":
        Table[x+y*NbrColone].Visu = True
    if Table[x+y*NbrColone].nom == "0" :
        for k in range(-1,2):
            for n in range(-1,2):
                if x+(y+k)*NbrColone+n>= 0 and x+(y+k)*NbrColone+n<NbrColone*NbrLigne :
                    if (n == 1 and x!= NbrColone-1) or (n == -1 and x!= 0) or n == 0 :
                        if Table[x+n+(k+y)*NbrColone].Visu == False :
                            Clic(x+n,y+k)

    if Table[x+y*NbrColone].nom ==  "2" :
        for k in range(-1,2):
            for n in range(-1,2):
                if x+(y+k)*NbrColone+n>= 0 and x+(y+k)*NbrColone+n<NbrColone*NbrLigne :
                    if (n == 1 and x!= NbrColone-1) or (n == -1 and x!= 0) or n == 0 :
                        if Table[x+n+(k+y)*NbrColone].Visu == False :
                            Clic(x+n,y+k)

    
    elif Table[x+y*NbrColone].nom == "X":
        return -1
    elif Table[x+y*NbrColone].nom == "":
        return 2
    else :
        return -2
#=============================================#

def Creation(Mode,NbrDeMine, NbrLigne, NbrColone):
    
    
    Table = []
    
    for i in range(NbrLigne):
        for n in range(NbrColone):
            Table = BoutonAjout(Table, i*NbrColone+n,"B", False)
    
    if Mode == 1 or Mode == 2 : 
        for i in range(len(Table)):
            if not(i%NbrColone == 0 or i%NbrColone == NbrLigne-1 or i//NbrColone == 0 or i//NbrColone == NbrColone-1) :
                Table[i].nom = "0"
                Table[i].visu = False
                #BoutonAjout(Table, i*NbrColone+n,"0", False)
    elif Mode == 3 :
        NbrCase = NbrColone
        if NbrLigne<NbrColone :
            NbrCase = NbrLigne
        for i in range(len(Table)) :
            module = math.sqrt(( i%NbrColone-NbrColone//2)**2 +( i//NbrColone-NbrLigne//2)**2)
            if module<NbrCase//2-(1+NbrCase)%2 :
                Table[i].nom = "0"
                Table[i].visu = False
            
    for i in Table :
        if i.nom == "B":
            i.Visu = True
    Temp = 0
    while Temp<NbrDeMine:
        alea = r.randrange(0,NbrColone*NbrLigne)
        if Table[alea].nom!= "X" and Table[alea].nom!= "B":
            Table[alea].nom = "X"
            Temp+= 1
            
    if Mode == 1 or Mode == 3:
        for i in range(len(Table)):
            if Table[i].nom == "X" :
                for k in range(-1,2):
                    for n in range(-1,2):
                        if i+k*NbrColone+n>= 0 and i+k*NbrColone+n<NbrColone*NbrLigne :
                            if (n == 1 and i%NbrColone!= NbrColone-1) or (n == -1 and i%NbrColone!= 0) or n == 0 :
                                if Table[i+k*NbrColone+n].nom!= "X" and Table[i+k*NbrColone+n].nom!= "B":
                                    Table[i+k*NbrColone+n].nom = str(int(Table[i+k*NbrColone+n].nom)+1)
    elif Mode == 2:
        for z in range(1,9) :
            for i in range(len(Table)):
                if Table[i].nom == "X" :
                    for k in range(-z,z+1):
                        for n in range(-z,z+1):
                            if i+k*NbrColone+n>= 0 and i+k*NbrColone+n<NbrColone*NbrLigne :
                                if (n>0 and i%NbrColone <= NbrColone-n) or (n<0 and i%NbrColone >= 0-n) or n == 0 :
                                    if Table[i+k*NbrColone+n].nom == "0":
                                        Table[i+k*NbrColone+n].nom = str(z)
    
    return Table, []

#=============================================#
def Effet(liste, t, etape ): 
    Temp = 0    
    while Temp<etape:
        Temp+= 1
        dest = Wait(t)
        if dest == 1 :#a voir
            return 1
        elif dest == -1:
            return -1
        for i in Table :
            if i.nom!= "" :
                alea = r.randrange(len(liste))
                i.nom = liste[alea]

        Affichage(Sprite)

#=============================================#
def Jouer(Mode, NbrDeMine, NbrLigne, NbrColone):
    NbrFleche = 0
    
    Temp = 0
    dest = 0
    action  = True
    while True :
        if action :
            Affichage(Sprite)
            action = False
            
        for event in pygame.event.get():
            if event.type == QUIT :
                return -1

                        
            if event.type == MOUSEBUTTONDOWN :
                action  = True
                if event.button == 1 :
                    dest = clic(Table, event.pos[0], event.pos[1])
                    if dest!= -1 and Table[dest].Fleche == 0 :
                        Temp = Clic(dest%NbrColone, dest//NbrColone)
                        if Temp == 2 :
                            Menu()
                            return 0
                        
                        elif Temp == -1 :
                            print('BooM !')
                            Temp = 0

                            for i in Table :
                                if i.Visu == False :
                                    i.Visu = True
                                    Affichage(Sprite)
                                    
                                    if Temp == 0 and i.nom == "X":
                                        dest = Wait(90)
                                        if dest == 1 :
                                            Temp = 1
                                        elif dest == -1 :
                                            return -1
                                        
                                    elif Temp == 0  :
                                        dest = Wait(55)
                                        if dest == 1:
                                            Temp = 1
                                        elif dest == -1:
                                            return -1
                                    else :
                                        for n in Table :
                                            n.Visu = True
                                        Affichage(Sprite)
                                        break
                                
                            
                            Wait(200) 
                            Effet(["X","0"],80,16)
                            return 0
                        
                elif event.button == 3 :
                    dest = clic(Table, event.pos[0], event.pos[1])
                    if dest!= -2 :
                        if Table[dest].Fleche == 2 and Table[dest].Visu == False:
                            Table[dest].Fleche = 0
                            NbrFleche-= 1
                        elif Table[dest].Visu == False :
                            Table[dest].Fleche = (Table[dest].Fleche+1)%3
                            if Table[dest].Fleche == 1:
                                NbrFleche+= 1
                                if Mode == 2 :
                                    Temp = 0
                                    for i in Table :
                                        if i.Fleche and i.nom == "X" :
                                            Temp+= 1
                                    if Temp == NbrDeMine :
                                        for i in Table :
                                            if i.Visu :
                                                Temp+= 1
                                            else :
                                                i.Visu = True
                                        print("Win en",Temp," CouP !")
                                        
                                        Temp = 0
                                        for i in Table :
                                            if i.Visu == False :
                                                i.Visu = True
                                                Affichage(Sprite)
                                                
                                                if Temp == 0 and i.nom == "X":
                                                    dest = Wait(90)
                                                    if dest == 1 :
                                                        Temp = 1
                                                    elif dest == -1 :
                                                        return -1
                                                    
                                                elif Temp == 0  :
                                                    dest = Wait(55)
                                                    if dest==1:
                                                        Temp=1
                                                    elif dest==-1:
                                                        return -1
                                                else :
                                                    for n in Table :
                                                        n.Visu=True
                                                    Affichage(Sprite)
                                                    break
                                            
                                    
                        print("Reste :",NbrDeMine-NbrFleche," Bombes sur ", NbrDeMine," !")
                        Affichage(Sprite)
                Temp=0
                print(len(Table))
                for i in Table :
                    if not i.Visu:
                      Temp+=1
                print(NbrDeMine)
                print(Temp)
                if Temp<=NbrDeMine and NbrFleche==NbrDeMine:
                    print("WiN !")

                    Effet(["0","1","2","3","4"], 80,16)
                    return 1
                
            if True and event.type==KEYDOWN: #Triche
                action = True
                for i in Table :
                    i.Visu = not i.Visu
                    
        
#=============================================#
def Menu():
    Mode = 0
    print('Max : 37*68 (0 pour du 10//10, mode normale; pour une seed)')
    
    #seed = int(input("seed : "))
    NbrColone = int(input("NbrColone = "))
    NbrLigne = -1
    if NbrColone == 0:
        NbrLigne = 10
        Mode = 1
        NbrColone = 10
    else :
        if NbrLigne == -1 :
            
            NbrLigne = int(input("NbrLigne = "))
            Mode = int(input("Mode : Normal//Distance//Cercle (1//2//3) = "))

    Difficulte = 0
    while Difficulte == 0 or Difficulte>9 :
        Difficulte =  int(input("Difficulte [1;9] = "))
    NbrDeMine = NbrColone*NbrLigne//10*Difficulte
    if NbrDeMine<= 0 :
        NbrDeMine = 1

    if Mode == 3 :
        NbrColone+= (NbrColone+1)%2
        NbrLigne+= (NbrLigne+1)%2
    NbrColone+= 2
    NbrLigne+= 2
    global ecran
    ecran = pygame.display.set_mode((NbrColone*20,NbrLigne*20))
    global Sprite
    Sprite = pygame.image.load("Sprite.bmp").convert()
    return NbrColone,NbrLigne, [],0, NbrDeMine, Mode

#=============================================#
font = pygame.font.Font("font.ttf",18)
#lecture
try :
    global Sprite
    Sprite = pygame.image.load("Sprite.bmp").convert()
except :
    print("Fichier image incompatible ou inexistant")
#fin lecture


done = False
while not done :
    NbrColone,NbrLigne, Table,NbrFleche, NbrDeMine, Mode = Menu()

    Table = []
    OK = True
    while OK :
        seed = r.random()
        
        r.seed(seed)
        print("Seed : ",seed)
        Table, Visu =  Creation(Mode,NbrDeMine, NbrLigne, NbrColone)
        if Jouer(Mode, NbrDeMine, NbrLigne, NbrColone) == -1 :
            OK = False
        NbrFleche = 0
    


print("end")


