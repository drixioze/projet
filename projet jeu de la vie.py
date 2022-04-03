from __future__ import annotations
from random import random
import time
from tkinter import Tk,Button,Scale, Label, Canvas, Frame
from tkinter import RIGHT, HORIZONTAL, ALL, X, RIDGE  #SUNKEN, GROOVE, RAISED

# Variables globales pour l'interface
TAILLE_CELLULE = 12
LONGUEUR_GRILLE = 30
LARGEUR_GRILLE = 30
CONTROLE_BOUCLE = False
TAUX = 45
TEMPS = 200

class Cellule:

    def __init__(self):
        self.__etat_actuel = False
        self.__etat_futur = False
        self.__voisins = []

    # Accesseurs / Assesseurs
    def est_vivant(self) -> bool:
        return self.__etat_actuel

    def obtenir_voisins(self) -> list:
        return self.__voisins

    # Mutateurs
    def modifier_voisins(self, v:list):
        self.__voisins = v

    def naitre(self):
        self.__etat_futur = True

    def mourir(self):
        self.__etat_futur = False

    def basculer(self):
        self.__etat_actuel = self.__etat_futur

    def __str__(self):
        # https://emojiterra.com/pt/simbolos-geometrica-simbolos/
        if self.est_vivant():
            res = "\u2B1C"
        else:
            res = "\u2B1B"
        return res

    def calcule_etat_futur(self):
        nb_vivants = sum([c.est_vivant() for c in self.__voisins])
        if nb_vivants != 2 and nb_vivants != 3:
            self.mourir()
        elif nb_vivants == 3:
            self.naitre()
        else:
            self.__etat_futur = self.__etat_actuel


class Grille:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.matrice = [[Cellule() for i in range(self.largeur)] for j in range(self.hauteur)]

    # Accesseurs
    def obtenir_largeur(self):
        return self.largeur

    def obtenir_hauteur(self):
        return self.hauteur

    def obtenir_cellule(self, i, j) -> Cellule:
        if self.dans_grille(i,j):
            return self.matrice[j][i]
        else:
            raise TypeError("Ce ne sont pas de bonnes coordonnées")

    def dans_grille(self, i, j) -> bool:
        return 0 <= i < self.largeur and 0 <= j < self.hauteur

    @staticmethod
    def est_voisin(i, j, x, y):
        return max(abs(x-i), abs(y-j)) == 1

    def obtenir_voisins(self, x, y) -> list[Cellule]:
        v = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if self.dans_grille(i, j) and Grille.est_voisin(x, y, i, j):
                    v.append(self.obtenir_cellule(i, j))
        return v

    def affecte_voisins(self):
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.obtenir_cellule(i, j).modifier_voisins(self.obtenir_voisins(i, j))


    def __str__(self):
        res = ""
        print("Le jeu de la vie")
        for i in range(self.largeur):
            for j in range(self.hauteur):
                res += str(self.obtenir_cellule(i, j))
            res += "\n"
        return res

    def remplissage(self, taux):
        for i in range(self.largeur):
            for j in range(self.hauteur):
                if random() <= (taux/100.0):
                    self.obtenir_cellule(i, j).naitre()
                    self.obtenir_cellule(i, j).basculer()

    def mise_a_jour(self):  # Actualise
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.obtenir_cellule(i, j).calcule_etat_futur()

    def evolution(self):  # jeu
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.obtenir_cellule(i, j).basculer()

def jouer():
	# Permet la mise à jour et l'évolution du jeu
	# Temporise l'affichage
	# Ne se lance que si CONTROLE_BOUCLE est vrai
	affichage()
	if CONTROLE_BOUCLE == True:
		vie.mise_a_jour()
		vie.evolution()
		Fenetre.after(TEMPS, jouer)

def affichage():
	G.delete(ALL)
	# Définition de la grille
	if TAILLE_CELLULE >= 8:
		for i in range(LARGEUR_GRILLE+1):
			G.create_line(3,
						  TAILLE_CELLULE*i+3,
						  LONGUEUR_GRILLE*TAILLE_CELLULE+3,
						  TAILLE_CELLULE*i+3)
		for i in range(LONGUEUR_GRILLE+1):
  			G.create_line(TAILLE_CELLULE*i+3,
						  3,
			  			  TAILLE_CELLULE*i+3,
						  LARGEUR_GRILLE*TAILLE_CELLULE+3)
	# Définition des cellules
	for i in range(LARGEUR_GRILLE):
		for j in range(LONGUEUR_GRILLE):
			if vie.obtenir_cellule(i, j).est_vivant():
				G.create_rectangle(TAILLE_CELLULE*i+3,
								   TAILLE_CELLULE*j+3,
								   TAILLE_CELLULE*(i+1)+3,
								   TAILLE_CELLULE*(j+1)+3,
								   fill='blue')

def lancer():
	global CONTROLE_BOUCLE
	CONTROLE_BOUCLE = True
	jouer()

def stopper():
	global CONTROLE_BOUCLE
	CONTROLE_BOUCLE = False

def clicCellule(event):
	global TAILLE_CELLULE, CONTROLE_BOUCLE
	CONTROLE_BOUCLE = False
	i, j = (event.x - 3) // TAILLE_CELLULE, (event.y - 3) // TAILLE_CELLULE
	if vie.obtenir_cellule(i,j).est_vivant():
		vie.obtenir_cellule(i,j).mourir()
	else:
		vie.obtenir_cellule(i,j).naitre()
	vie.obtenir_cellule(i,j).basculer()
	affichage()

if __name__ == "__main__":
	vie = Grille(LARGEUR_GRILLE, LONGUEUR_GRILLE)
	vie.remplissage(TAUX)
	vie.affecte_voisins()

	Fenetre = Tk()
	Fenetre.title("Le jeu de la vie")
	G = Canvas(Fenetre, height=LARGEUR_GRILLE * TAILLE_CELLULE + 4,
			   width=LONGUEUR_GRILLE * TAILLE_CELLULE + 4,
			   bg="white")
	#G.bind("<Button-1>", clicCellule)
	G.pack(side=RIGHT)
	Button(Fenetre, text='Lancer le jeu', command=lancer).pack()
	Button(Fenetre, text='Stopper le jeu', command=stopper).pack()
	Button(Fenetre, text='Quitter', command=Fenetre.destroy).pack()
	jouer()
	Fenetre.mainloop()

