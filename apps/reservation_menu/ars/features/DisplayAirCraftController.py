from reservation_menu.ars.commons.Aircraft import Aircraft
from reservation_menu.ars.commons.ControllerId import ControllerId
from reservation_menu.ars.commons.utils.ConsoleUtils import ConsoleUtils
from reservation_menu.ars.features.Controller import Controller

class DisplayAirCraftController(Controller):

    def display(self):

        ConsoleUtils.println("Home >> Display Aircraft")
        ConsoleUtils.print_line()

        Aircraft.print()

        ConsoleUtils.press_enter_to_continue()

        return ControllerId.MENU
