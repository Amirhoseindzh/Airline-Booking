import re

from menu_reservation.ars.commons.Database import Database
from menu_reservation.ars.commons.utils.ConsoleUtils import ConsoleUtils
from menu_reservation.ars.commons.utils.StringUtils import StringUtils

class Aircraft:

    number_of_rows = 7

    number_of_columns = 2

    @staticmethod
    def print():

        reservations = Database.get_instance().get_reservations()

        seats = """
                                        @@
                                       @@@@
                                      @@@@@@
                                     @@@@@@@@
                                    @@@@@@@@@@
                                   @----||----@
                                   @ 1A || 1B @
              =====================@----||----@=====================
             @@@@@@@@@@@@@@@@@@@@@@@ 2A || 2B @@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@----||----@@@@@@@@@@@@@@@@@@@@@@@@
             @@@@@@@@@@@@@@@@@@@@@@@ 3A || 3B @@@@@@@@@@@@@@@@@@@@@@@
              =====================@----||----@=====================
                                   @ 4A || 4B @
                                   @----||----@
                                   @ 5A || 5B @
                                   @----||----@
                                   @ 6A || 6B @
                                   @----||----@
                                   @ 7A || 7B @
                                   @----||----@
                        ===========@@@@@@@@@@@@===========
                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                        ===========@@@@@@@@@@@@===========
                                     @@@@@@@@
            """

        for reservation in reservations:
            seats = seats.replace(
                reservation.get_seat_number(),
                ConsoleUtils.set_red_color("XX")
                )

        ConsoleUtils.println(seats)

    @staticmethod
    def get_valid_seat_numbers():

        valid_seats = []

        for i in range(1, Aircraft.number_of_rows+1):

            for j in range(0, Aircraft.number_of_columns):
                valid_seats.append(str(i) + "" + chr(j + 65))

        return valid_seats

    @staticmethod
    def is_valid_seat_number(seat_number):

        valid_seats = Aircraft.get_valid_seat_numbers()

        if seat_number in valid_seats:
            return True
        else:
            return False

    @staticmethod
    def is_valid_seat_number_format(seat_number):

        if StringUtils.is_blank(seat_number):
            return False

        p = re.compile(r'\d+[a-zA-Z]')

        # It is valid if the format is NUMBER+LETTER
        return bool(p.match(seat_number))
