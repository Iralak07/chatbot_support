import time
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.model_groq import groq_client
from database.qdrantDB import qdrant_client



llm = groq_client()


prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Eres un evaluador experto en determinar la relevancia de documentos sobre facturación electrónica en Paraguay.  
    Evalúa si el documento recuperado es útil para responder la pregunta del usuario.  
    - El documento proviene del manual técnico del Sistema Integrado de Facturación Electrónica Nacional (SIFEN).  
    - El manual cubre los siguientes temas (índice del manual):
      1. Introducción, objetivos y alcance del SIFEN.
      2. Estructura y subsistemas del SIFEN.
      3. Documentos Tributarios Electrónicos (DTE): Comprobantes de ventas, documentos complementarios y Nota de Remisión Electrónica.
      4. Modelo Operativo: Descriptores, plazos de transmisión, relación con contribuyentes, entrega y rechazo de DTE.
      5. Características tecnológicas: Formato XML, firma digital, certificados digitales, estándares de comunicación.
      6. Servicios Web del SIFEN: Recepción de documentos, consulta de lotes, consulta de RUC, recepción de eventos.
      7. Gestión de eventos: Inutilización, cancelación, devolución, conformidad, disconformidad, desconocimiento de DTE.
      8. Validaciones: Estructura de códigos de validación, validaciones de servicios web y formatos.
      9. Gráfica (KUDE): Definición, estructura, campos, código QR y cinta de papel.
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
