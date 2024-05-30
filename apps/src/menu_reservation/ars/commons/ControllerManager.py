from menu_reservation.ars.commons.utils.ConsoleUtils import ConsoleUtils

from menu_reservation.ars.commons.ControllerId import ControllerId
from menu_reservation.ars.features.ListofPassengersController import ListofPassengersController
from menu_reservation.ars.features.DisplayAirCraftController import DisplayAirCraftController
from menu_reservation.ars.features.MenuController import MenuController
from menu_reservation.ars.features.AlertController import AlertController
from menu_reservation.ars.features.ReserveASeatController import ReserveASeatController

class ControllerManager(object):

    def get_controller_by_id(self, id):

        if id == ControllerId.MENU:
            return MenuController()
        elif id == ControllerId.LIST_OF_PASSENGERS:
            return ListofPassengersController()
        elif id == ControllerId.DISPLAY_AIRCRAFT:
            return DisplayAirCraftController()
        elif id == ControllerId.RESERVE_A_SEAT:
            return ReserveASeatController()
        else:
            raise RuntimeError("Controller id not found")

    def run(self):

        current_id = ControllerId.MENU

        while True:

            ConsoleUtils.clear_screen()

            try:

                current = self.get_controller_by_id(current_id)

                current_id = current.display()

            except Exception as ex:
                ConsoleUtils.clear_screen()
                AlertController(str(ex)).display()
