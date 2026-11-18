class Product:
    def __init__(self, name, price, preparation_minutes=10):
        self.name=name
        self.price=price
        self.preparation_minutes=preparation_minutes

    def prepare(self):
        print(f"{self.name} - {self.price:,.0f} UZS "
            f"(preparation: {self.preparation_minutes} min)")



