# DataTalk: Natural Language Data Intelligence

DataTalk is an AI-powered analytical agent designed to make the Northwind B2B sales dataset accessible to non-technical business users. Using a dual-LLM architecture, it translates natural language questions into accurate SQL queries and dynamic visualizations.

## 🚀 Key Features
- **Query Intelligence**: Automatically refines vague user questions.
- **Data Storytelling**: Detects visualization intent and generates real-time charts (Matplotlib) based on query results.
- **SQL Agent Architecture**: Uses LangChain tool-calling for reliable schema inspection and query execution on PostgreSQL.
- **UI**: Built with Streamlit and custom CSS for a professional look and feel.

## 📂 Documentation Links
- [**Local Installation Guide**](./INSTALLATION.md) - Detailed steps for local environment setup.
- [**Docker Changes**](./DOCKER_CHANGES.md) - Summary of database fixes.
- [**Deployment Status**](./DEPLOYMENT.md) - Cloud deployment tracking and final live link.

## 🛠 Tech Stack
- **LLMs:** Google Gemini 3 Pro (Complex Reasoning) & Flash (Utility Tasks)
- **Frameworks:** LangChain, FastAPI, Streamlit
- **Database:** PostgreSQL (Northwind)
- **Visualization:** Matplotlib

---

## 🧠 Technical Deep-Dive

### 1. The "Query Analyst" Pattern (Query Intelligence)
- **Decision:** I implemented a pre-processing step that uses Gemini Flash to "refine" user questions before they hit the SQL Agent.
- **Trade-off:** This adds a small amount of latency (1-2s), but significantly increases reliability for vague queries like *"compare this year to last."* It’s a trade-off of speed for accuracy.

### 2. Schema Scaling
- **Decision:** The full Northwind schema is provided to the agent context.
- **Limitation:** This works for Northwind's size. For an Enterprise DB with hundreds of tables, the next step would be implementing **Metadata RAG** to retrieve only relevant schemas based on the question intent.


---
*Developed for the Altri Technical Lead Assessment.*

