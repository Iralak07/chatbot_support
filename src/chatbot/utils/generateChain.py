import time
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from models.model_groq import groq_client

llm = groq_client()


prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Eres un asistente experto en facturación electrónica en Paraguay.  
    - Usa exclusivamente la información proporcionada en los documentos para responder.  
    - Si la respuesta no está en los documentos, responde con: "No tengo información suficiente para responder esa pregunta."  
    - Proporciona una respuesta clara y detallada con ejemplos si es posible.  
    - Mantén un tono profesional y preciso.  
      
    <|eot_id|><|start_header_id|>user<|end_header_id|>  
    Pregunta: {question}  
    Contexto:  
    \n ------- \n  
    {context}  
    \n ------- \n  
      
    Respuesta detallada: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "context"],
)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Chain
start = time.time()
rag_chain = prompt | llm | StrOutputParser()

