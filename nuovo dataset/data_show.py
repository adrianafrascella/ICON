import calendar
import csv

import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import HeatMap

plt.style.use('fivethirtyeight')
pd.set_option('display.max_columns', 32)

# lettura dei dati
df = pd.read_csv('./CSVs/dataset_operativo.csv')
print(df.head())
df.info()

# vediamo come cambia il prezzo medio per notte in base al periodo dell'anno
# raggruppo i dati per anno e mese e calcola il prezzo medio per notte (se la prenotazione non è stata cancellata)
data_grouped = df.groupby(['arrival_date_year', 'arrival_date_month'])['adr'].mean().reset_index()

# converto i numeri dei mesi in nomi dei mesi
data_grouped['month_name'] = data_grouped['arrival_date_month'].apply(lambda x: calendar.month_name[x])

# imposto l'ordine dei mesi
month_order = [calendar.month_name[i] for i in range(1, 13)]
data_grouped['month_name'] = pd.Categorical(data_grouped['month_name'], categories=month_order, ordered=True).codes

# creo un grafico line plot per ogni anno
years = data_grouped['arrival_date_year'].unique()

for year in years:
    data_year = data_grouped[data_grouped['arrival_date_year'] == year]
    
    # ordino i dati in base all'ordine dei mesi
    data_year = data_year.sort_values('month_name')
    
    # creo il grafico line plot per l'anno corrente
    plt.plot(data_year['month_name'], data_year['adr'], marker='o', label=str(year))

# personalizzo il grafico
plt.xlabel('Mese')
plt.ylabel('Prezzo medio per notte')
plt.title('Variare del prezzo medio per notte in base al periodo dell\'anno')
plt.xticks(rotation=45)
plt.legend(title='Anno')
plt.show()

# ora mostriamo il rapporto tra il prezzo medio per notte e la cancellazione delle prenotazioni
# calcolo la percentuale di cancellazioni per ogni mese e anno
cancellation_grouped = df.groupby(['arrival_date_year', 'arrival_date_month'])['is_canceled'].sum() / df.groupby(['arrival_date_year', 'arrival_date_month'])['is_canceled'].count() * 100
cancellation_grouped = cancellation_grouped.reset_index().rename(columns={'is_canceled': 'Cancellation Percentage'})

# unisco i dati del prezzo medio e delle cancellazioni in un unico df
data_combined = data_grouped.merge(cancellation_grouped, on=['arrival_date_year', 'arrival_date_month'], how='inner')

# creo un grafico separato per ogni anno
years = data_combined['arrival_date_year'].unique()

for year in years:
    data_year = data_combined[data_combined['arrival_date_year'] == year]
    
    # ordino i dati in base all'ordine dei mesi
    data_year = data_year.sort_values('month_name')
    
    # creo un nuovo grafico per l'anno corrente
    fig, ax1 = plt.subplots(figsize=(8, 6))
    
    # prezzo medio per notte
    ax1.plot(data_year['month_name'], data_year['adr'], marker='o', label='Prezzo medio per notte')
    ax1.set_xlabel('Mese')
    ax1.set_ylabel('Prezzo medio per notte')
    ax1.tick_params(axis='y')
    
    # percentuale di cancellazioni
    ax2 = ax1.twinx()
    ax2.plot(data_year['month_name'], data_year['Cancellation Percentage'], marker='o', color='red', label='Percentuale cancellazioni')
    ax2.set_ylabel('Percentuale cancellazioni')
    ax2.tick_params(axis='y')
    
    # personalizzo il grafico
    plt.title('Variazione del prezzo medio per notte e percentuale cancellazioni per l\'anno ' + str(year))
    plt.xticks(rotation=45)
    
    # legenda
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper right')
    
    plt.show()

# adesso confrontiamo per ogni anno l'affluenza e le cancellazioni
# calcolo il numero totale di ospiti sommando adulti, bambini e neonati
df['guests'] = df['adults'] + df['children'] + df['babies']

# raggruppo i dati per anno e mese e calcolo il numero medio di ospiti
data_guests = df.groupby(['arrival_date_year', 'arrival_date_month']).agg({'guests': 'mean'}).reset_index()

# unisco i dati del prezzo medio e delle cancellazioni in un unico df
data_combined = data_combined.merge(data_guests, on=['arrival_date_year', 'arrival_date_month'], how='inner')

# creo un grafico per tutti gli anni
plt.figure(figsize=(10, 6))

# creo un grafico separato per ogni anno
for year in years:
    data_year = data_combined[data_combined['arrival_date_year'] == year]

    # ordino i dati in base all'ordine dei mesi
    data_year = data_year.sort_values('month_name')

    # creo un nuovo grafico per l'anno corrente
    fig = go.Figure()
    # prezzo medio per notte
    fig.add_trace(go.Scatter(x=data_year['month_name'], y=data_year['adr'], mode='lines+markers', name='Prezzo medio per notte'))
    # percentuale di cancellazioni
    fig.add_trace(go.Scatter(x=data_year['month_name'], y=data_year['Cancellation Percentage'], mode='lines+markers', name='Percentuale cancellazioni', yaxis='y2'))

    # imposto le etichette degli assi
    fig.update_layout(
        xaxis=dict(title='Mese'),
        yaxis=dict(title='Prezzo medio per notte'),
        yaxis2=dict(title='Percentuale cancellazioni', overlaying='y', side='right'),
        title='Variazione del prezzo medio per notte e percentuale cancellazioni per l\'anno ' + str(year),
        xaxis_tickangle=-45
    )
    # visualizzo il grafico
    fig.show()

# guardiamo il rapporto tra prenotazioni cancellate e prenotazioni onorate
# raggruppo i dati per lo stato della prenotazione
booking_status = df['is_canceled'].value_counts().reset_index()
booking_status.columns = ['Status', 'Count']

# mapping dei valori per lo stato della prenotazione
booking_status['Status'] = booking_status['Status'].map({0: 'Prenotazioni Rispettate', 1: 'Prenotazioni Cancellate'})

# calcolo le percentuali
booking_status['Percentage'] = booking_status['Count'] / booking_status['Count'].sum() * 100

# creo il grafico a barre
fig = px.bar(booking_status, x='Status', y='Count', color='Status', 
             text=booking_status['Percentage'].round(2),
             labels={'Count': 'Numero di prenotazioni', 'Status': 'Stato della prenotazione'},
             title='Differenza tra prenotazioni rispettate e prenotazioni cancellate')

# personalizzo il grafico
fig.update_layout(showlegend=False)
fig.update_traces(textposition='outside')

fig.show()

# raggruppo i dati per anno e mese e calcolo le medie mensili
data_means = df.groupby(['arrival_date_year', 'arrival_date_month']).agg({'total_nights_stay': 'mean'}).reset_index()

# unisco i dati in un unico df
data_combined = data_combined.merge(data_means, on=['arrival_date_year', 'arrival_date_month'], how='inner')

# ordino il dataframe sui mesi
data_combined = data_combined.sort_values('month_name')

# creo e personalizzo il grafico
plt.figure(figsize=(10, 6))
plt.plot(data_combined['month_name'], data_combined['guests'], marker='o', label='Media Ospiti')
plt.plot(data_combined['month_name'], data_combined['total_nights_stay'], marker='o', label='Media Notti Prenotate')
plt.plot(data_combined['month_name'], data_combined['adr'], marker='o', label='Media Costo Stanza/Notte')
plt.xlabel('Mese')
plt.ylabel('Media')
plt.title('Media Mensile di Ospiti, Notti Prenotate e Costo Stanza/Notte')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()