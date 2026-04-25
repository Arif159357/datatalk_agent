# Local Installation & Setup

Follow these steps to get DataTalk running on your local machine.

## 1. Prerequisites
- **Python 3.10+**
- **Docker** and **Docker Compose**
- **Google Gemini API Key** (Get it from [Google AI Studio](https://aistudio.google.com/))

## 2. Setting Up the Database
DataTalk uses the Northwind dataset. We have provided a `docker-compose.yml` to spin up the database and pre-load the schema.

```bash
# From the root directory
docker-compose up -d
```
This will start:
- **Postgres**: Accessible on port `5432`
  
## 3. Python Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Environment Variables:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   DATABASE_URL="postgresql://postgres:postgres@localhost:55432/northwind"
   ```

## 4. Running the Application
You need to run both the API (Backend) and the Streamlit App (Frontend).

### Start the Backend (FastAPI)
```bash
python src/api.py
```
*The API will be available at `http://localhost:5000`*

### Start the Frontend (Streamlit)
```bash
cd src
streamlit run app.py --server.address=0.0.0.0 --server.port=8080
```
