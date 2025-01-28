from management.library_manager import LibraryManager
from screens.login_gui import LoginScreen

# Entry point for the application
if __name__ == "__main__":
    # Initialize the library manager with file paths for books, logs, and users
    library_manager = LibraryManager("data/books.csv", "data/log.txt", "data/users.csv")

    # Initialize and run the login screen
    login_screen = LoginScreen(library_manager)
    login_screen.run()
