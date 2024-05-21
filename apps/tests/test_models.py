import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from models.db_handler import DatabaseConnector, Table, Email, User


class DatabaseConnectTestCase(unittest.TestCase):
    @patch("mysql.connector.connect")
    def test_connect_success(self, mock_connect):
        # Setup the mock to simulate successful connection
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        db = DatabaseConnector(
            host="localhost", user="root", password="password", database="test_db"
        )
        db.connect()

        # Assert connect was called with correct parameters
        mock_connect.assert_called_with(
            host="localhost", user="root", password="password", database="test_db"
        )

        # Assert the connection and cursor are set correctly
        self.assertIsNotNone(db.connection)
        self.assertIsNotNone(db.cursor)

    @patch("mysql.connector.connect")
    @patch("builtins.print")  # Mock the print function
    def test_connect_failure(self, mock_print, mock_connect):
        # Setup the mock to simulate a connection failure
        mock_connect.side_effect = mysql.connector.Error("Connection error")

        db = DatabaseConnector(
            host="localhost", user="root", password="password", database="test_db"
        )

        db.connect()

        # Check if the print function was called with the expected error message
        mock_print.assert_called_with("Error connecting to database: Connection error")


class DatabaseDisconnectTestCase(unittest.TestCase):
    def test_disconnect(self):
        db = DatabaseConnector(
            host="localhost", user="root", password="password", database="test_db"
        )

        # Create mock objects for connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()

        # Assign mock objects to the instance
        db.cursor = mock_cursor
        db.connection = mock_connection

        db.disconnect()
        # Assert cursor.close() and connection.close() is called
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


class ExecuteQueryTestCase(unittest.TestCase):
    @patch.object(DatabaseConnector, "connect")
    @patch.object(DatabaseConnector, "disconnect")
    def test_execute_query_success(self, mock_disconnect, mock_connect):
        db = DatabaseConnector(
            host="localhost", user="root", password="password", database="test_db"
        )

        # Create mock objects for connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()

        # Assign mock objects to the instance
        db.cursor = mock_cursor
        db.connection = mock_connection

        query = "SELECT * FROM test WHERE id= %s"
        params = (1,)

        db.execute_query(query, params)

        # Assert connect method is called
        mock_connect.assert_called_once()

        # Assert cursor.execute() and connection.commit() are called
        mock_cursor.execute.assert_called_once_with(query, params)
        mock_connection.commit.assert_called_once()

        # Assert the Disconnect method is called
        mock_disconnect.assert_called_once()

    @patch.object(DatabaseConnector, "connect")
    @patch.object(DatabaseConnector, "disconnect")
    @patch("builtins.print")  # Mock the print function
    def test_execute_query_failure(self, mock_print, mock_disconnect, mock_connect):
        db = DatabaseConnector(
            host="localhost", user="root", password="password", database="test_db"
        )

        # Simulate connection success
        mock_connect.side_effect = None

        # Create mock objects for connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()

        # Assign mock objects to the instance
        db.cursor = mock_cursor
        db.connection = mock_connection

        query = "SELECT * FROM users WHERE id = %s"
        params = (1,)

        # Simulate an error during query execution
        mock_cursor.execute.side_effect = mysql.connector.Error("Execution error")

        db.execute_query(query, params)

        # Assert the connect method is called
        mock_connect.assert_called_once()

        # Assert the print function is called with the expected error message
        mock_print.assert_called_with("Error executing query: Execution error")

        # Assert the disconnect method is called
        mock_disconnect.assert_called_once()


class FetchDataTestCase(unittest.TestCase):
    @patch.object(DatabaseConnector, "connect")
    @patch.object(DatabaseConnector, "disconnect")
    def test_fetch_data_success(self, mock_disconnect, mock_connect):
        db = DatabaseConnector(
            host="localhost", user="root", password="password", database="test_db"
        )

        # Create mock objects for connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()

        # Assign mock objects to the instance
        db.cursor = mock_cursor
        db.connection = mock_connection

        query = "SELECT * FROM test WHERE id= %s"
        params = (1,)

        db.fetch_data(query, params)

        # Assert connect method is called
        mock_connect.assert_called_once()

        # Assert cursor.execute() and connection.commit() are called
        mock_cursor.execute.assert_called_once_with(query, params)
        mock_cursor.fetchall.assert_called_once()

        # Assert the Disconnect method is called
        mock_disconnect.assert_called_once()

    @patch.object(DatabaseConnector, "connect")
    @patch.object(DatabaseConnector, "disconnect")
    @patch("builtins.print")  # Mock the print function
    def test_fetch_data_failure(self, mock_print, mock_disconnect, mock_connect):
        db = DatabaseConnector(
            host="localhost", user="root", password="password", database="test_db"
        )

        # Simulate connection success
        mock_connect.side_effect = None

        # Create mock objects for connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()

        # Assign mock objects to the instance
        db.cursor = mock_cursor
        db.connection = mock_connection

        query = "SHOW TABLES LIKE %s"
        params = ("test_1",)

        # Simulate an error during query execution
        mock_cursor.execute.side_effect = mysql.connector.Error("fetching error")

        db.fetch_data(query, params)

        # Assert the connect method is called
        mock_connect.assert_called_once()

        # Assert the print function is called with the expected error message
        mock_print.assert_called_with("Error fetching data: fetching error")

        # Assert the disconnect method is called
        mock_disconnect.assert_called_once()


class TableTestCase(unittest.TestCase):
    def setUp(self):
        self.table = Table(
            host="localhost", user="root", password="password", database="test_db"
        )
        self.maxDiff = None  # Set maxDiff to None to see full diffs

    @patch.object(Table, "fetch_data")
    def test_table_exists_true(self, mock_fetch_data):
        # mock the fetch_data method to return empty results
        mock_fetch_data.return_value = [("example_table")]

        self.assertTrue(self.table.table_exists("non_existant_table"))

    @patch.object(Table, "fetch_data")
    def test_table_exists_false(self, mock_fetch_data):
        mock_fetch_data.return_value = []

        self.assertFalse(self.table.table_exists("example_table"))

    @patch.object(Table, "fetch_data")
    def test_table_exists_exception(self, mock_fetch_data):
        # Mock the fetch_data method to raise an exception
        mock_fetch_data.side_effect = Exception("Database error")

        # Assert that table_exists returns False
        self.assertFalse(self.table.table_exists("example_table"))

    @patch.object(Table, "execute_query")
    def test_create_customer_table_success(self, mock_execute_query):
        # Mock execute_query to simulate a successful table creation
        # Normally no return value for a successful CREATE TABLE 
        mock_execute_query.return_value = (None)

        with self.assertLogs(level="INFO") as log:
            # Call the create_customers_table method
            self.table.create_customers_table()

            # Assert that execute_query was called once
            mock_execute_query.assert_called_once()

            # Check the log output for the success message
            self.assertIn("Customers table created successfully.", log.output[0])

    @patch.object(Table, "execute_query")
    def test_create_customers_table_failure(self, mock_execute_query):
        # Mock execute_query to raise an exception
        mock_execute_query.side_effect = Exception("Database error")

        # Call the create_customers_table method
        with self.assertLogs(level="ERROR") as log:
            # Call the create_customers_table method
            self.table.create_customers_table()

        # Assert that execute_query was called once
        mock_execute_query.assert_called_once()

        # Check the log output for the error message
        self.assertIn("Error creating customers table:", log.output[0])
        self.assertIn("Database error", log.output[0])


class EmailTestCase(unittest.TestCase):
    def setUp(self):
        self.email = Email(
            host="localhost", user="root", password="password", database="test_db"
        )

    @patch.object(Email, "fetch_data")
    def test_email_exists_true(self, mock_fetch_data):
        mock_fetch_data.return_value = [("example@example.com")]

        self.assertTrue(self.email.email_exists("non_existent_email"))

    @patch.object(Email, "fetch_data")
    def test_email_exists_false(self, mock_fetch_data):
        mock_fetch_data.return_value = []

        self.assertFalse(self.email.email_exists("example@example.com"))

    @patch.object(Email, "fetch_data")
    def test_email_exists_exception(self, mock_fetch_data):
        # Mock the fetch_data method to raise an exception
        mock_fetch_data.side_effect = Exception("Database error")

        # Assert that table_exists returns False
        self.assertFalse(self.email.email_exists("example@example.com"))


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User(
            host='localhost', user='username', password='password', database='database'
        )

    @patch.object(User, 'execute_query')    
    def test_insert_user_success(self, mock_execute_query):
        mock_execute_query.return_value = (None)
         
        params = 'fullname','email', 'phone_no', 'city', 'state', 'hashed_password', 'salt', 'otp'
        self.user.insert_user(*params)

        mock_execute_query.assert_called_once()
    
    @patch.object(User, 'execute_query')
    def test_insert_user_failure(self, mock_execute_query):
        mock_execute_query.side_effect = Exception('database error')
        params = 'fullname','email', 'phone_no', 'city', 'state', 'hashed_password', 'salt', 'otp'

        # Call the create_customers_table method
        with self.assertLogs(level="ERROR") as log:
            # Call the create_customers_table method
            self.user.insert_user(*params)

        # Assert that execute_query was called once
        mock_execute_query.assert_called_once()

        # Check the log output for the error message
        self.assertIn("Failed to insert user data into database", log.output[0])


if __name__ == "__main__":
    unittest.main()
