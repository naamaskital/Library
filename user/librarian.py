from user.user import User
from user.observer import Observer

class Librarian(User):
    def __init__(self, first_name, last_name, username, password, active=False):
        super().__init__(first_name, last_name, username, password, active)

