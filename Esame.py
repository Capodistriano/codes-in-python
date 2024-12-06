class ExamException(Exception):
  pass

class CSVFile:
  def __init__(self, filename):
      self.filename = filename

class CSVTimeSeriesFile(CSVFile):
  def get_data(self):
      # Inizializzo la lista per contenere la serie temporale
      time_series = []

      # Controllo che il file esista e sia leggibile
      try:
          file = open(self.filename, 'r')

          if not file.readable():
              raise ExamException("File non leggibile")
#se non leggibile
      except Exception:
          raise ExamException("Errore nella lettura del file")

      last_timestamp = None  # Variabile che controlla che i timestamp siano ordinati

      # Legge tutte le righe(con la funzione built-in) e le salva in 'lines' come una lista di stringhe
      lines = file.readlines()
      file.close()

      # Ciclo ogni riga del file csv
      for i in range(len(lines)):
          line = lines[i].strip()  # Rimuovo i caratteri di newline

          # Ignoro la prima riga se contiene l'intestazione
          if i == 0 and line.split(",")[0] == "date":
              continue

          # salvo la lunghezza dell'input dividendolo con ","
          len_input = len(line.split(","))
          # se c'è un valore di troppo
          if len_input > 2:
              # prendo solo i primi 2, più avanti verifico se sono interi positivi
              line = ",".join(line.split(",")[:2])

          # Divido la riga in due elementi: anno-mese e numero di passeggeri
          # Se fallisce, ci sono troppi o insufficienti valori
          # In caso di errore salta la riga
          try:
              year_and_month, passengers = line.split(',')
              year, month = year_and_month.split("-")
          except Exception:
              continue

          # Verifico che il numero di passeggeri, anno e mese siano interi positivi
          try:
              year = int(year)
              month = int(month)
              passengers = int(passengers)
              if passengers < 0 or year < 0 or month < 0:
                  continue  # Ignoro righe con valori negativi
          except:
              continue  # Ignoro righe con dati non numerici

          #Verifico che i timestamp siano ordinati (nel senso crescente) e non duplicati
          #se ad esempio ho ['1949-01', 112] e ['1950-01', 234] ossia un anno non completo
          #ma il valire successivo è crescente (anno dopo) allora lo considero valido
          #e lo inserisco nella lista
          if last_timestamp is not None and year_and_month <= last_timestamp:
              raise ExamException("Errore: Timestamp fuori ordine o duplicato")

          # Aggiungo il timestamp e il numero di passeggeri alla lista
          #[
          #[“1949-01”, 112],
          #[“1949-02”, 118],
          #[“1949-03”, 132]
          #]
          time_series.append([year_and_month, passengers])

          # Aggiorno il last_timestamp per il prossimo confronto
          last_timestamp = year_and_month

      # Restituisco la lista di serie temporali
      return time_series

def compute_avg_monthly_difference(time_series, first_year, last_year):
  # Controllo se i numeri in input sono validi
  try:
      first_year = int(first_year)
      last_year = int(last_year)
  except:
      raise ExamException("Gli anni devono essere numeri validi.")

  # Verifica che first_year sia minore o uguale a last_year
  if first_year > last_year:
      raise ExamException("Il primo anno deve essere minore o uguale all'ultimo anno.")

  # Inizializzo il dizionario per salvare anno e lista passeggeri
  #[
  #[anno,	[passeggeri_mese1, passeggeri_mese2, passeggeri_mese3]]
  #[1920,	[100, 200, 300]]
  #]
  requested_values = {}

  # Itero sugli elementi del time_series e prendo solo gli anni che mi interessano
  #definiti entro (inclusi) i parametri fist_year e last_year
  for i in range(len(time_series)):
      year, month = time_series[i][0].split("-") 

      # Cast tutti a int
      year = int(year)
      month = int(month)

      # Se l'anno è inferiore al primo anno richiesto, continua
      if year < first_year:
          continue
      # Se l'anno è maggiore dell'ultimo anno richiesto, interrompi il ciclo
      elif year > last_year:
          break

      # Ora che sono nell'anno richiesto, estraggo i passeggeri
      passengers = time_series[i][1]

      # Se l'anno non è presente nel dizionario risultante
      if year not in requested_values.keys():
          # Aggiungo  un nuovo anno e inizializzazio l'array di zeri
          requested_values.update({year: [0] * 12})

      # Aggiungo il numero dei passeggeri per il mese i-1
      requested_values[year][month - 1] = passengers

  #ordina le chiavi degli anni in ordine crescente
  list_of_years = sorted(requested_values.keys())
  #memorizza la differenza media dei passeggeri tra anni consecutivi
  #per ciascun mese (da gennaio a dicembre).
  avg_diff_month = []

  for i in range(12):
      diff_month = []
      for year in range(len(list_of_years) - 1):
          next_month_passenger_value = requested_values[list_of_years[year + 1]][i]
          actual_month_passenger_value = requested_values[list_of_years[year]][i]
          if next_month_passenger_value == 0 or actual_month_passenger_value == 0:
              continue  # Se uno dei valori è 0, il risultato finale sarà 0

          diff_month.append((next_month_passenger_value - actual_month_passenger_value))

      # Calcolo la media delle differenze mensili
      if len(diff_month) > 0:
          avg_diff_month.append(sum(diff_month) / len(diff_month))

  return avg_diff_month


# Esempio di utilizzo

#try:
  # Legge i dati dal file CSV
 # file = CSVTimeSeriesFile('data.csv')  # mi assicuro che 'data.csv' esista nella directory
  #data = file.get_data()

  # Calcola la differenza media mensile tra due anni
 # differenze_medie = compute_avg_monthly_difference(data, 1949, 1951)
  #print('Differenze medie mensili:', differenze_medie)

#except ExamException as e:
 # print(e)
