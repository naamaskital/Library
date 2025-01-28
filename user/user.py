from tkinter import Toplevel, Button, Label
from user.observer import Observer


class User(Observer):
    def __init__(self, first_name, last_name, username, password, active=False):
        """
        Initialize a User object with basic attributes such as name, ID, username, and password.
        :param first_name: User's first name
        :param last_name: User's last name
        :param id_number: User's unique identification number
        :param username: User's username for login
        :param password: User's password (can be encrypted in the future)
        :param active: Boolean indicating if the user is active
        """
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._password = password  # Encryption can be added later
        self._active = active
        self.notifications = []

    def update(self, notification):
        """
        Receives a notification and saves it in the notifications list.
        Displays a popup window to the user if the user is active.
        :param notification: The received notification message.
        """
        self.notifications.append({"message": notification, "type": "info"})
        if self.is_active():
            # Create a new popup window for the notification
            popup_root = Toplevel()
            popup_root.title("Notification")
            popup_root.geometry("300x100")
            popup_root.resizable(False, False)

            # Add content to the popup window
            msg_label = Label(popup_root, text=notification, wraplength=280, justify="center")
            msg_label.pack(pady=10)

            # Add a close button to the popup window
            close_button = Button(popup_root, text="Close", command=popup_root.destroy)
            close_button.pack(pady=10)

            # Ensure the popup window stays on top
            popup_root.attributes("-topmost", True)

    def get_notifications(self):
        """
        Returns the list of notifications for the user.
        :return: List of notifications
        """
        return self.notifications

    def clear_notifications(self):
        """
        Clears all notifications for the user.
        """
        self.notifications.clear()

    def activate(self):
        """
        Activates the user by setting the active status to True.
        """
        self._active = True

    def deactivate(self):
        """
        Deactivates the user by setting the active status to False.
        """
        self._active = False

    def is_active(self):
        """
        Checks whether the user is currently active.
        :return: Boolean indicating if the user is active
        """
        return self._active

    def get_first_name(self):
        """
        Returns the user's first name.
        :return: First name
        """
        return self._first_name

    def get_last_name(self):
        """
        Returns the user's last name.
        :return: Last name
        """
        return self._last_name


    def get_username(self):
        """
        Returns the user's username.
        :return: Username
        """
        return self._username

    def get_password(self):
        """
        Returns the user's password.
        Note: Consider encrypting passwords in production.
        :return: Password
        """
        return self._password
