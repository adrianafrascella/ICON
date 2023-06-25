import csv

from numpy import nanvar
from pyswip import Prolog

# eseguo il file .pl con pyswip
prolog = Prolog()

prolog.consult('./KB/customers.pl'),
prolog.consult('./KB/reservations.pl')

# queste regole calcolano dei valori avg, max o min nel dataset su 5200 fatti, ho salvato i risultati su file
# eseguo query per ottenere le asserzioni derivate sui clienti
# numero medio di neonati per prenotazione
prolog.assertz('avg_babies(Avg_b):- findall(B, customer(_, _, _, _, _, _, B, _), Values), sumlist(Values, Sum), findall(_, reservation(R,_,_,_,_,_,_,_,_,_,_,_,_,_,_), Bookings), length(Bookings, Count), Avg_b is Sum/Count')
#numero medio di bambini per prenotazione
prolog.assertz('avg_children(Avg_c):- findall(C, customer(_, _, _, _, _, C, _, _), Values), sumlist(Values, Sum), findall(_, reservation(R,_,_,_,_,_,_,_,_,_,_,_,_,_,_), Bookings), length(Bookings, Count), Avg_c is Sum/Count')

# apro il file .pl in modalità scrittura
with open('./KB/commands_c.pl', 'w') as file:
    # scrivo le asserzioni derivate nel file .pl utilizzando il metodo write()
    for result_b in prolog.query("avg_babies(X)"):
        file.write('avg_babies = {}\n'.format(result_b["X"]))
    for result_c in prolog.query("avg_children(Y)"):
        file.write('avg_children = {}\n'.format(result_c["Y"]))

# eseguo query per ottenere le asserzioni derivate sulle prenotazioni
# numero medio di notti prenotate
prolog.assertz('avg_stay_in(Avg) :- findall(N, reservation(_,_,_,_,_,_,_,N,_,_,_,_,_,_,_,_,_), Values), sumlist(Values, Sum), length(Values, Count), Avg is Sum/Count')
# stanza più richiesta - viene restituito solo il primo tipo se ci sono più stanze con la stessa richiesta
prolog.assertz('most_desired_room(Room_type) :-  findall(RR, reservation(_,_,_,_,_,_,_,_,RR,_,_,_,_,_,_,_,_), Room_list), bagof(Oc-Room, (member(Room, Room_list), findall(X, member(X, Room_list), L), length(L, Oc)), Room_types_oc), keysort(Room_types_oc, Ordered_room_types_oc), reverse(Ordered_room_types_oc, Ordered_room_types_oc_dec), Ordered_room_types_oc_dec = [_-Room_type | _]')
# stanza meno richiesta - viene restituito solo il primo tipo se ci sono più stanze con la stessa richiesta
prolog.assertz('least_desired_room(Room_type) :-  findall(RR, reservation(_,_,_,_,_,_,_,_,RR,_,_,_,_,_,_,_,_), Room_list), bagof(Oc-Room, (member(Room, Room_list), findall(X, member(X, Room_list), L), length(L, Oc)), Room_types_oc), keysort(Room_types_oc, Ordered_room_types_oc), Ordered_room_types_oc = [_-Room_type | _]')
# maggior numero di notti per cui si estende una prenotazione
prolog.assertz('longest_reservation(Nights) :-  findall(Nights-Res, reservation(Res,_,_,_,_,_,_,Nights,_,_,_,_,_,_,_,_,_), Reservation_nights), keysort(Reservation_nights, Ordered_reservation_nights), reverse(Ordered_reservation_nights, Ordered_reservation_nights_dec), Ordered_reservation_nights_dec = [Nights-_ | _]')
# minor numero di notti per cui si estende una prenotazione
prolog.assertz('shortest_reservation(Nights) :-  findall(Nights-Res, reservation(Res,_,_,_,_,_,_,Nights,_,_,_,_,_,_,_,_,_), Reservation_nights), keysort(Reservation_nights, Ordered_reservation_nights), Ordered_reservation_nights = [Nights-_ | _]')
# periodo più lungo per cui una prenotazione ha aspettato di essere confermata
prolog.assertz('longest_wait(Waiting_days)  :-  findall(WD-Res, reservation(Res,_,_,_,_,_,_,_,_,_,_,_,WD,_,_,_,_), Confermation_wait), keysort(Confermation_wait, Ordered_confermation_wait), reverse(Ordered_confermation_wait, Ordered_confermation_wait_dec), Ordered_confermation_wait_dec = [Waiting_days-_ | _]')
# periodo più corto per cui una prenotazione ha aspettato di essere confer
prolog.assertz('shortest_wait(Waiting_days)  :-  findall(WD-Res, reservation(Res,_,_,_,_,_,_,_,_,_,_,_,WD,_,_,_,_), Confermation_wait), keysort(Confermation_wait, Ordered_confermation_wait), Ordered_confermation_wait = [Waiting_days-_ | _]')

# apro il file .pl in modalità scrittura
with open('./KB/commands_r.pl', 'w') as file:
    # scrivo le asserzioni derivate nel file .pl utilizzando il metodo write()
    for result in prolog.query("avg_stay_in(A)"):
        file.write('avg_stay_in= {}\n'.format(result["A"]))
    for result in prolog.query("most_desired_room(R)"):
        file.write('most_desired_room = {}\n'.format(str(result["R"])))
    for result in prolog.query("least_desired_room(R)"):
        file.write('least_desired_room = {}\n'.format(str(result["R"])))
    for result in prolog.query("longest_reservation(N)"):
        file.write('longest_reservation = {}\n'.format(str(result["N"])))
    for result in prolog.query("shortest_reservation(N)"):
        file.write('shortest_reservation = {}\n'.format(str(result["N"])))
    for result in prolog.query("longest_wait(D)"):
        file.write('longest_wait_for_confermation = {}\n'.format(str(result["D"])))
    for result in prolog.query("shortest_wait(D)"):
        file.write('shortest_wait_for_confermation = {}\n'.format(str(result["D"])))