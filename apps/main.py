from reservation_menu.ars.commons.ControllerManager import ControllerManager
from authentication.authentication import UserRegistrationService
from authentication.authentication import get_user_info, AuthLogin, AuthRegister
from models.db_config import get_user_db_auth
import os


class MainMenu(object):
    #! Everything starts in this class.
    @classmethod
    def main(cls):
        """! When the user runs this app, the menu will be displayed
        """
        ControllerManager().run()

def main_auth():
    os.system('cls')
    """Main entry point for the application"""
    print(f"\n{'*'*25}WELCOME TO FLIGHT BOOKING SYSTEM{'*'*25}\n")
    try:
        auth = get_user_db_auth()
        user_registration_service = UserRegistrationService(**auth)
        # asking user if he/she already have an account or not
        # then run the command
        acc = input("\nDO YOU HAVE AN ACCOUNT (Y/N)? ").lower()

        if acc in ["n", "no"]:
            auth_register = AuthRegister(user_registration_service)
            user_info = get_user_info()
            if user_info is not None:
                auth_register.register(**user_info)

        elif acc in ["y", "yes"]:
            auth_login = AuthLogin(**auth)
            auth_login.login()

    except Exception as e:
        print("An error occurred during database connection:", e)
        return False


if __name__ == "__main__":
    main_auth()
    main_menu = MainMenu()
    main_menu.main()
