import random
import time
import copy
from PIL import Image, ImageDraw, ImageFont

class Sudoku():
    def __init__(self, nbr_case_a_retirer) -> None:
        self.grille = [[0 for i in range(9)] for i in range(9)]
        self.nbr_case_a_retirer = nbr_case_a_retirer

    def creer_sudoku(self):
        self.remplir_diagonale()
        self.remplir_grille()
        self.enregistrer_sudoku_en_image('sudokuoriginale.png')
        self.generer_puzzle()
        self.enregistrer_sudoku_en_image('sudoku1.png')


    def remplir_diagonale(self):
        chiffre = [1,2,3,4,5,6,7,8,9]
        random.shuffle(chiffre)
        i_chiffre = 0
        for i in range(0 , 9, 4): #regarder chaque liste de la diagonale
            for y in range(0, 9, 4): #regarder chaque chiffre de la diagonale
                #remplir avec des chiffres
                self.grille[i][y] = chiffre[i_chiffre]
                i_chiffre += 1

    def is_valid(self, grille, chiffre, i, y):
        return chiffre not in grille[i] \
            and chiffre not in [grille[i2][y2] for i2 in range(i//3*3, i//3*3 + 3) for y2 in range(y//3*3, y//3*3 +3)]\
            and chiffre not in [grille[i3][y3] for i3 in range(i%3, 9, 3) for y3 in range(y%3, 9, 3)]

    def remplir_grille(self):
        while True:
            grille_copie = copy.deepcopy(self.grille)
            continuer = True
            nbr_case = 9
            for i, bloc in enumerate(grille_copie):
                choice_chiffre = [i for i in range(1,10) if i not in bloc]   
                for y, chiffre in enumerate(grille_copie[i]):
                    already_try = []
                    while grille_copie[i][y] == 0 and choice_chiffre != [] and set(already_try) != set(choice_chiffre) and continuer:
                        random_chiffre = random.choice(choice_chiffre)
                        already_try.append(random_chiffre)
                        if self.is_valid(grille_copie, random_chiffre, i, y):
                            grille_copie[i][y] = random_chiffre
                            choice_chiffre.remove(random_chiffre)
                            nbr_case += 1
                            if nbr_case == 81:
                                self.grille = copy.deepcopy(grille_copie)
                                return None
                        elif set(already_try) == set(choice_chiffre):
                            continuer=False
    
    def element_dans_liste_de_listes(self, element, liste_de_listes):
        occurence = 0
        for liste in liste_de_listes:
            if element in liste:
                occurence += 1
                if occurence > 1:
                    return True
        return False
    
    def is_at_least_two_element(self, liste:list)->bool:
        nbr = 0
        for element in liste:
            if element != 0:
                nbr += 1
                if nbr > 1:
                    return True
        return False
    
    def generer_puzzle(self)->list:
        puzzle = copy.deepcopy(self.grille)
        while self.nbr_case_a_retirer > 0:
            ligne = random.randint(0, 8)
            colonne = random.randint(0, 8)
            if puzzle[ligne][colonne] != 0 and self.is_at_least_two_element(puzzle[ligne]):
                if self.element_dans_liste_de_listes(puzzle[ligne][colonne],puzzle):
                    puzzle[ligne][colonne] = 0
                    self.nbr_case_a_retirer -= 1
        #il faudra vérifier qu'il y est une solution
        self.grille = copy.deepcopy(puzzle)
        print("grille = ", self.grille)
    
    def enregistrer_sudoku_en_image(self, nom_fichier):
        taille_case = 50
        taille_bordure = 2
        taille_image = 9 * taille_case + 10 * taille_bordure + 2 # Taille totale de l'image (9 cases x 9 cases)
        image = Image.new("RGB", (taille_image, taille_image), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 32)

        for i in range(9):
            for j in range(9):
                x =  (i%3*3 + j%3)* (taille_case + taille_bordure)
                y =  (i//3*3 + j//3)* (taille_case + taille_bordure)
                valeur = str(self.grille[i][j]) if self.grille[i][j] != 0 else ""
                draw.rectangle((x, y, x + taille_case, y + taille_case), fill="white", outline="black", width=taille_bordure)
                draw.text((x + 15, y + 10), valeur, fill="black", font=font)
                x_bordure = j * (taille_case + taille_bordure)
                y_bordure = i * (taille_case + taille_bordure)
                if (j + 1) % 3 == 0 and j != 8:
                    draw.line((x_bordure + taille_case, y_bordure, x_bordure + taille_case, y_bordure + taille_case), fill="black", width=4) # Ajout de lignes verticales entre les blocs

            if (i + 1) % 3 == 0 and i != 8:
                draw.line((0, y_bordure + taille_case, taille_image, y_bordure + taille_case), fill="black", width=4) # Ajout de lignes horizontales entre les blocs

        image.save(nom_fichier)