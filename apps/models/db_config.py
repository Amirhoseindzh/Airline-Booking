
def get_user_db_auth():
    """Returns the database auth for the given user data if available otherwise None."""
    print("> ENTER THE DATABASE INFORMATIONS  :\n")
    __host = input("HOST NAME :")
    __user = input("USERNAME :")
    __password = input("PASSWORD :")
    __database = input("DATABASE :")

    _db_config = {
        "host": __host,
        "user": __user,
        "password": __password,
        "database": __database, 
    }

    return _db_config
