import streamlit as st
import os
import google.generativeai as genai
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

# Config
genai.configure(api_key=st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

URI = st.secrets["NEO4J_URI"] if "NEO4J_URI" in st.secrets else os.getenv("NEO4J_URI")
AUTH = (
    st.secrets["NEO4J_USERNAME"] if "NEO4J_USERNAME" in st.secrets else os.getenv("NEO4J_USERNAME"),
    st.secrets["NEO4J_PASSWORD"] if "NEO4J_PASSWORD" in st.secrets else os.getenv("NEO4J_PASSWORD")
)

def run_query(cypher):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session() as session:
            result = session.run(cypher)
            return [record.data() for record in result]

# --- UI ---
st.set_page_config(page_title="SAP Graph AI", layout="wide")
st.title("🚀 SAP Order-to-Cash Graph Explorer")
st.markdown("Identify broken process flows using Natural Language.")

user_input = st.text_input("Ask a question (e.g., 'Show me Sales Orders missing Billing Documents')")

if user_input:
    sys_prompt = f"""
    You are a Neo4j Cypher expert. 
    Schema: 
    - Nodes: SalesOrder {{id, date}}, BillingDocument {{id}}
    - Relationship: (SalesOrder)-[:HAS_BILL_DOC]->(BillingDocument)
    
    Task: Convert the user's question into a Cypher query.
    If the question is not about the dataset, reply 'OFF_TOPIC'.
    Output: Return ONLY the Cypher query.
    
    User Question: {user_input}
    """
    
    response = model.generate_content(sys_prompt).text.strip().replace('```cypher', '').replace('```', '')
    
    if "OFF_TOPIC" in response:
        st.error("⚠️ This assistant only handles SAP O2C data queries.")
    else:
        st.info(f"Generated Cypher: {response}")
        try:
            results = run_query(response)
            if results:
                st.success(f"Found {len(results)} records")
                st.table(results)
            else:
                st.warning("No data found for this query.")
        except Exception as e:
            st.error(f"Execution Error: {e}")