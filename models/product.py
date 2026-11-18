class Product:
    def __init__(self, name, price, preparation_minutes=10):
        self.name=name
        self.price=price
        self.preparation_minutes=preparation_minutes

    def show(self):
        print(f"- {self.name}")
        print(f"  Price: {self.price:,.0f} UZS")
        print(f"  Preparation: {self.preparation_minutes} min")
        print()



