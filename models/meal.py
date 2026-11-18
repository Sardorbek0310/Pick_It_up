from models.product import Product

class Meal(Product):
    def __init__(self, name, price, category, preparation_minutes=15):
        super().__init__(name, price, preparation_minutes)
        self.category = category
    def show(self):
        print(f"{self.name} ({self.category}) - {self.price:,.0f} UZS "
            f"(preparation: {self.preparation_minutes} min)")



  