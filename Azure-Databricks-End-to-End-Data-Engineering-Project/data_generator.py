import pandas as pd
import random
from faker import Faker

fake = Faker()

# -----------------------------
# 1. Customers (100 rows)
# -----------------------------
def generate_customers(n=100):
    customers = []
    for i in range(n):
        first = fake.first_name()
        last = fake.last_name()

        customers.append({
            "customer_id": i + 1,
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{random.randint(1,99)}@{fake.free_email_domain()}",
            "country": fake.country()
        })
    return pd.DataFrame(customers)

# -----------------------------
# 2. Products (100 rows realistic)
# -----------------------------
def generate_products(n=100):
    base_products = [
        ("iPhone", "Electronics"),
        ("Samsung Galaxy", "Electronics"),
        ("Laptop", "Electronics"),
        ("Headphones", "Electronics"),
        ("T-Shirt", "Clothing"),
        ("Jeans", "Clothing"),
        ("Jacket", "Clothing"),
        ("Sneakers", "Clothing"),
        ("Dining Table", "Home"),
        ("Office Chair", "Home"),
        ("Cookware Set", "Home"),
        ("Bookshelf", "Home"),
        ("Football", "Sports"),
        ("Cricket Bat", "Sports"),
        ("Tennis Racket", "Sports"),
        ("Yoga Mat", "Sports"),
        ("Novel Book", "Books"),
        ("Science Book", "Books"),
        ("Notebook", "Books"),
        ("Backpack", "Accessories")
    ]

    brands = ["Nike", "Adidas", "Apple", "Samsung", "Sony", "Dell", "HP", "Puma", "Lenovo"]

    products = []
    for i in range(n):
        base, category = random.choice(base_products)
        brand = random.choice(brands)

        products.append({
            "product_id": i + 1,
            "product_name": f"{brand} {base}",
            "category": category,
            "price": round(random.uniform(10, 1500), 2)
        })

    return pd.DataFrame(products)

# -----------------------------
# 3. Orders (100 rows)
# -----------------------------
def generate_orders(customers_df, products_df, n=100):
    orders = []

    for i in range(n):
        orders.append({
            "order_id": i + 1,
            "customer_id": random.choice(customers_df["customer_id"].tolist()),
            "product_id": random.choice(products_df["product_id"].tolist()),
            "quantity": random.choices([1, 2, 3, 4], weights=[65, 20, 10, 5])[0],
            "order_date": fake.date_between(start_date='-6M', end_date='today')
        })

    return pd.DataFrame(orders)

# -----------------------------
# Generate datasets
# -----------------------------
customers_df = generate_customers(100)
products_df = generate_products(100)
orders_df = generate_orders(customers_df, products_df, 100)

# -----------------------------
# Save CSV files
# -----------------------------
customers_df.to_csv("customers.csv", index=False)
products_df.to_csv("products.csv", index=False)
orders_df.to_csv("orders.csv", index=False)

print("Generated 100 rows for each dataset!")