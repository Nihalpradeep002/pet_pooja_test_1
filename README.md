Petpooja Sales Data Integration (Python + SQLite)

This project fetches sales data from the Petpooja API and stores it in a SQLite database using Python.

IMPORTANT: This script will not add duplicate records based on receipt number


Install the necessary libraries
Libraries used:
requests
sqlite3
python-dotenv


Project Structure:
petpooja/
│
├── fetch_sales_data.py   # Main Python script
├── sales_data.db         # SQLite database 
├── .env                  # Environment variables 
├── README.md             # Project documentation




How to Run
Run the script:
C:/Python313/python.exe fetch_sales_data.py



Database Schema
Table: sales_data

Column	Type
id	INTEGER PRIMARY KEY AUTOINCREMENT
receipt_number	TEXT
sale_date	TEXT
transaction_time	TEXT
sale_amount	REAL
tax_amount	REAL
discount_amount	REAL
round_off	REAL
net_sale	REAL
payment_mode	TEXT
order_type	TEXT
transaction_status	TEXT
 API → Database Mapping
API Field	DB Column
Receipt number	receipt_number
Receipt Date	sale_date
Transaction Time	transaction_time
Invoice amount	sale_amount
Tax amount	tax_amount
Discount amount	discount_amount
Round Off	round_off
Net sale	net_sale
Payment Mode	payment_mode
Order Type	order_type
Transaction status	transaction_status
