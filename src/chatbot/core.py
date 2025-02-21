# Importaciones necesarias
from models.model_groq import groq_client  # Cliente para interactuar con el modelo Groq
from database.qdrantDB import qdrant_client  # Cliente para interactuar con la base de datos vectorial Qdrant
from typing_extensions import TypedDict  # Para definir tipos de datos estructurados
from typing import List  # Para trabajar con listas
from chatbot.utils.questionRouter import prompt  # Plantilla de prompt para el enrutamiento de preguntas
from chatbot.utils.generateChain import rag_chain, format_docs  # Cadena de generación y función para formatear documentos
from chatbot.utils.retrievalGrader import retrieval_grader  # Evaluador de relevancia de documentos
from chatbot.tools import web_search_tool  # Herramienta para realizar búsquedas web
from langchain.schema import Document  # Esquema para documentos
from chatbot.utils.questionRouter import question_router
from chatbot.utils.hallucinationGrader import hallucination_grader
from chatbot.utils.answerGrader import answer_grader
from langgraph.graph import END, StateGraph

### Estado del Grafo
class GraphState(TypedDict):
    """
    Define el estado del grafo, que incluye:
    - question: La pregunta del usuario.
    - generation: La respuesta generada por el modelo.
    - web_search: Indica si se debe realizar una búsqueda web.
    - documents: Lista de documentos recuperados.
    """
    question: str
    generation: str
    web_search: str
    documents: List[str]
    context: str

# Inicialización de clientes
vector_store = qdrant_client()  # Conectar con la base de datos vectorial Qdrant
model = groq_client()  # Inicializar el cliente del modelo Groq

# Configurar el retriever para recuperar documentos
retriever = vector_store.as_retriever(search_kwargs={"k": 2})  # Recupera los 2 documentos más relevantes

# Función para recuperar documentos desde Qdrant
def retrieve(state):
    """
    Recupera documentos relevantes desde la base de datos vectorial basados en la pregunta del usuario.

    Args:
        state (dict): El estado actual del grafo.

    Returns:
        state (dict): Nuevo campo añadido al estado, 'documents', que contiene los documentos recuperados.
    """
    print("---RECUPERAR DOCUMENTOS---")
    question = state["question"]

    # Recuperación de documentos
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

# Función para generar una respuesta usando RAG
def generate(state):
    """
    Genera una respuesta utilizando el modelo RAG (Retrieval-Augmented Generation) sobre los documentos recuperados.

    Args:
        state (dict): El estado actual del grafo.

    Returns:
        state (dict): Nuevo campo añadido al estado, 'generation', que contiene la respuesta generada por el LLM.
    """
    print("---GENERAR RESPUESTA---")
    question = state["question"]
    documents = state["documents"]
    
    # formatear el documento
    context = format_docs(documents)

    
    # Generación de la respuesta usando RAG
    generation = rag_chain.invoke({"documents": documents, "question": question, "context": context})
    return {"documents": documents, "question": question, "generation": generation}

# Función para evaluar la relevancia de los documentos
def grade_documents(state: GraphState):
    """
    Determina si los documentos recuperados son relevantes para la pregunta.
    Si ningún documento es relevante, se activa una bandera para realizar una búsqueda web.

    Args:
        state (dict): El estado actual del grafo.

    Returns:
        state (dict): Documentos filtrados (solo los relevantes) y estado actualizado de 'web_search'.
    """
    print("---EVALUAR RELEVANCIA DE DOCUMENTOS---")
    question = state["question"]
    documents = state["documents"]
    
    # Calificar cada documento
    filtered_docs = []
    for d in documents:
        # Evaluar la relevancia del documento
        score = retrieval_grader.invoke({"question": question, "document": d.page_content})
        grade = score['score']
        print(grade)
        
        if grade.lower() == "yes":
            print("---DOCUMENTO RELEVANTE---")
            filtered_docs.append(d)
        else:
            print("---DOCUMENTO NO RELEVANTE---")
    
    # Activar búsqueda web solo si NO hay documentos relevantes
    web_search = "Yes" if not filtered_docs else "No"

    return {"documents": filtered_docs, "question": question, "web_search": web_search}


# Función para realizar una búsqueda web
def web_search(state: GraphState):
    """
    Realiza una búsqueda web basada en la pregunta del usuario.

    Args:
        state (dict): El estado actual del grafo.

    Returns:
        state (dict): Resultados de la búsqueda web añadidos a los documentos.
    """
    print("---BÚSQUEDA WEB---")
    question = state["question"]
    documents = state.get("documents", [])
    # Realizar la búsqueda web
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}


def route_question(state: GraphState):
    """
    Enruta la pregunta a una búsqueda web o a RAG (Recuperación de documentos desde la base de datos vectorial).

    Args:
        state (dict): El estado actual del grafo, que contiene la pregunta del usuario.

    Returns:
        str: El nombre del siguiente nodo a ejecutar ("websearch" o "vectorstore").
    """

    print("---ENRUTAR PREGUNTA---")
    question = state["question"]  # Obtener la pregunta del estado actual
    print(question)  # Imprimir la pregunta para depuración

    # Enrutar la pregunta usando el "question_router"
    source = question_router.invoke({"question": question})  
    print(source)  # Imprimir el resultado del enrutamiento para depuración
    # print(source['datasource'])  # Imprimir la fuente de datos elegida

    # Decidir a dónde enrutar la pregunta
    if source['datasource'] == 'web_search':
        print("---ENRUTAR PREGUNTA A BÚSQUEDA WEB---")
        return "websearch"  # Retornar "websearch" para usar la búsqueda web
    elif source['datasource'] == 'vectorstore':
        print("---ENRUTAR PREGUNTA A RAG---")
        return "vectorstore"  # Retornar "vectorstore" para usar la base de datos vectorial
    


def decide_to_generate(state):
    """
    Determina si se debe generar una respuesta o realizar una búsqueda web.

    Args:
        state (dict): El estado actual del grafo, que contiene:
            - question: La pregunta del usuario.
            - web_search: Indica si se debe realizar una búsqueda web.
            - documents: Los documentos recuperados y filtrados.

    Returns:
        str: Decisión binaria para el siguiente nodo a ejecutar ("websearch" o "generate").
    """

    print("---EVALUAR DOCUMENTOS FILTRADOS---")
    web_search = state["web_search"]  # Obtener el estado de la búsqueda web

    # Decidir si realizar una búsqueda web o generar una respuesta
    if web_search == "Yes":
        # Si se debe realizar una búsqueda web
        print("---DECISIÓN: LOS DOCUMENTOS NO SON RELEVANTES, INCLUIR BÚSQUEDA WEB---")
        return "websearch"  # Retornar "websearch" para realizar una búsqueda web
    else:
        # Si los documentos son relevantes, generar una respuesta
        print("---DECISIÓN: GENERAR RESPUESTA---")
        return "generate"  # Retornar "generate" para generar una respuesta
    


def grade_generation_v_documents_and_question(state):
    """
    Determina si la respuesta generada está basada en los documentos y responde a la pregunta.

    Args:
        state (dict): El estado actual del grafo, que contiene:
            - question: La pregunta del usuario.
            - documents: Los documentos recuperados.
            - generation: La respuesta generada por el modelo.

    Returns:
        str: Decisión para el siguiente nodo a ejecutar ("useful", "not useful", o "not supported").
    """

    print("---VERIFICAR ALUCINACIONES---")
    question = state["question"]  # Obtener la pregunta del estado actual
    documents = state["documents"]  # Obtener los documentos recuperados
    generation = state["generation"]  # Obtener la respuesta generada

    # Verificar si la respuesta está basada en los documentos (no es una alucinación)
    score = hallucination_grader.invoke({"documents": documents, "generation": generation})
    grade = score['score']  # Obtener la calificación ("yes" o "no")

    # Si la respuesta está basada en los documentos
    if grade == "yes":
        print("---DECISIÓN: LA RESPUESTA ESTÁ BASADA EN LOS DOCUMENTOS---")
        
        # Verificar si la respuesta responde adecuadamente a la pregunta
        print("---EVALUAR RESPUESTA vs PREGUNTA---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score['score']  # Obtener la calificación ("yes" o "no")

        # Si la respuesta responde a la pregunta
        if grade == "yes":
            print("---DECISIÓN: LA RESPUESTA RESPONDE A LA PREGUNTA---")
            return "useful"  # Retornar "useful" (útil)
        else:
            print("---DECISIÓN: LA RESPUESTA NO RESPONDE A LA PREGUNTA---")
            return "not useful"  # Retornar "not useful" (no útil)
    else:
        # Si la respuesta no está basada en los documentos
        print("---DECISIÓN: LA RESPUESTA NO ESTÁ BASADA EN LOS DOCUMENTOS, REINTENTAR---")
        return "not supported"  # Retornar "not supported" (no respaldada)
    

workflow = StateGraph(GraphState)

# Definir los nodos
workflow.add_node("websearch", web_search)  # Nodo para realizar una búsqueda web
workflow.add_node("retrieve", retrieve)  # Nodo para recuperar documentos
workflow.add_node("grade_documents", grade_documents)  # Nodo para evaluar documentos
workflow.add_node("generate", generate)  # Nodo para generar una respuesta

# Establecer el punto de entrada condicional
workflow.set_conditional_entry_point(
    route_question,  # Función que decide el primer nodo
    {
        "websearch": "websearch",  # Si route_question devuelve "websearch", ir al nodo "websearch"
        "vectorstore": "retrieve",  # Si route_question devuelve "vectorstore", ir al nodo "retrieve"
    },
)

# Conexión directa entre "retrieve" y "grade_documents"
workflow.add_edge("retrieve", "grade_documents")

# Conexión condicional desde "grade_documents"
workflow.add_conditional_edges(
    "grade_documents",  # Nodo desde el cual se decide el siguiente paso
    decide_to_generate,  # Función que decide si generar una respuesta o realizar una búsqueda web
    {
        "websearch": "websearch",  # Si decide_to_generate devuelve "websearch", ir al nodo "websearch"
        "generate": "generate",  # Si decide_to_generate devuelve "generate", ir al nodo "generate"
    },
)

# Conexión directa entre "websearch" y "generate"
workflow.add_edge("websearch", "generate")

# Conexión condicional desde "generate"
workflow.add_conditional_edges(
    "generate",  # Nodo desde el cual se decide el siguiente paso
    grade_generation_v_documents_and_question,  # Función que evalúa la respuesta generada
    {
        "not supported": "generate",  # Si la respuesta no está respaldada, reintentar en "generate"
        "useful": END,  # Si la respuesta es útil, terminar el flujo
        "not useful": "websearch",  # Si la respuesta no es útil, ir al nodo "websearch"
    },
)

'''
    El código define un grafo de estados que representa el flujo de trabajo del sistema.

    Se agregan nodos para cada etapa del proceso (búsqueda web, recuperación de documentos, generación de respuestas, etc.).

    Se establecen conexiones y condiciones para decidir cómo el sistema debe moverse entre las etapas.

    El flujo comienza con la función route_question, que decide si usar la búsqueda web o la base de datos vectorial.

    Dependiendo de las evaluaciones en cada etapa, el sistema puede reintentar, terminar o cambiar de estrategia (por ejemplo, realizar una búsqueda web si los documentos no son relevantes).
'''

app = workflow.compile()





# from pprint import pprint
# inputs = {"question": "Que es la factura electronica, sifen y el kude?"}
# for output in app.stream(inputs):
#     for key, value in output.items():
#         pprint(f"Finished running: {key}:")
# pprint(value["generation"])
