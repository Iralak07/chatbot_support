
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_huggingface import HuggingFaceEmbeddings
import os
import dotenv
dotenv.load_dotenv()

hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

class QdrantSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QdrantSingleton, cls).__new__(cls)
            
            # Configuración para Qdrant Cloud
            cls._instance.client = QdrantClient(
                url="https://a5975a6b-e907-4020-8f5d-a85d9ae52f58.us-east4-0.gcp.cloud.qdrant.io", 
                api_key=os.environ.get("QDRANT_API")
            )
            
            # Verificar si la colección existe, si no, crearla
            if not cls._instance.client.collection_exists(collection_name="my_documents"):
                print("Creando colección en Qdrant Cloud...")
                cls._instance.client.recreate_collection(
                    collection_name="my_documents",
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                )
        return cls._instance

    def get_vector_store(self):
        """
        Retorna una instancia de QdrantVectorStore configurada con el cliente y la colección.
        
        Args:
            embedding_function: Función de embedding que se utilizará para convertir textos en vectores.
        
        Returns:
            QdrantVectorStore: Instancia configurada.
        """
        return QdrantVectorStore(
            client=self.client,
            collection_name="my_documents",
            embedding=hf_embeddings,
        )

def qdrant_client():
    """
    Función de conveniencia para obtener el vector store configurado.
    
    Args:
        embedding_function: Función de embedding que se utilizará para convertir textos en vectores.
    
    Returns:
        QdrantVectorStore: Instancia configurada.
    """
    qdrant_singleton = QdrantSingleton()
    return qdrant_singleton.get_vector_store()