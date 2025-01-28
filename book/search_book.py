class SearchStrategy:
    """
    A template for searching books based on a specific field.
    """
    @staticmethod
    def search(sub_str, books, field):
        """
        Searches for books in the list based on a substring in a specific field.
        :param sub_str: The substring to search for (if empty, returns all books).
        :param books: The list of books to search within.
        :param field: The name of the field to search (title, author, genre).
        :return: A list of books matching the search criteria.
        """
        # If the search string is empty (as any string contains an empty string),
        # return all books.
        if not sub_str.strip():  # .strip() removes unnecessary whitespace.
            return books

        # Convert the substring to lowercase for case-insensitive searching.
        sub_str = sub_str.lower()

        # Search for books where the substring appears in the specified field.
        return [book for book in books if sub_str in getattr(book, f"_{field}").lower()]


class SearchByName(SearchStrategy):
    @staticmethod
    def search(sub_str, books):
        # Searches books by title.
        return SearchStrategy.search(sub_str, books, "title")

class SearchByAuthor(SearchStrategy):
    @staticmethod
    def search(sub_str, books):
        # Searches books by author.
        return SearchStrategy.search(sub_str, books, "author")

class SearchByGenre(SearchStrategy):
    @staticmethod
    def search(sub_str, books):
        # Searches books by genre.
        return SearchStrategy.search(sub_str, books, "genre")
