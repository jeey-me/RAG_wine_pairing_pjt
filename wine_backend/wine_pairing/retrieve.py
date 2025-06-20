# chains/retrieve.py
import os
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableLambda

def retrieve_chain():
    def search_wines(dish_flavor):
        embedding = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
        vector_store = PineconeVectorStore(
            index_name=os.getenv("PINECONE_INDEX_NAME"),
            embedding=embedding,
            namespace=os.getenv("PINECONE_NAMESPACE")
        )
        results = vector_store.similarity_search(dish_flavor, k=5)
        return {
            "dish_flavor": dish_flavor,
            "wine_reviews": "\n".join([doc.page_content for doc in results])
        }
    return RunnableLambda(search_wines)
