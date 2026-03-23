import os
import json
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

# Connect to Neo4j
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
driver = GraphDatabase.driver(URI, auth=AUTH)

def upload_billing_data(tx, record):
    # This Cypher query creates a 'BillingDocument' node
    # It uses 'MERGE' to avoid creating the same document twice
    query = """
    MERGE (b:BillingDocument {id: $doc_id})
    SET b.type = $doc_type, 
        b.date = $doc_date, 
        b.status = 'Cancelled'
    """
    tx.run(query, 
           doc_id=record.get('billingDocument'),
           doc_type=record.get('billingDocumentType'),
           doc_date=record.get('billingDocumentDate'))

# Path to your specific file from the screenshot
file_path = "data/billing_document_cancellations/part-20251119-133433-51.jsonl"

print("🚀 Starting upload...")

with driver.session() as session:
    with open(file_path, 'r') as f:
        for line in f:
            record = json.loads(line)
            session.execute_write(upload_billing_data, record)

print("✅ Data uploaded to Neo4j successfully!")
driver.close()