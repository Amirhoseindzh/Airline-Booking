import mysql.connector


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
                print("Query executed successfully.")
                return data
            else:
                print("No connection to database.")
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            self.disconnect()
