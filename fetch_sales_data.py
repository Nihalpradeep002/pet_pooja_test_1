import requests
import sqlite3
import time
import os
from dotenv import load_dotenv

load_dotenv()
# -------------------------------
# Read credentials from env vars
# -------------------------------
APP_KEY = os.getenv("PETPOOJA_APP_KEY")
APP_SECRET = os.getenv("PETPOOJA_APP_SECRET")
ACCESS_TOKEN = os.getenv("PETPOOJA_ACCESS_TOKEN")
REST_ID = os.getenv("PETPOOJA_REST_ID")

if not all([APP_KEY, APP_SECRET, ACCESS_TOKEN, REST_ID]):
    raise EnvironmentError("Missing one or more API environment variables")

# -------------------------------
# API URL
# -------------------------------
API_URL = (
    "http://api.petpooja.com/V1/orders/get_sales_data/"
    f"?app_key={APP_KEY}"
    f"&app_secret={APP_SECRET}"
    f"&access_token={ACCESS_TOKEN}"
    f"&restID={REST_ID}"
    "&from_date=2025-01-20%2000:00:00"
    "&to_date=2025-01-20%2023:59:59"
)

# -------------------------------
# Connect to SQLite
# -------------------------------
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()
print("Connected to SQLite database")

# -------------------------------
# Create table
# -------------------------------
cursor.execute(
    "CREATE TABLE IF NOT EXISTS sales_data ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "receipt_number TEXT UNIQUE, "
    "sale_date TEXT, "
    "transaction_time TEXT, "
    "sale_amount REAL, "
    "tax_amount REAL, "
    "discount_amount REAL, "
    "round_off REAL, "
    "net_sale REAL, "
    "payment_mode TEXT, "
    "order_type TEXT, "
    "transaction_status TEXT)"
)

# -------------------------------
# Fetch sales data (with retry)
# -------------------------------
def fetch_sales_data(retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            print(f"Fetching data (Attempt {attempt})...")
            response = requests.get(API_URL, timeout=30)
            response.raise_for_status()

            records = response.json().get("Records", [])
            print(f"Fetched {len(records)} records from API")
            return records

        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")

        except ValueError:
            print("Invalid JSON response")

        if attempt < retries:
            print(f"Retrying in {delay} seconds...\n")
            time.sleep(delay)

    print("Failed to fetch data after multiple attempts")
    return []

# -------------------------------
# Insert data into database
# -------------------------------
def insert_sales_data(records):
    if not records:
        print("No data to insert")
        return

    query = (
        "INSERT OR IGNORE INTO sales_data (receipt_number, sale_date, transaction_time, "
        "sale_amount, tax_amount, discount_amount, round_off, net_sale, "
        "payment_mode, order_type, transaction_status) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )

    try:
        for r in records:
            cursor.execute(query, (
                r.get("Receipt number", "Unknown"),
                r.get("Receipt Date", "N/A"),
                r.get("Transaction Time", "N/A"),
                float(r.get("Invoice amount", 0) or 0),
                float(r.get("Tax amount", 0) or 0),
                float(r.get("Discount amount", 0) or 0),
                float(r.get("Round Off", 0) or 0),
                float(r.get("Net sale", 0) or 0),
                r.get("Payment Mode", "Unknown"),
                r.get("Order Type", "Unknown"),
                r.get("Transaction status", "Unknown"),
            ))

        conn.commit()
        print("Sales data inserted successfully")

    except sqlite3.DatabaseError as e:
        conn.rollback()
        print("Database error:", e)

# -------------------------------
# Main
# -------------------------------
def main():
    try:
        records = fetch_sales_data()
        insert_sales_data(records)
    finally:
        conn.close()
        print("Database connection closed")

# -------------------------------
# Run
# -------------------------------
main()
