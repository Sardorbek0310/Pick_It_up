from users.user import User
from models.cart import Cart

class Customer(User):
    def __init__(self, name, username, password):
        super().__init__(name, username, password)
        self.cart=Cart()
        self.orders=[]
        self.reports=[]
