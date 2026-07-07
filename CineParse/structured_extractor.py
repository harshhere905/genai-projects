from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List,Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    Plot_Summary: str


parser=PydanticOutputParser(pydantic_object=Movie)

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert movie information extractor. 
Given a paragraph that may contain information about a movie, 
extract all the essential details mentioned. Do not assume or invent 
information that isn't present in the text — only extract what's explicitly stated.

If a field is not mentioned in the paragraph, use null for optional fields, 
or an empty list for list fields (genre, cast) if no info is found.

{format_instructions}"""),
    ("human", "{paragraph}")
])

para = """Christopher Nolan's Inception, released in 2010, is a mind-bending sci-fi thriller 
starring Leonardo DiCaprio, Joseph Gordon-Levitt, and Elliot Page. The film explores the concept 
of dream manipulation and corporate espionage through shared dreaming technology. It holds an 
IMDb rating of 8.8 and is widely regarded as one of the best films of the decade."""

final_prompt = extraction_prompt.invoke({
    "paragraph": para,
    "format_instructions": parser.get_format_instructions()
})

response=model.invoke(final_prompt);
parsed_movie = parser.parse(response.content)

print(parsed_movie)
print(parsed_movie.title)
