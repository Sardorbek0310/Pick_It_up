from users.user import User

class Business(User):
    def __init__(self, name, username, password, business_name, business_type, place):
        super().__init__(name, username, password)
        self.business_name=business_name
        self.business_type=business_type
        self.place=place

