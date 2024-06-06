import os

from reservation_menu.ars.commons.utils.NumberUtils import NumberUtils
from reservation_menu.ars.commons.utils.OSUtils import OSUtils

class ConsoleUtils(object):

    ANSI_RED = "\033[0;31m"
    ANSI_GREEN = "\033[0;32m"
    ANSI_RESET = "\u001B[0m"

    @classmethod
    def print_line(cls):
        ConsoleUtils.println("------------------------------------------------------------")

    @classmethod
    def clear_screen(cls):

        if OSUtils.is_windows():
            os.system('cls')
        elif OSUtils.is_mac():
            print("\033c")
        else:
            os.system('clear')

    @classmethod
    def println(cls, str_):
        print(str_ + ConsoleUtils.ANSI_RESET)

    @classmethod
    def print_header(cls):
        ConsoleUtils.print_line()
        ConsoleUtils.print_line()

    @classmethod
    def print_footer(cls):
        ConsoleUtils.println(ConsoleUtils.set_green_color("Bye! =)"))

    @classmethod
    def show_error(cls, text):
        ConsoleUtils.println(ConsoleUtils.set_red_color("> Oops! " + text))
        ConsoleUtils.println("")
        ConsoleUtils.press_enter_to_continue()

    @classmethod
    def ask_string(cls, prefix):
        ConsoleUtils.println(prefix)
        #  Ask the user for any string
        text = input()
        if not isinstance(text, str) or isinstance(text, int):
            raise ValueError(" Your inputs must be a string or a number!")
        
        #  A good approach would be removing all leading and trailing spaces before returning it
        return text.strip()

    @classmethod
    def ask_integer(cls, field):

        text = ConsoleUtils.ask_string(field)

        if not NumberUtils.is_int(text):
            raise RuntimeError("This is not an integer number. Please try again.")

        return NumberUtils.to_int(text)

    @classmethod
    def press_enter_to_continue(cls):
        """ generated source for method pressEnterToContinue """
        cls.ask_string("Press \"ENTER\" to continue...")

    @classmethod
    def set_red_color(cls, str_):

        return cls.ANSI_RED + str_ + cls.ANSI_RESET

    @classmethod
    def set_green_color(cls, str_):

        return cls.ANSI_GREEN + str_ + cls.ANSI_RESET
