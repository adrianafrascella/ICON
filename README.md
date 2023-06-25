# ICON

## Progetto di Classificazione delle Cancellazioni di Prenotazioni in un Hotel

Questo progetto si propone di identificare il modello di classificazione migliore per prevedere le cancellazioni di prenotazioni in un hotel. L'obiettivo è aiutare la gestione delle risorse e ridurre le perdite economiche dovute alle cancellazioni.

### Struttura della Cartella del Progetto

- La cartella "CSVs" contiene il file del dataset originale e i successivi file creati durante il processo di sviluppo, al fine di soddisfare le esigenze del progetto.
- La cartella "gestione dataset originale" contiene le operazioni di pulizia e preprocessing del dataset, con la conversione delle righe del file in fatti Prolog.
- La cartella "grafici" contiene le immagini dei grafici creati per lo studio dei dati e per la documentazione.
- La cartella "KB" contiene il codice e i file Prolog utilizzati per la gestione della base di conoscenza e la creazione di nuove regole, oltre ai risultati delle query numeriche suddivise tra gli individui.
- La cartella "regole" contiene i risultati delle query eseguite sulla base di conoscenza.
- La cartella "nuovo dataset" contiene file per ulteriori operazioni di preprocessing dei dati, la creazione di grafici e la gestione dei classificatori.
- La cartella "valutazioni" contiene i risultati prodotti dai file "k_fold_cross_validation", "grid_plus_k_fold" e "grid_plus_k_fold_2".

**Nota:** Per visualizzare i grafici finali dei risultati ottenuti sui set di test e di addestramento dai migliori modelli selezionati (grafici_finali.py), è necessario eseguire il file "grid_plus_k_fold_2", che salva i migliori modelli.

### Librerie Utilizzate

Le librerie utilizzate in questo progetto includono:

- numpy
- pyswip
- csv
- calendar
- pandas
- sklearn
- matplotlib
- folium
- plotly
- seaborn
- MinMaxScaler
- datetime
- os

Si consiglia di installare le librerie mancanti utilizzando il comando `pip install nome_libreria` per eseguire il codice senza errori.
