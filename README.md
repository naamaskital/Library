# Library Management System - Object-Oriented Programming Project

This project is part of an Object-Oriented Programming (OOP) course, focusing on implementing design patterns and showcasing OOP principles.
The system is designed exclusively for librarians and supports features such as book management, librarian registration, and more.

---

## Project Structure

### Main Components
1. **Entities**:
   - `User`: Represents a generic user in the system.
   - `Observer`: Interface used by objects that receive notifications.
   - `Librarian` (inherits `User`): Represents a librarian.
   - `Book`: Represents a book in the library. Handles book details, waiting list management, and notifications for availability.
   - `BookIterator`: Provides an iterator for iterating through books.
   - `PopularBooksIterator`: Specialized iterator to fetch the most borrowed books in descending order of popularity.

2. **Search Strategies**:
   - `SearchStrategy`: Abstract class for search strategies, defining a template for searching books by specific fields.
   - Concrete strategies:
     - `SearchByName`: Searches for books by their title.
     - `SearchByGenre`: Searches for books by their genre.
     - `SearchByAuthor`: Searches for books by their author.

3. **Management**:
   - `FileManager`: Handles file operations for text files (e.g., `csv`, `txt`).
     - **Key Features**:
       - Ensures necessary files exist and initializes them with headers if required.
       - Supports loading books from a file into `Book` objects.
       - Saves updated book data, including waiting lists and lending information, back to the file.
       - Manages user data by appending new users to the file.
       - Logs system actions to a log file for transparency and debugging purposes.
   - `LibrarianManager`: Manages librarians and serves as the subject for the Observer pattern.
     - **Key Features**:
       - Uses a decorator (`@hash_password`) to securely hash passwords during librarian registration and login.
       - Notifies all registered librarians of important system updates or events.
       - Validates user credentials during login attempts and checks for existing usernames to avoid duplication.
       - Loads librarian data from a CSV file and maintains it in memory for efficient operations.
   - `LibraryManager`: Manages overall library operations, including books and librarians. Implements additional iterators for filtered views and popular books.
     - **Key Features**:
       - Manages user authentication and session control with decorators like `@requires_login`.
       - Handles adding, removing, and returning books while maintaining accurate records.
       - Provides filtered views of books (all, available, unavailable, by genre).
       - Integrates search functionality using search strategies (`SearchByName`, `SearchByGenre`, `SearchByAuthor`).
       - Manages waiting lists for books and notifies users when books become available.
       - Allows librarians to view and borrow the most popular books using the `PopularBooksIterator`.

4. **Screens** (GUI):
   - `LoginScreen`: Handles user login.
     - **Key Features**:
       - Provides username and password fields for authentication.
       - Navigates to the `LibraryMenu` screen upon successful login.
       - Includes a registration option to create a new librarian account.
       - Validates user input and displays appropriate messages for errors or success.
   - `RegisterScreen`: Handles librarian registration.
     - **Key Features**:
       - Provides input fields for first name, last name, ID number, username, and password.
       - Validates all inputs before attempting to register the user.
       - Redirects to the `LoginScreen` upon successful registration.
       - Displays meaningful error messages if registration fails.
   - `LibraryScreen`: Main interface for library operations. Includes a decorator to ensure only logged-in librarians can perform actions.
   - `LibraryMenu`: Provides the main menu GUI for library operations, offering features like adding, removing, searching, lending, and returning books.

5. **Data**:
   - `books.csv`: Stores book data.
   - `books_copy.csv`
   - `users..csv`
   - `log.txt`: Logs system actions.

6. **Tests**:
   - Located in the `tests` folder, ensuring all features are thoroughly tested without altering production data.
     - **Key Tests**:
       - `test_add_new_book`: Validates adding a new book.
       - `test_remove_book`: Ensures a book can be removed if not borrowed.
       - `test_borrow_unavailable_book`: Confirms that unavailable books cannot be borrowed.
       - `test_waiting_list_allocation`: Verifies the correct allocation of books to users in the waiting list.
       - `test_log_write_on_borrow`: Ensures borrowing operations are properly logged.
       - `test_add_book_requires_login`: Confirms that adding a book without logging in returns the correct response.
       - `test_return_book_requires_login`: Verifies that returning a book without login fails.
       - `test_borrow_book_requires_login`: Checks that borrowing requires user authentication.
       - `test_login_not_registered`: Ensures that logging in with an unregistered user fails.
       - `test_search_by_name_full_match`: Ensures searching by the exact name returns correct results.
       - `test_search_by_name_partial`: Validates partial name searches yield expected books.
       - `test_search_by_author_full_match`: Confirms searching by full author name retrieves the correct books.
       - `test_search_by_genre_partial`: Tests partial genre matches during search.
       - `test_search_by_name_and_genre`: Verifies combined search by name and genre returns expected results.
       - `test_search_by_three_criteria`: Ensures searches by name, author, and genre simultaneously work correctly.
       - `test_set_filter_all`: Checks displaying all books in the library.
       - `test_set_filter_available`: Confirms filtering only available books functions properly.
       - `test_set_filter_unavailable`: Validates that unavailable books are displayed correctly.
       - `test_set_filter_by_genre`: Ensures filtering by a specific genre yields accurate results.
       - `test_set_filter_by_nonexistent_genre`: Verifies filtering by a non-existent genre returns no results.
       - `test_set_filter_after_borrow_and_return`: Confirms that filtering updates correctly after borrowing and returning books.
       - and more

---

## Design Patterns

### 1. Observer Pattern
   - **Context**: Used for the librarian notification system.
   - **Implementation**:
     - `LibrarianManager` acts as the **Subject**.
     - Librarian objects receive notifications through the observer interface.
     - The notification mechanism is associated with library updates and book availability.

### 2. Strategy Pattern
   - **Context**: Used for flexible book search functionality.
   - **Implementation**:
     - `SearchStrategy` defines the interface for search behavior.
     - Concrete strategies (`SearchByName`, `SearchByGenre`, `SearchByAuthor`) implement specific search logic.

### 3. Decorator Pattern
   - **Context**: Enhances methods with additional functionality.
   - **Implementation**:
     - `@hash_password`: Applies password hashing during registration or authentication.
     - `@requires_login`: Ensures certain methods can only be executed by logged-in librarians.
     - `@check_librarian`: Ensures only registered librarians can access certain GUI functions.

### 4. Iterator Pattern
   - **Context**: Used for traversing book collections.
   - **Implementation**:
     - `BookIterator`: Provides sequential access to books, supporting different filters (all, available, borrowed).
     - `PopularBooksIterator`: Returns the top 10 most borrowed books in descending order of lendings.

### Working with Multiple Library Instances

In the current implementation, we deliberately chose **not** to enforce a Singleton pattern for the library instance. This decision provides the following benefits:

- **Flexibility**: Allows the creation of multiple library instances simultaneously.
- **Parallel Access**: If the same files are passed to multiple `LibraryManager` instances, they can effectively "connect" to the same library data and perform operations in parallel.

#### Key Considerations:
1. Developers can create separate library instances using different files or the same files for testing or other use cases.
2. Concurrent modifications to the same file by multiple instances may lead to data conflicts if not handled properly.

For future requirements, a Singleton pattern or a centralized resource management system can be implemented to enforce strict single-instance behavior.

---

## Instructions for Running the Project

Open the repository root as the working directory when running the project, so local imports resolve consistently.

### Prerequisites
1. Install Python 3.8 or higher.
2. Install the required packages manually by running:
   ```bash
   python -m pip install numpy pandas bcrypt
   ```

### Running the Project
1. Run the main script to start the application:
   ```bash
   python main.py
   ```

This will launch the login screen, where you can log in or register as a new librarian.

### Running Tests
To run all unit tests and ensure the application is working as expected, execute:
```bash
python -m unittest discover -s tests
```

