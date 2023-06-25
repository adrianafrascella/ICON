from numpy import nanvar
from pyswip import Prolog
from pyswip.easy import *
from datetime import datetime
import csv

# eseguo il file .pl con pyswip
prolog = Prolog()

prolog.query("use_module(library(datetime))")
prolog.query("use_module(library(date))")

prolog.consult('./KB/customers_complete.pl'),
prolog.consult('./KB/reservations_complete.pl'),
prolog.consult('./KB/regole.pl')

# apro il file .pl in modalità scrittura e scrivo le asserzioni derivate nel file .pl utilizzando il metodo write()
with open('./regole/extended_waiting_request.pl', 'w') as file:
    for result in prolog.query("extended_waiting_request(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/short_stay.pl', 'w') as file:
    for result in prolog.query("short_stay(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/medium_stay.pl', 'w') as file:
    for result in prolog.query("medium_stay(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/long_stay.pl', 'w') as file:
    for result in prolog.query("long_stay(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/changed_room_type.pl', 'w') as file:
    for result in prolog.query("changed_room_type(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/advanced_booking.pl', 'w') as file:
    for result in prolog.query("advanced_booking(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/last_minute_booking.pl', 'w') as file:
    for result in prolog.query("last_minute_booking(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/customer_requested_room_change.pl', 'w') as file:
    for result in prolog.query("customer_requested_room_change(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/luxury_booking.pl', 'w') as file:
    for result in prolog.query("luxury_booking(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/weekend_booking.pl', 'w') as file:
    for result in prolog.query("weekend_booking(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/romantic_weekend.pl', 'w') as file:
    for result in prolog.query("romantic_weekend(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/family_vacation.pl', 'w') as file:
    for result in prolog.query("family_vacation(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/friend_vacation.pl', 'w') as file:
    for result in prolog.query("friend_vacation(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))
with open('./regole/work_vacation.pl', 'w') as file:
    for result in prolog.query("work_vacation(ReservationID)"):
        file.write('{}\n'.format(str(result["ReservationID"])))