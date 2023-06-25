import csv

from numpy import nanvar
from pyswip import Prolog

# leggo il file CSV dei clienti
# newline vuoto perchè rilevato automaticamente
with open('.\CSVs\customers.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #salto la prima riga
    next(reader)
    # creo un fatto Prolog per ogni riga del dataset
    facts = []
    for row in reader:
        # forma: nome_fatto(argomento1, argomento2, ...)
        fact = f"{'customer'}({', '.join(row[0:])})."
        facts.append(fact)
        
# scrivo i fatti Prolog in un file .pl
with open('.\KB\customers.pl', 'w') as plfile:
    plfile.write('\n'.join(facts))

with open('.\CSVs\customers_complete.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #salto la prima riga
    next(reader)
    # creo un fatto Prolog per ogni riga del dataset
    facts = []
    for row in reader:
        # forma: nome_fatto(argomento1, argomento2, ...)
        fact = f"{'customer'}({', '.join(row[0:])})."
        facts.append(fact)
        
# scrivo i fatti Prolog in un file .pl
with open('.\KB\customers_complete.pl', 'w') as plfile:
    plfile.write('\n'.join(facts))

# leggo il file CSV delle prenotazioni
# newline vuoto perchè rilevato automaticamente
with open('./CSVs/reservations.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #salto la prima riga
    next(reader)
    # creo un fatto Prolog per ogni riga del dataset
    facts = []
    for row in reader:
        # forma: nome_fatto(argomento1, argomento2, ...)
        fact = f"{'reservation'}({', '.join(row[0:])})."
        facts.append(fact)
        
# scrivo i fatti Prolog in un file .pl
with open('./KB/reservations.pl', 'w') as plfile:
    plfile.write('\n'.join(facts))

# leggo il file CSV delle prenotazioni
# newline vuoto perchè rilevato automaticamente
with open('./CSVs/reservations_complete.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #salto la prima riga
    next(reader)
    # creo un fatto Prolog per ogni riga del dataset
    facts = []
    for row in reader:
        # forma: nome_fatto(argomento1, argomento2, ...)
        fact = f"{'reservation'}({', '.join(row[0:])})."
        facts.append(fact)
        
# scrivo i fatti Prolog in un file .pl
with open('./KB/reservations_complete.pl', 'w') as plfile:
    plfile.write('\n'.join(facts))