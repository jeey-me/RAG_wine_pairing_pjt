# chains/recommend.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda

def recommend_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 와인 소믈리에야. 반드시 한글로 대답해줘."),
        ("human", "음식 풍미:\n{dish_flavor}\n\n와인 리뷰:\n{wine_reviews}\n\n추천 와인과 이유를 json으로 알려줘.")
    ])
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return RunnableLambda(lambda x: (prompt | llm | JsonOutputParser()).invoke(x))