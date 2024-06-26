import bcrypt
import secrets
from models.db_handler import (
    DatabaseConnector as dbconn, Email, Table, User)

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
        
        # extract the password from user_data
        _, stored_password, _ = user_data[0] 
        try:
            # check if the password is valid
            if bcrypt.checkpw(
                password.encode("utf-8"), str(stored_password).encode("utf-8")
            ):
                return True
            else:
                return False
        except Exception as e:
            print("An error occurred during authentication:", str(e))
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
                fullname, email, phone_no,
                city, state, hashed_password, salt, otp
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
    try:
        fullname = input("\nENTER YOUR FULL NAME:-")
        if not isinstance(fullname, str) or not fullname.strip():
            raise ValueError("Full name must be a non-empty string")

        phone_no = input("\nENTER YOUR PHONE NO:-")
        if not phone_no.isdigit():
            raise ValueError("Phone number must be numeric")
        phone_no = int(phone_no)

        city = input("\nENTER YOUR CITY NAME:-")
        if not isinstance(city, str) or not city.strip():
            raise ValueError("City name must be a non-empty string")

        state = input("\nENTER YOUR STATE:-")
        if not isinstance(state, str) or not state.strip():
            raise ValueError("State must be a non-empty string")

        email = input("\nENTER YOUR EMAIL ID:-")
        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email must be a non-empty string")

        password = input("\nENTER YOUR PASSWORD:-")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password must be a non-empty string")

        print(
            f"\n > ENTER OTP SENT TO {phone_no} AND {email}\n",
            "(Not Configured yet)\n")

        user_info = {
            "fullname": fullname,
            "phone_no": phone_no,
            "city": city,
            "state": state,
            "email": email,
            "password": password,
        }
        return user_info

    except ValueError as e:
        print(f"Input error: {e}")
        return None
