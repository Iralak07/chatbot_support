import time
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.model_groq import groq_client
from database.qdrantDB import qdrant_client



llm = groq_client()


# Conectar con Qdrant
vector_store = qdrant_client()
retrieve = vector_store.as_retriever(search_kwargs={"k":4})

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Eres un evaluador experto en determinar la relevancia de documentos sobre facturación electrónica en Paraguay.  
    Evalúa si el documento recuperado es útil para responder la pregunta del usuario.  
    - El documento proviene del manual técnico del Sistema Integrado de Facturación Electrónica Nacional (SIFEN).  
    - Un documento es relevante si contiene información específica sobre:
      - Facturación electrónica y su estructura en Paraguay.
      - Documentos tributarios electrónicos (DTE) y sus validaciones.
      - Modelos operativos, firma digital, protocolos de comunicación y SIFEN.
      - Código de Control (CDC), código QR, KUDE y eventos asociados.
    - Si el documento no cubre estos temas o su contenido no responde directamente a la pregunta del usuario, márcalo como no relevante.  
    - El objetivo es filtrar recuperaciones incorrectas o no útiles.  

    Devuelve un JSON con una única clave 'score', cuyo valor será:  
    - 'yes' si el documento es relevante.  
    - 'no' si el documento no es relevante.  
    No incluyas explicaciones ni preámbulos.  

    Documento recuperado:  
    {document}  

    Pregunta del usuario:  
    {question}  
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "document"],
)

retrieval_grader = prompt | llm | JsonOutputParser()

# question = "Que es la facturacion electronica?"
# docs = retrieve.invoke(question)
# print(prompt.template)
# doc_txt = docs[1].page_content
# print(retrieval_grader.invoke({"question": question, "document": doc_txt}))
# end = time.time()
# print(f"The time required to generate response by the retrieval grader in seconds:{end - start}")
