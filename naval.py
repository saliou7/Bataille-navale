import numpy as np
import matplotlib.pyplot as plt
import random

len_ship = {
        1:5,
        2:4,
        3:3,
        4:3,
        5:2
}

class Grille :
    """docstring for Grille"""
    def __init__(self):
        self.grille = np.zeros((10,10))
        
    """ verifier si un bateau peut être placé"""
    def peut_placer(self, bateau, position, direction ) : 
        x, y = position 
        #Si la direction est horizontale 
        if direction == 'h': 
            if len_ship[bateau] + y > len(self.grille[0]) :
                return False
            for j in range(y , y + len_ship[bateau]) :
                if self.grille[x][j] != 0:
                    return False 
            return True 

        #Si la direction est verticale
        if direction == 'v':
            if len_ship[bateau] + x > len(self.grille[0]):
                return False
            for i in range(x , x + len_ship[bateau]):
                if self.grille[i][y] != 0:
                    return False
            return True
        return False
        
    """placer un bateau sur la grille"""
    def place(self, bateau, position, direction) :
        x, y = position 

        if direction == 'h': #placer de façon horizontale
            for j in range(y , y + len_ship[bateau]) :
               self.grille[x][j] = bateau
        elif direction == 'v' : #placer de façon verticale 
            for i in range(x , x + len_ship[bateau]) :
               self.grille[i][y] = bateau
        
    """Placer un bateau aleatoirement sur la grille"""
    def place_alea(self, bateau) : 
        while True:
            position = random.choice(['h','v'])
            i = random.randrange(10)
            j = random.randrange(10)
            if self.peut_placer(bateau, (i,j), position) :
                self.place(bateau, (i,j), position)
                break 

    def affiche(self) :
        plt.imshow(self) 
        plt.show(self.grille)
        
    """Tester l'égalité entre deux grilles"""
    def eq(self,grilleB) :
        return np.array_equal(self.grille, grilleB)

    """generer une grille remplie des 5 bateaux aleatoirement"""
    def genere_grille(self) :
        for bateau in range(1,6) : 
            self.place_alea(bateau)
        return np.copy(self.grille)

    #------------------------------------Partie Combinatoire-------------------------------#

    """Effacer un bateau dans la grille connaissant sa position et sa direction """
    def del_ship(self, bateau, position, direction) : 
        x, y = position
        if direction == 'h' : #si le bateau est positionné horizontalement 
            for j in range(y, y + len_ship[bateau]) : 
                self.grille[x][j] = 0
        elif direction == 'v' : #si le bateau est posititonné verticalement 
            for i in range(x, x + len_ship[bateau]) : 
                self.grille[i][y] = 0

    """Nombre de possibilité de placer un bateau sur une grille"""
    def nb_possiblite(self, bateau) : 
        cpt = 0
        for i in range(10) : 
            for j in range(10) :
                if self.peut_placer(bateau, (i,j), 'h'):
                    cpt += 1
                if self.peut_placer(bateau, (i,j), 'v'):
                    cpt +=1
        return cpt 

    """Nombre de possibilité de placer un liste de bateau dans une grille"""
    def nb_place_possible(self, liste) : #liste -> liste des bateaux 
        cpt = 0
        if len(liste) == 0 :
            return 1
        for i in range(10):
            for j in range(10):
                if self.peut_placer(liste[0], (i,j), 'h'): #si le premier bateau de la liste peut etre placé horizontalement
                    self.place(liste[0], (i,j), 'h') # on place le bateau sur la grille
                    cpt += self.nb_place_possible(liste[1:]) # on rappelle la fonction sans le premier bateau de la liste
                    self.del_ship(liste[0], (i,j), 'h') # on supprime le premier bateau placé sur la grille
                
                if self.peut_placer(liste[0], (i,j), 'v'):
                    self.place(liste[0], (i,j), 'v')
                    cpt += self.nb_place_possible(liste[1:])
                    self.del_ship(liste[0], (i,j), 'v')
        return cpt  

    
    def eq_grille_alea(self) : 
        cpt = 0
        self.genere_grille()
        while self.eq(self.genere_grille()) != True :
            cpt += 1
        return cpt


