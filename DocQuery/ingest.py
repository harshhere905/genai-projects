import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = "sample.pdf"
PERSIST_DIR = "chroma_db"

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"Could not find '{PDF_PATH}' in the current directory: {os.getcwd()}")

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()
print(f"Loaded {len(docs)} page(s) from {PDF_PATH}")

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(docs)
print(f"Split into {len(chunks)} chunk(s)")

# Create embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=PERSIST_DIR
)

print(f"Vectorstore created and persisted to '{PERSIST_DIR}'")