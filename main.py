
from sudoku import Sudoku
from solver import Solver


if __name__ == "__main__":
    mon_sudoku = Sudoku(4)
    mon_sudoku.creer_sudoku()
    sudoku = Solver(mon_sudoku.grille)
    sudoku.solve()
    



