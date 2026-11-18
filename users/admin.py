from users.user import User

class Admin(User):
    def __init__(self, name, username, password):
        super().__init__(name, username, password)
