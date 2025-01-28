from pathlib import Path
import bcrypt
import csv
import os
from exceptions import UsernameTakenError, UserNotFoundError
from user.librarian import Librarian


def hash_password(func):
    """
    Decorator to hash the password before calling the function.
    """
    def wrapper(self, *args, **kwargs):
        # If 'password' is in kwargs, hash it before passing to the function.
        if 'password' in kwargs:
            kwargs['password'] = self._hash_password(kwargs['password'])
        result = func(self, *args, **kwargs)
        return result
    return wrapper


class LibrarianManager:
    def __init__(self, data_file, file_manager):
        # Initialize LibrarianManager with a data file and file manager.
        current_directory = Path(__file__)
        self._data_file = current_directory.parent.parent / data_file  # Path to the data file.
        self._file_manager = file_manager  # Reference to the FileManager object.
        self._fieldnames = ['first_name', 'last_name', 'username', 'password']  # CSV field names.
        self._observers = self._load_users()  # Load existing users into the system.
        self.salt = b'$2b$12$UwvIkfpYveGnZ3XKXf28w.'  # Salt used for password hashing.

        # Create the data file if it doesn't exist and write headers.
        if not os.path.exists(self._data_file):
            with open(self._data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self._fieldnames)
                writer.writeheader()

    def notify_observers(self, notification):
        """
        Notify all observers (librarians) with the given notification.
        :param notification: The message to notify users with.
        """
        for observer in self._observers:
            observer.update(notification)

    def _hash_password(self, password):
        """
        Hash a password with the predefined salt.
        :param password: The plaintext password to hash.
        :return: The hashed password.
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        return hashed_password

    def _check_password(self, stored_hashed_password, entered_password):
        """
        Compare the entered password with the stored hashed password.
        :param stored_hashed_password: The stored hash of the password.
        :param entered_password: The plaintext password entered by the user.
        :return: True if the passwords match, otherwise False.
        """
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password)

    @hash_password
    def add_user(self, **user_data):
        """
        Add a new librarian to the system.
        :param user_data: A dictionary containing the librarian's details.
        """
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        username = user_data['username']
        password = user_data['password'].decode('utf-8')  # Decode the hashed password.

        # Check if the username already exists.
        if any(user.get_username() == username for user in self._observers):
            raise UsernameTakenError(f"Username '{username}' already exists. Registration failed.")

        # Create a new librarian and add them to the system.
        new_librarian = Librarian(first_name, last_name, username, password)
        self._file_manager.add_user(new_librarian, self._fieldnames)  # Save the librarian to the file.
        self._observers.append(new_librarian)  # Add the librarian to the list of observers.

    def _load_users(self):
        """
        Load all users from the data file.
        :return: A list of Librarian objects.
        """
        users = []
        try:
            with open(self._data_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = Librarian(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        username=row['username'],
                        password=row['password']  # The hashed password from the file.
                    )
                    users.append(user)
        except Exception as e:
            print(f"Error loading users: {e}")
        return users

    @hash_password
    def check_user(self, **dict):
        """
        Check if a user exists in the system.
        :param dict: A dictionary containing 'username' and 'password'.
        :return: The Librarian object if the user exists and the password matches.
        :raises UserNotFoundError: If the user is not found.
        """
        username = dict['username']
        password = dict['password']

        for librarian in self._observers:
            if librarian.get_username() == username:
                # Compare the entered password with the stored hashed password.
                if str(librarian.get_password()) == str(password.decode('utf-8')):
                    return librarian

        # Raise an error if the user is not found.
        raise UserNotFoundError(f"User '{username}' not found.")
