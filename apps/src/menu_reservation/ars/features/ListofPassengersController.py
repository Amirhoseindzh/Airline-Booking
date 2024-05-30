from menu_reservation.ars.commons.utils.ConsoleUtils import ConsoleUtils
from menu_reservation.ars.commons.ControllerId import ControllerId
from menu_reservation.ars.features.Controller import Controller
from menu_reservation.ars.commons.Database import Database
from menu_reservation.ars.commons.Aircraft import Aircraft

class ListofPassengersController(Controller):

    db = Database.get_instance()

    def display(self):

        ConsoleUtils.println("Home >> List of Passengers")
        ConsoleUtils.print_line()

        for seat_number in Aircraft.get_valid_seat_numbers():

            output = seat_number + "\t"

            reservation = self.db.get_reservation_by_seat_number(seat_number)

            if reservation is None:
                output += ConsoleUtils.set_green_color("Empty")
            else:
                output += ConsoleUtils.set_red_color(self.getWhen(reservation)) + "\t"
                output += ConsoleUtils.set_red_color(self.get_passenger_name(reservation)) + "\t"

            ConsoleUtils.println(output)

        ConsoleUtils.println("")
        ConsoleUtils.press_enter_to_continue()

        return ControllerId.MENU

    @classmethod
    def get_passenger_name(cls, reservation):

        if reservation is None:
            return ""

        return reservation.get_passenger_name()

    @classmethod
    def getWhen(cls, reservation):

        if reservation is None:
            return ""

        return reservation.get_when_formatted()
