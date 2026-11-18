class Order:
    def __init__(
        self, order_id, customer_username, place_name, items, total, ready_at, preparation_minutes, order_type):
        self.order_id=order_id
        self.customer_username=customer_username
        self.place_name=place_name
        self.items=items
        self.total=total
        self.status="Active"
        self.ready_at=ready_at
        self.preparation_minutes=preparation_minutes
        self.order_type=order_type

    def show(self):
        print(f"Order #{self.order_id} | {self.place_name} | "
            f"{self.total:,.0f} UZS | Status: {self.status}")
        for item in self.items:
            print(f"  - {item['name']} x {item['quantity']}")
        if self.order_type=="ASAP":
            print(f"  Estimated preparation: {self.preparation_minutes} minutes")
        else:
            print("  Scheduled order")
        print(f"  Ready at: {self.ready_at.strftime('%I:%M %p')}")


