import streamlit as st
import os
import google.generativeai as genai
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load local .env for testing, Streamlit Cloud will use st.secrets
load_dotenv()

# --- Configuration & AI Setup ---
# This looks for keys in Streamlit Secrets first, then local Environment Variables
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Fixed the 'NotFound' error by using the full model path string
model = genai.GenerativeModel('models/gemini-1.5-flash-001')

# Database Credentials
URI = st.secrets.get("NEO4J_URI") or os.getenv("NEO4J_URI")
USER = st.secrets.get("NEO4J_USERNAME") or os.getenv("NEO4J_USERNAME", "neo4j")
PWD = st.secrets.get("NEO4J_PASSWORD") or os.getenv("NEO4J_PASSWORD")

def run_query(cypher):
    """Executes the Cypher query against Neo4j AuraDB"""
    try:
        with GraphDatabase.driver(URI, auth=(USER, PWD)) as driver:
            with driver.session() as session:
                result = session.run(cypher)
                return [record.data() for record in result]
    except Exception as e:
        return f"Database Error: {str(e)}"

# --- Streamlit UI ---
st.set_page_config(page_title="SAP Graph AI", layout="wide")
st.title("🚀 SAP Order-to-Cash Graph Explorer")
st.markdown("Query your SAP Graph using Natural Language to find process gaps.")

user_input = st.text_input("Ask a question (e.g., 'List SalesOrders with no BillingDocument')")

if user_input:
    # Strict prompt to ensure Gemini behaves as a Cypher translator
    sys_prompt = f"""
    You are a Neo4j Cypher expert for SAP O2C data.
    Schema:
    - Nodes: SalesOrder {{id, date}}, BillingDocument {{id}}
    - Relationship: (SalesOrder)-[:HAS_BILL_DOC]->(BillingDocument)
    
    Task: Convert the user's question into a valid Cypher query.
    Rules:
    - If the user asks for 'broken flows' or 'missing billing', use: MATCH (s:SalesOrder) WHERE NOT (s)-[:HAS_BILL_DOC]->() RETURN s.id
    - Return ONLY the Cypher query text. No markdown formatting.
    - If the question is irrelevant to SAP O2C, return 'OFF_TOPIC'.
    
    User Question: {user_input}
    """
    
    with st.spinner("Generating Graph Query..."):
        # Generate and clean the response
        raw_response = model.generate_content(sys_prompt).text.strip()
        clean_query = raw_response.replace('```cypher', '').replace('```', '').strip()
    
    if "OFF_TOPIC" in clean_query:
        st.error("⚠️ This assistant only handles SAP O2C data queries.")
    else:
        st.code(clean_query, language="cypher")
        
        with st.spinner("Fetching data from Neo4j..."):
            results = run_query(clean_query)
            
            if isinstance(results, str): # Error message
                st.error(results)
            elif results:
                st.success(f"Found {len(results)} records")
                st.table(results)
            else:
                st.warning("No data matches this query in the graph.")

# Footer info
st.sidebar.info("Connected to Neo4j AuraDB & Gemini 1.5 Flash")