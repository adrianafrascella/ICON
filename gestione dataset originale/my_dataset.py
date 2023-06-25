import calendar

import pandas as pd

# carico il dataset CSV
df = pd.read_csv('./CSVs/hotel_booking.csv')

# aggiungo una nuova colonna chiamata 'reservation_ID' con valori iniziali a 0
df = df.assign(reservation_ID= "r0")

# itero sulle righe e assegno un nuovo valore alla colonna 'reservation_ID'
for index, row in df.iterrows():
    # assegno il nuovo valore
    nuovo_valore = f"r{index+1}"
    df.at[index, 'reservation_ID'] = nuovo_valore
    
# riordino le colonne per posizionare l'ID come primo campo
colonne = df.columns.tolist()
colonne = colonne[-1:] + colonne[:-1]
df = df.reindex(columns=colonne)

# voglio sostituire il campo name con un id poichè il nome non fornisce 
# un'informazione necessaria, creo quindi una lista di ID alfanumerici univoci
id_map = {}
def get_id(name):
    if name in id_map:
        return id_map[name]
    else:
        new_id = "c" + str(len(id_map) + 1)
        id_map[name] = new_id
        return new_id
    
# sostituisco la colonna "name" con gli ID alfanumerici
df["customer_ID"] = df["name"].apply(get_id)
df.drop('name', axis=1, inplace=True)

# oltre a sapere quanti giorni settimanali e quanti nel weekend ciascun cliente ha soggiornato, è utile conoscere i giorni totali
df["total_nights_stay"]= df["stays_in_weekend_nights"] + df["stays_in_week_nights"]

# ottengo il mapping dei nomi dei mesi ai numeri utilizzando il modulo calendar
mapping_mesi = {mese: numero for numero, mese in enumerate(calendar.month_name) if numero != 0}
# sostituisco i valori dell'attributo corrispondente al mese con i valori numerici corrispondenti utilizzando il dizionario di mapping
df['arrival_date_month'] = df['arrival_date_month'].map(mapping_mesi)

#codice non più valido perchè per una delle regole prodotte è opportuno mantenere i tre dati separati
'''# sarebbe più utile mantenere un unico dato 'data' piuttosto che avere tre campi separati per anno, mese e giorno
# combino le colonne 'anno', 'mese' e 'giorno' in una colonna di tipo stringa
df['date'] = df['arrival_date_year'].astype(str) + '-' + df['arrival_date_month'].astype(str) + '-' + df['arrival_date_day_of_month'].astype(str)
# converto la colonna 'data' in formato datetime, lo faccio anche per l'altro dato temporale presente nel dataset
df['date'] = pd.to_datetime(df['date'])
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])'''

# controllo se ci siano colonne con valori nulli per decidere se eliminarle in base al dato che rappresentano
# df['nuova_colonna'] = 0 --> usata per vierificare che effettivamente non ce ne fossero
colonne_tutti_zeri = []
for colonna in df.columns:
    if (df[colonna] == 0).all():
        colonne_tutti_zeri.append(colonna)

if not colonne_tutti_zeri:
    print("\nNon ci sono colonne che abbiano 0 come unico valore.")
else:
    print("\nLe seguenti colonne contengono solamente 0:")
    for colonna in colonne_tutti_zeri:
        print(colonna)

# controllo se ci siano colonne con valori nulli per decidere se eliminarle in base al dato che rappresentano
colonne_con_valori_nulli = df.columns[df.isnull().any()]

if colonne_con_valori_nulli.empty:
    print("\nNon ci sono colonne con valori nulli.")
else:
    print("\nLe seguenti colonne contengono valori nulli:")
    for colonna in colonne_con_valori_nulli:
        print(colonna)

# controllo se ci siano colonne composte da soli valori nulli per decidere se eliminarle in base al dato che rappresentano
colonne_solo_valori_nulli = []
for colonna in df.columns:
    if df[colonna].isnull().all():
        colonne_solo_valori_nulli.append(colonna)

if not colonne_solo_valori_nulli:
    print("\nNon ci sono colonne con solo valori nulli.")
else:
    print("\nLe seguenti colonne contengono solo valori nulli:")
    for colonna in colonne_solo_valori_nulli:
        print(colonna)

# eliminazione di alcune colonne non utili al nostro scopo
df = df.drop(colonne_solo_valori_nulli, axis=1) # per prima cosa elimino le eventuali colonne che contengono solo valori nulli
df = df.drop(columns=['distribution_channel'])
df = df.drop(columns=['required_car_parking_spaces'])
df = df.drop(columns=['arrival_date_week_number'])
df = df.drop(columns=['credit_card'])
df = df.drop(columns=['email'])
df = df.drop(columns=['phone-number'])
df = df.drop(columns=['market_segment'])
df = df.drop(columns=['reservation_status']) # l'informazione è già presente in is_canceled
df = df.drop(columns=['previous_bookings_not_canceled']) # non è utile poichè è già presente il dato previous_cancellations, molto più utile
df = df.drop(columns=['agent']) # molti valori nan + allontana dal principale obiettivo dello studio
df = df.drop(columns=['company']) # molti valori nan + allontana dal principale obiettivo dello studio
df = df.drop(columns=['country']) # molti valori nan + non utile allo scopo poichè, non conoscendo la posizione dell'hotel, 
                                    # conoscere la posizione del cliente (molto approssimativa) non è importante

# elimino quelle righe del dataset che contengono valori nulli per tipi di dati utili se presenti. Ho poi
# ottenuto i due df persona e prenotazione partendo dal dataset filtrato
# poichè la colonna children presenta valori non validi ma è un dato utile, sostituisco i Nan con 0 trattandosi di un dato numerico
df['children'] = df['children'].fillna(0)
# selezionare le righe da eliminare
prenotazioni_zero_utenti = (df['children'] == 0) & (df['adults'] == 0) & (df['babies'] == 0)
# e elimino le righe corrispondenti alla maschera
df_filtrato = df.drop(df[prenotazioni_zero_utenti].index)
df_filtrato = df[df['total_nights_stay'] != 0]

num_righe_prima = df.shape[0]
num_righe_dopo = df_filtrato.shape[0]
print(f"\nNumero di righe prima del filtraggio: {num_righe_prima}. Numero di righe dopo il filtraggio: {num_righe_dopo}.")

# AGGIORNAMENTO SUCCESSIVO: il dataset filtrato risulta comunque troppo grande per le query con valori come risultato,
# procedo con l'eliminazione di alcune righe
df_filtrato = df_filtrato.head(5200)
# num_righe = df_filtrato.shape[0]
# print(f"\nNumero di righe: {num_righe}.")

# seleziono le colonne relative al cliente
persona_df = df_filtrato[['reservation_ID','customer_ID', 'previous_cancellations', 'customer_type', 'adults', 'children', 'babies', 'is_repeated_guest']]

# seleziono le colonne relative alla prenotazione
prenotazione_df = df_filtrato[['reservation_ID', 'hotel', 'is_canceled', 'lead_time', 'arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month', 'total_nights_stay', 'reserved_room_type', 'assigned_room_type', 'booking_changes', 'deposit_type', 'days_in_waiting_list', 'adr', 'total_of_special_requests', 'reservation_status_date', 'meal']]

# salvo i dataframe in due file separati ed eseguo le modifiche elencate
persona_df.to_csv('.\CSVs\customers.csv', index=False)
df = pd.read_csv('.\CSVs\customers.csv')
# metto tutte le stringhe in minuscolo per rispettare la sintassi prolog, altrimenti risulterebbero variabili
df = df.apply(lambda x: x.astype(str).str.lower())
# se ci sono spazi tra parole inserisco il carattere _, gli spazzi non rispettano la sintassi
df = df.applymap(lambda x: "_".join(x.split()) if isinstance(x, str) else x)
# trasformo il dato numerico in children in un intero per facilitare operazioni future
df['children'] = pd.to_numeric(df['children'], errors='coerce').fillna(0).astype(int)
#df.to_csv('./CSVs/customers_complete.csv', index=False, header=True)
df.to_csv('.\CSVs\customers.csv', index=False, header=True)

prenotazione_df.to_csv('./CSVs/reservations.csv', index=False)
df = pd.read_csv('./CSVs/reservations.csv')
# metto tutte le stringhe in minuscolo per rispettare la sintassi prolog, altrimenti risulterebbero variabili
df = df.apply(lambda x: x.astype(str).str.lower())
# se ci sono spazi tra parole inserisco il carattere _, gli spazzi non rispettano la sintassi
df = df.applymap(lambda x: "_".join(x.split()) if isinstance(x, str) else x)
#df.to_csv('./CSVs/reservations_complete.csv', index=False, header=True)
df.to_csv('./CSVs/reservations.csv', index=False, header=True)