
class csp:

    """Classe che rappresenta i problemi CSP.
    Questo tipo di problemi sono composti da:
    Variabili = una lista di variabili;
    Domini = un dizionario, che ad ogni variabile associa i valori che le possono essere assegnati;
    Vincolo = una funzione (A,a,B,b) che ritorna TRUE se i vicini A e B soddisfano il vincolo quando A=a e B=b
                (questa definizione di vincolo è la stessa usata in http://aima.cs.berkeley.edu/python/readme.html che
                rende il vincolo più semplice di un insieme di valori);
    Vicini = dizionario che ad ogni variabili associa i suoi vicini, ovvero altre variabili che partecipano con la
                prima in un qualche vincolo"""

    def __init__(self, var, domini,vincolo, vicini, assignment = {}):
        self.var = var
        self.domini = domini
        self.vicini = vicini
        self.assignment = assignment
        self.vincolo = vincolo

    def assign(self, var, val, assignment):
        """Assegna una variabile"""
        assignment[var] = val
        self.domini[var] = [val]

    def unassign(self, assignment, var):
        """Toglie l'assegnamento di una variabile"""
        if var in assignment.keys():
            del assignment[var]

    def valueIsConsistent(self, assignment, value, var):
        """Controlla se aggiungendo X = x all'assegnamento, quest'ultimo rimane consistente"""
        tem_ass = assignment.copy()
        tem_ass[var] = value
        if self.isConsistent(tem_ass):
            return True
        return False

    def isConsistent(self, assignment):
        """Controlla se tutte le variabili assegnate soddisfano i vincoli"""
        vars = [var for var in assignment.keys()]
        consistent = True
        for var in vars:
            neig = self.vicini[var]
            for k in neig:
                if not self.vincolo(var, assignment.get(var), k, assignment.get(k)):
                    consistent = False
        return consistent

    def isComplete(self, assignment):
        """Controlla se l'assegnamento è completo"""
        if len(assignment) == len(self.var):
            return True
        return False

    def variabiliRimanenti(self,var = None):
        """Metodo che ritorna le variabili non ancora assegnate"""
        if var == None:
            var = self.var.copy()
        rim = var - self.assignment.keys()
        return rim
