from datetime import datetime, timedelta
from models.order import Order

class OrderService:
    def estimate_preparation(self, cart):
        if cart.is_empty():
            return 0
        longest_time = 0
        for item in cart.items.values():
            product = item["product"]
            longest_time = max(longest_time, product.preparation_minutes)
        extra_items = max(0, len(cart.items) - 1)
        return longest_time + (extra_items * 2)

    def checkout(self, customer, place_name, order_id, promo=None, scheduled_time=None):
        if customer.cart.is_empty():
            return None
        items = []
        for item in customer.cart.items.values():
            product = item["product"]
            items.append({"name": product.name,
                "quantity": item["quantity"],
                "unit_price": product.price,})

        total = customer.cart.total()
        if promo:
            total = promo.apply(total)

        preparation_minutes = self.estimate_preparation(customer.cart)
        now = datetime.now()

        if scheduled_time is None:
            ready_at = now + timedelta(minutes=preparation_minutes)
            order_type = "ASAP"
        else:
            ready_at = scheduled_time
            order_type = "SCHEDULED"

        order = Order(order_id,
            customer.username,
            place_name,
            items,
            total,
            ready_at,
            preparation_minutes,
            order_type,)
        customer.orders.append(order)
        customer.cart = customer.cart.__class__()
        return order

    def cancel(self, customer, order_id):
        for order in customer.orders:
            if order.order_id == order_id and order.status == "Active":
                order.status = "Cancelled"
                return True
        return False
    





    