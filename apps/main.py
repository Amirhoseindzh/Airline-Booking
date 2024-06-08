from reservation_menu.ars.commons.ControllerManager import ControllerManager
from authentication.authentication import UserRegistrationService
from authentication.authentication import get_user_info, AuthLogin, AuthRegister
from models.db_config import get_user_db_auth
import os
import time
import sys


class MainMenu(object):
    #! Everything starts in this class.
    @classmethod
    def main(cls):
        """! When the user runs this app, the menu will be displayed
        """
        ControllerManager().run()

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def loading_animation(duration=3):
    """Displays a loading animation for the specified duration (in seconds)."""
    animation = "|/-\\"
    print('-'*20)
    for i in range(duration * 10):
        time.sleep(0.1)
        sys.stdout.write(f"\rLoading  + {animation[i % len(animation)]}")
        sys.stdout.flush()
    

def main_auth():
    """Main entry point for the application"""
    clear_screen()
    main_menu = MainMenu()
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
                print(
                "Your account has been created successfully.\n",
                "An email has been sent for verification.◄",
                )
                loading_animation()  # Show loading animation before main menu
                main_menu.main()

        elif acc in ["y", "yes"]:
            auth_login = AuthLogin(auth)
            if auth_login.login():
                print("\nLogin successful.")
                loading_animation()  # Show loading animation before main menu
                main_menu.main()
            else:
                print("\nInvalid email or password.")
                

    except Exception as e:
        print("An error occurred during database connection:", e)
        return False


if __name__ == "__main__":
    main_auth()
    
