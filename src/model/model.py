from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import GEMINI_API_KEY

# Initialize gemini model
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # model name
    temperature=0.2,  # temperature for the model
    max_tokens=None,  # max tokens for the model
    timeout=None,  # timeout for the model
    max_retries=2,  # max retries for the model
    google_api_key=GEMINI_API_KEY,
)
