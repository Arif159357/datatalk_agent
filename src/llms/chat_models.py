from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    temperature=0,
)