import json

from management import librarian_manager


class Book:
    def __init__(self, title, author, genre, year, copies, is_loaned=False, lendings=0, borrowed_books=0, waiting_list=None):
        # Initialize a book object with its properties.
        self._title = title
        self._author = author
        self._genre = genre
        self._year = year
        self._copies = copies
        self._is_loaned = is_loaned
        self._lendings = lendings
        self._borrowed_books = borrowed_books
        self._waiting_list = waiting_list if waiting_list is not None else []

    @staticmethod
    def create_book_from_row(row):
        """
        Create a Book object from a dictionary-like row (e.g., from a CSV file).
        """
        return Book(
            title=row['title'],
            author=row['author'],
            genre=row['genre'],
            year=row['year'],
            copies=int(row['copies']),
            is_loaned=True if row['is_loaned'] == 'Yes' else False,
            lendings=int(row['lendings']),
            borrowed_books=int(row['borrowed_books']),
            waiting_list=json.loads(row['waiting_list']) if row['waiting_list'] else []  # Convert JSON string to a list.
        )

    def get_title(self):
        # Return the title of the book.
        return self._title

    def get_author(self):
        # Return the author of the book.
        return self._author

    def get_genre(self):
        # Return the genre of the book.
        return self._genre

    def get_year(self):
        # Return the year of publication of the book.
        return self._year

    def get_copies(self):
        # Return the number of copies available.
        return self._copies

    def is_loaned(self):
        # Check if all copies of the book are loaned out.
        return self._is_loaned

    def get_lendings(self):
        # Return the total number of times the book has been borrowed.
        return self._lendings

    def get_borrowed_books(self):
        # Return the number of currently borrowed copies.
        return self._borrowed_books

    def get_waiting_list(self):
        # Return the waiting list for the book.
        return self._waiting_list

    def add_copies(self, copies, librarian_manager):
        """
        Add copies to the book. If there is a waiting list, allocate copies in order until
        either the list is empty or no copies remain.
        """
        self._copies += copies
        self._is_loaned = copies < 0
        i = self._borrowed_to_waiting_list(librarian_manager)
        return i

    def is_in_waiting_list(self, mail, phone):
        # Check if a user with the given email or phone number is already in the waiting list.
        for person in self._waiting_list:
            if person['email'] == mail or person['phone'] == phone:
                return True
        return False

    def add_to_waiting_list(self, mail, phone):
        # Add a user to the waiting list if they are not already in it.
        if not self.is_in_waiting_list(mail, phone):
            self._waiting_list.append({'email': mail, 'phone': phone})
            self.add_lendings(1)
            return True
        else:
            return False

    def has_borrowed_books(self):
        # Check if there are any borrowed books.
        return self._borrowed_books > 0

    def add_lendings(self, lendings):
        # Increment the total number of times the book has been borrowed.
        self._lendings += lendings

    def add_borrowed_books(self, borrowed_books):
        """
        Increment the number of borrowed copies. If all copies are borrowed,
        mark the book as loaned.
        """
        self._borrowed_books += borrowed_books
        if self._borrowed_books >= self._copies:
            self._is_loaned = True
        self.add_lendings(borrowed_books)

    def sub_borrowed_books(self, borrowed_books, librarian_manager):
        """
        Decrement the number of borrowed copies. If copies become available,
        allocate them to users on the waiting list.
        """
        self._borrowed_books -= borrowed_books
        if self._borrowed_books < self._copies:
            self._is_loaned = False
        i = self._borrowed_to_waiting_list(librarian_manager)
        return i

    def _borrowed_to_waiting_list(self, librarian_manager):
        """
        Allocate available copies to users on the waiting list in order.
        Notify users when a copy becomes available for them.
        """
        i = 0
        while self._waiting_list and not self.is_loaned():
            # Allocate a copy to the first person in the waiting list.
            person = self._waiting_list.pop(0)
            email = person.get('email')
            phone = person.get('phone')
            librarian_manager.notify_observers(
                f"The book: {self._title} is now available for borrowing to the user with the email: {email} and has been borrowed automatically"
            )
            self._lendings-=1
            self.add_borrowed_books(1)
            i += 1
        return i

    def __str__(self):
        # Return a string representation of the book.
        return str(self._title + ", " + self._author + ", " + self._genre + ", " + str(self._year))
