import time
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.model_groq import groq_client
from database.qdrantDB import qdrant_client


llm = groq_client()
# Conectar con Qdrant
vector_store = qdrant_client()
retriever= vector_store.as_retriever(search_kwargs={"k":2})

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Eres un evaluador experto en facturación electrónica en Paraguay.  
    Tu tarea es determinar si una respuesta es útil para resolver una pregunta.  
    - Si la respuesta responde claramente la pregunta con información relevante, califícala como 'yes'.  
    - Si la respuesta es vaga, incorrecta o irrelevante, califícala como 'no'.  
    - No incluyas explicaciones ni preámbulos, solo devuelve el JSON solicitado.  
      
    <|eot_id|><|start_header_id|>user<|end_header_id|>  
    Pregunta: {question}  
    \n ------- \n  
    Respuesta: {generation}  
    \n ------- \n  
      
    Devuelve un JSON con la clave 'score' y el valor correspondiente.  
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["generation", "question"],
)

answer_grader = prompt | llm | JsonOutputParser()



# question = "Que es la facturacion electronica?"
# generation = retriever.invoke(question)
# start = time.time()
# answer_grader_response = answer_grader.invoke({"question": question,"generation": generation})
# # end = time.time()
# # print(f"El tiempo requerido para generar la respuesta por el answer grader en segundos:{end - start}")
# # print(answer_grader_response)