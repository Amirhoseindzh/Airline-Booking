from menu_reservation.ars.commons.ControllerManager import ControllerManager

class MainClass(object):
    """! Everything starts in this class.
    """

    @classmethod
    def main(cls):
        """! When the user runs this app, the menu will be displayed
        """

        ControllerManager().run()

main = MainClass()

main.main()
