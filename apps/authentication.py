import bcrypt
import secrets
import datetime
from database.db_handler import DatabaseConnector as dbconn
from database.db_config import get_user_db_auth
from decorators import check_email_exists

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


class AuthRegister:
    def __init__(self, auth):
        self.db = dbconn(**auth)
        self.db.connect()

    def register(self):
        
        user_info = get_customer_info()
        fullname, phone_no, city, state, email, password = user_info
        if not self.db:
            print(NOT_INIT_CONN)
            return
    
        # Check if we already have a customer table
        if not self.table_exists("customers"):
            self.create_customers_table()

        # Check if email address exists    
        self.email_exists(email) #(working on issue)
            
        
        # Hash the password with a random salt using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        # Generate an OTP for email verification
        otp = secrets.randbelow(10000)  # This should be sent to the user's email
        try:
            # Store user details in the database
            self.db.execute_query(
                """INSERT INTO customers (
                    fullname, email, phone_no, city, state, is_verified, otp,
                    password, salt, created_at, updated_at) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    fullname,
                    email,
                    phone_no,
                    city,
                    state,
                    True,
                    otp,
                    hashed_password,
                    salt,
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                ),
            )

            print(
                """\nYour account has been created successfully.
                An email has been sent for verification."""
            )
        except Exception as e:
            print("Error registering user:", e)

    def table_exists(self, table_name):
        """True if the table exists and is not empty"""
        if not self.db:
            print(NOT_INIT_CONN)
            return False
        try:
            result = self.db.fetch_data("SHOW TABLES LIKE %s", (table_name,))
            if result is not None and len(result) > 0:
                return True  # Table exists
            else:
                return False  # Table does not exist
        except Exception as e:
            print(f"Failed to get tables from database {table_name}", e)
            return False

    @check_email_exists
    def email_exists(self, email):
        """Check if email address already exists."""
        return False

    def create_customers_table(self):
        """Create customers table if it doesn't exist"""
        if not self.db:
            print(NOT_INIT_CONN)
            return
        try:
            self.db.execute_query(
                """CREATE TABLE customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fullname VARCHAR(255),
                    email VARCHAR(255) UNIQUE,
                    phone_no VARCHAR(255) UNIQUE,
                    city VARCHAR(255),
                    state VARCHAR(255),
                    is_verified BOOLEAN,
                    otp VARCHAR(255),
                    password VARCHAR(255),
                    salt VARCHAR(255),
                    created_at DATETIME,
                    updated_at DATETIME
                )"""
            )
            print("Customers table created successfully.")
        except Exception as e:
            print("Error creating customers table:", e)


def get_customer_info():
    """Register a user with the given data"""
    fullname = input("\nENTER YOUR FULL NAME:-")
    phone_no = int(input("\nENTER YOUR PHONE NO:-"))
    city = input("\nENTER YOUR CITY NAME:-")
    state = input("\nENTER YOUR STATE:-")
    email = input("\nENTER YOUR EMAIL ID:-")
    password = input("\nENTER YOUR PASSWORD:-")
    print(f"\n ENTER OTP SENDED TO {phone_no} AND {email} (Not Configed yet)")
    user_info = {fullname, email, password, phone_no, city, state}
    return user_info


def main():
    """Main entry point for the application"""
    print(f"\n{'*'*25}WELCOME TO FLIGHT BOOKING SYSTEM{'*'*25}")
    try:
        auth = get_user_db_auth()
        # asking user if he/she already have an account or not then run the command
        acc = input("\nDO YOU HAVE AN ACCOUNT (Y/N)? ").lower()
        if acc in ["n", "no"]:
            auth_register = AuthRegister(auth)
            auth_register.register()
        elif acc in ["y", "yes"]:
            auth_login = AuthLogin(auth)
            auth_login.login()

    except Exception as e:
        print("An error occurred during database connection:", e)
        return False


main()
