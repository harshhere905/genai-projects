import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

st.set_page_config(page_title="Movie Info Extractor (Structured)", page_icon="🎬")

st.title("🎬 Movie Info Extractor")
st.caption("Extracts structured movie details (JSON schema powered by Pydantic) from a paragraph.")


class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    Plot_Summary: str


@st.cache_resource
def get_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
    )


@st.cache_resource
def get_parser():
    return PydanticOutputParser(pydantic_object=Movie)


@st.cache_resource
def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """You are an expert movie information extractor. 
Given a paragraph that may contain information about a movie, 
extract all the essential details mentioned. Do not assume or invent 
information that isn't present in the text — only extract what's explicitly stated.

If a field is not mentioned in the paragraph, use null for optional fields, 
or an empty list for list fields (genre, cast) if no info is found.

{format_instructions}"""),
        ("human", "{paragraph}")
    ])


model = get_model()
parser = get_parser()
extraction_prompt = get_prompt()

sample_para = """Christopher Nolan's Inception, released in 2010, is a mind-bending sci-fi thriller 
starring Leonardo DiCaprio, Joseph Gordon-Levitt, and Elliot Page. The film explores the concept 
of dream manipulation and corporate espionage through shared dreaming technology. It holds an 
IMDb rating of 8.8 and is widely regarded as one of the best films of the decade."""

# Sidebar
with st.sidebar:
    st.header("Options")
    if st.button("Load Sample Paragraph"):
        st.session_state.para_input = sample_para
    show_raw = st.checkbox("Show raw JSON", value=False)

if "para_input" not in st.session_state:
    st.session_state.para_input = ""

paragraph = st.text_area(
    "Paste your movie paragraph here:",
    value=st.session_state.para_input,
    height=220,
    placeholder="e.g. Christopher Nolan's Inception, released in 2010, is a sci-fi thriller starring..."
)

extract_btn = st.button("Extract Movie Info", type="primary")

if extract_btn:
    if not paragraph.strip():
        st.warning("Please enter a paragraph first.")
    else:
        with st.spinner("Extracting details..."):
            try:
                final_prompt = extraction_prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions()
                })
                response = model.invoke(final_prompt)
                parsed_movie = parser.parse(response.content)
            except Exception as e:
                st.error(f"Failed to extract/parse movie info: {e}")
                parsed_movie = None

        if parsed_movie:
            st.subheader(parsed_movie.title)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Release Year:** {parsed_movie.release_year or 'Not mentioned'}")
                st.markdown(f"**Director:** {parsed_movie.director or 'Not mentioned'}")
                st.markdown(f"**Rating:** {parsed_movie.rating if parsed_movie.rating is not None else 'Not mentioned'}")
            with col2:
                st.markdown(f"**Genre:** {', '.join(parsed_movie.genre) if parsed_movie.genre else 'Not mentioned'}")
                st.markdown(f"**Cast:** {', '.join(parsed_movie.cast) if parsed_movie.cast else 'Not mentioned'}")

            st.markdown("**Plot Summary:**")
            st.write(parsed_movie.Plot_Summary)

            if show_raw:
                st.subheader("Raw JSON")
                st.json(parsed_movie.model_dump())