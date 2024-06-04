from reservation_menu.ars.commons.Aircraft import Aircraft
from reservation_menu.ars.commons.ControllerId import ControllerId
from reservation_menu.ars.commons.Database import Database
from reservation_menu.ars.commons.utils.ConsoleUtils import ConsoleUtils
from reservation_menu.ars.commons.utils.StringUtils import StringUtils
from reservation_menu.ars.features.Controller import Controller

class ReserveASeatController(Controller):

    def display(self):

        ConsoleUtils.println("Home >> Reserve Seat")
        ConsoleUtils.print_line()

        Aircraft.print()

        seat_number = self.askSeatNumber()
        passenger_name = self.askPassengerName()

        Database.get_instance().reserve(seat_number, passenger_name)

        return ControllerId.MENU

    def askPassengerName(self):
        """! Ask the passenger name. If the user provides a blank string
        a RuntimeError still be raised.
        @return the passenger name
        """

        passenger_name = ConsoleUtils.ask_string("Passenger Name: ")

        if StringUtils.is_blank(passenger_name):
            raise RuntimeError("The passenger name should not be empty")

        return passenger_name

    def askSeatNumber(self):

        seat_number = ConsoleUtils.ask_string("Seat Number: ")

        if StringUtils.is_blank(seat_number):
            raise RuntimeError("The seat number should not be empty")

        #  we need to make all letter capitalized to have consistency
        if seat_number is not None:
            seat_number = seat_number.upper()

        if not Aircraft.is_valid_seat_number_format(seat_number):
            raise RuntimeError("The seat number is in the wrong format")

        if not Aircraft.is_valid_seat_number(seat_number):
            raise RuntimeError("The airplane does not have this seat")

        if not Database.get_instance().is_available(seat_number):
            raise RuntimeError("The seat number is not available. Try another one")

        return seat_number
