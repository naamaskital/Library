import unittest
from pathlib import Path
from management.library_manager import LibraryManager
import csv


class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        """
        Method that runs before each test.
        Creates empty test files for books, users, and logs, and initializes the LibraryManager.
        """
        # Define the directory for the test files
        self.test_directory = Path(__file__).parent

        # Define paths for the temporary test files
        self.test_books_file = self.test_directory / "books_test.csv"
        self.test_users_file = self.test_directory / "users_test.csv"
        self.test_log_file = self.test_directory / "logs_test.txt"

        # Create empty files with headers
        self.create_empty_csv(self.test_books_file, ["title", "author", "genre", "year", "copies", "borrowed"])
        self.create_empty_csv(self.test_users_file, ["first_name", "last_name", "username", "password"])
        self.create_empty_file(self.test_log_file)

        # Initialize the library manager with the test files
        self.library_manager = LibraryManager(
            books_file=str(self.test_books_file),
            log_file=str(self.test_log_file),
            users_file=str(self.test_users_file),
        )

    def create_empty_csv(self, file_path, headers):
        """
        Creates an empty CSV file with the specified headers.
        """
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

    def create_empty_file(self, file_path):
        """
        Creates an empty text file.
        """
        with open(file_path, mode='w', encoding='utf-8') as f:
            pass


    def test_add_book_requires_login(self):
        """Test that adding a book returns False if no user is logged in."""
        result = self.library_manager.add_book("Test Book", "Test Author", "Test Genre", 2022, 10)
        self.assertFalse(result)

    def test_remove_book_requires_login(self):
        """Test that removing a book returns False if no user is logged in."""
        result = self.library_manager.remove_book("Test Book")
        self.assertFalse(result)

    def test_return_book_requires_login(self):
        """Test that returning a book returns False if no user is logged in."""
        result = self.library_manager.return_book("Pride and Prejudice")
        self.assertFalse(result)

    def test_get_popular_books_requires_login(self):
        """Test that fetching popular books returns False if no user is logged in."""
        result = self.library_manager.get_popular_books()
        self.assertFalse(result)

    def test_search_books_requires_login(self):
        """Test that searching for books returns False if no user is logged in."""
        result = self.library_manager.search_books({"name": "Test Book"})
        self.assertFalse(result)

    def test_borrow_book_requires_login(self):
        """Test that borrowing a book returns False if no user is logged in."""
        result = self.library_manager.borrow_book("Test Book")
        self.assertFalse(result)

    def test_add_to_waiting_list_requires_login(self):
        """Test that adding to a waiting list returns False if no user is logged in."""
        result = self.library_manager.add_to_waiting_list("Test Book", "test@example.com", "123456789")
        self.assertFalse(result)

    def test_set_filter_requires_login(self):
        """Test that setting a filter returns False if no user is logged in."""
        result = self.library_manager.get_filtered_books("Available")
        self.assertFalse(result)


    def test_login_not_registered(self):
        """Test that logging in with an unregistered user returns False."""
        result = self.library_manager.set_current_user("avi", "111")
        self.assertFalse(result)

    def tearDown(self):
        """
        Method that runs after each test.
        Deletes the temporary test files.
        """
        self.test_books_file.unlink(missing_ok=True)
        self.test_users_file.unlink(missing_ok=True)
        self.test_log_file.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
