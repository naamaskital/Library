class UsernameTakenError(Exception):
    """Exception raised when the username already exists."""
    pass


class FileWriteError(Exception):
    """Exception raised when there is an error writing to the file."""
    pass


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""
    pass

