# Creazione della lista di 10 liste con id, idProf, capienza e slot
richieste = [
    [1, 101, 30, [9, 32]],
    [2, 102, 25, [9, 6, 21, 15, 13, 35]],
    [3, 103, 40, [16, 17, 26, 14, 5]],
    
]

aule = [
    [1, 30],
    [2, 25],
    [3, 40],
    [4, 35],
    
]

def trovaRichiesta(id):
    for r in richieste:
        if r[0] == id:
            return r
        

def aulePossibiliCapienza(idR): #restituisce lista di aule possibili per capienza per una richiesta in ordine crescente
    aulePossibili = []
    r = trovaRichiesta(idR)
    for a in aule:
        if a[1] >= r[2]:
            aulePossibili.append(a)
            aulePossibili.sort()

    return aulePossibili

def AssegnazioniPerCapienza(): #assegna la prima aula possibile per capienza
    assegnazioni = []
    for r in richieste:
        ap =aulePossibiliCapienza(r[0])
        assegnazioni.append([r, ap[0]])  #inserisco nella lista assegnazioni una lista di due elementi ichiesta-assegnazione (prima aula disponibile)

    return assegnazioni

def assegnazioni():
    primaAssegnazione = AssegnazioniPerCapienza()
    sov = ControlloSovrapposizione(primaAssegnazione)
    nuoveAssegnazioni = primaAssegnazione
    while sov != []:
        i=0
        for s in sov:
            r = s[0]
            a = s[1]
            nuoveAule = aulePossibiliCapienza(r[0])
            nuoveAule.remove(a) #rimuove aula in quanro non più possibile 
            nuoveAssegnazioni.remove[sov[i]] #rimuove vecchia assegnazione
            nuovaAula = nuoveAule[0]
            nuoveAssegnazioni.append([s[0], nuovaAula])
            ControlloSovrapposizione(nuoveAssegnazioni)
            i +=1
    return nuoveAssegnazioni

    



def ControlloSovrapposizione(assegnazioni): #da una lista di liste-assegnazioni con sovrapposizione
    
    sovrapposizioni = []
    for ass1 in assegnazioni:
        for ass2 in assegnazioni:
            if ass1[0]!= ass2[0] and ass1[1] == ass2[1] : #se le richieste sono diverse ma l'aula è la stessa
               r1 = ass1[0]
               r2 = ass2[0]
               slot1 = r1[3]
               slot2 = r2[3]

               for s1 in slot1:
                   for s2 in slot2:
                       if s1 == s2: #se uno slot è uguale
                           sovrapposizioni.append([r2, ass2[1]])
                           
                           
    return sovrapposizioni

        

print(assegnazioni())


