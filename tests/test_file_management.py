import unittest
import csv
from pathlib import Path
from management.file_manager import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        """
        Set up temporary test files and initialize the FileManager.
        Creates separate files for books, users, and logs to test functionality.
        """
        self.test_directory = Path(__file__).parent
        self.books_file = self.test_directory / "test_books.csv"
        self.users_file = self.test_directory / "test_users.csv"
        self.log_file = self.test_directory / "test_logs.txt"

        # Initialize FileManager
        self.file_manager = FileManager(
            books_file=str(self.books_file),
            users_file=str(self.users_file),
            log_file=str(self.log_file),
        )

    def test_ensure_file_exists(self):
        """
        Test that FileManager creates files if they do not exist.
        Ensures that all necessary files are present and structured correctly.
        """
        # Ensure files are created
        self.assertTrue(self.books_file.exists())
        self.assertTrue(self.users_file.exists())
        self.assertTrue(self.log_file.exists())

        # Check headers in books file
        with open(self.books_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            expected_headers = [
                "title", "author", "genre", "year", "copies", "is_loaned", "lendings", "borrowed_books", "waiting_list"
            ]
            self.assertEqual(headers, expected_headers)

    def test_save_and_load_books(self):
        """
        Test saving and loading books.
        Ensures books can be written to and read from the file without data loss.
        """
        # Create mock books
        books = [
            MockBook("Book 1", "Author 1", "Genre 1", 2020, 2),
            MockBook("Book 2", "Author 2", "Genre 2", 2021, 1),
        ]
        self.file_manager.save_books(books)

        # Load books and check equality
        loaded_books = self.file_manager._load_books()
        self.assertEqual(len(loaded_books), 2)
        self.assertEqual(loaded_books[0].get_title(), "Book 1")
        self.assertEqual(loaded_books[1].get_title(), "Book 2")

    def test_add_user(self):
        """
        Test adding a user to the users file.
        Verifies that user data is correctly appended to the file.
        """
        # Mock user
        mock_user = MockUser("John", "Doe", "johndoe", "password")
        fieldnames = ["first_name", "last_name", "username", "password"]
        self.file_manager.add_user(mock_user, fieldnames)

        # Check user in file
        with open(self.users_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users = list(reader)
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0]["username"], "johndoe")

    def test_write_log(self):
        """
        Test writing to the log file.
        Ensures log messages are correctly written to the log file.
        """
        self.file_manager.write_log("Test log message")
        with open(self.log_file, mode='r', encoding='utf-8') as file:
            logs = file.read().strip()
        self.assertEqual(logs, "Test log message")

    def tearDown(self):
        """
        Clean up test files.
        Deletes temporary files created during testing to ensure a clean environment.
        """
        for file in [self.books_file, self.users_file, self.log_file]:
            if file.exists():
                file.unlink()

class MockBook:
    """
    Mock book class for testing.
    Simulates the behavior of a book object with basic attributes and methods.
    """
    def __init__(self, title, author, genre, year, copies):
        self._title = title
        self._author = author
        self._genre = genre
        self._year = year
        self._copies = copies

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def get_genre(self):
        return self._genre

    def get_year(self):
        return self._year

    def get_copies(self):
        return self._copies

    def is_loaned(self):
        return False

    def get_lendings(self):
        return 0

    def get_borrowed_books(self):
        return 0

    def get_waiting_list(self):
        return []

class MockUser:
    """
    Mock user class for testing.
    Simulates the behavior of a user object with basic attributes and methods.
    """
    def __init__(self, first_name, last_name, username, password):
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._password = password

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

if __name__ == "__main__":
    unittest.main()
