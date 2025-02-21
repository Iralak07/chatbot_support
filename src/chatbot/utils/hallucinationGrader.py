import time
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.model_groq import groq_client
from database.qdrantDB import qdrant_client
from chatbot.utils.generateChain import rag_chain, format_docs
llm = groq_client()
# Conectar con Qdrant
vector_store = qdrant_client()
retriever= vector_store.as_retriever(search_kwargs={"k":2})

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Eres un evaluador experto en determinar si una respuesta sobre facturación electrónica en Paraguay está basada en los hechos proporcionados.  
    - Compara la respuesta generada con los documentos de referencia.  
    - La respuesta es respaldada si su contenido coincide con la información proporcionada en los documentos o es una reformulación fiel de los mismos.  
    - La respuesta NO es respaldada si:
      - Contiene información no presente en los documentos.
      - Hace afirmaciones incorrectas o extrapola más allá de los hechos proporcionados.
      - Incluye interpretaciones subjetivas o especulativas.  
      - No está relacionada con los siguientes temas:  
        - Facturación electrónica, incluyendo estructura, subsistemas y regulaciones (SIFEN).  
        - Documentos tributarios electrónicos (DTE), comprobantes, notas de remisión y validaciones.  
        - Modelos operativos, flujos de aprobación y transmisión de documentos electrónicos.  
        - Características tecnológicas, estándares XML, firma digital y certificados.  
        - Servicios web del SIFEN, protocolos de comunicación y validaciones.  
        - Gestión de eventos, cancelaciones, conformidad/disconformidad y notificaciones.  
        - Estructura y generación del Código de Control (CDC), código QR y KUDE.  

    Devuelve un JSON con una única clave 'score', cuyo valor será:  
    - 'yes' si la respuesta está respaldada por los documentos.  
    - 'no' si la respuesta no está respaldada por los documentos.  
    No incluyas explicaciones ni preámbulos.  

    Hechos proporcionados:  
    \n ------- \n  
    {documents}  
    \n ------- \n  

    Respuesta generada:  
    {generation}  
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["generation", "documents"],
)

hallucination_grader = prompt | llm | JsonOutputParser()



# question = "¿Qué es la factura electronica?"
# retrieved_docs = retriever.invoke(question)
# # Paso 2: Generar respuesta
# context = format_docs(retrieved_docs)
# generation = rag_chain.invoke({"question": question, "context": context})
# # Paso 3: Evaluar si la respuesta está respaldada por los hechos
# hallucination_grader= hallucination_grader.invoke({"documents": retrieved_docs, "generation": generation})
