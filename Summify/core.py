from dotenv import load_dotenv
load_dotenv()

from langchain_tavily import TavilySearch
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearch(max_results=5)

llm = ChatMistralAI(model="mistral-small-latest") 

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Summarize the following news into clear bullet points:

{news}
"""
)

chain = prompt | llm | StrOutputParser()

search_result = search_tool.invoke("Latest news of AI 2026")


results = search_result.get("results", search_result) if isinstance(search_result, dict) else search_result
news_text = "\n\n".join(r.get("content", "") for r in results)

result = chain.invoke({"news": news_text})

print(result)
print(search_tool.description)
print(search_tool.name)
print(search_tool.args)