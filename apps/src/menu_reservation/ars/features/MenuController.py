from menu_reservation.ars.commons.ControllerId import ControllerId
from menu_reservation.ars.commons.utils.ConsoleUtils import ConsoleUtils
from menu_reservation.ars.features.Controller import Controller

class MenuController(Controller):

    def display(self):

        ConsoleUtils.println("Home")
        ConsoleUtils.print_line()
        ConsoleUtils.println("1 - Reserve Seat")
        ConsoleUtils.println("2 - Cancel Reservation")
        ConsoleUtils.println("3 - Display Aircraft")
        ConsoleUtils.println("4 - List of Passengers")
        ConsoleUtils.println("5 - Exit")
        ConsoleUtils.print_line()

        option = ConsoleUtils.ask_integer("Option: ")

        if option == 1:
            return ControllerId.RESERVE_A_SEAT
        elif option == 2:
            return -1
        elif option == 3:
            return ControllerId.DISPLAY_AIRCRAFT
        elif option == 4:
            return ControllerId.LIST_OF_PASSENGERS
        elif option == 5:
            ConsoleUtils.print_footer()
            quit()
        else:
            raise RuntimeError("Invalid option. Type a number between 1 to 5")
