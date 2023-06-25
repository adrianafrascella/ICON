import csv
from datetime import datetime

from numpy import nanvar
from pyswip import Prolog
from pyswip.easy import *

# Eseguo il file .pl con pyswip
prolog = Prolog()

prolog.consult('./KB/customers_complete.pl')
prolog.consult('./KB/reservations_complete.pl')

prolog.assertz('has_reservations(C, Res) :- findall(R, customer(R, C, _, _, _, _, _, _), Res)')
prolog.assertz('customer(Res, C) :- customer(Res, C, _, _, _, _, _, _)')

prolog.assertz('babies(C, R, B) :- customer(R, C, _, _, _, _, B, _)')
prolog.assertz('children(C, R, C) :- customer(R, C, _, _, _, C, _, _)')
prolog.assertz('customer_type(C, R, T) :- customer(R, C, _, T, _, _, _, _)')
prolog.assertz('previous_cancellations(C, R, PC) :- customer(R, C, PC, _, _, _, _, _)')
prolog.assertz('adults(C, R, A) :- customer(R, C, _, _, A, _, _, _)')
prolog.assertz('is_repeated_guest(C, R, RG) :- customer(R, C, _, _, _, _, _, RG)')

prolog.assertz('hotel(R, H) :- reservation(R,H,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_)')
prolog.assertz('is_canceled(R, C) :- reservation(R,_,C,_,_,_,_,_,_,_,_,_,_,_,_,_,_)')
prolog.assertz('lead_time(R, LT) :- reservation(R,_,_,LT,_,_,_,_,_,_,_,_,_,_,_,_,_)')
prolog.assertz('arrival_date_year(R, Y) :- reservation(R,_,_,_,Y,_,_,_,_,_,_,_,_,_,_,_,_)')
prolog.assertz('arrival_date_month(R, M) :- reservation(R,_,_,_,_,M,_,_,_,_,_,_,_,_,_,_,_)')
prolog.assertz('arrival_date_day_of_month(R, D) :- reservation(R,_,_,_,_,_,D,_,_,_,_,_,_,_,_,_,_)')
prolog.assertz('total_nights(R, N) :- reservation(R,_,_,_,_,_,_,N,_,_,_,_,_,_,_,_,_)')
prolog.assertz('reserved_room_type(R, RR) :- reservation(R,_,_,_,_,_,_,_,RR,_,_,_,_,_,_,_,_)')
prolog.assertz('assigned_room_type(R, AR) :- reservation(R,_,_,_,_,_,_,_,_,AR,_,_,_,_,_,_,_)')
prolog.assertz('booking_changes(R, C) :- reservation(R,_,_,_,_,_,_,_,_,_,C,_,_,_,_,_,_)')
prolog.assertz('deposit_type(R, DT) :- reservation(R,_,_,_,_,_,_,_,_,_,_,DT,_,_,_,_,_)')
prolog.assertz('days_in_waiting_list(R, W) :- reservation(R,_,_,_,_,_,_,_,_,_,_,_,W,_,_,_,_)')
prolog.assertz('adr(R, A) :- reservation(R,_,_,_,_,_,_,_,_,_,_,_,_,A,_,_,_)')
prolog.assertz('total_of_special_requests(R, SR) :- reservation(R,_,_,_,_,_,_,_,_,_,_,_,_,_,SR,_,_)')
prolog.assertz('reservation_status_date(R, RSD) :- reservation(R,_,_,_,_,_,_,_,_,_,_,_,_,_,_,RSD,_)')
prolog.assertz('meal(R, M) :- reservation(R,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,M)')

reservations = []
customers = []

with open('./CSVs/customers_complete.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        customer_id = row['customer_ID']
        reservation_id = row['reservation_ID']
        customers.append(customer_id)
        reservations.append(reservation_id)

# Itero su ogni cliente e prenotazione per recuperare le proprietà
for customer_id, reservation_id in zip(customers, reservations):
    print("Customer:", customer_id)
    print("Reservation ID:", reservation_id)

    for result in prolog.query("babies({}, {}, B)".format(customer_id, reservation_id)):
        print("Babies:", result["B"])
    for result in prolog.query("children({}, {}, C)".format(customer_id, reservation_id)):
        print("Children:", result["C"])
    for result in prolog.query("customer_type({}, {}, T)".format(customer_id, reservation_id)):
        print("Customer Type:", result["T"])
    for result in prolog.query("previous_cancellations({}, {}, PC)".format(customer_id, reservation_id)):
        print("Previous Cancellations:", result["PC"])
    for result in prolog.query("adults({}, {}, A)".format(customer_id, reservation_id)):
        print("Adults:", result["A"])
    for result in prolog.query("is_repeated_guest({}, {}, RG)".format(customer_id, reservation_id)):
        print("Is Repeated Guest:", result["RG"])
    
    for result in prolog.query("hotel({}, H)".format(reservation_id)):
        print("Hotel:", result["H"])
    for result in prolog.query("is_canceled({}, C)".format(reservation_id)):
        print("Is Canceled:", result["C"])
    for result in prolog.query("lead_time({}, LT)".format(reservation_id)):
        print("Lead Time:", result["LT"])
    for result in prolog.query("arrival_date_year({}, Y)".format(reservation_id)):
        print("Arrival Date Year:", result["Y"])
    for result in prolog.query("arrival_date_month({}, M)".format(reservation_id)):
        print("Arrival Date Month:", result["M"])
    for result in prolog.query("arrival_date_day_of_month({}, D)".format(reservation_id)):
        print("Arrival Date Day of Month:", result["D"])
    for result in prolog.query("total_nights({}, N)".format(reservation_id)):
        print("Total Nights:", result["N"])
    for result in prolog.query("reserved_room_type({}, RR)".format(reservation_id)):
        print("Reserved Room Type:", result["RR"])
    for result in prolog.query("assigned_room_type({}, AR)".format(reservation_id)):
        print("Assigned Room Type:", result["AR"])
    for result in prolog.query("booking_changes({}, C)".format(reservation_id)):
        print("Booking Changes:", result["C"])
    for result in prolog.query("deposit_type({}, DT)".format(reservation_id)):
        print("Deposit Type:", result["DT"])
    for result in prolog.query("days_in_waiting_list({}, W)".format(reservation_id)):
        print("Days in Waiting List:", result["W"])
    for result in prolog.query("adr({}, A)".format(reservation_id)):
        print("ADR:", result["A"])
    for result in prolog.query("total_of_special_requests({}, SR)".format(reservation_id)):
        print("Total of Special Requests:", result["SR"])
    for result in prolog.query("reservation_status_date({}, RSD)".format(reservation_id)):
        reservation_status_date = result["RSD"]
        # Rimuovo i caratteri non numerici dalla stringa
        reservation_status_date = reservation_status_date.replace('(', '').replace(')', '').replace('-', '')
        # Divido la stringa in una lista di valori separati da virgola
        date_parts = reservation_status_date.split(',')
        # Estraggo l'anno, il mese e il giorno dalle parti della data
        year = date_parts[0]
        month = date_parts[1].strip()
        day = date_parts[2].strip()
        # Riunisco tutto in una stringa 
        reservation_status_date = "{}/{}/{}".format(year, month, day)
        print("Reservation Status Date:", reservation_status_date)
    for result in prolog.query("meal({}, M)".format(reservation_id)):
        print("Meal:", result["M"])

    print()