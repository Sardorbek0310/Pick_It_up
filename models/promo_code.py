class PromoCode:
    def __init__(self, code, discount, description):
        self.code=code
        self.discount=discount
        self.description=description

    def apply(self, total):
        return total - (total*self.discount/100)

 