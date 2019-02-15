import CSP

class sudoku:

    """Classe che rappresenta il problema Sudoku. Vengono quindi inizializzate le variabili, i domini, i vincoli e i
    vicini. Inoltre, nel momento della creazione di un oggetto di tipo sudoku, vuole in ingresso un assegnamento
    iniziale"""

    def __init__(self,ass_init):
        self.var = []
        self.domini = {}
        self.vicini = {}
        self.assignment = {}
        self.lettere = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        self.numeri = [i for i in range(1, 10)]
        self.row = []
        self.col = []
        self.box = []
        self.creaGioco(ass_init)

    def creaTab(self):
        """Crea la tabella 9x9, identificano 81 variabili. Ogni variabile è una tupla con una lettera e un numero che
        identificano rispettivamente la riga e la colonna. Inoltre vengono anche inizializzate:
        row = una lista di liste, ogni sottolista identifica l'insieme delle variabili contentute in una riga;
        col = una lista di liste, ogni sottolista identifica l'insieme delle variabili contentute in una colonna;
        box = una lista di liste, ogni sottolista identifica l'insieme delle variabili contenute in un box;

                  c c c   c c c   c c c
                  o o o   o o o   o o o
                  l l l   l l l   l l l
                  1 2 3   4 5 6   7 8 9

                  1 2 3 | 4 5 6 | 7 8 9
        row1    A       |       |
        row2    B  box1 |  box2 |  box3
        row3    C       |       |
                ------------------------
        row4    D       |       |
        row5    E  box4 |  box5 | box6
        row6    F       |       |
                ------------------------
        row7    G       |       |
        row8    H  box7 |  box8 | box9
        row9    I       |       |


        """
        for r in range(0,9):
            self.row.append([])
            for i in self.numeri:
                self.row[r].append((self.lettere[r], i))
        for r in range(0,9):
            self.col.append([])
            for i in self.lettere:
                self.col[r].append((i,r+1))
        for t in range(0,9):
            self.box.append([])
        k = 0
        for i in [0,3,6]:
            for j in [0,1,2]:
                for t in [1,2,3]:
                    self.box[i].append((self.lettere[k + j], t))
                    self.box[i+1].append((self.lettere[k + j], t + 3))
                    self.box[i+2].append((self.lettere[k + j], t + 6))
            k += 3
        for k in range(0,9):
            self.var += self.row[k]

    def creaDomini(self):
        """Inizializza i domini per ogni variabile: i numeri da 1 a 9"""
        for i in self.var:
            self.domini[i] = [k for k in range(1,10)]

    def creaVicini(self):
        """Per ogni variabile, aggiunge al dizionario dei vicini tutti gli elementi della sua riga, colonna e box."""
        for r in range(0,9):
            for i in range(0,9):
                self.vicini[self.row[r][i]] = self.row[r]
        for i in self.lettere:
            for k in range(1,10):
                self.vicini[(i,k)] = self.vicini[(i,k)] + self.col[k-1]
        k = 0
        for i in [0,3,6]:
            for j in [0,1,2]:
                for t in [1,2,3]:
                    self.vicini[self.lettere[k + j], t] = self.vicini[self.lettere[k + j], t] + self.box[i]
                    self.vicini[self.lettere[k + j], t + 3] = self.vicini[self.lettere[k + j], t + 3] + self.box[i+1]
                    self.vicini[self.lettere[k + j], t + 6] = self.vicini[self.lettere[k + j], t + 6] + self.box[i+2]
            k += 3
        for i in self.var:
            """Per come è stato costruito il dizionario dei vicini, ogni variabile ha come vicino anche se stessa per 3
                volte. Con questo ciclo elimino questa ridondanza"""
            for j in [0,1,2]:
                self.vicini[i].remove(i)

    def creaGioco(self, ass_init):
        """Metodo che crea la Tabella, i Domini e i Vicini e assegna l'assegnamento iniziale"""
        self.creaTab()
        self.creaDomini()
        self.creaVicini()
        for i in ass_init.keys():
            CSP.csp.assign(self,i, ass_init[i], self.assignment)

    def vincolo(self,A,a,B,b):
        """Vincolo per il sudoku. Ogni vicino di una variabile deve essere diverso dalla variabile stessa"""
        if a == (None) or b == (None):
            return True
        A = a
        B = b
        if A != B:
            return True
        return False

    def display(self):
        """Metodo che permette di far vedere graficamente la soluzione"""
        count = 0
        for i in self.row:
            doc = 0
            for k in i:
                print(self.assignment[k], end=" ")
                doc += 1
                if doc == 3 or doc == 6:
                    print("|",end=" ")
            print("")
            count += 1
            if count == 3 or count == 6:
                print("---------------------")