from datetime import datetime, timedelta
from users.admin import Admin
from users.business import Business
from users.customer import Customer
from models.shop import Shop
from models.restaurant import Restaurant
from models.product import Product
from models.meal import Meal
from models.promo_code import PromoCode
from services.order_service import OrderService

admins=[Admin("Administrator", "admin", "admin123")]
business=[]
customer=[]
shops=[Shop("Tech Store", [Product("MacBook M1 PRO", 10000000), Product("iPhone 18 Pro", 15000000), Product("Charger", 80000), Product("Cable", 45000)]),
         Shop("Book Store", [Product("Tushda kechgan umrlar", 90000), Product("Shamollarda qolgan hislarim", 100000), Product("Otamdan qolgan dalalar", 120000), Product("Dafter hoshiyasidagi bitiklar", 35000)])]
restaurants=[Restaurant("Osh Markazi", [Meal("To'y oshi", 55000, "Milliy taom"), Meal("Zig'ir oshi", 60000, "Milliy taom"), Meal("Coca-Cola", 15000, "Ichimlik")]),
               Restaurant("Tarnov", [Meal("Lag'mon", 65000, "Uyg'ur taomi"), Meal("Somsa", 9000, "Milliy taom"), Meal("Bliss", 13000, "Ichimlik")])]
promocodes=[PromoCode("WELCOME10", 10, "Welcome discount")]
order_service=OrderService()
next_order_id=1

def users():
    return admins+business+customer

def username_exist(username):
    for user in users():
        if user.username.lower()==username.lower():
            return True
    return False

def strong_password(password):
    if len(password)<8:
        return False
    for character in password:
        if character.isdigit():
            return True
    return False

def login():
    users = admins+business+customer
    while True:
        username=input("Enter username(or exit): ")
        if username.lower()=="exit":
            return
        password=input("Enter password: ")
        for user in users:
            if user.username==username and user.password==password:
                print("Successful login!")
                if isinstance(user, Admin):
                    admin_menu(user)
                elif isinstance(user, Business):
                    business_menu(user)
                elif isinstance(user, Customer):
                    customer_menu(user)
                return
        print("Incorrect username or password")

def registration():
    users=admins+business+customer
    print("=== Registration ===")
    name=input("Enter your name: ")
    username=input("Enter your username: ")
    if not name or not username:
        print("Name and username are required!")
        return
    for user in users:
        if user.username.lower()==username.lower():
            print("Username already exists")
            return
    while True:
        password=input("Enter password: ")
        if not strong_password(password):
            print("Password needs 8 characters and at least 1 digit.")
            continue
        confirmation=input("Confirm password: ")
        if confirmation!=password:
            print("Passwords do not match")
            continue
        break
    while True:
        print("1. Register")
        print("2. Back")
        choose=input("Choose: ")
        if choose=="1":
            new_customer=Customer(name, username, password)
            customer.append(new_customer)
            print("Registration successful! Please log in.")
            return
        elif choose=="2":
            return
        else:
            print("Invalid option!")

def show_places(places):
    for number, place in enumerate(places, 1):
        print(f"{number}. {place.name}")


def browse(customer_user, places):
    while True:
        print("Choose a place:")
        show_places(places)
        print("0. Back")
        choose=input("Choose: ")
        if choose=="0":
            return
        if not choose.isdigit() or int(choose)<1 or int(choose)>len(places):
            print("Invalid choice")
            continue
        place=places[int(choose)-1]
        place_menu(customer_user, place)

def place_menu(customer_user, place):
    while True:
        print("\n==========", place.name.upper(), "==========")
        place.show_products()
        print("1. Add product to cart")
        print("2. View cart")
        print("3. Remove product from cart")
        print("4. Checkout / Book pickup")
        print("0. Back")
        choose=input("Choose: ")
        if choose=="1":
            name=input("Product name: ")
            product=place.find_product(name)
            if product is None:
                print("Product not found")
                continue
            amount=input("Quantity: ")
            if amount.isdigit() and int(amount)>0:
                customer_user.cart.add(product, int(amount))
                print("Added!")
            else:
                print("Enter a positive quantity")
        elif choose=="2":
            customer_user.cart.show()
        elif choose=="3":
            name=input("Remove product:")
            if customer_user.cart.remove(name):
                print("Removed!")
            else:
                print("Not in cart")
        elif choose=="4":
            checkout(customer_user, place)
        elif choose=="0":
            return
        else:
            print("Invalid choice")

def checkout(customer_user, place):
    global next_order_id
    if customer_user.cart.is_empty():
        print("Cart is empty.")
        return
    customer_user.cart.show()
    code=input("Promo code (Enter to skip): ").upper()
    promo=None
    for item in promocodes:
        if item.code==code:
            promo=item
    if code and promo is None:
        print("Promocode not found")
    minutes=order_service.estimate_preparation(customer_user.cart)
    print("Preparation time:", minutes, "minutes")
    print("1. Order now")
    print("2. Schedule pickup today")
    choose=input("Choose: ")
    scheduled_time = None
    if choose=="2":
        time_text=input("Pickup time (example 04:30 PM): ")
        try:
            pickup_time=datetime.strptime(time_text, "%I:%M %p").time()
            scheduled_time=datetime.combine(datetime.now().date(), pickup_time)
            if scheduled_time<datetime.now() + timedelta(minutes=minutes):
                print("Pickup time is too soon")
                return
        except ValueError:
            print("Invalid time format")
            return
    elif choose!="1":
        print("Cancelled")
        return
    order=order_service.checkout(customer_user, place.name, next_order_id, promo, scheduled_time)
    if order is not None:
        next_order_id += 1
        print("Order placed successfully!")
        order.show()

def customer_orders(customer_user):
    if not customer_user.orders:
        print("No orders yet")
        return
    for order in customer_user.orders:
        order.show()
    choose=input("Order ID to cancel (Enter to go back): ")
    if choose.isdigit():
        if order_service.cancel(customer_user, int(choose)):
            print("Order cancelled")
        else:
            print("Active order not found")

def customer_menu(customer_user):
    while True:
        print("=== CUSTOMER MENU ===")
        print("1. Shops")
        print("2. Restaurants")
        print("3. My orders")
        print("4. Support")
        print("5. Promo codes")
        print("6. Log out")
        print("7. Exit")

        choose=input("Choose: ")
        if choose=="1":
            browse(customer_user, shops)
        elif choose=="2":
            browse(customer_user, restaurants)
        elif choose=="3":
            customer_orders(customer_user)
        elif choose=="4":
            message = input("Your request: ")
            if message:
                customer_user.reports.append(message)
                print("Request sent")
        elif choose=="5":
            for promo in promocodes:
                print(promo.code, "-", promo.discount, "% off")
        elif choose=="6":
            print("Logged out")
            return
        elif choose=="7":
            print("Thank you for using Pick It Up!")
            print("We look forward to seeing you again!")
            raise SystemExit
        else:
            print("Invalid choice")

def create_business():
    print("=== Create Business User ===")
    name=input("Owner name: ")
    username=input("Username: ")
    business_name=input("Business name: ")
    if not name or not username or not business_name or username_exist(username):
        print("Missing information or username already exists")
        return
    
    print("1. Shop")
    print("2. Restaurant")
    kind=input("Choose: ")
    if kind!="1" and kind!="2":
        print("Invalid choice")
        return
    places=shops if kind=="1" else restaurants
    for place in places:
        if place.name.lower()==business_name.lower():
            print("Business name already exists")
            return
        
    password=input("Password: ")
    if not strong_password(password):
        print("Weak password")
        return
    if kind=="1":
        place=Shop(business_name)
        business_type="Shop"
    else:
        place=Restaurant(business_name)
        business_type="Restaurant"
    places.append(place)
    new_business=Business(name, username, password, business_name, business_type, place)
    business.append(new_business)
    print("Business user created!")

def manage_business_users():
    while True:
        print("=== Business Users ===")
        for user in business:
            print(user.username, "-", user.business_name)
        print("1. Create business user")
        print("2. Remove business user")
        print("0. Back")
        choose=input("Choose: ")
        if choose=="1":
            create_business()
        elif choose=="2":
            username=input("Username to remove: ")
            found=False
            for user in business:
                if user.username==username:
                    business.remove(user)
                    if user.business_type=="Shop":
                        shops.remove(user.place)
                    else:
                        restaurants.remove(user.place)
                    found=True
                    print("User has been removed")
                    break
            if not found:
                print("User not found")
        elif choose=="0":
            return
        else:
            print("Invalid choice")

def manage_customers():
    print("=== Customer Users ===")
    for user in customer:
        print(user.username, "-", user.name)
    username=input("Username to remove: ")
    if username:
        for user in customer:
            if user.username==username:
                customer.remove(user)
                print("User has been removed")
                return
        print("User not found")

def manage_promocodes():
    while True:
        for promo in promocodes:
            print(promo.code, "-", promo.discount, "%")
        print("1. Add promo code")
        print("2. Remove promo code")
        print("0. Back")
        choose=input("Choose: ")
        if choose=="1":
            code=input("New promocode: ").upper()
            percent=input("Discount (1-100): ")
            if not code or not percent.isdigit() or not 1<=int(percent)<= 100:
                print("Invalid code or discount")
                continue
            found=False
            for promocode in promocodes:
                if promocode.code==code:
                    found=True
            if found:
                print("This promocode already exists")
            else:
                promocodes.append(PromoCode(code, int(percent), "Discount"))
                print("Added")
        elif choose=="2":
            code=input("Remove promocode: ").upper()
            for promocode in promocodes:
                if promocode.code==code:
                    promocodes.remove(promo)
                    print("Removed")
                    break
        elif choose=="0":
            return
        else:
            print("Invalid choice")

def all_orders():
    orders=[]
    for user in customer:
        for order in user.orders:
            orders.append(order)
    return orders

def admin_menu(admin_user):
    while True:
        print("=== ADMIN MENU ===")
        print("1. Manage business users")
        print("2. Manage customer users")
        print("3. Manage promocodes")
        print("4. Customer requests")
        print("5. Revenue")
        print("6. All orders")
        print("7. Log out")
        print("8. Exit")
        choose=input("Choose: ")
        if choose=="1":
            manage_business_users()
        elif choose=="2":
            manage_customers()
        elif choose=="3":
            manage_promocodes()
        elif choose=="4":
            for user in customer:
                for message in user.reports:
                    print(user.username, ":", message)
        elif choose=="5":
            total=0
            for order in all_orders():
                if order.status!="Cancelled":
                    total+=order.total
            print("Revenue:", total, "UZS")
        elif choose=="6":
            for order in all_orders():
                order.show()
        elif choose=="7":
            print("Logged out")
            return
        elif choose=="8":
            print("\nBehind every great project is great leader!")
            print("See you soon, friend! ")
            raise SystemExit
        else:
            print("Invalid choice")

def manage_business_products(business_user):
    place=business_user.place
    while True:
        print("=== Manage Products ===")
        place.show_products()
        print("1. Add product")
        print("2. Remove product")
        print("0. Back")
        choose=input("Choose: ")
        if choose=="1":
            name=input("Product name: ")
            price_text=input("Price in UZS: ")
            if not name or place.find_product(name) is not None:
                print("Same or invalid name")
                continue
            try:
                price = float(price_text)
            except ValueError:
                print("Invalid price")
                continue
            if price<=0:
                print("Price must be positive number")
                continue
            if business_user.business_type=="Restaurant":
                category=input("Meal: ")
                product=Meal(name, price, category)
            else:
                product=Product(name, price)
            place.products.append(product)
            print("Product added")
        elif choose=="2":
            name=input("Product name to remove: ")
            product=place.find_product(name)
            if product is None:
                print("Product is not available")
            else:
                place.products.remove(product)
                print("Product has been removed")
        elif choose=="0":
            return
        else:
            print("Invalid choice")

def business_menu(business_user):
    while True:
        print("=== BUSINESS MENU ===")
        print("1. Manage products")
        print("2. View my orders")
        print("3. Business information")
        print("4. Log out")
        print("5. Exit")
        choose=input("Choose: ")
        if choose=="1":
            manage_business_products(business_user)
        elif choose=="2":
            for order in all_orders():
                if order.place_name==business_user.place.name:
                    order.show()
        elif choose=="3":
            print("Business:", business_user.business_name)
            print("Type:", business_user.business_type)
            print("Owner:", business_user.name)
        elif choose=="4":
            print("Logged out")
            return
        elif choose=="5":
            print("\nYour success is our success!")
            print("See you soon, friend!")
            raise SystemExit
        else:
            print("Invalid choice")

def main():
    while True:
        print("=== PICK IT UP ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choose=input("Choose: ")
        if choose=="1":
            login()
        elif choose=="2":
            registration()
        elif choose=="3":
            print("See you soon!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":main()











