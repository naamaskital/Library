from book import search_book, book
from book.book import Book
from book.book_iterator import BookIterator, PopularBooksIterator
from exceptions import UserNotFoundError, UsernameTakenError
from management.file_manager import FileManager
from management.librarian_manager import LibrarianManager

def requires_login(func):
    """
    Decorator to ensure the user is logged in before executing the function.
    """
    def wrapper(self, *args, **kwargs):
        if self._current_user is not None:
            return func(self, *args, **kwargs)
        else:
            return False
    return wrapper


class LibraryManager:
    def __init__(self, books_file, log_file, users_file):
        # Initialize the library manager with file paths for books, logs, and users.
        self._file_manager = FileManager(books_file, users_file, log_file)  # File manager for file operations.
        self._log_file = log_file  # Log file path.
        self._books = self._file_manager._load_books()  # Load books from the file.
        self._log_file = log_file  # Log file path (duplicate assignment).
        self._librarian_manager = LibrarianManager(users_file, self._file_manager)  # Librarian manager for user handling.
        self._current_user = None  # Initially, no user is logged in.
        self.is_logged_in = False  # Login status.
        self._current_books = self._books  # List of currently active books (filtered or unfiltered).

    def set_current_user(self, user_name, password):
        """
        Set the currently logged-in user.
        """
        try:
            if self.is_logged_in is False:
                user = self._librarian_manager.check_user(**{'username': user_name, 'password': password})
                if self._current_user is not None:
                    self._current_user.deactivate()
                self._current_user = user
                self._file_manager.write_log("logged in successfully")
                self._current_user.activate()
                self.is_logged_in = True
                return True
            else:
                self._file_manager.write_log("logged in fail")
                return False
        except UserNotFoundError as e:
            self._file_manager.write_log("logged in fail")
            return False
        except Exception as e:
            return False

    @requires_login
    def log_out(self):
        """
        Log out the currently logged-in user.
        """
        if self.is_logged_in:
            self._current_user.deactivate()
            self.is_logged_in = False
            self._file_manager.write_log("log out successful")
            return True
        self._file_manager.write_log("log out fail")
        return False

    def add_user(self, first_name, last_name, username, password):
        """
        Add a new user to the system.
        """
        try:
            self._librarian_manager.add_user(**{'first_name': first_name, 'last_name': last_name, 'username': username, 'password': password})
            self._file_manager.write_log("registered successfully")
            return True
        except UsernameTakenError as e:
            self._file_manager.write_log("registered fail")
            return False
        except Exception as e:
            return False

    @requires_login
    def return_book(self, book_title):
        """
        Return a borrowed book to the library.
        """
        try:
            for book in self._books:
                if book.get_title() == book_title:
                    if book.has_borrowed_books():
                        i = book.sub_borrowed_books(1, self._librarian_manager)
                        self._file_manager.write_log("book returned successfully")
                        if i > 0:
                            self._file_manager.write_log("book borrowed successfully")
                        self._file_manager.save_books(self._books)
                        return True
                    else:
                        self._file_manager.write_log("book returned fail")
                        return False
            return False
        except Exception as e:
            return False

    @requires_login
    def add_book(self, title, author, genre, year, copies):
        """
        Add a new book to the library or update an existing book.
        """
        try:
            year = int(year)  # Ensure year is an integer.
            copies = int(copies)  # Ensure copies is an integer.
            existing_book = next((book for book in self._books if book.get_title() == title ), None)
            if existing_book:
                num = existing_book.add_copies(copies, self._librarian_manager)
                self._file_manager.write_log("book added successfully")
                for i in range(num):
                    self._file_manager.write_log("book borrowed successfully")
                self._file_manager.save_books(self._books)
                return True
            else:
                new_book = Book(title, author, genre, year, copies)
                self._books.append(new_book)
                self._file_manager.write_log("book added successfully")
                self._file_manager.save_books(self._books)
                return True
        except Exception as e:
            return False

    @requires_login
    def remove_book(self, title):
        """
        Remove a book from the library if it is not currently borrowed.
        """
        try:
            existing_book = next((book for book in self._books if book.get_title() == title), None)
            if existing_book:
                if existing_book.has_borrowed_books():
                    self._file_manager.write_log("book removed fail")
                    return False
                else:
                    self._books.remove(existing_book)
                    self._file_manager.save_books(self._books)
                    self._file_manager.write_log("book removed successfully")
                    return True
            else:
                self._file_manager.write_log("book removed fail")
                return False
        except Exception as e:
            return False

    @requires_login
    def get_popular_books(self):
        """
        Get an iterator for the most popular books in the library.
        """
        try:
            if self._books==[]:
                self._file_manager.write_log("displayed fail")
                return []
            popular_books_iterator = PopularBooksIterator(self._books)
            self._file_manager.write_log("displayed successfully")
            return popular_books_iterator
        except Exception as e:
            return []

    @requires_login
    def search_books(self, criteria):
        """
        Search for books in the library based on specific criteria.
        """
        name, author, genre = "", "", ""
        search_all_books = set(self._books)  # Start with all books.
        try:
            for field, sub_string in criteria.items():
                if field == 'name':
                    search_all_books &= set(search_book.SearchByName.search(sub_string, self._books))
                    name = sub_string
                elif field == 'author':
                    search_all_books &= set(search_book.SearchByAuthor.search(sub_string, self._books))
                    author = sub_string
                elif field == 'genre':
                    search_all_books &= set(search_book.SearchByGenre.search(sub_string, self._books))
                    genre = sub_string
            if(len(search_all_books) > 0):
                if name != "":
                    self._file_manager.write_log(f"search book '{name}' by name completed successfully")
                if author != "":
                    self._file_manager.write_log(f"search book '{author}' by author name completed successfully")
                if genre != "":
                    self._file_manager.write_log(f"search book '{genre}' by genre completed successfully")
                return search_all_books
            raise Exception
        except Exception as e:
            if name!="":
                self._file_manager.write_log(f"search book '{name}' by name completed fail")
            if author!="":
                self._file_manager.write_log(f"search book '{author}' by author name completed fail")
            if genre!="":
                self._file_manager.write_log(f"search book '{genre}' by genre completed fail")
            return None

    @requires_login
    def borrow_book(self, book_title):
        """
        Borrow a book from the library.
        """
        try:
            for book in self._books:
                if book.get_title() == book_title:
                    if book.is_loaned():
                        self._file_manager.write_log("book borrowed fail")
                        return False
                    else:
                        book.add_borrowed_books(1)
                        self._file_manager.save_books(self._books)
                        self._file_manager.write_log("book borrowed successfully")
                        return True
        except Exception as e:
            return False

    @requires_login
    def add_to_waiting_list(self, book_title, email, phone_number):
        """
        Add a user to the waiting list for a book.
        """
        try:
            for book in self._books:
                if book.get_title() == book_title:
                    if book.add_to_waiting_list(email, phone_number):
                        self._file_manager.save_books(self._books)
                        return True
            return False
        except Exception as e:
            return False

    @requires_login
    def get_filtered_books(self, filter_type="All"):
        """
        Get an iterator for books based on a filter type.
        """
        current_books=[]
        try:
            if filter_type == "All":
                current_books = self._books
            elif filter_type == "Available":
                current_books = [book for book in self._books if not book.is_loaned()]
            elif filter_type == "Unavailable":
                current_books = [book for book in self._books if book.is_loaned()]
            elif filter_type in self.get_genres():
                current_books = [book for book in self._books if book.get_genre() == filter_type]
            else:
                raise ValueError(f"Invalid filter type: {filter_type}")
            if current_books==[]:
                raise Exception("No books found")
            if filter_type == "All":
                self._file_manager.write_log("Displayed all books successfully")
            elif filter_type == "Available":
                self._file_manager.write_log("Displayed available books successfully")
            elif filter_type == "Unavailable":
                self._file_manager.write_log("Displayed borrowed books successfully")
            elif filter_type in self.get_genres():
                self._file_manager.write_log("Displayed successfully")
            return BookIterator(current_books)
        except Exception as e:
            if filter_type == "All":
                self._file_manager.write_log("Displayed all books fail")
            elif filter_type == "Available":
                self._file_manager.write_log("Displayed available books fail")
            elif filter_type == "Unavailable":
                self._file_manager.write_log("Displayed borrowed books fail")
            elif filter_type in self.get_genres():
                self._file_manager.write_log("Displayed fail")
            return None

    def get_genres(self):
        """
        Return a sorted list of all genres in the library.
        """
        genres = set(book.get_genre() for book in self._books)  # Create a unique list of genres.
        return sorted(genres)  # Return genres sorted alphabetically.
