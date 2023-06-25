import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


def ottieni_ids(file_name):
    with open(file_name, 'r') as file:
        ids = [line.strip() for line in file]

    return ids

# carico i dataset CSV
df1 = pd.read_csv('./CSVs/customers_complete.csv')
df2 = pd.read_csv('./CSVs/reservations_complete.csv')

# li combino in un unico dataset
df = pd.merge(df1, df2, on='reservation_ID')

# elimino le colonne che indicano il tipo di stanza prenotata e quella assegnata in quanto queste sono indicate tramite sigle che non hanno potere
# informativo, pertanto successivamente introduco al loro posto la feature 'changed_room_type' che indica appunto se è stata assegnata la stanza richiesta
df.drop(['reserved_room_type', 'assigned_room_type'], axis=1, inplace=True)

# procedo inserendo la nuova conoscenza
# definisco la lista dei file cui accedere
file_names = ['./regole/changed_room_type.pl','./regole/advanced_booking.pl', './regole/family_vacation.pl', './regole/work_vacation.pl', './regole/friend_vacation.pl', './regole/last_minute_booking.pl', './regole/weekend_booking.pl', './regole/romantic_weekend.pl']

# ciclo per ciascun file/caratteristica
for file_name in file_names:
    # estraggo il nome della caratteristica dal percorso del file
    caratteristica = os.path.basename(file_name).split('.')[0]

    # aggiungo la colonna corrispondente al df con il nome della caratteristica
    df[caratteristica] = 0

    # ottieni gli ID che soddisfano la caratteristica dal file
    ids_caratteristica = ottieni_ids(file_name)

    # imposto 1 nelle colonne corrispondenti per gli ID della caratteristica
    for id_caratteristica in ids_caratteristica:
        # ottengo gli indici delle righe corrispondenti all'ID nella colonna 'reservation_ID' del df
        indici_righe = df.index[df['reservation_ID'] == id_caratteristica].tolist()

        # imposto 1 nelle colonne corrispondenti alla caratteristica per gli indici delle righe
        df.loc[indici_righe, caratteristica] = 1

# salvo il dataset aggiornato
df.to_csv('./CSVs/dataset_operativo.csv', index = False)

# PREPROCESSING
df = pd.read_csv('./CSVs/dataset_operativo.csv')
numeric_features = df.select_dtypes(include=['int', 'float'])

# rimuovo gli id poichè possono causare leakage e non hanno potere informativo
df = df.drop(['reservation_ID', 'customer_ID'], axis=1)

# è più semplice proseguire se separlo i tre termini della data 'reservation_status_date'
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
df['status_update_year'] = df['reservation_status_date'].dt.year
df['status_update_month'] = df['reservation_status_date'].dt.month
df['status_update_day'] = df['reservation_status_date'].dt.day
df.drop(['reservation_status_date'] , axis = 1, inplace = True)

# stampo i valori unici per ciascuna colonna
for col in df.columns:
    print(f"{col}: \n{df[col].unique()}\n")

# codifico alcune tra le variabili categoriche rendendo i valori variabili booleane indipendenti (one hot encoding/dummie encoding)
columns_to_encode= ['hotel','meal','deposit_type','customer_type']
df = pd.get_dummies(df, columns=columns_to_encode, dtype=int)

df.rename(columns={'hotel_resort_hotel': 'resort_hotel', 'hotel_city_hotel': 'city_hotel', 'customer_type_contract': 'ct_contract', 'customer_type_group': 'ct_group', 'customer_type_transient': 'ct_transient', 'customer_type_transient-party': 'ct_transient-party', 'deposit_type_non_refund': 'dt_non_refund', 'deposit_type_no_deposit': 'dt_no_deposit', 'deposit_type_refundable': 'dt_refundable'}, inplace=True)

features_to_normalize = df[['previous_cancellations','ct_contract','ct_group','ct_transient', 'ct_transient-party','adults','children','babies','resort_hotel','city_hotel','lead_time','arrival_date_year','arrival_date_month','arrival_date_day_of_month','total_nights_stay','booking_changes','dt_non_refund','dt_no_deposit','dt_refundable','days_in_waiting_list','adr','total_of_special_requests','status_update_year','status_update_month','status_update_day','meal_bb','meal_fb','meal_hb','meal_sc','meal_undefined']]
features_bool= df[['is_repeated_guest','is_canceled','changed_room_type','advanced_booking','family_vacation','work_vacation','friend_vacation','last_minute_booking','weekend_booking','romantic_weekend']]
print(features_bool)

# normalizzo tramite MinMaxScaler
column_names = features_to_normalize.columns

scaler = MinMaxScaler()
df_normalized = scaler.fit_transform(features_to_normalize)

df_normalized = pd.DataFrame(df_normalized, columns=column_names)
df = pd.concat([df_normalized, features_bool], axis=1)
df.to_csv('./CSVs/dataset_normalizzato.csv', index = False)

# creo una heat map per la correlazione tra le variabili categoriche e una numeriche perchè altrimenti risulta poco leggibile
plt.figure(figsize = (24, 12))
corr = numeric_features.corr()
sns.heatmap(corr, annot = True, linewidths = 1)
plt.show()

categorical_features = df[['ct_contract','ct_group','ct_transient','ct_transient-party','dt_non_refund','dt_no_deposit','dt_refundable','meal_bb','meal_fb','meal_hb','meal_sc','meal_undefined']]
categorical_features = categorical_features.copy()
categorical_features['is_canceled'] = df.loc[:, 'is_canceled']
plt.figure(figsize = (24, 12))
corr = categorical_features.corr()
sns.heatmap(corr, annot = True, linewidths = 1)
plt.show()

df.info()

# in particolare ora mi soffermo sulla correlazione con il target
correlation = df.corr()['is_canceled'].abs().sort_values(ascending = False)
print(correlation)