from abc import ABC, abstractmethod
import logging
from models.db_handler import DatabaseConnector as dbconn, Flight

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
        """TODO: book by flight number """

    def book_by_details(
        self, airline_name, departure, destination, passenger_count, class_no
    ):
        """TODO: book by some input details """

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


# DEVELOPED BY AMIRHOSEIN DEZHABDOLLAHI (@amirhoseindzh)
