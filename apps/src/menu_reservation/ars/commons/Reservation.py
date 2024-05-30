from menu_reservation.ars.commons.utils.DateTimeUtils import DateTimeUtils

class Reservation:

    seat_number = None
    passenger_name = None
    when = None

    def __init__(self, seat_number,  passenger_name) :
        self.seat_number = seat_number
        self.passenger_name = passenger_name
        self.when = DateTimeUtils.get_now()

    def  get_seat_number(self) :
        return self.seat_number

    def  get_passenger_name(self) :
        return self.passenger_name

    def  get_when_formatted(self) :
        return DateTimeUtils.format(self.when)
