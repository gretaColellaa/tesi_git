class Aula:
    def __init__(self, id_aula, capienza):
        self.id_aula = id_aula
        self.capienza = capienza

    def __str__(self):
        return f"Aula {self.id_aula} - Capienza: {self.capienza}"

class Professore:
    def __init__(self, id_prof, nome, cognome, email, password):
        self.id_prof = id_prof
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password

    def __str__(self):
        return f"Prof. {self.nome} {self.cognome} - Email: {self.email}"


class Richiesta:
    def __init__(self, id_richiesta, id_prof, capienza_richiesta, slot_ids):
        """
        slot_ids: lista di ID degli slot richiesti (es. [2, 3, 4] se serve un blocco di 3 slot)
        """
        self.id_richiesta = id_richiesta
        self.id_prof = id_prof
        self.capienza_richiesta = capienza_richiesta
        self.slot_ids = slot_ids  # ad es. [2, 3] se occupa due fasce orarie

    def __str__(self):
        return (f"Richiesta {self.id_richiesta} di Prof. {self.id_prof}, "
                f"capienza: {self.capienza_richiesta}, slot_ids: {self.slot_ids}")



class Slot:
    def __init__(self, id_slot, giorno, ora_inizio, ora_fine):
        self.id_slot = id_slot
        self.giorno = giorno
        self.ora_inizio = ora_inizio
        self.ora_fine = ora_fine

    def __str__(self):
        return (f"Slot {self.id_slot} - {self.giorno} "
                f"{self.ora_inizio}-{self.ora_fine}")
