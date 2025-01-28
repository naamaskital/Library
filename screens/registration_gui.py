import tkinter as tk
from tkinter import messagebox


class RegistrationScreen:
    def __init__(self, library_manager):
        """
        Initialize the registration screen with a reference to the LibraryManager.
        Sets up the main registration window.
        """
        self.library_manager = library_manager
        self.root = tk.Tk()
        self.root.title("Registration")

        # Set the size of the registration window
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the registration screen, including fields for personal details,
        username, password, and a register button.
        """
        # First Name field
        first_name_label = tk.Label(self.root, text="First Name:")
        first_name_label.pack(pady=5)
        self.first_name_entry = tk.Entry(self.root, width=30)
        self.first_name_entry.pack(pady=5)

        # Last Name field
        last_name_label = tk.Label(self.root, text="Last Name:")
        last_name_label.pack(pady=5)
        self.last_name_entry = tk.Entry(self.root, width=30)
        self.last_name_entry.pack(pady=5)

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

        # Register button
        register_button = tk.Button(self.root, text="Register", command=self.register_user)
        register_button.pack(pady=20)

    def register_user(self):
        """
        Handle the user registration process by validating the inputs.
        If the registration is successful, navigate to the login screen.
        Otherwise, show an error message.
        """
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if first_name and last_name and username and password:
            # Attempt to add a user through the LibraryManager
            try:
                if self.library_manager.add_user(first_name, last_name, username, password):
                    messagebox.showinfo('Registration Successful', f'User {first_name} registered successfully')
                    self.root.destroy()
                    self.open_login_screen()  # Navigate to the login screen
                else:
                    messagebox.showerror('Registration Failed', f'Username {username} is already exist')
            except ValueError:
                messagebox.showerror("Error", "ID number must be an integer.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def open_login_screen(self):
        """
        Navigate to the login screen after successful registration.
        """
        from screens.login_gui import LoginScreen
        login_screen = LoginScreen(self.library_manager)
        login_screen.run()  # Run the login screen

    def run(self):
        """
        Run the main loop for the registration screen.
        """
        self.root.mainloop()
