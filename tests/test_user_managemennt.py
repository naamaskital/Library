import unittest
from pathlib import Path
from management.library_manager import LibraryManager
import csv


class MyTestCase(unittest.TestCase):
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

    def read_csv(self, file_path):
        """
        Reads the content of a CSV file and returns a list of rows as dictionaries.
        """
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def test_register_with_the_same_username(self):
        """Test that registering a user with the same username fails."""
        # Register the first user - should succeed
        self.assertTrue(self.library_manager.add_user("yon", "levi", "username", "111"))

        # Verify that the user exists in the file
        users = self.read_csv(self.test_users_file)
        expected_user = {"first_name": "yon", "last_name": "levi", "username": "username"}
        for user in users:
            user.pop("password", None)  # Remove the password from comparison
        self.assertIn(expected_user, users)

        # Attempt to register another user with the same username - should fail
        self.assertFalse(self.library_manager.add_user("dan", "chen", "username", "432a"))

        # Ensure the second user was not added
        users = self.read_csv(self.test_users_file)
        usernames = [user['username'] for user in users]
        self.assertEqual(usernames.count("username"), 1)



    def test_login_logout(self):
        """Test the login and logout functionality."""
        # Add a valid user
        self.assertTrue(self.library_manager.add_user("valid", "user", "valid_user", "valid_password"))

        # Login with valid user credentials
        self.assertTrue(self.library_manager.set_current_user("valid_user", "valid_password"))

        # Verify that the log file is updated
        with open(self.test_log_file, 'r', encoding='utf-8') as log_file:
            logs = log_file.read()
        self.assertIn("logged in successfully", logs)

        # Logout
        self.assertTrue(self.library_manager.log_out())

        # Verify that the log file is updated with the logout
        with open(self.test_log_file, 'r', encoding='utf-8') as log_file:
            logs = log_file.read()
        self.assertIn("log out successful", logs)

        # Attempt to login with invalid user credentials
        self.assertFalse(self.library_manager.set_current_user("invalid_user", "wrong_password"))
        with open(self.test_log_file, 'r', encoding='utf-8') as log_file:
            logs = log_file.read()
        self.assertIn("logged in fail", logs)

    def tearDown(self):
        """
        Method that runs after each test.
        Deletes the temporary test files.
        """
        self.test_books_file.unlink(missing_ok=True)
        self.test_users_file.unlink(missing_ok=True)
        self.test_log_file.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
