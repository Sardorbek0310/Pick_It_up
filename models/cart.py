class Cart:
    def __init__(self):
        self.items={}

    def add(self, product, quantity):
        if product.name in self.items:
            self.items[product.name]["quantity"] += quantity
        else:
            self.items[product.name]={"product": product, "quantity": quantity}

    def remove(self, product_name):
        key = product_name.strip().lower()
        for name in list(self.items.keys()):
            if name.lower()==key:
                del self.items[name]
                return True
        return False

    def total(self):
        amount=0
        for item in self.items.values():
            amount+=item["product"].price * item["quantity"]
        return amount

    def is_empty(self):
        return len(self.items)==0

    def show(self):
        if self.is_empty():
            print("Your cart is empty.")
            return
        print("\\nYOUR CART:")
        for item in self.items.values():
            product = item["product"]
            quantity = item["quantity"]
            print(f"{product.name} x {quantity} = {product.price * quantity:,.0f} UZS")
        print(f"Total: {self.total():,.0f} UZS")


 
















