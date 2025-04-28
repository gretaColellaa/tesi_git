# Nuovo algoritmo avanzato per assegnare aule

def assegna_aule_avanzato(richieste, aule, slots):
    """
    Assegna le aule alle richieste in modo intelligente:
    - Prioritizza le richieste "più critiche" (meno alternative).
    - Cerca di massimizzare il numero di richieste soddisfatte.
    - Effettua tentativi di riassegnazione dinamica se necessario.

    Parametri:
    - richieste: lista di oggetti Richiesta
    - aule: lista di oggetti Aula
    - slots: lista di oggetti Slot

    Ritorna:
    - assegnazioni: dizionario {id_richiesta: id_aula o None}
    - motivazioni: dizionario {id_richiesta: stringa motivazione}
    """
    
    # 1. Prepara struttura di disponibilità per (aula, slot)
    disponibilita = {}
    for aula in aule:
        for slot in slots:
            disponibilita[(aula.id_aula, slot.id)] = True  # All'inizio tutto libero

    # 2. Precalcola per ogni richiesta quante alternative ha
    alternative_per_richiesta = {}
    for richiesta in richieste:
        alternative = 0
        for aula in aule:
            if aula.capienza >= richiesta.capienza_richiesta:
                # Controlla se è libera su tutti gli slot richiesti
                if all(disponibilita[(aula.id_aula, id_slot)] for id_slot in richiesta.slotIds):
                    alternative += 1
        alternative_per_richiesta[richiesta.id] = alternative #memorizza quante alternative ci sono per una richiesta

    # 3. Ordina richieste: prima chi ha meno alternative, a parità di alternative chi chiede meno posti
    richieste_ordinate = sorted(richieste, key=lambda r: (alternative_per_richiesta[r.id], r.capienza_richiesta))

    # 4. Prepara struttura di assegnazione
    assegnazioni = {}
    motivazioni = {}

    # 5. Assegna aule
    for richiesta in richieste_ordinate:
        aula_trovata = None
        # Ordina aule per capienza crescente
        aule_ordinate = sorted(aule, key=lambda a: a.capienza) 

        for aula in aule_ordinate:
            if aula.capienza >= richiesta.capienza_richiesta:
                # Controlla disponibilità dell'aula su tutti gli slot
                if all(disponibilita[(aula.id_aula, id_slot)] for id_slot in richiesta.slotIds): #se sono tutti True, ritorna True
                    aula_trovata = aula
                    break

        if aula_trovata:
            # Aula trovata, assegna
            assegnazioni[richiesta.id] = aula_trovata.id_aula
            motivazioni[richiesta.id] = "Assegnazione diretta"
            for id_slot in richiesta.slotIds:
                disponibilita[(aula_trovata.id_aula, id_slot)] = False
        else:
            # Nessuna aula subito libera, proviamo riassegnazione dinamica
            if tenta_riassegnazione(richiesta, assegnazioni, disponibilita, richieste, aule):
                motivazioni[richiesta.id] = "Assegnata dopo riassegnazione dinamica"
            else:
                assegnazioni[richiesta.id] = None
                motivazioni[richiesta.id] = "Impossibile assegnare: capienza insufficiente o slot occupati"

    return assegnazioni, motivazioni


def tenta_riassegnazione(richiesta_corrente, assegnazioni, disponibilita, richieste, aule):
    """
    Tenta di liberare slot riassegnando una richiesta precedente meno critica.

    Parametri:
    - richiesta_corrente: Richiesta da soddisfare
    - assegnazioni: dizionario id_richiesta -> id_aula
    - disponibilita: dizionario (id_aula, id_slot) -> bool
    - richieste: lista di tutte le richieste
    - aule: lista di tutte le aule

    Ritorna:
    - True se riassegnazione avvenuta, False altrimenti
    """
    # Prendo aule candidate che potrebbero ospitare la richiesta
    aule_candidate = [aula for aula in aule if aula.capienza >= richiesta_corrente.capienza_richiesta]

    for aula in aule_candidate:
        # Controlla quali slot sono occupati
        slot_bloccanti = []
        for id_slot in richiesta_corrente.slotIds:
            if not disponibilita[(aula.id_aula, id_slot)]:
                slot_bloccanti.append(id_slot)

        if not slot_bloccanti:
            # Questa aula è libera su tutti gli slot --> errore nella logica principale
            continue

        # Vedi quale richiesta sta occupando questi slot
        richieste_bloccanti = []
        for id_slot in slot_bloccanti:
            for r in richieste:
                if assegnazioni.get(r.id) == aula.id_aula and id_slot in r.slotIds: #Controlla se la richiesta r è stata assegnata a questa aula, 
                                                                                    #e se lo slot che sto guardando è uno di quelli richiesti da r.
                    richieste_bloccanti.append(r)

        # Prova a spostare la richiesta bloccante su un'altra aula
        for richiesta_bloccante in richieste_bloccanti:
            # Prova a riassegnare la richiesta bloccante
            nuova_aula_per_bloccante = trova_nuova_aula(richiesta_bloccante, disponibilita, aule)
            if nuova_aula_per_bloccante:
                # Sposta la richiesta bloccante
                vecchia_aula = assegnazioni[richiesta_bloccante.id]
                assegnazioni[richiesta_bloccante.id] = nuova_aula_per_bloccante.id_aula
                for id_slot in richiesta_bloccante.slotIds:
                    disponibilita[(vecchia_aula, id_slot)] = True #libero lo slot della vecchia aula
                    disponibilita[(nuova_aula_per_bloccante.id_aula, id_slot)] = False #occupo lo slot della nuova aula

                # Ora aula libera --> assegna la nuova richiesta
                assegnazioni[richiesta_corrente.id] = aula.id_aula
                for id_slot in richiesta_corrente.slotIds:
                    disponibilita[(aula.id_aula, id_slot)] = False
                return True

    return False  # Impossibile riassegnare


def trova_nuova_aula(richiesta, disponibilita, aule):
    """
    Trova una nuova aula libera per una richiesta già assegnata.
    """
    aule_ordinate = sorted(aule, key=lambda a: a.capienza)
    for aula in aule_ordinate:
        if aula.capienza >= richiesta.capienza_richiesta:
            if all(disponibilita[(aula.id_aula, id_slot)] for id_slot in richiesta.slotIds):
                return aula
    return None
