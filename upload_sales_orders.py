import os
import json
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
driver = GraphDatabase.driver(URI, auth=AUTH)

def upload_sales_header(tx, record):
    # This creates the SalesOrder node
    query = """
    MERGE (s:SalesOrder {id: $so_id})
    SET s.type = $so_type, 
        s.date = $so_date,
        s.currency = $currency
    """
    tx.run(query, 
           so_id=record.get('salesOrder'),
           so_type=record.get('salesOrderType'),
           so_date=record.get('salesOrderDate'),
           currency=record.get('transactionCurrency'))

# Your specific path
file_path = "data/sales_order_headers/part-20251119-133429-440.jsonl"

print("📦 Uploading Sales Order Headers...")

with driver.session() as session:
    with open(file_path, 'r') as f:
        for line in f:
            record = json.loads(line)
            session.execute_write(upload_sales_header, record)

print("✅ Sales Orders uploaded successfully!")
driver.close()