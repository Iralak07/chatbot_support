from langchain_groq import ChatGroq

def groq_client():
    return ChatGroq(
        model="Llama3-8b-8192", 
        api_key="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"
    )
     