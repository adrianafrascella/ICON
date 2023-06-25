% regola per definire se una prenotazione è rimasta in attesa di conferma per un tempo superiore allo standard
extended_waiting_request(ReservationID) :- reservation(ReservationID,_,_,_,_,_,_,_,_,_,_,_,Days,_,_,_,_), Days > 7.

% regola per definire se una prenotazione è di corta, media o lunga durata
short_stay(ReservationID) :- reservation(ReservationID,_,_,_,_,_,_,Nights,_,_,_,_,_,_,_,_,_), Nights < 3.
medium_stay(ReservationID) :- reservation(ReservationID,_,_,_,_,_,_,Nights,_,_,_,_,_,_,_,_,_), Nights >= 3, Nights < 7.
long_stay(ReservationID) :- reservation(ReservationID,_,_,_,_,_,_,Nights,_,_,_,_,_,_,_,_,_), Nights >= 7.

% regola per stabilire se la stanza assegnata è uguale a quella richiesta
changed_room_type(ReservationID) :- reservation(ReservationID,_,_,_,_,_,_,_,ReservedType,_,_,_,_,_,_,_,_), 
                                    reservation(ReservationID,_,_,_,_,_,_,_,_,AssignedType,_,_,_,_,_,_,_), ReservedType \= AssignedType.

% regola per capire se il cambio di stanza è stato richiesto dal cliente
customer_requested_room_change(ReservationID) :-    changed_room_type(ReservationID), 
                                                    reservation(ReservationID,_,_,_,_,_,_,_,_,_,Booking_changes,_,_,_,_,_,_), Booking_changes > 0;
                                                    reservation(ReservationID,_,_,_,_,_,_,_,_,_,_,_,_,_,Special_requests,_,_), Special_requests > 0.

% regola per stabilire se la prenotazione è una prenotazione anticipata
advanced_booking(ReservationID) :- reservation(ReservationID,_,_,Days,_,_,_,_,_,_,_,_,_,_,_,_,_), Days > 90.

% regola per definire se una prenotazione è last minute
last_minute_booking(ReservationID) :- reservation(ReservationID,_,_,Days,_,_,_,_,_,_,_,_,_,_,_,_,_), Days =< 3.

% regola che definisce una prenotazione di lusso - non risultano prenotazioni lussuose
luxury_booking(ReservationID) :-    reservation(ReservationID,_,_,_,_,_,_,_,_,_,_,_,_,Adr,_,_,_), Adr >= 200.0,
                                    reservation(ReservationID,_,_,_,_,_,_,_,_,_,_,_,_,_,Special_requests,_,_), Special_requests > 0,
                                    reservation(ReservationID,_,_,_,_,_,_,_,_,_,_,Deposit_type,_,_,_,_,_), Deposit_type \== 'no_deposit',
                                    reservation(ReservationID,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,Meal), Meal == 'fb'.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
days_between_booking_and_cancellation(ReservationID, Days) :-   reservation(ReservationID,_,_,_,Booking_year,Booking_month,Booking_day,_,_,_,_,_,_,_,_,_,_),
                                                                reservation(ReservationID,_,_,_,_,_,_,_,_,_,_,_,_,_,_,Cancellation_date,_),
                                                                
                                                                % conversione degli anni, mesi e giorni di arrivo in atomi
                                                                atom_number(BookingYearAtom, Booking_year),
                                                                atom_number(BookingMonthAtom, Booking_month),
                                                                atom_number(BookingDayAtom, Booking_day),

                                                                % parsing della data di prenotazione e della data di cancellazione
                                                                date_time_stamp(date(BookingYearAtom, BookingMonthAtom, BookingDayAtom, 0, 0, 0, 0, -1, false), BookingTimestamp),
                                                                atom_date(Cancellation_date, CancellationDateTime),
                                                                date_time_stamp(CancellationDateTime, CancellationTimestamp),
                                                                
                                                                % calcolo della differenza in giorni
                                                                DaysFloat is (CancellationTimestamp - BookingTimestamp) / (24 * 60 * 60),
                                                                Days is floor(DaysFloat).

% regola per stabilire se si tratta di una cancellazione di ultimo minuto 
last_minute_cancellation(ReservationID) :-  reservation(ReservationID,_,Is_canceled,_,_,_,_,_,_,_,_,_,_,_,_,_,_), Is_canceled = 1,
                                            days_between_booking_and_cancellation(ReservationID, Days),
                                            Days =< 3.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% regola per stabilire il giorno della settimana occupato in quella data in base alla formula Zellers Congruence
day_of_the_week(Year, Month, Day, DayOfWeek) :- Month > 2,  % Gennaio e febbraio devono essere considerati come i mesi 13 e 14 anno precedente
                                                NewMonth is Month - 2,
                                                NewYear is Year,
                                                Z is NewYear // 100,
                                                C is NewYear mod 100,
                                                F is Day + ((13 * NewMonth - 1) // 5) + C + (C // 4) + (Z // 4) - (2 * Z),
                                                DayOfWeek is (F mod 7 + 6) mod 7 + 1.

% regola che stabilisce se si tratta di una prenotazione per un weekend
weekend_booking(ReservationID) :-   reservation(ReservationID,_,_,_,_,_,_,Nights,_,_,_,_,_,_,_,_,_), Nights > 0, Nights < 3,
                                    reservation(ReservationID,_,_,_,Year,Month,Day,_,_,_,_,_,_,_,_,_,_),
                                    day_of_the_week(Year, Month, Day, DayOfWeek),
                                    member(DayOfWeek, [5, 6]). % Venerdì (5) o sabato (6)

% regola che stabilisce se potrebbe trattarsi di una prenotazione per un weekend romantico
romantic_weekend(ReservationID) :-  weekend_booking(ReservationID),
                                    customer(ReservationID,_,_,_,Adults,_,_,_), Adults = 2,
                                    customer(ReservationID,_,_,_,_,Children,_,_), Children = 0,
                                    customer(ReservationID,_,_,_,_,_,Babies,_), Babies = 0.

% regola che stabilisce se potrebbe trattarsi di una prenotazione per un viaggio di famiglia
family_vacation(ReservationID) :-   customer(ReservationID,_,_,_,Adults,_,_,_), Adults > 0,
                                    customer(ReservationID,_,_,_,_,Children,_,_), Children > 0,
                                    customer(ReservationID,_,_,_,_,_,Babies,_), Babies > 0.

% regola che stabilisce se potrebbe trattarsi di una prenotazione per un viaggio tra amici
friend_vacation(ReservationID) :-   customer(ReservationID,_,_,_,Adults,_,_,_), Adults > 2,
                                    customer(ReservationID,_,_,_,_,Children,_,_), Children = 0,
                                    customer(ReservationID,_,_,_,_,_,Babies,_), Babies = 0.

% regola che stabilisce se potrebbe trattarsi di una prenotazione per un viaggio di lavoro
work_vacation(ReservationID) :- customer(ReservationID,_,_,_,Adults,_,_,_), Adults = 1,
                                customer(ReservationID,_,_,_,_,Children,_,_), Children = 0,
                                customer(ReservationID,_,_,_,_,_,Babies,_), Babies = 0,
                                \+ weekend_booking(ReservationID),
                                reservation(ReservationID,_,_,_,_,_,_,Nights,_,_,_,_,_,_,_,_,_), Nights > 0, Nights < 4.