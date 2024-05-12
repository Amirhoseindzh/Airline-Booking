
def email_validator(email):
    """this function is used to validate email address"""
    pass


def check_email_exists(func):
    """this decorator function is used to check email address exists"""
    def wrapper(self, email):
        result = self.fetch_data(
            "SELECT COUNT(*) FROM customers WHERE email = %s", (email,)
        )
        if result is not None and len(result) > 0 and result[0]["COUNT(*)"] > 0:
            print("Email address already in use")
            return True
        else:
            return func(self, email)

    return wrapper
