import csv
import unittest
from pathlib import Path
from management.library_manager import LibraryManager

class TestBooksManagement(unittest.TestCase):
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
        self.assertTrue(self.library_manager.add_user("valid", "user", "valid_user", "valid_password"))

        # Save initial content of files
        self.initial_books_content = self.read_csv_content(self.test_books_file)
        self.initial_log_content = self.read_file_content(self.test_log_file)

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

    def read_file_content(self, file_path):
        """
        Reads and returns the content of a file.
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            return file.read()

    def read_csv_content(self, file_path):
        """
        Reads and returns the content of a CSV file as a list of rows.
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def assert_file_changed_with_expected(self, initial_content, expected_content, file_path, file_type="csv"):
        """
        Assert that the content of a file has changed compared to the initial content and matches the expected content.
        :param initial_content: The original content of the file.
        :param expected_content: The expected content of the file after the operation.
        :param file_path: Path to the file.
        :param file_type: Type of the file ('csv' or 'text').
        """
        if file_type == "csv":
            current_content = self.read_csv_content(file_path)
        else:
            current_content = self.read_file_content(file_path)

        self.assertNotEqual(
            initial_content, current_content,
            f"The content of the file {file_path} has not changed."
        )
        self.assertEqual(
            current_content, expected_content,
            f"The content of the file {file_path} does not match the expected content."
        )

    def test_add_new_book(self):
        """Test that a new book can be added to the library."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        result = self.library_manager.add_book("New Book", "New Author", "Fiction", 2023, 5)
        self.assertTrue(result)

    def test_add_existing_book(self):
        """Test that adding copies to an existing book updates the inventory."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        self.library_manager.add_book("Existing Book", "Author", "Science", 2020, 3)
        result = self.library_manager.add_book("Existing Book", "Author", "Science", 2020, 2)
        self.assertTrue(result)


    def test_add_existing_unavailable_book(self):
        """Test that adding copies to an existing book updates the inventory."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        self.library_manager.add_book("Existing Book", "Author", "History", 2019, 1)
        self.assertTrue(self.library_manager.borrow_book("Existing Book"))
        self.assertFalse(self.library_manager.borrow_book("Existing Book"))
        self.assertTrue(self.library_manager.add_book("Existing Book", "Author", "History", 2019, 1))
        self.assertTrue(self.library_manager.borrow_book("Existing Book"))

    def test_add_existing_book_with_waiting_list(self):
        """Test that adding copies to an existing book updates the inventory."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        self.library_manager.add_book("Existing Book", "Author", "History", 2019, 1)
        self.assertTrue(self.library_manager.borrow_book("Existing Book"))
        self.assertFalse(self.library_manager.borrow_book("Existing Book"))
        self.assertTrue(self.library_manager.add_to_waiting_list("Existing Book","sxac@gmail.com",43132))
        self.assertTrue(self.library_manager.add_book("Existing Book", "Author", "History", 2019, 1))
        self.assertFalse(self.library_manager.borrow_book("Existing Book"))


    def test_remove_book(self):
        """Test that a book can be removed if it is not borrowed."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        self.library_manager.add_book("Removable Book", "Author", "History", 2019, 1)
        result = self.library_manager.remove_book("Removable Book")
        self.assertTrue(result)

    def test_remove_borrowed_book(self):
        """Test that a borrowed book cannot be removed."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        self.library_manager.add_book("Borrowed Book", "Author", "Adventure", 2021, 1)
        self.library_manager.borrow_book("Borrowed Book")
        result = self.library_manager.remove_book("Borrowed Book")
        self.assertFalse(result)

    def test_borrow_book(self):
        """Test that a book can be borrowed if available."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        self.library_manager.add_book("Available Book", "Author", "Fantasy", 2022, 1)
        result = self.library_manager.borrow_book("Available Book")
        self.assertTrue(result)

    def test_borrow_unavailable_book(self):
        """Test that a book cannot be borrowed if it is not available."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        self.library_manager.add_book("Unavailable Book", "Author", "Drama", 2020, 1)
        self.assertTrue(self.library_manager.borrow_book("Unavailable Book"))
        result = self.library_manager.borrow_book("Unavailable Book")
        self.assertFalse(result)
        self.library_manager.add_to_waiting_list("Unavailable Book","sxac@gmail.com",43132)

    def test_return_book(self):
        """Test that a borrowed book can be returned."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        self.library_manager.add_book("Returnable Book", "Author", "Horror", 2021, 1)
        self.library_manager.borrow_book("Returnable Book")
        result = self.library_manager.return_book("Returnable Book")
        self.assertTrue(result)

    def test_return_non_borrowed_book(self):
        """Test that returning a book that is not borrowed fails."""
        self.library_manager.set_current_user("valid_user", "valid_password")  # Login required
        self.library_manager.add_book("Non-Borrowed Book", "Author", "Mystery", 2019, 1)
        result = self.library_manager.return_book("Non-Borrowed Book")
        self.assertFalse(result)

    def test_add_book_invalid_data(self):
        """Test adding a book with invalid data."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        result = self.library_manager.add_book("Invalid Book", "Author", "Genre", "Not a year", 5)
        self.assertFalse(result)

    def test_add_book_zero_copies(self):
        """Test adding a book with zero copies."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        result = self.library_manager.add_book("Zero Copies Book", "Author", "Genre", 2023, 0)
        self.assertTrue(result)
        book = next((b for b in self.library_manager._books if b.get_title() == "Zero Copies Book"), None)
        self.assertIsNotNone(book)
        self.assertFalse(book.is_loaned())

    def test_add_duplicate_to_waiting_list(self):
        """Test adding the same user to the waiting list multiple times."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        self.library_manager.add_book("Waiting List Book", "Author", "Genre", 2023, 1)
        self.library_manager.borrow_book("Waiting List Book")
        self.assertTrue(self.library_manager.add_to_waiting_list("Waiting List Book", "email@example.com", "12345"))
        self.assertFalse(self.library_manager.add_to_waiting_list("Waiting List Book", "email@example.com", "12345"))

    def test_remove_nonexistent_book(self):
        """Test removing a book that does not exist."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        result = self.library_manager.remove_book("Nonexistent Book")
        self.assertFalse(result)

    def test_borrow_nonexistent_book(self):
        """Test borrowing a book that does not exist."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        result = self.library_manager.borrow_book("Nonexistent Book")
        self.assertFalse(result)

    def test_log_write_on_borrow(self):
        """Test that borrowing writes to the log file."""
        self.library_manager.set_current_user("valid_user", "valid_password")
        self.library_manager.add_book("Log Test Book", "Author", "Genre", 2023, 1)
        self.library_manager.borrow_book("Log Test Book")
        log_content = self.read_file_content(self.test_log_file)
        self.assertIn("book borrowed successfully", log_content)

    def test_waiting_list_allocation(self):
        """Test that a book with a waiting list allocates to the next person when a copy becomes available."""
        self.library_manager.set_current_user("valid_user", "valid_password")

        # Add a book with 1 copy
        self.library_manager.add_book("Waiting List Book", "Author", "Genre", 2023, 1)

        # Borrow the only copy
        self.assertTrue(self.library_manager.borrow_book("Waiting List Book"))

        # Add two users to the waiting list
        self.assertTrue(self.library_manager.add_to_waiting_list("Waiting List Book", "email1@example.com", "12345"))
        self.assertTrue(self.library_manager.add_to_waiting_list("Waiting List Book", "email2@example.com", "67890"))

        # Return the borrowed book
        self.assertTrue(self.library_manager.return_book("Waiting List Book"))

        # Check that the first person in the waiting list got the book
        book = next((b for b in self.library_manager._books if b.get_title() == "Waiting List Book"), None)
        self.assertIsNotNone(book)

        # Verify the book is still loaned (allocated to the first person in the waiting list)
        self.assertTrue(book.is_loaned())
        self.assertEqual(len(book.get_waiting_list()), 1)  # Only one person left in the waiting list
        self.assertEqual(book.get_waiting_list()[0]['email'], "email2@example.com")  # Next person is now first in line

    def tearDown(self):
        """
        Method that runs after each test.
        Deletes temporary test files.
        """
        self.test_books_file.unlink(missing_ok=True)
        self.test_users_file.unlink(missing_ok=True)
        self.test_log_file.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
