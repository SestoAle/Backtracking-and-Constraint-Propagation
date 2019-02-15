class n_queens:

    """Classe che rappresenta il problema delle N-Queens.
    In questo caso:
    le variabili sono le colonne (di modo da eliminare eventuali vincoli sulle colonne), formate da una tupla
    contentente la lettera X e il numero della colonna;
    i domini per ogni variabile sono i numeri da 1 fino a n (che mi rappresentano le righe);
    i vicini di una variabile sono tutte le altre colonne;
    il vincolo è una funzione che presi 2 vicini, controlla che questi non abbiano lo stesso valore (quindi che 2
    regine non siano sulla stessa riga), e controlla che b != a - |numero_colonna_A - numero_colonna_B| e che
    b != a + |numero_colonna_A - numero_colonna_B|


    n = 8



              X2   X3   X4   X5   X6   X7   X8
            |----|----|----|----|----|----|----|
          1 |    |x-2 |    |    |    |    |    |
            |----|----|----|----|----|----|----|
          2 |    |    |x-1 |    |x-1 |    |    |
            |----|----|----|----|----|----|----|
          3 |    |    |    | x  |    |    |    |
            |----|----|----|----|----|----|----|
          4 |    |    |x+1 |    |x+1 |    |    |
            |----|----|----|----|----|----|----|
          5 |    |    |    |    |    |x+2 |    |
            |----|----|----|----|----|----|----|
          6 |    |    |    |    |    |    |    |
            |----|----|----|----|----|----|----|
          7 |    |    |    |    |    |    |    |
            |----|----|----|----|----|----|----|
          8 |    |    |    |    |    |    |    |
            |----|----|----|----|----|----|----|

    """


    def __init__(self,n,assignment = {}):
        self.n = n
        self.var = []
        self.domini = {}
        self.vicini = {}
        self.assignment = assignment
        self.creaGioco()

    def creaGioco(self):
        for i in range(1,self.n+1):
            self.var.append(("X",i))
        for var in self.var:
            self.domini[var] = [k for k in range (1,self.n+1)]
        for var in self.var:
            self.vicini[var] = []
            for vic in self.var:
                self.vicini[var] = self.vicini[var] + [vic]
        for i in self.var:
            self.vicini[i].remove(i)

    def vincolo(self,A,a,B,b):
        if a == None or b == None:
            return True
        if a != b and b != a - abs((A[1]-B[1])) and b != a + abs((A[1]-B[1])):
            return True
        return False

    def display(self):
        """Metodo che permette di far vedere graficamente la soluzione"""
        for i in range(0,self.n):
            print("|",end="-----")
        print("|")
        for j in range(0,self.n):
            for i in range(0,self.n):
                if self.assignment[("X"),i+1] == j+1:
                    print("|",end="  Q  ")
                else: print("|",end="     ")
            print("|")
            for i in range(0,self.n):
                print("|",end="-----")
            print("|")
