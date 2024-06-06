from abc import ABC, abstractmethod
from csv import DictReader
from csv import DictWriter
import os
import logging
from models.db_handler import DatabaseConnector as dbconn, Flight
from models.db_config import get_user_db_auth


class SearchFlights:
    """TODO:
    1: get number of flights from user and return a flight
    row
    2: get information about flight from user like
    deparcher and destination and alirlines name ,return flights rows
    """

    def serach_by_number(self, number):
        """TODO: get number of flights from user and return a flight"""
        pass

    def serach_by_information(self, information):
        """TODO: get information of flight from user and return a flights"""
        pass


class PassengerData:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class Passenger:
    def __init__(self):
        self.passenger_data = []

    def get_passenger_details(self):
        passenger_count = int(input("\nEnter number of passengers: "))
        for _ in range(passenger_count):
            name = input("\nEnter name of passenger: ")
            age = int(input(f"Enter age of {name}: "))
            gender = input("Enter gender (Male/Female): ")
            self.passenger_data.append(PassengerData(name, age, gender))

    def save_passenger_data(self):
        CSV_FILE = "userdata.csv"

        with open(CSV_FILE, "a", newline="") as csvfile:
            csvwriter = DictWriter(csvfile, fieldnames=["name", "age", "gender"])
            csvwriter.writeheader()
            for passenger in self.passenger_data:
                csvwriter.writerow(passenger.__dict__)
        print("\nData entered successfully.")
    
    def read_passenger_data(self):
        csv_file = CsvFile()
        csv_file.read_csv()
        

class CsvFile:
    CSV_FILE = "userdata.csv"
    HEADER_ROW = 'name'
    def read_csv(self):
        with open(self.CSV_FILE, mode="r") as csvreader:
            reader = DictReader(csvreader)
            for row in reader:
                if row["name"] != self.HEADER_ROW:
                    self.print_data(row)
        self.remove_file()
        self.print_separator()

    def print_data(self, row):
        print(f"name: {row['name']}, age: {row['age']}, gender: {row['gender']}")

    def remove_file(self):
        os.remove(self.CSV_FILE)

    def print_separator(self):
        print("------------------------------------")


class Booking:
    CLASS_MULTIPLIERS = {
        1: 1.0,  # Economy
        2: 1.2,  # Business
        3: 1.4,  # First Class
    }

    def __init__(self, **auth):
        self.db = dbconn(**auth)
        self.db.connect()
        self.flight = Flight(**self.db.__dict__)

    def book_by_flight_no(self, flight_no, passenger_count, class_no):
        class_multiplier = self.CLASS_MULTIPLIERS.get(class_no, 1.0)
        flight_info = self.flight.get_flight_info_by_no(flight_no)
        if not flight_info:
            logging.error("Flight not found.")
            return

        charges = self.flight.get_flight_charges(
            flight_no, passenger_count, class_multiplier
        )
        self.print_booking_details(flight_info, passenger_count, charges, class_no)

    def book_by_details(
        self, airline_name, departure, destination, passenger_count, class_no
    ):
        class_multiplier = self.CLASS_MULTIPLIERS.get(class_no, 1.0)
        flight_info = self.flight.get_flight_info_by_details(
            airline_name, departure, destination
        )
        if not flight_info:
            logging.error("Flight not found.")
            return

        charges = self.flight.get_flight_charges(
            flight_info[0][0], passenger_count, class_multiplier
        )  # Assuming first flight
        self.print_booking_details(flight_info, passenger_count, charges, class_no)

    def print_booking_details(self, flight_info, passenger_count, charges, class_no):
        class_names = {1: "Economy", 2: "Business", 3: "First Class"}
        logging.info(f"\nFlight Info: {flight_info}")
        logging.info(f"Class: {class_names.get(class_no, 'Unknown')}")
        logging.info(f"Number of Passengers: {passenger_count}")
        logging.info(f"Total Charges: {charges}")


PROMPT_CONTINUE_PAYMENT = "\nTO CONTINUE PAYMENT PRESS (P):-"
PROMPT_ENTER_OTP = "\nENTER A OTP SENT TO YOUR PHONE NO AND EMAIL:-"
TRANSACTION_SUCCESS = "\nTRANSACTION SUCCESSFUL------------"
THANK_YOU = "\n**********THANK YOU***********"
PAYMENT_AMOUNT_TEMPLATE = "PAY {} TOMANS"


class PaymentMethod(ABC):
    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def process_payment(self):
        pass


class GooglePay(PaymentMethod):
    def process_payment(self):
        print("\n-------------------GOOGLE PAY---------------------------")
        print(PAYMENT_AMOUNT_TEMPLATE.format(self.amount))
        input(PROMPT_CONTINUE_PAYMENT)
        int(input(PROMPT_ENTER_OTP))
        print(TRANSACTION_SUCCESS)
        print(THANK_YOU)


class AmazonPay(PaymentMethod):
    def process_payment(self):
        print("\n-------------------AMAZON PAY---------------------------")
        print(PAYMENT_AMOUNT_TEMPLATE.format(self.amount))
        input(PROMPT_CONTINUE_PAYMENT)
        int(input(PROMPT_ENTER_OTP))
        print(TRANSACTION_SUCCESS)
        print(THANK_YOU)


class PayPal(PaymentMethod):
    def process_payment(self):
        print("\n-------------------PAYPAL---------------------------")
        print(PAYMENT_AMOUNT_TEMPLATE.format(self.amount))
        input(PROMPT_CONTINUE_PAYMENT)
        int(input(PROMPT_ENTER_OTP))
        print(TRANSACTION_SUCCESS)
        print(THANK_YOU)


class ApplePay(PaymentMethod):
    def process_payment(self):
        print("\n-------------------APPLE PAY---------------------------")
        print(PAYMENT_AMOUNT_TEMPLATE.format(self.amount))
        input(PROMPT_CONTINUE_PAYMENT)
        int(input(PROMPT_ENTER_OTP))
        print(TRANSACTION_SUCCESS)
        print(THANK_YOU)


class CardPayment(PaymentMethod):
    def process_payment(self):
        print("\n-------------------CARD PAYMENT---------------------------")
        print(PAYMENT_AMOUNT_TEMPLATE.format(self.amount))
        input(PROMPT_CONTINUE_PAYMENT)
        int(input(PROMPT_ENTER_OTP))
        print(TRANSACTION_SUCCESS)
        print(THANK_YOU)


# Example usage
if __name__ == "__main__":
    auth = get_user_db_auth()
    booking = Booking(**auth)

    # Example inputs
    print("\nCHOOSE THE CLASS YOU WANT:-")
    print("1.ECONOMY CLASS")
    print("2.BUSINESS CLASS (+20% CHARGES)")
    print("3.FIRST CLASS (+40% CHARGES)")
    ans = 1  # or 2 for booking by details
    cl = 1  # 1: Economy, 2: Business, 3: First Class
    passenger = 2
    num = "FL1234"
    fli = ["Airline1"]
    deplo = ["CityA"]
    arrlo = ["CityB"]

    if ans == 1:
        booking.book_by_flight_no(num, passenger, cl)
    elif ans == 2:
        booking.book_by_details(fli[0], deplo[0], arrlo[0], passenger, cl)

    


# DEVELOPED BY AMIRHOSEIN DEZHABDOLLAHI (@amirhoseindzh)
