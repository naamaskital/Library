import csv
import unittest
from pathlib import Path
from management.library_manager import LibraryManager

class TestSearchAndFilter(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment: Create test files and initialize the LibraryManager.
        """
        self.test_directory = Path(__file__).parent
        self.test_books_file = self.test_directory / "books_test.csv"
        self.test_users_file = self.test_directory / "users_test.csv"
        self.test_log_file = self.test_directory / "logs_test.txt"

        # Create test files
        self.create_empty_csv(self.test_books_file, ["title", "author", "genre", "year", "copies", "borrowed"])
        self.create_empty_csv(self.test_users_file, ["first_name", "last_name", "username", "password"])
        self.create_empty_file(self.test_log_file)

        # Initialize LibraryManager
        self.library_manager = LibraryManager(
            books_file=str(self.test_books_file),
            log_file=str(self.test_log_file),
            users_file=str(self.test_users_file),
        )
        # Add test user and login
        self.library_manager.add_user("test", "user", "test_user", "password")
        self.library_manager.set_current_user("test_user", "password")

        # Add a variety of books
        self.library_manager.add_book("Harry Potter", "J.K. Rowling", "Fantasy", 2000, 1)
        self.library_manager.add_book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, 2)
        self.library_manager.add_book("1984", "George Orwell", "Dystopian", 1949, 2)
        self.library_manager.add_book("A Tale of Two Cities", "Charles Dickens", "Classic", 1859, 4)
        self.library_manager.add_book("Pride and Prejudice", "Jane Austen", "Romance", 1813, 6)
        self.library_manager.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, 3)
        self.library_manager.add_book("Crime and Punishment", "Fyodor Dostoevsky", "Classic", 1866, 2)
        self.library_manager.add_book("Catch-22", "Joseph Heller", "Satire", 1961, 3)


    def create_empty_csv(self, file_path, headers):
        """Create an empty CSV file with the given headers."""
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

    def create_empty_file(self, file_path):
        """Create an empty text file."""
        with open(file_path, mode='w', encoding='utf-8') as f:
            pass

    # Single Parameter Tests
    def test_search_by_name_full_match(self):
        """Search for a book by its full name."""
        results = self.library_manager.search_books({"name": "Harry Potter"})
        self.assertEqual(len(results), 1)
        self.assertEqual(next(iter(results)).get_title(), "Harry Potter")

    def test_search_by_name_partial(self):
        """Search for books by partial name."""
        results = self.library_manager.search_books({"name": "The"})
        result_titles = [book.get_title() for book in results]
        expected_titles = ["The Hobbit", "The Great Gatsby"]
        self.assertEqual(set(result_titles), set(expected_titles))

    def test_search_by_author_full_match(self):
        """Search for books by full author name."""
        results = self.library_manager.search_books({"author": "George Orwell"})
        self.assertEqual(len(results), 1)
        self.assertEqual(next(iter(results)).get_author(), "George Orwell")

    def test_search_by_genre_partial(self):
        """Search for books by partial genre."""
        results = self.library_manager.search_books({"genre": "Fan"})
        result_titles = [book.get_title() for book in results]
        expected_titles = ["Harry Potter", "The Hobbit"]
        self.assertEqual(set(result_titles), set(expected_titles))

    # Multi-Parameter Tests
    def test_search_by_name_and_genre(self):
        """Search for books by partial name and genre."""
        results = self.library_manager.search_books({"name": "Great", "genre": "Classic"})
        self.assertEqual(len(results), 1)
        self.assertEqual(next(iter(results)).get_title(), "The Great Gatsby")

    def test_search_by_author_and_genre(self):
        """Search for books by author and genre."""
        results = self.library_manager.search_books({"author": "Jane Austen", "genre": "Romance"})
        self.assertEqual(len(results), 1)
        self.assertEqual(next(iter(results)).get_title(), "Pride and Prejudice")

    def test_search_by_three_criteria(self):
        """Search for books by name, author, and genre."""
        results = self.library_manager.search_books({"name": "1984", "author": "George Orwell", "genre": "Dystopian"})
        self.assertEqual(len(results), 1)
        self.assertEqual(next(iter(results)).get_title(), "1984")

    # No Results Test
    def test_search_no_results(self):
        """Search for books with no matching criteria."""
        results = self.library_manager.search_books({"name": "Nonexistent", "genre": "Unknown"})
        self.assertFalse(results)

    # Large Result Sets
    def test_search_multiple_results(self):
        """Search for books with a common criterion that returns multiple results."""
        results = self.library_manager.search_books({"genre": "Classic"})
        result_titles = [book.get_title() for book in results]
        expected_titles = [
            "A Tale of Two Cities",
            "The Great Gatsby",
            "Crime and Punishment"
        ]
        self.assertEqual(set(result_titles), set(expected_titles))

    def test_set_filter_all(self):
        """Test filtering to show all books."""
        iterator = self.library_manager.get_filtered_books("All")
        results = [book.get_title() for book in iterator]
        expected_titles = [
            "Harry Potter",
            "The Hobbit",
            "1984",
            "A Tale of Two Cities",
            "Pride and Prejudice",
            "The Great Gatsby",
            "Crime and Punishment",
            "Catch-22",
        ]
        self.assertEqual(set(results), set(expected_titles))

    def test_set_filter_available(self):
        """Test filtering to show only available books."""
        # Borrow one copy of "Harry Potter"
        self.library_manager.borrow_book("Harry Potter")
        iterator = self.library_manager.get_filtered_books("Available")
        results = [book.get_title() for book in iterator]
        expected_titles = [
            "The Hobbit",
            "1984",
            "A Tale of Two Cities",
            "Pride and Prejudice",
            "The Great Gatsby",
            "Crime and Punishment",
            "Catch-22",
        ]
        self.assertEqual(set(results), set(expected_titles))

    def test_set_filter_unavailable(self):
        """Test filtering to show only unavailable books."""
        # Borrow all copies of "Harry Potter"
        self.library_manager.borrow_book("Harry Potter")
        self.library_manager.borrow_book("Harry Potter")

        iterator = self.library_manager.get_filtered_books("Unavailable")
        results = [book.get_title() for book in iterator]

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "Harry Potter")

    def test_set_filter_by_genre(self):
        """Test filtering books by genre."""
        iterator = self.library_manager.get_filtered_books("Classic")
        results = [book.get_title() for book in iterator]
        expected_titles = [
            "A Tale of Two Cities",
            "The Great Gatsby",
            "Crime and Punishment",
        ]
        self.assertEqual(set(results), set(expected_titles))

    def test_set_filter_by_nonexistent_genre(self):
        """Test filtering books by a genre that does not exist."""
        iterator = self.library_manager.get_filtered_books("Nonexistent Genre")
        self.assertIsNone(iterator)  # Check if iterator is None

    def test_set_filter_after_borrow_and_return(self):
        """Test filtering books after borrowing and returning a book."""
        # Borrow all copies of "The Hobbit"
        self.library_manager.borrow_book("The Hobbit")
        self.library_manager.borrow_book("The Hobbit")

        # Check "Unavailable" filter
        iterator = self.library_manager.get_filtered_books("Unavailable")
        results = [book.get_title() for book in iterator]
        self.assertIn("The Hobbit", results)

        # Return one copy
        self.library_manager.return_book("The Hobbit")
        iterator = self.library_manager.get_filtered_books("Available")
        results = [book.get_title() for book in iterator]
        self.assertIn("The Hobbit", results)

    def tearDown(self):
        """Clean up test files after each test."""
        self.test_books_file.unlink(missing_ok=True)
        self.test_users_file.unlink(missing_ok=True)
        self.test_log_file.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
