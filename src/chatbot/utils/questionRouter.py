import time
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.model_groq import groq_client

llm = groq_client()

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Eres un experto en enrutar preguntas de usuarios hacia la fuente de información más adecuada.  
    - Usa la base de datos vectorial (vectorstore) si la pregunta está relacionada con:
      - Facturación electrónica, incluyendo estructura, subsistemas y regulaciones (SIFEN).
      - Documentos tributarios electrónicos (DTE), comprobantes, notas de remisión y validaciones.
      - Modelos operativos, flujos de aprobación y transmisión de documentos electrónicos.
      - Características tecnológicas, estándares XML, firma digital y certificados.
      - Servicios web del SIFEN, protocolos de comunicación y validaciones.
      - Gestión de eventos, cancelaciones, conformidad/disconformidad y notificaciones.
      - Estructura y generación del Código de Control (CDC), código QR y KUDE.
    - Si la pregunta no está relacionada con estos temas, usa la búsqueda web.  
    - No es necesario que seas estricto con las palabras clave; comprende el contexto general de la pregunta.  
    - Si la pregunta es ambigua, prioriza la base de datos vectorial.  
    Devuelve un JSON con una única clave 'datasource', cuyo valor será 'vectorstore' o 'web_search', sin preámbulos ni explicaciones.  

    Pregunta a enrutar: {question}  
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question"],
)

question_router = prompt | llm | JsonOutputParser()

