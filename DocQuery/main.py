import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

PERSIST_DIR = "chroma_db"

if not os.path.exists(PERSIST_DIR):
    raise FileNotFoundError(
        f"'{PERSIST_DIR}' not found. Run ingest.py first to create the vectorstore."
    )

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embedding_model
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.5
    }
)

llm = ChatMistralAI(model="mistral-small-2603")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}
"""
        )
    ]
)

print("DocQuery is ready to use!!")
print("To exit please press 0")

while True:
    question = input("Enter your question: ").strip()

    if question == '0':
        break

    if not question:
        print("Please enter a question.")
        continue

    try:
        docs = retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])

        final_prompt = prompt.invoke({
            "context": context,
            "question": question
        })

        response = llm.invoke(final_prompt)
        print(f"\nAI: {response.content}\n")

    except Exception as e:
        print(f"\n[Error] Something went wrong while answering: {e}\n")