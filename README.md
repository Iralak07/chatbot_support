# README

## Descripción del Proyecto
Este proyecto implementa un chatbot de soporte técnico utilizando **Streamlit** como interfaz de usuario y **Groq** como proveedor de modelos de lenguaje. El chatbot está diseñado para responder preguntas relacionadas con el **Sistema Integrado de Facturación Electrónica Nacional (SIFEN)** en Paraguay. Además, utiliza una base de datos vectorial (**Qdrant**) para recuperar documentos relevantes y herramientas de búsqueda web para obtener información adicional cuando sea necesario.

---

## Requisitos Previos
Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:
- **Python 3.8 o superior**.
- **Git** (para clonar el repositorio).
- **virtualenv** (para crear un entorno virtual).

---

## Instalación y Configuración

### 1. Clonar el Repositorio
Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Crear un Entorno Virtual
Crea un entorno virtual para aislar las dependencias del proyecto:

```bash
virtualenv venv
```

Activa el entorno virtual:

- **En Linux/MacOS**:
  ```bash
  source venv/bin/activate
  ```
- **En Windows**:
  ```bash
  venv\Scripts\activate
  ```

### 3. Instalar Dependencias
Instala las dependencias del proyecto utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar el Archivo `.env`
Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes claves de API:

```plaintext
serper_api = "tu_clave_serper_api"
TAVILY_API_KEY = "tu_clave_tavily_api"
QDRANT_API = "tu_clave_qdrant_api"
GRAQ_API_KEY = "tu_clave_groq_api"
```

Asegúrate de reemplazar `"tu_clave_..."` con las claves correspondientes que hayas obtenido de los servicios mencionados.

---

## Ejecución de la Aplicación

Una vez configurado el entorno y las claves de API, puedes ejecutar la aplicación con el siguiente comando:

```bash
streamlit run src/app.py
```

Esto iniciará la aplicación en tu navegador web. La interfaz de usuario te permitirá interactuar con el chatbot, hacer preguntas y obtener respuestas basadas en la información proporcionada.

---

## Estructura del Proyecto

- **src/app.py**: Punto de entrada de la aplicación. Contiene la lógica de la interfaz de usuario y la interacción con el chatbot.
- **src/models/**: Módulos relacionados con la conexión a Groq y otros modelos de lenguaje.
- **src/database/**: Módulos para la conexión y gestión de la base de datos vectorial Qdrant.
- **src/chatbot/**: Lógica del chatbot, incluyendo enrutamiento de preguntas, generación de respuestas y evaluación de relevancia.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar el proyecto.
- **.env**: Archivo de configuración para almacenar las claves de API.

---

## Consideraciones Finales

- **Seguridad**: Nunca compartas tus claves de API. Asegúrate de que el archivo `.env` esté incluido en tu `.gitignore` para evitar subirlo accidentalmente a un repositorio público.
- **Personalización**: Puedes modificar el archivo `src/app.py` para adaptar la interfaz de usuario o agregar nuevas funcionalidades.
- **Escalabilidad**: El uso de Qdrant y Groq permite manejar grandes volúmenes de datos y generar respuestas precisas y rápidas.

---
## Flujo de trabajo del Agente
![workflow](https://github.com/user-attachments/assets/93b576e6-da86-41a6-ae87-dd2b97339c7d)

---

# Dentro del proyecto tenemos los siguientes modulos

## app.y
El archivo `app.py` es el punto de entrada principal de la aplicación. Utiliza **Streamlit** para crear una interfaz de usuario (UI) que permite a los usuarios interactuar con un chatbot de soporte técnico relacionado con el **Sistema Integrado de Facturación Electrónica Nacional (SIFEN)**. La aplicación incluye un historial de chat, preguntas frecuentes en un panel lateral y la capacidad de procesar preguntas del usuario utilizando un módulo de chatbot.

---

## Dependencias
El archivo `app.py` depende de las siguientes bibliotecas y módulos:

1. **Streamlit**: Para crear la interfaz de usuario web.
2. **chatbot.core**: Módulo que contiene la lógica del chatbot.

---

## Configuración de la Página
Se configura la página de Streamlit con un título y un ícono personalizados. Además, se aplican estilos CSS personalizados para el título, que incluyen una fuente específica (`Poppins`), un efecto de gradiente en el texto, sombra y ajustes de tamaño y alineación.

---

## Historial del Chat
Se utiliza el estado de sesión de Streamlit (`st.session_state`) para almacenar y mostrar el historial de conversaciones entre el usuario y el chatbot. Si no existe un historial de chat, se inicializa como una lista vacía. La función `display_chat_history` recorre el historial de chat y muestra los mensajes del usuario y del bot de manera diferenciada.

---

## Panel Lateral con Preguntas Frecuentes
En el panel lateral, se muestran preguntas frecuentes (FAQ) en formato de acordeón. Cada pregunta expandible contiene una respuesta detallada. Las preguntas están relacionadas con temas como la autorización de proveedores de servicios tecnológicos, contribuyentes habilitados, conservación de documentos electrónicos, eventos del receptor y emisor, y procesos de cancelación e inutilización de documentos.

---

## Entrada de Texto del Usuario
Se utiliza un campo de entrada de texto (`st.chat_input`) para permitir al usuario escribir una pregunta. Cuando el usuario envía una pregunta, esta se añade al historial de chat y se procesa utilizando el módulo `chatbot.core`. Mientras se procesa la pregunta, se muestra un mensaje de carga. Una vez que el chatbot genera una respuesta, esta se añade al historial de chat y se muestra en la interfaz.

---

## Recarga de la Página
Después de procesar la pregunta y mostrar la respuesta, la página se recarga para limpiar el campo de entrada de texto y prepararse para una nueva interacción.

---

# (Flujo de Trabajo del Chatbot) Modulo core.py

## Descripción General
El archivo `app.py` implementa un flujo de trabajo para un chatbot que utiliza un modelo de lenguaje (LLM) junto con una base de datos vectorial (Qdrant) y herramientas de búsqueda web para responder preguntas de los usuarios. El flujo de trabajo está diseñado como un grafo de estados (`StateGraph`), donde cada nodo representa una etapa del proceso, como la recuperación de documentos, la generación de respuestas y la evaluación de la relevancia de la información.

El sistema combina técnicas de **Retrieval-Augmented Generation (RAG)** y búsqueda web para garantizar que las respuestas sean precisas, relevantes y basadas en información confiable. Además, incluye mecanismos para evaluar la calidad de las respuestas y decidir si es necesario realizar una búsqueda web adicional o reintentar la generación de una respuesta.

---

## Componentes Principales

### 1. **Importaciones y Configuración Inicial**
- **Modelo Groq**: Se utiliza un cliente para interactuar con el modelo de lenguaje Groq.
- **Base de Datos Vectorial (Qdrant)**: Se conecta a una base de datos vectorial para recuperar documentos relevantes.
- **Herramientas de Búsqueda Web**: Se incluye una herramienta para realizar búsquedas en la web cuando los documentos locales no son suficientes.
- **Evaluadores**: Se utilizan varios evaluadores para verificar la relevancia de los documentos, la coherencia de las respuestas y la ausencia de alucinaciones (respuestas no basadas en los documentos).

### 2. **Estado del Grafo (`GraphState`)**
El estado del grafo es un diccionario que contiene:
- **question**: La pregunta del usuario.
- **generation**: La respuesta generada por el modelo.
- **web_search**: Indica si se debe realizar una búsqueda web.
- **documents**: Lista de documentos recuperados.
- **context**: Contexto formateado para la generación de respuestas.
- **retry_count**: Contador de reintentos para manejar casos en los que la respuesta no es satisfactoria.

### 3. **Funciones del Flujo de Trabajo**

#### a. **Recuperación de Documentos (`retrieve`)**
- Recupera documentos relevantes de la base de datos vectorial (Qdrant) basados en la pregunta del usuario.
- Utiliza un retriever configurado para obtener los 4 documentos más relevantes.

#### b. **Generación de Respuestas (`generate`)**
- Genera una respuesta utilizando el modelo RAG (Retrieval-Augmented Generation).
- Combina la pregunta del usuario, los documentos recuperados y el contexto formateado para producir una respuesta.

#### c. **Evaluación de Documentos (`grade_documents`)**
- Evalúa la relevancia de los documentos recuperados.
- Si ningún documento es relevante, activa una bandera (`web_search`) para realizar una búsqueda web.

#### d. **Búsqueda Web (`web_search`)**
- Realiza una búsqueda web basada en la pregunta del usuario.
- Añade los resultados de la búsqueda a la lista de documentos para su posterior procesamiento.

#### e. **Enrutamiento de Preguntas (`route_question`)**
- Decide si la pregunta debe ser respondida utilizando la base de datos vectorial (RAG) o mediante una búsqueda web.
- Utiliza un enrutador de preguntas para tomar esta decisión.

#### f. **Decisión de Generación (`decide_to_generate`)**
- Determina si se debe generar una respuesta con los documentos disponibles o realizar una búsqueda web.
- Basado en la evaluación de la relevancia de los documentos.

#### g. **Evaluación de la Respuesta (`grade_generation_v_documents_and_question`)**
- Verifica si la respuesta generada está basada en los documentos y responde adecuadamente a la pregunta.
- Evalúa la coherencia y la ausencia de alucinaciones en la respuesta.
- Decide si la respuesta es útil, no útil o no está respaldada por los documentos.

### 4. **Configuración del Grafo de Estados**
- Se define un grafo de estados (`StateGraph`) que conecta los nodos (funciones) según la lógica del flujo de trabajo.
- Los nodos principales son:
  - **websearch**: Realiza una búsqueda web.
  - **retrieve**: Recupera documentos de la base de datos vectorial.
  - **grade_documents**: Evalúa la relevancia de los documentos.
  - **generate**: Genera una respuesta utilizando RAG.
- Las conexiones entre nodos se establecen de manera condicional, dependiendo de los resultados de las evaluaciones.

### 5. **Punto de Entrada Condicional**
- El flujo de trabajo comienza con la función `route_question`, que decide si la pregunta debe ser procesada mediante RAG o una búsqueda web.
- Dependiendo de la decisión, el flujo se dirige al nodo correspondiente (`websearch` o `retrieve`).

### 6. **Conexiones y Condiciones**
- **Conexión Directa**: Algunos nodos están conectados directamente, como `retrieve` → `grade_documents`.
- **Conexiones Condicionales**: Otras conexiones dependen de evaluaciones, como:
  - Si `grade_documents` determina que no hay documentos relevantes, el flujo se dirige a `websearch`.
  - Si `generate` produce una respuesta no útil, el flujo puede reintentar o realizar una búsqueda web.

### 7. **Compilación del Flujo de Trabajo**
- El grafo de estados se compila en una aplicación (`app`) que puede ejecutarse para procesar preguntas y generar respuestas.

---

## Flujo de Trabajo Resumido
1. **Entrada**: El usuario hace una pregunta.
2. **Enrutamiento**: Se decide si la pregunta se responde con RAG o búsqueda web.
3. **Recuperación**: Si se usa RAG, se recuperan documentos relevantes.
4. **Evaluación de Documentos**: Se verifica la relevancia de los documentos.
5. **Búsqueda Web (opcional)**: Si no hay documentos relevantes, se realiza una búsqueda web.
6. **Generación de Respuesta**: Se genera una respuesta utilizando RAG o los resultados de la búsqueda web.
7. **Evaluación de la Respuesta**: Se verifica si la respuesta es útil y está basada en los documentos.
8. **Salida**: Si la respuesta es satisfactoria, se devuelve al usuario. De lo contrario, se reintenta o se realiza una búsqueda web adicional.

---


# Documentación de los Módulos de Evaluación y Generación (src/chatbot/utils)

## Descripción General
Este conjunto de módulos implementa funcionalidades clave para un sistema de chatbot basado en **Retrieval-Augmented Generation (RAG)**. Incluye evaluadores de relevancia, generadores de respuestas y enrutadores de preguntas, todos diseñados para trabajar con un modelo de lenguaje (Groq) y una base de datos vectorial (Qdrant). Estos componentes garantizan que las respuestas sean precisas, relevantes y basadas en información confiable.

---

## Componentes Principales

### 1. **Evaluador de Respuestas (`answer_grader`)**
- **Propósito**: Evalúa si una respuesta generada es útil para resolver una pregunta específica.
- **Entradas**:
  - `question`: La pregunta del usuario.
  - `generation`: La respuesta generada por el modelo.
- **Salida**: Un JSON con una clave `score` que puede ser `yes` (útil) o `no` (no útil).
- **Plantilla de Prompt**: Se utiliza un prompt estructurado para guiar al modelo en la evaluación.

```python
prompt = PromptTemplate(
    template="""...""",
    input_variables=["generation", "question"],
)
answer_grader = prompt | llm | JsonOutputParser()
```

---

### 2. **Generador de Respuestas (`rag_chain`)**
- **Propósito**: Genera respuestas detalladas basadas en documentos recuperados y una pregunta del usuario.
- **Entradas**:
  - `question`: La pregunta del usuario.
  - `context`: Contexto formateado a partir de los documentos recuperados.
- **Salida**: Una respuesta textual generada por el modelo.
- **Plantilla de Prompt**: Se utiliza un prompt que enfatiza la precisión y la claridad en la respuesta.

```python
prompt = PromptTemplate(
    template="""...""",
    input_variables=["question", "context"],
)
rag_chain = prompt | llm | StrOutputParser()
```

---

### 3. **Evaluador de Alucinaciones (`hallucination_grader`)**
- **Propósito**: Determina si una respuesta generada está respaldada por los documentos proporcionados.
- **Entradas**:
  - `generation`: La respuesta generada por el modelo.
  - `documents`: Los documentos recuperados.
- **Salida**: Un JSON con una clave `score` que puede ser `yes` (respaldada) o `no` (no respaldada).
- **Plantilla de Prompt**: Se utiliza un prompt que compara la respuesta con los documentos para detectar alucinaciones.

```python
prompt = PromptTemplate(
    template="""...""",
    input_variables=["generation", "documents"],
)
hallucination_grader = prompt | llm | JsonOutputParser()
```

---

### 4. **Enrutador de Preguntas (`question_router`)**
- **Propósito**: Decide si una pregunta debe ser respondida utilizando la base de datos vectorial (RAG) o mediante una búsqueda web.
- **Entradas**:
  - `question`: La pregunta del usuario.
- **Salida**: Un JSON con una clave `datasource` que puede ser `vectorstore` (RAG) o `web_search` (búsqueda web).
- **Plantilla de Prompt**: Se utiliza un prompt que evalúa el contexto de la pregunta para tomar la decisión.

```python
prompt = PromptTemplate(
    template="""...""",
    input_variables=["question"],
)
question_router = prompt | llm | JsonOutputParser()
```

---

### 5. **Evaluador de Relevancia de Documentos (`retrieval_grader`)**
- **Propósito**: Evalúa si un documento recuperado es relevante para responder una pregunta específica.
- **Entradas**:
  - `question`: La pregunta del usuario.
  - `document`: El documento recuperado.
- **Salida**: Un JSON con una clave `score` que puede ser `yes` (relevante) o `no` (no relevante).
- **Plantilla de Prompt**: Se utiliza un prompt que compara el contenido del documento con la pregunta.

```python
prompt = PromptTemplate(
    template="""...""",
    input_variables=["question", "document"],
)
retrieval_grader = prompt | llm | JsonOutputParser()
```

---

## Flujo de Trabajo

1. **Recuperación de Documentos**:
   - Se recuperan documentos relevantes de la base de datos vectorial (Qdrant) utilizando un retriever configurado.

2. **Generación de Respuestas**:
   - Se genera una respuesta utilizando el modelo RAG, combinando la pregunta del usuario y los documentos recuperados.

3. **Evaluación de Respuestas**:
   - Se evalúa si la respuesta generada es útil (`answer_grader`) y si está respaldada por los documentos (`hallucination_grader`).

4. **Enrutamiento de Preguntas**:
   - Se decide si la pregunta debe ser respondida utilizando RAG o una búsqueda web (`question_router`).

5. **Evaluación de Relevancia de Documentos**:
   - Se verifica si los documentos recuperados son relevantes para la pregunta (`retrieval_grader`).

---

# Documentación del Módulo de Conexión a Qdrant (src/database)

## Descripción General
Este módulo implementa una conexión a **Qdrant**, una base de datos vectorial, utilizando el patrón de diseño **Singleton** para garantizar que solo exista una instancia del cliente Qdrant en toda la aplicación. Además, se configura un almacén de vectores (`QdrantVectorStore`) que permite almacenar y recuperar documentos basados en embeddings generados por un modelo de Hugging Face.

---

## Componentes Principales

### 1. **Configuración del Entorno**
- Se utiliza la biblioteca `dotenv` para cargar variables de entorno desde un archivo `.env`.
- La clave de API de Qdrant (`QDRANT_API`) se obtiene desde las variables de entorno.

```python
import os
import dotenv
dotenv.load_dotenv()
```

---

### 2. **Embeddings de Hugging Face**
- Se utiliza el modelo `sentence-transformers/all-mpnet-base-v2` de Hugging Face para generar embeddings de texto.
- Este modelo convierte textos en vectores de 768 dimensiones.

```python
from langchain_huggingface import HuggingFaceEmbeddings
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
```

---

### 3. **Patrón Singleton para Qdrant**
- Se implementa el patrón Singleton para garantizar que solo exista una instancia del cliente Qdrant en toda la aplicación.
- La instancia se configura para conectarse a Qdrant Cloud utilizando una URL y una clave de API.

```python
class QdrantSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QdrantSingleton, cls).__new__(cls)
            cls._instance.client = QdrantClient(
                url="https://a5975a6b-e907-4020-8f5d-a85d9ae52f58.us-east4-0.gcp.cloud.qdrant.io", 
                api_key=os.environ.get("QDRANT_API")
            )
            # Verificar y crear la colección si no existe
            if not cls._instance.client.collection_exists(collection_name="my_documents"):
                print("Creando colección en Qdrant Cloud...")
                cls._instance.client.recreate_collection(
                    collection_name="my_documents",
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                )
        return cls._instance
```

---

### 4. **Configuración del Almacén de Vectores**
- El método `get_vector_store` retorna una instancia de `QdrantVectorStore` configurada con el cliente Qdrant y la colección `my_documents`.
- Se utiliza el modelo de embeddings de Hugging Face para convertir textos en vectores.

```python
def get_vector_store(self):
    return QdrantVectorStore(
        client=self.client,
        collection_name="my_documents",
        embedding=hf_embeddings,
    )
```

---

### 5. **Función de Conveniencia (`qdrant_client`)**
- Proporciona una forma sencilla de obtener el almacén de vectores configurado.
- Utiliza la instancia Singleton de `QdrantSingleton` para garantizar que solo exista una conexión a Qdrant.

```python
def qdrant_client():
    qdrant_singleton = QdrantSingleton()
    return qdrant_singleton.get_vector_store()
```

---

## Flujo de Trabajo

1. **Inicialización**:
   - Se carga la clave de API de Qdrant desde las variables de entorno.
   - Se inicializa el modelo de embeddings de Hugging Face.

2. **Conexión a Qdrant**:
   - Se crea una instancia Singleton del cliente Qdrant.
   - Si la colección `my_documents` no existe, se crea con un tamaño de vector de 768 y una métrica de distancia coseno.

3. **Configuración del Almacén de Vectores**:
   - Se configura un `QdrantVectorStore` utilizando el cliente Qdrant y el modelo de embeddings.

4. **Uso**:
   - La función `qdrant_client` permite obtener el almacén de vectores configurado para su uso en otras partes de la aplicación.

---

# Documentación del Módulo de Conexión a Groq (src/models)

## Descripción General
Este módulo implementa una conexión al servicio de **Groq**, un proveedor de modelos de lenguaje (LLM), utilizando la biblioteca `langchain_groq`. El módulo proporciona una función para obtener un cliente configurado que permite interactuar con el modelo de lenguaje **Llama3-8b-8192**. La configuración se realiza utilizando una clave de API almacenada en variables de entorno.

---

## Componentes Principales

### 1. **Configuración del Entorno**
- Se utiliza la biblioteca `dotenv` para cargar variables de entorno desde un archivo `.env`.
- La clave de API de Groq (`GRAQ_API_KEY`) se obtiene desde las variables de entorno.

---

### 2. **Función `groq_client`**
- **Propósito**: Retorna una instancia configurada de `ChatGroq` para interactuar con el modelo de lenguaje.
- **Parámetros**:
  - `model`: Especifica el modelo de lenguaje a utilizar. En este caso, se utiliza el modelo **Llama3-8b-8192**.
  - `api_key`: Clave de API para autenticar las solicitudes al servicio de Groq.
- **Retorno**: Una instancia de `ChatGroq` configurada y lista para su uso.

---

## Flujo de Trabajo

1. **Inicialización**:
   - Se carga la clave de API de Groq desde las variables de entorno.
   
2. **Configuración del Cliente**:
   - Se crea una instancia de `ChatGroq` utilizando el modelo **Llama3-8b-8192** y la clave de API proporcionada.

3. **Uso**:
   - La función `groq_client` retorna el cliente configurado, que puede ser utilizado para generar respuestas, realizar consultas o interactuar con el modelo de lenguaje en otras partes de la aplicación.

---

