from menu_reservation.ars.commons.Reservation import Reservation

class Database:

    instance_ = None
    reservations = []

    @classmethod
    def get_instance(cls):
        if cls.instance_ is None:
            cls.instance_ = cls.__new__(cls)
            # Put any initialization here.
        return cls.instance_

    def get_reservations(self):
        return self.reservations

    def is_available(self, seat_number):

        reservation = self.get_reservation_by_seat_number(seat_number)

        return reservation is None

    def reserve(self, seat_number, passenger_name):

        """! Save into the database the seat number and passenger name
        @param seatNumber The seat number to be saved
        @param passengerName the passenger name to be saved
        """

        self.reservations.append(Reservation(seat_number, passenger_name))

    def get_reservation_by_seat_number(self, seat_number):

        for reservation in self.reservations:

            if reservation.get_seat_number() == seat_number:
                return reservation

        return None
