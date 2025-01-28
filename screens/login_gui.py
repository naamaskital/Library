import tkinter as tk
from tkinter import messagebox
from management.library_manager import LibraryManager


class LoginScreen:
    def __init__(self, library_manager):
        """
        Initialize the login screen with a reference to the LibraryManager.
        Sets up the main login window.
        """
        self.library_manager = library_manager
        self.root = tk.Tk()
        self.root.title("Login")

        # Set the size of the login window
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the login screen, including username and password fields,
        a login button, and an option to register.
        """
        # Username field
        username_label = tk.Label(self.root, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        # Password field
        password_label = tk.Label(self.root, text="Password:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(self.root, text="Login", command=self.login_user)
        login_button.pack(pady=10)

        # Registration option
        registration_frame = tk.Frame(self.root)
        registration_frame.pack(pady=10)

        no_account_label = tk.Label(registration_frame, text="Don't have an account?")
        no_account_label.pack(side="left", padx=5)

        register_button = tk.Button(registration_frame, text="Register", command=self.register_user)
        register_button.pack(side="left")

    def login_user(self):
        """
        Handle the user login process by validating the username and password.
        If the credentials are correct, navigate to the library menu.
        Otherwise, show an error message.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            # Check if the username and password exist in the system
            if self.library_manager.set_current_user(username, password):
                messagebox.showinfo("Login", f"Welcome back, {username}!")
                self.show_manu_screen()  # Navigate to the library menu screen
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Both username and password are required.")

    def show_manu_screen(self):
        """
        Navigate to the library menu screen after successful login.
        """
        from screens.library_gui import LibraryMenu
        self.root.destroy()  # Close the login window
        library_screen = LibraryMenu(self.library_manager)
        library_screen.run()

    def register_user(self):
        """
        Navigate to the registration screen when the user clicks on "Register."
        """
        self.root.destroy()
        self.open_registration_screen()

    def open_registration_screen(self):
        """
        Open the registration screen for the user to create a new account.
        """
        from screens.registration_gui import RegistrationScreen
        registration_screen = RegistrationScreen(self.library_manager)
        registration_screen.run()  # Run the registration window

    def run(self):
        """
        Run the main loop for the login screen.
        """
        self.root.mainloop()
