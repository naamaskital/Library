class BookIterator:
    def __init__(self, books):
        # Initialize the iterator with a list of books and a starting index.
        self.books = books  # List of books to iterate over.
        self.index = 0      # Starting index for iteration.

    def __iter__(self):
        # Return the iterator object itself.
        return self

    def __next__(self):
        # Return the next book in the list or raise StopIteration if no more books are available.
        if self.index < len(self.books):
            book = self.books[self.index]  # Get the current book.
            self.index += 1                # Move to the next index.
            return book
        else:
            raise StopIteration  # End of the iteration.

class PopularBooksIterator:
    def __init__(self, books):
        # Initialize the iterator for popular books, sorted by lending count in descending order.
        # Only the top 10 most popular books are included.
        self.books = sorted(books, key=lambda book: book.get_lendings(), reverse=True)[:10]
        self.index = 0  # Starting index for iteration.

    def __iter__(self):
        # Return the iterator object itself.
        return self

    def __next__(self):
        # Return the next popular book in the sorted list or raise StopIteration if no more books are available.
        if self.index < len(self.books):
            current_book = self.books[self.index]  # Get the current popular book.
            self.index += 1                        # Move to the next index.
            return current_book
        else:
            raise StopIteration  # End of the iteration.
