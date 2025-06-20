# chains/describe.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

def describe_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 요리 풍미 분석 전문가야. 한글로 대답해줘."),
        ("human", "이미지의 요리 풍미를 한 문장으로 요약해줘.")
    ])
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return RunnableLambda(lambda x: (prompt | llm | StrOutputParser()).invoke(x))
