import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_tavily import TavilySearch
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="AI News Summarizer", page_icon="📰", layout="centered")

st.title("📰 News Summarizer")
st.caption("Search the web for a topic and get a clean, bullet-point summary.")

MODEL_NAME = "mistral-small-latest"

with st.sidebar:
    st.header("Settings")
    max_results = st.slider("Number of search results", min_value=1, max_value=10, value=5)

query = st.text_input("What news topic do you want to summarize?", value="Latest news of AI 2026")
run = st.button("Search & Summarize", type="primary")


@st.cache_resource
def get_chain(model_name: str):
    llm = ChatMistralAI(model=model_name)
    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful assistant.

Summarize the following news into clear bullet points:

{news}
"""
    )
    return prompt | llm | StrOutputParser()


def extract_news_text(search_result):
    results = (
        search_result.get("results", search_result)
        if isinstance(search_result, dict)
        else search_result
    )
    return results, "\n\n".join(r.get("content", "") for r in results)


if run:
    if not query.strip():
        st.warning("Please enter a topic to search for.")
    else:
        try:
            with st.spinner("Searching the web..."):
                search_tool = TavilySearch(max_results=max_results)
                search_result = search_tool.invoke(query)
                results, news_text = extract_news_text(search_result)

            if not news_text.strip():
                st.warning("No search results found for that query. Try rephrasing it.")
            else:
                with st.spinner("Summarizing..."):
                    chain = get_chain(MODEL_NAME)
                    summary = chain.invoke({"news": news_text})

                st.subheader("Summary")
                st.markdown(summary)

                with st.expander(f"View {len(results)} raw search result(s)"):
                    for r in results:
                        st.markdown(f"**[{r.get('title', 'Untitled')}]({r.get('url', '')})**")
                        st.write(r.get("content", ""))
                        st.markdown("---")

        except Exception as e:
            st.error(f"Something went wrong: {e}")