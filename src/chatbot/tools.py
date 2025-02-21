import requests
import json
import os
import dotenv
dotenv.load_dotenv()


# Definir herramienta de búsqueda
def search_google_serper(query: str):
    try:
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query,
            "gl": "py",
            "hl": "es"
        })
        headers = {
            'X-API-KEY': os.environ.get('serper_api'),
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        return response.json()  

    except Exception as e:
        return {"error": str(e)}
    


from langchain_community.tools import TavilySearchResults

web_search_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    api_key=os.environ.get('TAVILY_API_KEY'),
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)