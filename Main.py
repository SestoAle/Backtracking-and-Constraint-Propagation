import Backtrack,CSP,Nqueens,Sudoku, ast

"""Modulo per far risolvere i giochi. Avviando questo modulo, verrà chiesta prima la grandezza della scacchiera
del problema N-Queens, e in seguito risolverà il problema.
Poi verrà chiesto l'assegnamento iniziale del Sudoku e in seguito lo risolverà.
Degli assegnamenti iniziali già compilati sono disponibili nel file readme, con la relativa difficoltà"""


"N-Queens"

print("N-Queens")

n = input("Inserisci grandezza tabella ")

while n == "" or n == "0":
    n = input("Valore sbagliato: inserisci nuovamente grandezza tabella ")

n = int(n)

nqueens = Nqueens.n_queens(n)

problema = CSP.csp(nqueens.var,nqueens.domini,nqueens.vincolo,nqueens.vicini,nqueens.assignment)

input("Premi per risolvere N-Queens")

Backtrack.risolvi(problema, nqueens)


"Sudoku"

print("Sudoku")

print("Inserisci Assegnamento")
ass = input()

while ass == "":
    print("Inserimento sbagliato: inserisci nuovamente assegnamento")
    ass = input()

ass = ast.literal_eval(ass)

sudoku = Sudoku.sudoku(ass)

problema = CSP.csp(sudoku.var,sudoku.domini,sudoku.vincolo,sudoku.vicini,sudoku.assignment)

input("Premi per risolvere Sudoku")

Backtrack.risolvi(problema, sudoku)