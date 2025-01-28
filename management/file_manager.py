import csv
import json
from pathlib import Path

from book import book
from exceptions import FileWriteError


class FileManager:
    def __init__(self, books_file, users_file, log_file):
        # Initialize FileManager with file paths for books, users, and logs.
        current_path = Path(__file__)
        self._books_directory = current_path.parent.parent / books_file  # Path to the books file.
        self._users_directory = current_path.parent.parent / users_file  # Path to the users file.
        self._logs_directory = current_path.parent.parent / log_file  # Path to the logs file.

        # Ensure the necessary files exist, creating them with headers if required.
        self._ensure_file_exists(self._books_directory, [
            "title", "author", "genre", "year", "copies", "is_loaned", "lendings", "borrowed_books", "waiting_list"
        ])
        self._ensure_file_exists(self._users_directory, [
            "first_name", "last_name", "username", "password"
        ])
        self._ensure_file_exists(self._logs_directory)

    def _ensure_file_exists(self, file_path, fieldnames=None):
        """
        Ensure that the specified file exists. If not, create it and optionally write headers.
        :param file_path: Path to the file.
        :param fieldnames: Optional list of headers for CSV files.
        """
        if not file_path.exists():
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    if fieldnames:
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()  # Write headers if provided.
            except Exception as e:
                print(f"Failed to create file {file_path}: {e}")

    def _load_books(self):
        """
        Load books from the books file into a list of Book objects.
        :return: List of Book objects.
        """
        books = []
        try:
            with open(self._books_directory, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    books.append(book.Book.create_book_from_row(row))  # Convert row data to Book object.
        except Exception as e:
            pass  # Ignore errors while loading books.
        return books

    def save_books(self, books):
        """
        Save the current list of books to the books file.
        :param books: List of Book objects to save.
        """
        with open(self._books_directory, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["title", "author", "genre", "year", "copies", "is_loaned", "lendings", "borrowed_books",
                          "waiting_list"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row.
            for book in books:
                writer.writerow({
                    "title": book.get_title(),
                    "author": book.get_author(),
                    "genre": book.get_genre(),
                    "year": book.get_year(),
                    "copies": book.get_copies(),
                    "is_loaned": "Yes" if book.is_loaned() else "No",  # Convert boolean to string.
                    "lendings": book.get_lendings(),
                    "borrowed_books": book.get_borrowed_books(),
                    "waiting_list": json.dumps(book.get_waiting_list())  # Serialize the waiting list as JSON.
                })

    def add_user(self, new_user, fieldnames):
        """
        Add a new user to the users file.
        :param new_user: The user object containing user details.
        :param fieldnames: List of field names for the users file.
        """
        try:
            with open(self._users_directory, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write headers only if the file is empty.
                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow({
                    'first_name': new_user.get_first_name(),
                    'last_name': new_user.get_last_name(),
                    'username': new_user.get_username(),
                    'password': new_user.get_password() if isinstance(new_user.get_password(), bytes) else new_user.get_password(),
                })
        except Exception as e:
            raise FileWriteError(f"Failed to write user '{new_user.get_username()}': {e}")

    def write_log(self, message):
        """
        Write a log message to the log file.
        :param message: The message to log.
        """
        try:
            with open(self._logs_directory, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{message}\n")  # Append the message to the log file.
        except Exception as e:
            print(f"Error writing to log file: {e}")
