from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert movie information extractor. 
Given a paragraph that may contain information about one or more movies, 
extract all the essential details mentioned. Do not assume or invent 
information that isn't present in the text — only extract what's explicitly stated.

Extract the following details wherever available:
- Movie Name
- Release Year
- Genre
- Director
- Cast (main actors/actresses)
- Rating (IMDb, critics, or any mentioned)
- Plot Summary (brief, 1-2 lines)
- Language
- Box Office Collection (if mentioned)
- Awards (if mentioned)

If any detail is not present in the paragraph, simply skip it — do not write "N/A" or make guesses.

Present the extracted information in a clean, readable format like this:

Movie Name: ...
Release Year: ...
Genre: ...
Director: ...
Cast: ...
Rating: ...
Plot Summary: ...
Language: ...
Box Office: ...
Awards: ...

If the paragraph mentions multiple movies, extract details for each movie separately, 
clearly labeled (e.g., "Movie 1:", "Movie 2:")."""),

    ("human", "{paragraph}")
])
para="""Christopher Nolan's Inception, released in 2010, is a mind-bending sci-fi thriller starring 
Leonardo DiCaprio, Joseph Gordon-Levitt, and Elliot Page. The film explores dream manipulation 
and has an IMDb rating of 8.8. It grossed over $836 million worldwide and won 4 Academy Awards, 
including Best Visual Effects. On the other hand, 3 Idiots, a 2009 Bollywood comedy-drama 
directed by Rajkumar Hirani, features Aamir Khan, R. Madhavan, and Sharman Joshi in lead roles. 
The movie, which critiques the Indian education system, holds an IMDb rating of 8.4 and became 
one of the highest-grossing Bollywood films of its time, earning around ₹460 crore globally. 
It was shot primarily in Hindi and received widespread critical acclaim along with several 
Filmfare Awards."""
final_prompt = extraction_prompt.invoke({"paragraph": para})

response=model.invoke(final_prompt);
print(response.content)