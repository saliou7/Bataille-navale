import modelisation as mod
import naval as nvl
import random 
import numpy as np


class Joueur(mod.Bataille) :
	
	"""constructeur de la classe Joueur"""
	def __init__(self, name):
		self.name = name
		mod.Bataille.__init__(self) #appel au constructeur de la classe Mere (Bataille)
	
	#********************************************* version aléatoire ***************************************#
	
	
	def jouer_alea(self):
		positions = [(i,j) for i in range(10) for j in range(10)] #generer toutes les positions de la grille
		cpt = 0
		while not self.victoire() : # Boucle tant qu'on a pas gagné
			i, j = random.choice(positions) #choisir une postion aleatoire dans la liste des postions
			self.joue((i,j)) #tirer la case choisie
			cpt += 1
			positions.remove((i,j)) #effacer la position choisie de la liste des positions 
		return cpt 
	 

	#************************************************ version heuristique ************************************#

	def joue_heuristique(self) : 
		positions = [(i,j) for i in range(10) for j in range(10)]
		cpt = 0
		touche = False # on suppose qu'aucune bateau n'est touché au debut
		
		while not self.victoire() : # boucle tant qu'on a pas gagné
			i, j = random.choice(positions) #choisir une position aleatoire
			touche = self.joue((i,j)) #tirer sur la cible et recuperer la valeur de retour
			positions.remove((i,j)) #effacer la position choisie dans la liste des positions
			
			if touche : #si un bateau est touché, on joue sur les cases connexes 
				for x, y in [(1,0),(0,1),(-1,0),(0,-1)] :
					if i+x >= 10 or i+x < 0 or j+y >= 10 or j+y < 0 : # on verifie qu'il n'y a pas de debordement 
						continue
					if (i+x, j+y) in positions : #si la case connexe n'a pas encore été joué, on tire sur cette case sinon on fait rien						
						self.joue((i+x, j+y))
						positions.remove((i+x,j+y))
						cpt +=1
			cpt +=1

		return cpt #retourner le nombre de coup joué

	#****************************************version probabiliste simplifiée ***************************************#
	"""Cherche la case plus probable de contenir un bateau"""
	def case_probable(self):

		grille_proba = np.zeros((10,10)) #generer une grille 10*10 vide pour mettre la probabilité des cases
		debut = 0 
		boost = 0 # pour booster la probabilité de certaines cases
		peut_poser = False
		list_bateau = [1,2,3,4,5]

		for bateau in list_bateau : #pour chaque bateau dans la liste
			if self.bat_restant[bateau] <= 0 : #si le bateau est coulé
				continue #on itere sur le bateau suivant

			for i in range(10) :
				for j in range(10) :
					#pour chaque case de la grille de jeu
					
					"""si une case a deja eté jouée, la proba de sa case correspondante sur la grille des probas est 0 """
					if self.grille[i][j] == -1 : 
						continue
					
					#si debut == 0 ==> la case (i, j) n'est pas un bateau touché
					#si debut == 1 ==> la case (i, j) est un bateau touché
					debut = 0
					boost = 0

					"""si la case est un bateau touché, on boost la proba qu'il y est un bateau a coté"""
					if self.grille[i][j] == -2 :
						boost = 1
						debut = 1
					"""Placement vertical"""

					peut_poser = True #on suppose qu'on peut placer le bateau courant verticalement
					for x in range(1, nvl.len_ship[bateau]) : # len_ship[bateau] -> taille du bateau courant.
						if not self.check_position((i+x,j)) or self.grille[i+x][j] == -1 : #si ça deborde ou que la case est déja jouée
							peut_poser = False
							break # on sort du boucle 

						if self.grille[i+x][j] == -2 : #si on rencontre une case dont un bateau est touché
							boost += 1 #on boost la probabilité

					""" Attribution des probabilités """
					if peut_poser : # si le bateau peut être placé
						for x in range(debut, nvl.len_ship[bateau]) : #iteration sur les lignes
							if self.grille[i+x][j] != -2 :
								grille_proba[i+x][j] += 1 + boost*2 #on attribut la proba des cases sauf la case deja jouée

					""" Placement horizontal """
					peut_poser = True
					for y in range(1, nvl.len_ship[bateau]) : #iteration sur les colonnes
						if not self.check_position((i,j+y)) or self.grille[i][j+y] == -1 :
							peut_poser = False
							break

						if self.grille[i][j+y] == -2 :
							boost += 1
					""" Attribution des probabilités """
					if peut_poser :
						for y in range(debut, nvl.len_ship[bateau]) :
							if self.grille[i][j+y] != -2 :
								grille_proba[i][j+y] += 1 + boost*2

		list_proba = [item for sublist in grille_proba for item in sublist] #transformer la grille en une liste de proba
		maxiProba = max(list_proba) #recuperer la plus grande valeur de la lise
		x = list_proba.index(maxiProba)//10 #recuperer son indice ligne
		y = (list_proba.index(maxiProba)+10)%10 #recuperer son indice de colonne
		return x , y #retourner la case avec la plus forte proba
	
	"""Faire une partie complete de bataille navale avec la version probabiliste"""
	def jouer_probabiliste(self) :
		cpt = 0
		while not self.victoire() : 
			x, y = self.case_probable()
			self.joue((x,y))
			cpt += 1
		return cpt 
	#*********************************************************************************************************#

def main() : 
	# Partie test #
	j = Joueur("alea")
	print(j.jouer_probabiliste())
if __name__ == '__main__':
	main()