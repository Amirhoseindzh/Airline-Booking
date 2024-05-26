import unittest
from unittest.mock import patch
import bcrypt
from authentication import AuthLogin


class LoginCredentialsTestCase(unittest.TestCase):
    def setUp(self):
        # Patch the DatabaseConnector for each test
        patcher = patch("models.db_handler.DatabaseConnector")
        self.addCleanup(patcher.stop)
        self.MockDatabaseConnector = patcher.start()

        # Mock database connection
        self.mock_db = self.MockDatabaseConnector.return_value
        self.mock_db.connect.return_value = None

        auth = {
            "host": "localhost",
            "user": "user",
            "password": "pass",
            "database": "db",
        }
        self.login = AuthLogin(auth)

    @patch(
        "builtins.input",
        side_effect=[
            "john.doe@example.com",  # email
            "securepassword",  # password
        ],
    )
    def test_prompt_credentional_valid_input(self, mock_input):
        expected_username = ("john.doe@example.com", "securepassword")

        result = self.login.prompt_credentials()
        self.assertEqual(expected_username, result)

    @patch(
        "builtins.input",
        side_effect=[
            "john.doe@example.com",  # email
            123456,  # password
        ],
    )
    def test_prompt_credentional_invalid_input(self, mock_input):
        expected_username = ("john.doe@example.com", "securepassword")

        result = self.login.prompt_credentials()
        self.assertNotEqual(expected_username, result)

    def test_verify_credentials_success(self):
        # Setup mock fetch_data to return user data
        self.mock_db.fetch_data.return_value = [
            {"id": 1, "password": "hashed_password", "salt": "salt"}
        ]

        email = "test@example.com"
        result = self.login.verify_credentials(email)
        self.assertIsNone(result)

    def test_verify_credentials_no_user(self):
        # Setup mock fetch_data to return no results
        self.mock_db.fetch_data.return_value = []

        email = "test@example.com"
        result = self.login.verify_credentials(email)

        self.assertIsNone(result)

    def test_verify_credentials_exception(self):
        # Setup mock fetch_data to raise an exception
        self.mock_db.fetch_data.side_effect = Exception("Database error")

        email = "test@example.com"

        with patch("builtins.print") as mock_print:
            result = self.login.verify_credentials(email)
            # mock_print.assert_any_call("An error occurred while verifying credentials:", 'Database error')

        self.assertIsNone(result)

    def test_verify_credentials_no_connection(self):
        # Simulate no database connection
        self.login.db.connection = None

        email = "test@example.com"

        with patch("builtins.print") as mock_print:
            result = self.login.verify_credentials(email)
            mock_print.assert_any_call("No connection to database.")

        self.assertIsNone(result)


class TestAuthLogin(unittest.TestCase):
    def setUp(self):
        self.auth = {
            "host": "localhost",
            "user": "user",
            "password": "pass",
            "database": "db",
        }
        self.login_instance = AuthLogin(self.auth)

    def test_login_with_invalid_credentials(self):
        # Setup: Mock prompt_credentials to return invalid email and password
        with patch(
            "authentication.AuthLogin.prompt_credentials", return_value=("", "")
        ):
            with patch("builtins.print") as mock_print:
                self.login_instance.login()
                mock_print.assert_called_once_with("Invalid email or password.")

    def test_login_with_no_user_data(self):
        # Setup: Mock prompt_credentials and verify_credentials to simulate no user data
        with patch(
            "authentication.AuthLogin.prompt_credentials",
            return_value=("test@example.com", "password"),
        ):
            with patch(
                "authentication.AuthLogin.verify_credentials", return_value=None
            ):
                with patch("builtins.print") as mock_print:
                    self.login_instance.login()
                    mock_print.assert_called_once_with("\nInvalid email or password.")

    def test_login_success(self):
        # Setup: Mock prompt_credentials and verify_credentials to simulate successful login
        hashed_password = bcrypt.hashpw(
            "password".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        user_data = [{"id": 1, "password": hashed_password, "salt": "salt"}]

        with patch(
            "authentication.AuthLogin.prompt_credentials",
            return_value=("test@example.com", "password"),
        ):
            with patch(
                "authentication.AuthLogin.verify_credentials", return_value=user_data
            ):
                with patch("bcrypt.checkpw", return_value=True):
                    with patch("builtins.print") as mock_print:
                        self.login_instance.login()
                        mock_print.assert_called_once_with("\nLogin successful.")

    def test_login_with_invalid_password(self):
        # Setup: Mock prompt_credentials and verify_credentials to simulate invalid password
        hashed_password = bcrypt.hashpw(
            "password".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        user_data = [{"id": 1, "password": hashed_password, "salt": "salt"}]

        with patch(
            "authentication.AuthLogin.prompt_credentials",
            return_value=("test@example.com", "wrong_password"),
        ):
            with patch(
                "authentication.AuthLogin.verify_credentials", return_value=user_data
            ):
                with patch("bcrypt.checkpw", return_value=False):
                    with patch("builtins.print") as mock_print:
                        self.login_instance.login()
                        mock_print.assert_called_once_with(
                            "\nInvalid email or password."
                        )

    def test_login_authentication_exception(self):
        # Setup: Mock prompt_credentials and verify_credentials to simulate authentication exception
        hashed_password = bcrypt.hashpw(
            "password".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        user_data = [{"id": 1, "password": hashed_password, "salt": "salt"}]

        with patch(
            "authentication.AuthLogin.prompt_credentials",
            return_value=("test@example.com", "password"),
        ):
            with patch(
                "authentication.AuthLogin.verify_credentials", return_value=user_data
            ):
                with patch("bcrypt.checkpw", side_effect=Exception("bcrypt error")):
                    with patch("builtins.print") as mock_print:
                        result = self.login_instance.login()
                        mock_print.assert_called_with(
                            "An error occurred during authentication:", "bcrypt error"
                        )
                        self.assertFalse(result)


class UserRegistrationServiceTestCase(unittest.TestCase):
    """
    TODO: Create a test case for UserRegistration
    first intiate a connection and pass the connection to Table, User, Email
    2nd create a test for register_user method
    3rd create a test for generate_otp
    """


class AuthRegisterTestCase(unittest.TestCase):
    """
    TODO: Create a test for AuthRegister
    first create a mock of user registration service
    2nd create a test for register method
    """
