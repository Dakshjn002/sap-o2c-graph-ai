# SAP Order-to-Cash (O2C) Graph Explorer & AI Assistant

### 📌 Overview
This project unifies fragmented SAP Order-to-Cash (O2C) data into a high-performance **Neo4j Graph Database**. It provides a conversational interface powered by **Google Gemini 1.5 Flash**, allowing users to query complex business flows using natural language. 

The system specifically identifies "Broken Flows"—business process gaps where sales orders have been placed but never reached the billing stage, representing potential revenue leakage.

---

### 🛠️ Tech Stack
- **Graph Database**: Neo4j AuraDB (Cloud)
- **LLM**: Google Gemini 1.5 Flash
- **Backend/UI**: Python & Streamlit
- **Language**: Cypher (Graph Query Language)
- **Environment**: Python 3.x, Dotenv, Git

---

### 🚀 Core Functionalities
1. **Graph Construction**: Ingests SAP JSONL headers and items to build a network of `SalesOrder` and `BillingDocument` nodes.
2. **NL-to-Cypher Translation**: Uses LLM prompting to translate natural language questions into structured graph queries dynamically.
3. **Process Gap Detection**: Visualizes orphaned nodes (Sales Orders without linked Invoices) to pinpoint operational inefficiencies.
4. **Domain Guardrails**: Implements strict system prompts to ensure the AI only responds to SAP-related data queries.

---

### 🔍 Example Queries Supported
- "Show me all sales orders that have not been billed yet."
- "What is the total number of billing documents in the system?"
- "List the IDs of broken process flows from November."

---

### 📁 Repository Structure
- `app.py`: Main Streamlit application and AI logic.
- `upload_to_graph.py`: Data ingestion pipeline for Neo4j.
- `requirements.txt`: Python dependencies for deployment.
- `logs/`: (Optional) AI coding session logs for evaluation.