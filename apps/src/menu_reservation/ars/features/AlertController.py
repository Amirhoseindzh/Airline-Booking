from menu_reservation.ars.commons.utils.ConsoleUtils import ConsoleUtils
from menu_reservation.ars.features.Controller import Controller

class AlertController(Controller):

    message = str()

    def __init__(self, message):
        self.message = message

    def display(self):

        ConsoleUtils.println("")
        ConsoleUtils.show_error(self.message)

        return 0
