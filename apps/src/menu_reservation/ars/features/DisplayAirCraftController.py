from menu_reservation.ars.commons.Aircraft import Aircraft
from menu_reservation.ars.commons.ControllerId import ControllerId
from menu_reservation.ars.commons.utils.ConsoleUtils import ConsoleUtils
from menu_reservation.ars.features.Controller import Controller

class DisplayAirCraftController(Controller):

    def display(self):

        ConsoleUtils.println("Home >> Display Aircraft")
        ConsoleUtils.print_line()

        Aircraft.print()

        ConsoleUtils.press_enter_to_continue()

        return ControllerId.MENU
