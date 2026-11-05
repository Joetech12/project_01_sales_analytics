
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


# Reproducible random data
random.seed(42)

# Resolve the project root from this file's location
PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "sales_data.csv"


PRODUCTS = [
    {
        "product_id": "PRD001",
        "product_name": "Wireless Headphones",
        "category": "Electronics",
        "unit_price": 85000,
        "unit_cost": 52000,
    },
    {
        "product_id": "PRD002",
        "product_name": "Bluetooth Speaker",
        "category": "Electronics",
        "unit_price": 65000,
        "unit_cost": 38000,
    },
    {
        "product_id": "PRD003",
        "product_name": "Smart Watch",
        "category": "Electronics",
        "unit_price": 120000,
        "unit_cost": 80000,
    },
    {
        "product_id": "PRD004",
        "product_name": "Office Chair",
        "category": "Furniture",
        "unit_price": 175000,
        "unit_cost": 110000,
    },
    {
        "product_id": "PRD005",
        "product_name": "Study Desk",
        "category": "Furniture",
        "unit_price": 220000,
        "unit_cost": 145000,
    },
    {
        "product_id": "PRD006",
        "product_name": "Running Shoes",
        "category": "Fashion",
        "unit_price": 95000,
        "unit_cost": 58000,
    },
    {
        "product_id": "PRD007",
        "product_name": "Leather Backpack",
        "category": "Fashion",
        "unit_price": 70000,
        "unit_cost": 42000,
    },
    {
        "product_id": "PRD008",
        "product_name": "Air Fryer",
        "category": "Home Appliances",
        "unit_price": 135000,
        "unit_cost": 90000,
    },
    {
        "product_id": "PRD009",
        "product_name": "Electric Kettle",
        "category": "Home Appliances",
        "unit_price": 35000,
        "unit_cost": 21000,
    },
    {
        "product_id": "PRD010",
        "product_name": "Water Bottle",
        "category": "Accessories",
        "unit_price": 12000,
        "unit_cost": 5000,
    },
]

CUSTOMERS = [
    ("CUST001", "John Okafor", "john@example.com"),
    ("CUST002", "Mary Adeyemi", "mary@example.com"),
    ("CUST003", "David Eze", "david@example.com"),
    ("CUST004", "Grace Ibrahim", "grace@example.com"),
    ("CUST005", "Daniel Musa", "daniel@example.com"),
    ("CUST006", "Sarah Bello", "sarah@example.com"),
    ("CUST007", "Peter Nwosu", "peter@example.com"),
    ("CUST008", "Esther James", "esther@example.com"),
    ("CUST009", "Michael Obi", "michael@example.com"),
    ("CUST010", "Ruth Adebayo", "ruth@example.com"),
    ("CUST011", "Samuel Udo", "samuel@example.com"),
    ("CUST012", "Faith Chukwu", "faith@example.com"),
    ("CUST013", "Emeka Nnamdi", "emeka@example.com"),
    ("CUST014", "Blessing Yusuf", "blessing@example.com"),
    ("CUST015", "Joseph Ojo", "joseph@example.com"),
]

LOCATIONS = [
    ("Lagos", "Lagos"),
    ("Ikeja", "Lagos"),
    ("Abuja", "FCT"),
    ("Port Harcourt", "Rivers"),
    ("Ibadan", "Oyo"),
    ("Enugu", "Enugu"),
    ("Benin City", "Edo"),
    ("Kano", "Kano"),
    ("Uyo", "Akwa Ibom"),
    ("Owerri", "Imo"),
]

PAYMENT_METHODS = [
    "Card",
    "Bank Transfer",
    "USSD",
    "Cash on Delivery",
]

ORDER_STATUSES = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Processing",
    "Shipped",
    "Cancelled",
    "Returned",
]


def generate_sales_data(number_of_records: int = 1000) -> pd.DataFrame:
    """Generate synthetic eCommerce sales records."""

    records = []

    start_date = datetime(2025, 1, 1)

    for index in range(number_of_records):
        product = random.choice(PRODUCTS)
        customer = random.choice(CUSTOMERS)
        city, state = random.choice(LOCATIONS)

        order_date = start_date + timedelta(
            days=random.randint(0, 364),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        quantity = random.randint(1, 5)
        discount = random.choice([0, 0, 0, 5, 10, 15, 20])

        record = {
            "order_id": f"ORD{index + 1:05d}",
            "order_date": order_date,
            "customer_id": customer[0],
            "customer_name": customer[1],
            "email": customer[2],
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "quantity": quantity,
            "unit_price": product["unit_price"],
            "unit_cost": product["unit_cost"],
            "discount": discount,
            "payment_method": random.choice(PAYMENT_METHODS),
            "order_status": random.choice(ORDER_STATUSES),
            "city": city,
            "state": state,
        }

        records.append(record)

    df = pd.DataFrame(records)

    # Introduce intentional data-quality issues.
    if len(df) >= 10:
        df.loc[3, "email"] = None
        df.loc[8, "city"] = None
        df.loc[12, "quantity"] = None

        # Duplicate an order reference.
        df.loc[20, "order_id"] = df.loc[19, "order_id"]

    return df


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_sales_data()

    df.to_csv(OUTPUT_FILE, index=False)

    print("Sales dataset generated successfully.")
    print(f"Records: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
