import copy

class Solver():
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.croise = [[{k:False for k in range(1,10)}for j in range(9)] for i in range(9)] #False:ne croise pas, True: croise

    def solve(self):
        self.definir_croise()
        print(self.solve_step_by_step())

    def verifier_croise(self, i, y, chiffre):
        return chiffre  in [self.sudoku[i2][y2] for i2 in range(i//3*3, i//3*3 + 3) for y2 in range(y//3*3, y//3*3 +3)]\
            or chiffre in [self.sudoku[i3][y3] for i3 in range(i%3, 9, 3) for y3 in range(y%3, 9, 3)]

    def two_false_in_bloc_row(self, bloc, case, nbr):
        occurence = 0
        for i in range(case//3*3, case//3*3 +3):
            if self.sudoku[bloc][i] == 0 and self.croise[bloc][i][nbr] == False:
                occurence += 1
                if occurence > 1:
                    return True
    
    def two_false_in_bloc_col(self, bloc, case, nbr):
        occurence = 0
        for i in range(case%3, 9, 3):
            if self.sudoku[bloc][i] == 0 and self.croise[bloc][i][nbr] == False:
                occurence += 1
                if occurence > 1:
                    return True
        

    def definir_croise(self):
        #vérifier si les cases sont croisées par des chiffres sur la colonne ou sur la ligne
        for i in range(9):
            for j in range(9):
                #vérifié sur la colonne:
                if self.sudoku[i][j] == 0: #éviter de tester pour les cases qu'on a déjà leur valeur
                    for y in range(1,10):
                        if self.verifier_croise(i, j, y):
                            self.croise[i][j][y] = True
                        if y not in self.sudoku[i]:
                            if self.two_false_in_bloc_row(i, j, y):
                                row =  [[i2, j2] for i2 in range(i//3*3, i//3*3 + 3) for j2 in range(j//3*3, j//3*3 +3) if self.sudoku[i2][j2] == 0 and i2 != i]
                                for case in row:
                                    self.croise[case[0]][case[1]][y] = True
                            if self.two_false_in_bloc_col(i,j,y):
                                col = [[i3, j3] for i3 in range(i%3, 9, 3) for j3 in range(j%3, 9, 3) if self.sudoku[i3][j3] == 0 and i3 != i]
                                for case2 in col:
                                    self.croise[case2[0]][case2[1]][y] = True
        
    def element_dans_liste_de_listes(self, element, liste_de_listes):
        occurence = 0
        for liste in liste_de_listes:
            if element in liste:
                occurence += 1
                if occurence > 1:
                    return True
        return False
    
    def verifier_occurence_de_croiser_dans_bloc(self, bloc:int, nbr):
        occurence = 0
        for j in range(9):
            if self.sudoku[bloc][j] == 0:
                if self.croise[bloc][j][nbr] == False:
                    occurence += 1
                    if occurence > 1:
                        return True
        return False

    def est_le_chiffre_manquant_dans_bloc(self, bloc, nbr):
        chiffre_manquant = [i for i in range(1,10)]
        if len([1 for i in range(9) if self.sudoku[bloc][i] == 0]) != 1:
            return False
        else:

            for j in range(9):
                if self.sudoku[bloc][j] != 0:
                    chiffre_manquant.remove(self.sudoku[bloc][j])
            return True if chiffre_manquant == [nbr] else False
    
    def est_le_chiffre_manquant_dans_ligne_ou_colonne(self, bloc, case):
        
        chiffre_ligne = [self.sudoku[i2][y2] for i2 in range(bloc//3*3, bloc//3*3 + 3) for y2 in range(case//3*3, case//3*3 +3) if self.sudoku[i2][y2] != 0]
        chiffre_colonne = [self.sudoku[i3][y3] for i3 in range(bloc%3, 9, 3) for y3 in range(case%3, 9, 3) if self.sudoku[i3][y3] != 0]
        if len(chiffre_ligne) == 8:
            
            chiffre_manquant = [i for i in range(1,10) if i not in chiffre_ligne]
            
            return chiffre_manquant[0]
        elif len(chiffre_colonne) == 8:

            chiffre_manquant =  [i for i in range(1,10) if i not in chiffre_colonne]

            return chiffre_manquant[0]
        return False



    def solve_step_by_step(self):
        while self.element_dans_liste_de_listes(0, self.sudoku):
            print("-------------------------")
            copy_sudoku = copy.deepcopy(self.sudoku)
            for i in range(9):
                for j in range(9):
                    if self.sudoku[i][j] == 0:
                        tester = True
                        chiffre_manquant = self.est_le_chiffre_manquant_dans_ligne_ou_colonne(i, j)
                        for x in range(1,10):
                            
                            if tester:
                                if self.croise[i][j][x] == False and self.verifier_occurence_de_croiser_dans_bloc(i, x) == False and x not in self.sudoku[i]:
                                    print(f"1 i: {i} j: {j} x: {x}")
                                    self.sudoku[i][j] = x
                                    tester = False
                                elif self.est_le_chiffre_manquant_dans_bloc(i,x):
                                    
                                    print(f"2 i: {i} j: {j} x: {x}")
                                    self.sudoku[i][j] = x
                                    tester = False
                                elif chiffre_manquant == x:
                                    print(f"3 i: {i} j: {j} x: {x}")
                                    self.sudoku[i][j] = x
                                    tester = False 
            if copy_sudoku == self.sudoku:
                print(self.sudoku)
                return False
            self.definir_croise()
        print(self.sudoku)
        return True
"""grille =[[6, 0, 0, 0, 
3, 0, 8, 5, 2], [5, 3, 0, 0, 8, 7, 0, 9, 4], [8, 9, 0, 0, 2, 0, 3, 7, 1], [0, 0, 0, 7, 0, 8, 0, 
9, 3], [0, 4, 3, 0, 0, 1, 7, 0, 0], [7, 0, 0, 4, 0, 9, 5, 0, 0], [2, 4, 
0, 5, 7, 9, 3, 8, 1], [8, 7, 9, 3, 1, 6, 4, 2, 5], [0, 5, 0, 0, 0, 8, 9, 6, 7]]
sudoku = Solver(grille)
sudoku.solve()"""
