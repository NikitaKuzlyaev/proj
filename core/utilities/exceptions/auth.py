

class PasswordDoesNotMatch(Exception):
    """
    Throw an exception when the account password does not match the entitiy's hashed password from the database.
    """

class TokenException(Exception):
    """

    """

class InvalidToken(TokenException):
    """

    """


class ExpiredToken(TokenException):
    """

    """


class UndecodedToken(TokenException):
    """

    """