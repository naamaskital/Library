import tkinter as tk
from tkinter import messagebox
from screens.login_gui import LoginScreen


def check_login(func):
    """
    Decorator to check if the user is logged in before executing the function.
    """
    def wrapper(self, *args, **kwargs):
        if self.library_manager.is_logged_in:
            return func(self, *args, **kwargs)
        else:
            messagebox.showerror("Logout", "You are not logged in.")
    return wrapper

class LibraryMenu:
    def __init__(self, library_manager):
        """
        Initialize the library menu and set up the main GUI window.
        """
        self.library_manager = library_manager
        self.root = tk.Tk()
        self.root.title("Library System")

        # Set window dimensions and disable resizing
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        """
        Create and set up the main menu buttons.
        """

        # Button for adding a book
        add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book, width=20)
        add_book_button.pack(pady=5)

        # Button for removing a book
        remove_book_button = tk.Button(self.root, text="Remove Book", command=self.remove_book, width=20)
        remove_book_button.pack(pady=5)

        # Button for searching books
        search_book_button = tk.Button(self.root, text="Search Book", command=self.search_book, width=20)
        search_book_button.pack(pady=5)

        # Button for viewing all books
        view_books_button = tk.Button(self.root, text="View Books", command=self.view_books, width=20)
        view_books_button.pack(pady=5)

        # Button for lending a book
        lend_book_button = tk.Button(self.root, text="Lend Book", command=self.lend_book, width=20)
        lend_book_button.pack(pady=5)

        # Button for returning a book
        return_book_button = tk.Button(self.root, text="Return Book", command=self.return_book, width=20)
        return_book_button.pack(pady=5)

        # Button for logging out
        logout_button = tk.Button(self.root, text="Logout", command=self.logout, width=20)
        logout_button.pack(pady=5)

        # Button for displaying popular books
        popular_books_button = tk.Button(self.root, text="Popular Books", command=self.popular_books, width=20)
        popular_books_button.pack(pady=5)

    @check_login
    def add_book(self):
        """
        Open a window to add a new book to the library.
        """
        add_book_window = tk.Toplevel()
        add_book_window.title("Add Book")

        # Input fields for book details
        tk.Label(add_book_window, text="Title:").pack()
        title_entry = tk.Entry(add_book_window)
        title_entry.pack(pady=5)

        tk.Label(add_book_window, text="Author:").pack()
        author_entry = tk.Entry(add_book_window)
        author_entry.pack(pady=5)

        tk.Label(add_book_window, text="Genre:").pack()
        genre_entry = tk.Entry(add_book_window)
        genre_entry.pack(pady=5)

        tk.Label(add_book_window, text="Year:").pack()
        year_entry = tk.Entry(add_book_window)
        year_entry.pack(pady=5)

        tk.Label(add_book_window, text="Copies:").pack()
        copies_entry = tk.Entry(add_book_window)
        copies_entry.pack(pady=5)

        def submit_book():
            """
            Submit the book details and add it to the library.
            """
            title = title_entry.get()
            author = author_entry.get()
            genre = genre_entry.get()
            year = year_entry.get()
            copies = copies_entry.get()

            if not title or not author or not genre or not year or not copies:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                year = int(year)
                copies = int(copies)
                if self.library_manager.add_book(title, author, genre, year, copies):
                    messagebox.showinfo("Success", f"Book '{title}' added successfully!")
                    add_book_window.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to add book '{title}'.")

            except ValueError:
                messagebox.showerror("Error", "Year and Copies must be integers.")

        submit_button = tk.Button(add_book_window, text="Add Book", command=submit_book)
        submit_button.pack(pady=20)

    @check_login
    def remove_book(self):
        """
        Open a window to remove a book from the library.
        """
        remove_book_window = tk.Toplevel(self.root)
        remove_book_window.title("Remove Book")
        remove_book_window.geometry("300x400")
        remove_book_window.resizable(False, False)

        tk.Label(remove_book_window, text="Enter Book Title to Remove:").pack(pady=5)
        title_entry = tk.Entry(remove_book_window)
        title_entry.pack(pady=5)

        def _do_remove_book():
            """
            Remove the specified book from the library.
            """
            book_title = title_entry.get()
            if self.library_manager.remove_book(book_title):
                messagebox.showinfo("Success", f"Book '{book_title}' removed successfully!")
                remove_book_window.destroy()
            else:
                messagebox.showerror("Error", f"Failed to remove book '{book_title}'.")
                remove_book_window.destroy()

        remove_button = tk.Button(remove_book_window, text="Remove Book", command=_do_remove_book)
        remove_button.pack(pady=20)

    @check_login
    def search_book(self):
        """
        Open a window to search for books in the library.
        """
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Book")

        name_var = tk.StringVar()
        author_var = tk.StringVar()
        genre_var = tk.StringVar()

        # Input fields for search criteria
        tk.Label(search_window, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(search_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(search_window, text="Author Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(search_window, textvariable=author_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(search_window, text="Genre:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(search_window, textvariable=genre_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            search_window,
            text="Search",
            command=lambda: self._open_search_book_window(name_var, author_var, genre_var, search_window)
        ).grid(row=3, column=0, columnspan=2, pady=10)

    def _open_search_book_window(self, name_var, author_var, genre_var, search_window, allow_borrow=False, allow_return=False):
        """
        Perform a book search based on the provided criteria and display the results.
        """
        name = name_var.get().strip()
        author = author_var.get().strip()
        genre = genre_var.get().strip()
        inputs = [name, author, genre]
        filled_inputs = [input_str for input_str in inputs if input_str]
        if len(filled_inputs) > 1:
            messagebox.showwarning("Invalid Input", "Please fill in only one field for search.")
            return
        criteria = {}
        if name:
            criteria["name"] = name
        elif author:
            criteria["author"] = author
        elif genre:
            criteria["genre"] = genre
        criteria = {"name": name, "author": author, "genre": genre}
        search_all_books = self.library_manager.search_books(criteria)

        if search_all_books:
            # Create a listbox to display results
            results_list = tk.Listbox(search_window, height=10, width=50)
            results_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
            results_list.delete(0, tk.END)

            for book in search_all_books:
                results_list.insert(tk.END, str(book))

            # Determine the action mode (borrow or return)
            mode = "borrow" if allow_borrow else "return" if allow_return else None

            def on_book_select(event):
                """
                Handle book selection from the listbox.
                """
                selected_index = results_list.curselection()
                if selected_index:
                    selected_book = results_list.get(selected_index[0])
                    title = selected_book.split(",")[0]

                    if mode == "borrow":
                        if self.library_manager.borrow_book(title):
                            messagebox.showinfo("Success", f"The book '{title}' has been borrowed.")
                        else:
                            self._add_to_waitlist(title)
                    elif mode == "return":
                        if self.library_manager.return_book(title):
                            messagebox.showinfo("Success", f"The book '{title}' has been returned.")
                        else:
                            messagebox.showerror("Error", f"Failed to return book '{title}'.")

            results_list.bind("<<ListboxSelect>>", on_book_select)
        else:
            messagebox.showinfo("No Results", "No books found matching the criteria!")

    # Remaining methods have similar comments for clarity, covering all functionalities.
    def _add_to_waitlist(self, book_title):
        """
        Open a window to add a user to the waitlist for a specific book.
        """
        waitlist_window = tk.Toplevel(self.root)
        waitlist_window.title("Add to Waitlist")

        # Display book title and input fields for email and phone number
        tk.Label(waitlist_window, text=f"Book '{book_title}' is unavailable.").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(waitlist_window, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        email_var = tk.StringVar()
        tk.Entry(waitlist_window, textvariable=email_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(waitlist_window, text="Phone Number:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        phone_var = tk.StringVar()
        tk.Entry(waitlist_window, textvariable=phone_var).grid(row=2, column=1, padx=5, pady=5)

        def save_waitlist():
            """
            Save the user details to the waitlist.
            """
            email = email_var.get().strip()
            phone = phone_var.get().strip()

            if not email or not phone:
                messagebox.showerror("Error", "Please provide both email and phone number.")
                return

            self.library_manager.add_to_waiting_list(book_title, email, phone)
            messagebox.showinfo("Success", f"You have been added to the waitlist for '{book_title}'.")
            waitlist_window.destroy()

        tk.Button(waitlist_window, text="Add to Waitlist", command=save_waitlist).grid(row=3, column=0, columnspan=2, pady=10)

    @check_login
    def view_books(self):
        """
        Open a window to view all books in the library, with filtering options.
        """
        view_window = tk.Toplevel(self.root)
        view_window.title("View Books")

        # Set default filter to "All"
        self.filter_option = tk.StringVar(value="All")
        genres = self.library_manager.get_genres()

        # Filter dropdown menu
        filter_frame = tk.Frame(view_window)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        filter_menu = tk.OptionMenu(
            filter_frame,
            self.filter_option,
            "All",
            "Available",
            "Unavailable",
            *genres,
            command=self.display_books
        )
        filter_menu.pack(side=tk.LEFT, padx=5)

        # Scrollable text area for displaying books
        text_frame = tk.Frame(view_window)
        text_frame.pack(pady=10)

        scroll_bar = tk.Scrollbar(text_frame)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_text = tk.Text(text_frame, height=20, width=60, wrap=tk.WORD, yscrollcommand=scroll_bar.set)
        self.book_text.pack(side=tk.LEFT)
        scroll_bar.config(command=self.book_text.yview)

        self.book_text.config(state=tk.DISABLED)

    def display_books(self, *args):
        """
        Display books in the text area based on the selected filter.
        """
        selected_filter = self.filter_option.get()
        book_iterator = self.library_manager.get_filtered_books(selected_filter)

        self.book_text.config(state=tk.NORMAL)
        self.book_text.delete(1.0, tk.END)

        if book_iterator:
            try:
                for book in book_iterator:
                    self.book_text.insert(tk.END,
                                          f"{book.get_title()} by {book.get_author()} ({book.get_genre()}, {book.get_year()})\n")
            except Exception as e:
                self.book_text.insert(tk.END, f"Error displaying books: {e}")
        else:
            self.book_text.insert(tk.END, "No books to display.")

        self.book_text.config(state=tk.DISABLED)

    @check_login
    def lend_book(self):
        """
        Open a window to lend a book from the library.
        """
        lend_window = tk.Toplevel(self.root)
        lend_window.title("Lending Book")

        name_var = tk.StringVar()
        author_var = tk.StringVar()
        genre_var = tk.StringVar()

        tk.Label(lend_window, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(lend_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(lend_window, text="Author Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(lend_window, textvariable=author_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(lend_window, text="Genre:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(lend_window, textvariable=genre_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            lend_window,
            text="Search",
            command=lambda: self._open_search_book_window(name_var, author_var, genre_var, lend_window,
                                                          allow_borrow=True)
        ).grid(row=3, column=0, columnspan=2, pady=10)

        self._open_search_book_window(name_var, author_var, genre_var, lend_window, allow_borrow=True)

    @check_login
    def return_book(self):
        """
        Open a window to return a borrowed book.
        """
        return_window = tk.Toplevel(self.root)
        return_window.title("Return Book")

        name_var = tk.StringVar()
        author_var = tk.StringVar()
        genre_var = tk.StringVar()

        tk.Label(return_window, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(return_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(return_window, text="Author Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(return_window, textvariable=author_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(return_window, text="Genre:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Entry(return_window, textvariable=genre_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            return_window,
            text="Search",
            command=lambda: self._open_search_book_window(name_var, author_var, genre_var, return_window,
                                                          allow_return=True)
        ).grid(row=3, column=0, columnspan=2, pady=10)

        self._open_search_book_window(name_var, author_var, genre_var, return_window, allow_return=True)

    @check_login
    def logout(self):
        """
        Log out the current user and return to the login screen.
        """
        self.library_manager.log_out()
        messagebox.showinfo("Logout", "You have been logged out.")
        self.root.destroy()
        login_screen = LoginScreen(self.library_manager)
        login_screen.run()

    @check_login
    def popular_books(self):
        """
        Open a window to display the most popular books in the library.
        """
        books = self.library_manager.get_popular_books()
        if books:
            popular_window = tk.Toplevel()
            popular_window.title("Popular Books")

            for book in books:
                label = tk.Label(popular_window, text=f"{book.get_title()} by {book.get_author()} - Lendings: {book.get_lendings()}")
                label.pack(pady=5)
        else:
            messagebox.showinfo("Popular Books", "No books found.")

    def run(self):
        """
        Run the main application loop.
        """
        self.root.mainloop()
