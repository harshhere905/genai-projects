import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

PERSIST_DIR = "chroma_db"

st.set_page_config(page_title="DocQuery", page_icon="📄", layout="centered")
st.title("📄 DocQuery")
st.caption("Ask questions about your PDF, answered only from its content.")


# ---------- Cached resources ----------
@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource
def get_llm():
    return ChatMistralAI(model="mistral-small-2603")


@st.cache_resource
def get_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
""",
            ),
            (
                "human",
                """Context:
{context}

Question:
{question}
""",
            ),
        ]
    )


def ingest_pdf(uploaded_file):
    """Save uploaded PDF, split it, embed it, and persist a fresh vectorstore."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        embedding_model = get_embedding_model()

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=PERSIST_DIR,
        )
        return vectorstore, len(docs), len(chunks)
    finally:
        os.remove(tmp_path)


def load_existing_vectorstore():
    embedding_model = get_embedding_model()
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding_model)


# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore_ready" not in st.session_state:
    st.session_state.vectorstore_ready = os.path.exists(PERSIST_DIR)


# ---------- Sidebar: upload & ingest ----------
with st.sidebar:
    st.header("Upload a document")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Process document", type="primary"):
            with st.spinner("Reading, splitting, and embedding the document..."):
                try:
                    ingest_pdf(uploaded_file)
                    st.session_state.vectorstore_ready = True
                    st.session_state.messages = []
                    st.success("Document processed! You can now ask questions.")
                except Exception as e:
                    st.error(f"Failed to process document: {e}")

    st.divider()
    if st.session_state.vectorstore_ready:
        st.success("Vectorstore is ready.")
    else:
        st.warning("No document processed yet.")

    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.rerun()


# ---------- Main chat interface ----------
if not st.session_state.vectorstore_ready:
    st.info("Upload and process a PDF from the sidebar to get started.")
    st.stop()

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
question = st.chat_input("Ask a question about your document...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                vectorstore = load_existing_vectorstore()
                retriever = vectorstore.as_retriever(
                    search_type="mmr",
                    search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5},
                )

                docs = retriever.invoke(question)
                context = "\n\n".join([doc.page_content for doc in docs])

                prompt = get_prompt()
                final_prompt = prompt.invoke({"context": context, "question": question})

                llm = get_llm()
                response = llm.invoke(final_prompt)
                answer = response.content

            except Exception as e:
                answer = f"Something went wrong while answering: {e}"

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})