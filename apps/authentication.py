import bcrypt
import secrets
from models.db_handler import DatabaseConnector as dbconn, Email, Table, User
from models.db_config import get_user_db_auth

NOT_INIT_CONN = "Database connection is not initialized."

class AuthLogin:
    def __init__(self, auth):
        self.db = dbconn(**auth)
        self.db.connect()

    def prompt_credentials(self):
        # Separate method for prompting user credentials
        email = input("\nEnter your email: ")
        password = input("\nEnter your password: ")
        return email, password

    def verify_credentials(self, email):
        if not self.db:
            print(NOT_INIT_CONN)
            return None
        try:
            # Separate method for verifying user credentials
            user_data = self.db.fetch_data(
                """SELECT id, password, salt FROM customers 
                    WHERE email = %s""",
                (email,),
            )
            return user_data
        except Exception as e:
            print("An error occurred while verifying credentials:", e)
            return None

    def login(self):
        email, password = self.prompt_credentials()
        if not email or not password:
            print("Invalid email or password.")
            return

        user_data = self.verify_credentials(email)
        if not user_data:
            print("\nInvalid email or password.")
            return

        _, stored_password, _ = user_data[0]  # extract the password from user_data
        try:
            if bcrypt.checkpw(
                password.encode("utf-8"), str(stored_password).encode("utf-8")
            ):
                print("\nLogin successful.")
                # Add code for user session management
            else:
                print("\nInvalid email or password.")
        except Exception as e:
            print("An error occurred during authentication:", e)
            return False


class UserRegistrationService:
    def __init__(self, **auth):
        self.db = dbconn(**auth)
        self.db.connect()
        self.table = Table(**self.db.__dict__)
        self.user = User(**self.db.__dict__)
        self.email = Email(**self.db.__dict__)

    def register_user(self, **user_info):
        if not self.db:
            print(NOT_INIT_CONN)
            return

        try:
            # Check if the customers table exists, create it if not
            if not self.table.table_exists("customers"):
                self.table.create_customers_table()

            fullname = user_info["fullname"]
            phone_no = user_info["phone_no"]
            city = user_info["city"]
            state = user_info["state"]
            email = user_info["email"]
            password = user_info["password"]

            if self.email.email_exists(email):
                print("Email address already exists. Please try again.")
                return

            # Hash the password with a random salt using bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
            otp = self.generate_otp()
            self.user.insert_user(
                fullname, email, phone_no, city, state, hashed_password, salt, otp
            )
            print(
                "Your account has been created successfully.\n",
                "An email has been sent for verification.◄",
            )
        except Exception as e:
            print("Error registering user:", e)

    def generate_otp(self):
        # Generate an random OTP for email verification
        return secrets.randbelow(10000)


class AuthRegister:
    def __init__(self, user_registration_service):
        self.user_registration_service = user_registration_service

    def register(self, **user_info):
        # Check if the database connection is initialized
        if not self.user_registration_service.db:
            print(NOT_INIT_CONN)
            return False
        else:
            self.user_registration_service.register_user(**user_info)


def get_user_info():
    """Register a user with the given data"""
    fullname = input("\nENTER YOUR FULL NAME:-")
    phone_no = int(input("\nENTER YOUR PHONE NO:-"))
    city = input("\nENTER YOUR CITY NAME:-")
    state = input("\nENTER YOUR STATE:-")
    email = input("\nENTER YOUR EMAIL ID:-")
    password = input("\nENTER YOUR PASSWORD:-")
    print(f"\n > ENTER OTP SENDED TO {phone_no} AND {email} (Not Configed yet)\n")
    user_info = {
        "fullname": fullname,
        "phone_no": phone_no,
        "city": city,
        "state": state,
        "email": email,
        "password": password,
    }
    return user_info


def main():
    """Main entry point for the application"""
    print(f"\n{'*'*25}WELCOME TO FLIGHT BOOKING SYSTEM{'*'*25}\n")
    try:
        auth = get_user_db_auth()
        user_registration_service = UserRegistrationService(**auth)
        # asking user if he/she already have an account or not then run the command
        acc = input("\nDO YOU HAVE AN ACCOUNT (Y/N)? ").lower()

        if acc in ["n", "no"]:
            auth_register = AuthRegister(user_registration_service)
            user_info = get_user_info()
            auth_register.register(**user_info)

        elif acc in ["y", "yes"]:
            auth_login = AuthLogin(**auth)
            auth_login.login()

    except Exception as e:
        print("An error occurred during database connection:", e)
        return False


main()
