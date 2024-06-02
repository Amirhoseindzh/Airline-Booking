import mysql.connector
import datetime
import logging


class DatabaseConnector:
    """The database connection interface"""

    def __init__(self, **kwargs):
        self.host = kwargs.get("host")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.database = kwargs.get("database")
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to the database server"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        """disconnect connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """execute a query: first try to connect to the database
        and then execute the query and commit, finally close the connection"""
        try:
            self.connect()
            if self.connection and self.cursor is not None:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
        finally:
            self.disconnect()

    def fetch_data(self, query, params=None):
        """fetch data from the database : firrst trying to connect, then check
        if function got a parameter or not, after that execute the query
        finally disconnect"""
        try:
            self.connect()
            if self.connection and self.cursor is not None:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                data = self.cursor.fetchall()
                return data
            else:
                print("No connection to database.")
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            self.disconnect()


class Table(DatabaseConnector):
    # table modifications
    def table_exists(self, table_name):
        # check if table exists
        try:
            result = self.fetch_data("SHOW TABLES LIKE %s", (table_name,))
            if result is not None and len(result) > 0:
                return True  # Table exists
            else:
                return False  # Table does not exist
        except Exception:
            logging.error(f"Failed to get tables from database {table_name}")
            return False

    def create_customers_table(self):
        # Create a table customer
        try:
            self.execute_query(
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
            logging.info("Customers table created successfully.")
        except Exception as e:
            logging.error("Error creating customers table:", exc_info=e)


class Email(DatabaseConnector):
    # email configuration
    def email_exists(self, email):
        """Check if email address already exists."""
        try:
            result = self.fetch_data(
                "SELECT COUNT(*) FROM customers WHERE email = %s", (email,)
            )
            if result is not None and len(result) > 0 and result[0] != (0,):
                return True
            else:
                return False
        except Exception:
            logging.error("Error fetching customers email address:")


class User(DatabaseConnector):
    # user data modification
    def insert_user(
        self, fullname, email, phone_no, city, state, hashed_password, salt, otp
    ):
        try:
            # Insert user data into the customers table
            self.execute_query(
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
        except Exception:
            logging.error("Failed to insert user data into database")


class Flight(DatabaseConnector):
    
    def get_flight_info_by_no(self, flight_no):
        query = """SELECT AIRLINES_NAME, DEPARTURE, DESTINATION,
        TIME_OF_DEPARTURE, TIME_OF_ARRIVAL FROM FLIGHTS WHERE FLIGHT_NO = %s"""
        return self.execute_query(query, (flight_no,))

    def get_flight_info_by_details(self, airline_name, departure, destination):
        query = """SELECT FLIGHT_NO, TIME_OF_DEPARTURE,
        TIME_OF_ARRIVAL FROM FLIGHTS WHERE airlines_name = %s AND
        DEPARTURE = %s AND DESTINATION = %s"""

        return self.execute_query(
            query, (airline_name, departure, destination)
        )

    def get_flight_charges(self, flight_no, passenger_count, class_multiplier=1.0):
        query = "SELECT (CHARGES * %s) * %s FROM FLIGHTS WHERE FLIGHT_NO = %s"
        return self.execute_query(
            query, (passenger_count, class_multiplier, flight_no)
        )

