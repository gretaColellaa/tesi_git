richieste = [
    [1, 101, 30, [9, 32]],
    [2, 102, 25, [9, 6, 21, 15, 13, 35]],
    [3, 103, 40, [16, 17, 26, 14, 5]],
    [4, 104, 35, [17, 1, 35, 23]],
    [5, 105, 50, [28, 21, 8]],
    [6, 106, 20, [11, 19, 29, 9]],
    [7, 107, 45, [35]],
    [8, 108, 30, [15, 20, 19, 23]],
    [9, 109, 60, [23, 13, 31]],
    [10, 110, 55, [17, 15, 9, 6, 7, 8]]
]

aule = [
    [1, 30],
    [2, 25],
    [3, 40],
    [4, 35],
    [5, 50],
    [6, 20],
    [7, 45],
    [8, 30],
    [9, 60],
    [10, 55]
]


"""assegnazioniTemporanee = []
# Verifica delle aule possibili per ogni richiesta in termini di capienza
for r in richieste:
    aulePossibili = []
    i = len[aulePossibili]-1
    for a in aule:
        if r[2] <= a[1]: #controllo capienza
            aulePossibili.append(a[0])  

    assegnazione = [r[0], aulePossibili[i], r[3]] #assegno la prima aula utile in termini di capienza 
    
    print(f"Per la richiesta {r[0]}, le aule possibili sono: {aulePossibili}")
    assegnazioniTemporanee.append(assegnazione)
    
    
#controllo sovrapposizioni
sov = True
while sov == True:
    for aT1 in assegnazioniTemporanee :
        sovrapposizione = False
        for aT2 in assegnazioniTemporanee :
            if aT1[1] == aT2[1] and aT1[0] != aT2[0]: #se richieste diverse ma la stessa aula
                for s1 in aT1[2] :
                    for s2 in aT2[2]:
                        if s1 == s2:
                            sovrapposizione = True
                            print(f"c'è sovrapposizione nello slot {s1} nell'aula {aT1[1]}")
                            
                            assegnazioniTemporanee.remove(aT2)
                            NuovaAssegnazione = [aT2[0], aulePossibili[i], aT2[2]]
                            assegnazioniTemporanee.append(NuovaAssegnazione)
                            sovrapposizione = False

    sov = sovrapposizione"""
