from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
    
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")


llm = init_chat_model(
    model="gpt-4o",
    model_provider="openai",
    base_url = BASE_URL,
    api_key = API_KEY
)
