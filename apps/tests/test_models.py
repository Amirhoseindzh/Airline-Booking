import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from models.db_handler import DatabaseConnector


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
        params = ('test_1',)

        # Simulate an error during query execution
        mock_cursor.execute.side_effect = mysql.connector.Error("fetching error")

        db.fetch_data(query, params)

        # Assert the connect method is called
        mock_connect.assert_called_once()

        # Assert the print function is called with the expected error message
        mock_print.assert_called_with("Error fetching data: fetching error")

        # Assert the disconnect method is called
        mock_disconnect.assert_called_once()






if __name__ == "__main__":
    unittest.main()
