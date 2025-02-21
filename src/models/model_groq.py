from langchain_groq import ChatGroq
import os
import dotenv
dotenv.load_dotenv()

def groq_client():
    return ChatGroq(
        model="Llama3-8b-8192", 
        api_key=os.environ.get("GRAQ_API_KEY")
    )
     