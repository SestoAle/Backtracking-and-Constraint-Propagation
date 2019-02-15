import random, copy, time


def ac3(csp, coda = None):
    """Tipico algoritmo AC-3: se non viene data nessuna coda in ingresso, allora l'algoritmo la inizializza con tutti gli
    archi del CSP. Per ogni arco, chiama REVISE. Alla fine di REVISE, se qualche dominio di Xi è rimasto vuoto, vuol
    dire che il problema è insoddisfacibile e ritorna Failure, altrimenti rimette tutti gli archi esistenti tra Xi e i
    suoi vicini (tranne (Xi,Xj)) perchè potrebbero essere diventati inconsistenti"""
    if coda == None:
        coda = [(Xi, Xk) for Xi in csp.var for Xk in csp.vicini[Xi]]
    cons = False
    while coda:
        (Xi, Xj) = coda.pop()
        if revise(csp, Xi, Xj):
            cons = True
            if len(csp.domini[Xi]) == 0:
                return "Failure"
            curr_vic = csp.vicini[Xi].copy()
            curr_vic.remove(Xj)
            for Xk in curr_vic:
                coda.append((Xk, Xi))
    return cons

def revise(csp, Xi, Xj):
    """REVISE: verifica la consistenza tra 2 variabili, elimina dal dominio valori che portano inconsistenza, e ritorna
    TRUE se toglie qualcosa dal dominio"""
    revised = False
    curr_dom = copy.deepcopy(csp.domini[Xi])
    for x in curr_dom:
        cons = False
        for y in csp.domini[Xj]:
            if (csp.vincolo(Xi, x, Xj, y)):
                cons = True
        if cons == False:
            csp.domini[Xi].remove(x)
            revised = True
    return revised

def backtrackSearch(csp):
    assignment = csp.assignment
    return backtrack(assignment, csp)

def backtrack(assignment, csp):
    """Il Backtracking è esattamente come una ricerca in profondità, ma fissando un ordinamento sia per quanto riguarda
    le variabili, sia per quanto rigurda i valori che queste variabili possono assumere. Ogni volta che viene fatto un
    assegnamento, si fa Constraint Propagation (in questo caso tramite l'algoritmo MAC). Se una particolare scelta porta
    ad un Dead-End, allora la scelta è sbagliata, si torna indietro nell'albero e si opta per un'altra scelta, così
    fino a che non si trova una soluzione (che potrebbe non essere ottima, ma subottima) o si trovano solo Dead-End.
    In questo ultimo caso, vuol dire che il problema è insoddisfacibile e l'algoritmo ritorna Failure.
    E' importante la scelta di 3 elementi:
    1- Qual'è l'ordine delle variabili?
    2- Qual'è l'ordine dei valori da assegnare?
    3- Qual'è l'inferenza che devo attuare"""
    inf = {}
    if csp.isComplete(assignment):
        "Se l'assegniment è completo, allora è una soluzione"
        return assignment
    "Scelta dell'ordine delle variabili, in questo caso MRV"
    var = mrv(csp, assignment)
    "Scelta dell'ordine dei valori, in questo caso un ordine casuale"
    for value in order_Domain_Values(var,assignment,csp):
        temp_dom = copy.deepcopy(csp.domini)
        if csp.valueIsConsistent(assignment, value, var):
            csp.assign(var, value, assignment)
            "Scelta dell'inferenza, in questo caso MAC"
            inference,inf = MAC(csp,var,assignment)
            if inference != "Failure":
                if not inf == {}:
                    for k in inf.keys():
                        csp.assign(k,inf[k],assignment)
                result = backtrack(assignment, csp)
                if result != "Failure":
                    return result
        csp.unassign(assignment, var)
        if not inf == {}:
           for k in inf.keys():
            csp.unassign(assignment,k)
        csp.domini = copy.deepcopy(temp_dom)
    return "Failure"

def FC(csp, var, value):
    """FORWARD CHECKING: Inferenza per Constraint Propagation, non espressamente richiesta dall'esercizio"""
    revised = False
    inf = {}
    vic = [k for k in csp.variabiliRimanenti(csp.vicini[var])]
    for x in vic:
        for y in csp.domini[x]:
            if not csp.vincolo(var,value,x,y):
                csp.domini[x].remove(y)
                revised = True
        if len(csp.domini[x]) == 0:
            revised = "Failure"
        if len(csp.domini[x]) == 1:
            inf[x] = csp.domini[x][0]
    return revised, inf

def MAC(csp,var,assignment):
    """MANTAINING ARC CONSISTENCY: algoritmo per Constraint Propagation. Dopo che il Backtracking ha assegnato una
    variabile Xi, il MAC chiama l'AC-3, ma invece che con una coda di tutti gli archi del problema, si inizia con quelli
    vicini a Xi. A questo punto l'AC-3 svolge il suo normale flusso, propagando per tutti i domini. Se trova un dominio
    vuoto, allora abbiamo sbagliato scelta e dobbiamo tornare indietro nell'albero"""
    coda = [(Xk, var) for Xk in csp.variabiliRimanenti(csp.vicini[var])]
    inf = {}
    cons = ac3(csp,coda)
    if cons == "Failure":
        return cons, inf
    for x in csp.variabiliRimanenti(csp.var):
        if len(csp.domini[x]) == 1:
            inf[x] = csp.domini[x][0]
    return cons, inf

def mrv(csp, assignment):
    """MINIMUM REMAINING VALUES: algoritmo con il quale si ordinano le variabili. In questo caso, si sceglie la
    variabile non assegnata con il minor numero di valori legali"""
    rimaste =[k for k in csp.variabiliRimanenti()]
    var = rimaste[0]
    for i in rimaste:
        if(len(csp.domini[i]) < len(csp.domini[var])):
            var = i
    return var

def order_Domain_Values(var, assignment, csp):
    """Metodo con il quale si ordinano i valori da assegnare. In questo caso si mescolano i domini in modo casuale"""
    lista = copy.deepcopy(csp.domini[var])
    random.shuffle(lista)
    while lista:
        yield lista.pop(0)

def risolvi(problema, gioco):
    """Metodo che chiama il Backtrack. Misura anche il tempo di esecuzione e, nel caso il CSP avesse un assegnamento
    iniziale (vedi Sudoku), chiama l'AC-3 per una Constraint Propagation iniziale ed eventualmente dire a priori se
    il problema è insoddisfacibile o no"""
    time_in = time.time()
    ac3(problema)
    for i in problema.variabiliRimanenti():
        if len(problema.domini[i]) == 1:
            problema.assign(i,problema.domini[i][0],problema.assignment)
    if problema.isComplete(problema.assignment):
        print("")
        print("Finito senza Backtacking")
        print("")
        gioco.display()
    else:
        result = backtrackSearch(problema)
        print("")
        if result == "Failure":
            print("Failure")
        else:
            gioco.display()
    print("")
    print("Tempo = ",time.time() - time_in,end="s")
    print("")