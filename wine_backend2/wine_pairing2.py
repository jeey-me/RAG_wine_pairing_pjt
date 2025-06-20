# wine_pairing.py
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def describe_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 요리 풍미 분석 전문가야."),
        ("human", "이미지의 요리 풍미를 한 문장으로 요약해줘.")
    ])
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return RunnableLambda(lambda x: (prompt | llm | StrOutputParser()).invoke(x))

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

def recommend_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 와인 소믈리에야. 음식 풍미와 리뷰를 보고 와인을 추천해줘."),
        ("human", "음식 풍미:\n{dish_flavor}\n\n와인 리뷰:\n{wine_reviews}\n\n추천 와인과 이유를 json으로 알려줘.")
    ])
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return RunnableLambda(lambda x: (prompt | llm | JsonOutputParser()).invoke(x))
