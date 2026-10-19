import csv

# classi di supporto
class Stand:
    def __init__(self, codice, metriquadri, padiglione, prezzo_base):
        self.codice = codice
        self.metriquadri = metriquadri
        self.padiglione = padiglione
        self.prezzo_base = float(prezzo_base)   #è un valore numerico,serve il float!!!

        self.disponibile = True
        self.espositore = None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __eq__(self,other):
        if isinstance(other,Stand):  #verifica il tipo
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        if isinstance(other,Stand):
            return self.calcola_prezzo() < other.calcola_prezzo()
        return NotImplemented

class Standard(Stand):
  # Eredita già tutto l'__init__, i metodi e gli attributi da Stand!
  # Definisco solo come deve essere stampato:
  def __str__(self):
      if self.disponibile:
          stato = "Disponibile"
      else:
          stato = "Occupato"
      return (
          f"{self.codice}: Standard | {self.metriquadri} mq - Padiglione"
          f" {self.padiglione} - Prezzo {self.calcola_prezzo()}€ - {stato}")

class StandPreseExtra(Stand):
    def __init__(self, codice, metriquadri, padiglione, prezzo_base, num_prese):
        super().__init__(codice, metriquadri, padiglione, prezzo_base) #invece di scrivere tutti gli attributi
        self.num_prese = int(num_prese)

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.num_prese)   # RICORDA RETURN

    def __str__(self):
        if self.disponibile is not None:
            stato = "Disponibile"
        else:
            stato = "Occupato"
        return (f"{self.codice}: Prese Extra | {self.metriquadri} mq - Padiglione {self.padiglione} "
                f"- Prezzo {self.calcola_prezzo()}€"
                f"- Prese aggiuntive: {self.num_prese} - {stato}")

class StandPremium(Stand):
    def __init__(self, codice, metriquadri, padiglione, prezzo_base, posizione):
        super().__init__(codice, metriquadri, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        if self.disponibile is not None:
            stato = "Disponibile"
        else:
            stato = "Occupato"
        return (f"{self.codice}: Premium | {self.metriquadri} mq - Padiglione {self.padiglione} "
                f"- Prezzo {self.calcola_prezzo()}€ - {stato}")

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand_assegnato = None

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        # Controllo se l'espositore ha uno stand assegnato
        if self.stand_assegnato is not None:
            stand_str = f" - Stand: {self.stand_assegnato.codice}"
        else:
            stand_str = " - Nessuno stand assegnato"

        # Restituisco la stringa completa
        return f"{self.codice}: {self.nome} {self.cognome}{stand_str}"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome  # uso l'underscore _nome per indicare attributo PRIVATO
        self.stand_list = []  # ricorda di costruire la LISTA
        self.espositori_list = []

    """Aggiungere setter e getter se necessari"""
    # serve per leggere e restituire il valore dell'attributo privato
    @property
    def nome(self):
        return self._nome

    # serve per modificare il valore di un attributo
    @nome.setter
    def nome(self, nuovo_nome):
       self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, mode = 'r', encoding = 'utf-8') as f:
                reader = csv.reader(f)
                for riga in reader:
                    if not riga:
                        continue
                    codice = riga[0]

                    # ora gestitsco gli stand
                    if codice[:2] == "ST":
                        metriquadri = float(riga[1])
                        padiglione = int(riga[2])
                        prezzo_base = float(riga[3])

                        if len(riga) == 4:
                            stand = Standard(codice, metriquadri, padiglione, prezzo_base)
                        elif len(riga) == 5:
                            valore_agg = riga[4]  #come distinguere i due tipi di stand
                            try:
                                num_prese = int(valore_agg)
                                stand = StandPreseExtra(codice, metriquadri, padiglione, prezzo_base, num_prese)
                            except ValueError:
                                stand = StandPremium(codice, metriquadri, padiglione, prezzo_base, valore_agg)
                        self.stand_list.append(stand)  #NOTA BENE

                    elif codice[:2] == "ES":
                        nome_esp = riga[1]
                        cognome_esp = riga[2]
                        espositore = Espositore(codice, nome_esp, cognome_esp)
                        self.espositori_list.append(espositore)

        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: Il file {file_path} non è stato trovato")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""

        stand_trovato = None
        for s in self.stand_list:
            if s.codice == codice_stand:
                stand_trovato = s
                break   #se non trova nulla, stand è rimasto None e quindi ho not stand

        espositore_trovato = None
        for e in self.espositori_list:
            if e.codice == codice_espositore:
                espositore_trovato = e
                break

        # potevo usare anche solo la funzione next
        # stand = next((s for s in self.stand_list if s.codice == codice_stand), None)
        # espositore = next((e for e in self.espositori_list if e.codice == codice_espositore), None)

        if not stand_trovato or not espositore_trovato:
            raise ValueError("Stand o espositore non trovati nel sistema.")
        if not stand_trovato.disponibile:
            raise ValueError(f"Lo stand {codice_stand} non è disponibile.")
        if espositore_trovato.stand_assegnato is not None:
            raise ValueError(f"L'espositore {codice_espositore} ha già uno stand assegnato.")

        # Aggiorna lo stato e i riferimenti bidirezionali usando i nomi corretti!
        stand_trovato.disponibile = False
        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand_assegnato = stand_trovato

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        if not self.espositori_list:
            print("Nessun espositore registrato nel sistema.")
            return
        for espositore in self.espositori_list:
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand_list)
