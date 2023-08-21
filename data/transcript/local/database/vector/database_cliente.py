from langchain.vectorstores import Chroma

class DatabaseClient:
    _instance = None

    def __new__(cls, embeddings, docs):
        if not cls._instance:
            cls._instance = super(DatabaseClient, cls).__new__(cls)
            
            # Inicialización de atributos
            cls._instance.embeddings = embeddings
            cls._instance.docs = docs
            cls._instance.persist_directory = "chroma_db"

            # Inicialización de la conexión
            cls._instance.connection = Chroma.from_documents(
                documents=cls._instance.docs, 
                embedding=cls._instance.embeddings, 
                persist_directory=cls._instance.persist_directory
            )
            cls._instance.connection.persist()
        return cls._instance

    def query(self, query, params=None):
        # Usamos el método similarity_search proporcionado por la conexión
        return self.connection.similarity_search(query)
