
import naval as nvl

class Bataille :
	
	def __init__(self):
		self.grille = nvl.Grille().genere_grille()
		self.bat_restant = [0,5,4,3,3,2] #liste des bateaux restants
		self.nb_dommage = 0 #nombre de case de bateau touché 

	def joue(self, cible):
		touche = False
		if not self.check_position(cible) : 
			print("tir impossible")
			return
		x , y = cible

		if self.grille[x][y] > 0 : #si un bateau est touché
			self.bat_restant[int(self.grille[x][y])] -= 1 #decrementer la taille du bateau touché
			self.nb_dommage += 1
			touche = True
			self.grille[x][y] = -2
		else:
			self.grille[x][y] = -1

		return touche	

		
	"""on gagne si nb_dommage est égal à la somme de taille de tous les bateaux"""
	def victoire(self):
		return self.nb_dommage == sum(nvl.len_ship.values())

	def reset(self):
		self.grille = nvl.Grille().genere_grille()

	def check_position(self, cible):
		return cible[0] < 10 and cible [0] >= 0 and cible[1] < 10 and cible[1] >= 0




	
