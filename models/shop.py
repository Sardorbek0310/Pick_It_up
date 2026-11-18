class Shop:
    def __init__(self, name, products=None):
        self.name=name
        self.products=products if products is not None else []

    def show_products(self):
        print("========== Products ==========:")
        if not self.products:
            print("No products available.")
        for product in self.products:
            product.show()
            print("----------------------------")

    def find_product(self, product_name):
        for product in self.products:
            if product.name.lower()==product_name.lower():
                return product
        return None
    
    