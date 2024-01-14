import random

lst = []
books = []
carts = {}
inventory = {}
orders = []
dic={}
order_id_counter = 1
cart_changes = {}


def user_management(id, password, email):
    lst.extend([password, email])
    global dic
    dic[id] = lst
    print("Logged in successfully:")


def user_profile():
    global lst, dic
    b = input("Do you want to Edit profile? (y/n): ")
    if b == 'y':
        password = input("Edit password: ")
        email = input("Edit email: ")
        lst = [password, email]
        dic[id] = lst
        print("Profile updated successfully.")
    else:
        pass


def add_book(title, author, price, availability):
    book = {"title": title.upper(), "author": author.upper(), "price": price, "availability": availability}
    books.append(book)
    return books


def add_to_cart(title, author):
    book = next((b for b in books if b["title"].upper() == title.upper() and b["author"].upper() == author.upper()), None)
    if book:
        if book["availability"] > 0:
            if title not in carts:
                carts[title] = {"book": book, "quantity": 1}
            else:
                carts[title]["quantity"] += 1
            book["availability"] -= 1
            print(f"Book '{title}' by '{author}' added to the cart.")
        else:
            print(f"Insufficient availability for '{title}' by '{author}' in the catalog. Book not added to cart.")
            book["availability"] = 0
    else:
        print("Book not found in the catalog or is not available.")


def inventory_operations(title, author, quantity):
    for book in books:
        if book["title"].upper() == title.upper() and book["author"].upper() == author.upper():
            if book["availability"] >= quantity:
                print("Available")
                return True
            else:
                print(f"Insufficient availability for '{title}' by '{author}' in the catalog.")
                return False
    print("Book not found in the catalog.")
    return False


def process_order():
    if len(carts) > 0:
        global order_id_counter
        order_id = order_id_counter
        order = {"order_id": order_id, "items": {}}

        for title, item in carts.items():
            book = item["book"]
            quantity = item["quantity"]

            order["items"][title] = {"author": book["author"], "price": book["price"], "quantity": quantity}
        for title, item in carts.items():
            book = item["book"]
            quantity = item["quantity"]
            book["availability"] -= quantity
        orders.append(order)
        clear_cart()
        print(f"Order '{order_id}' processed successfully.")
        order_id_counter += 1
        return order_id
    else:
        print("No items in the cart to process an order.")
    return None


def remove_from_cart(title):
    if title in carts:
        if carts[title]["quantity"] > 0:
            carts[title]["quantity"] -= 1
            print("Book removed from the cart.")
            book = carts[title]["book"]
            book["availability"] += 1
            cart_changes[title] = cart_changes.get(title, 0) + 1
            if carts[title]["quantity"] == 0:
                del carts[title]
        else:
            print("Book not found in the cart.")
    else:
        print("Book not found in the cart.")


def clear_cart():
    global cart_changes
    for title, change in cart_changes.items():
        book = next((b for b in books if b["title"] == title), None)
        if book:
            book["availability"] += change
    cart_changes.clear()
    carts.clear()
    print("Cart cleared.")


def view_cart():
    if not carts:
        print("Cart is empty.")
    else:
        for book_title in carts:
            print(f"Book: {book_title}, Author: {carts[book_title]}")
        k = input("Want to remove a book? (y/n): ")
        if k == "y":
            z = input("Enter title of the book: ")
            remove_from_cart(z)
    return


def get_book_availability(title, author):
    for i in books:
        if i["title"]==title and i["author"]==author:
            return True
    return False


def generate_invoice(order_id):
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if order:
        print(f"Generating invoice for Order '{order_id}'")
        total_price = 0
        print("Order details:")
        for title, item in order["items"].items():
            author = item["author"]
            price = int(item["price"])
            quantity = item["quantity"]
            book_total = price * quantity
            total_price += book_total
            print(f"Title: {title}, Author: {author}, Quantity: {quantity}, Price: {price} USD, Total: {book_total} USD")

        print(f"Total: {total_price} USD")
    else:
        print("Order not found.")


def display_available_books():
    print("Available Books:")
    for book in books:
        print(f"Title: {book['title']}, Author: {book['author']}, Price: {book['price']}, Availability: {book['availability']}")


def Book():
    display_available_books()
    title = input("What book would you like to purchase? ")
    author = input("Author of the book? ")
    quantity = 1
    a = inventory_operations(title, author, quantity)
    if a:
        b = input("Add to cart? (y/n): ")
        if b == 'y':
            add_to_cart(title, author)
    else:
        print("Book not added to cart. It is either not available or does not exist in the catalog.")

#already added books
add_book("House of Flame and Shadow", "Sarah J. Maas", 300, 3)
add_book("Iron Flame", "Rebecca Yarros", 550, 3)
add_book("Happy Place", "Emily Henry", 700, 2)
add_book("Hell Bent", "Leigh Bardugo", 400, 1)
add_book("ABSALOM, ABSALOM!", "WILLIAM FAULKNER", 730, 3)
add_book("A TIME TO KILL", "JOHN GRISHAM", 600, 2)
add_book("EAST OF EDEN", "JOHN STEINBECK", 340, 2)


print("Welcome")
id = random.randrange(100)
password = input("Enter password: ")
email = input("Enter Email: ")
user_management(id, password, email)


if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("0: Manage Profile")
        print("1: Select book")
        print("2: View cart")
        print("3: Clear cart")
        print("4: Checkout")
        print("5: Exit")

        choice = input("Enter your choice: ")

        if choice == "0":
            user_profile()
        elif choice == "1":
            Book()
        elif choice == "2":
            view_cart()
        elif choice == "3":
            clear_cart()
        elif choice == "4":
            val = process_order()
            if val:
                generate_invoice(val)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")