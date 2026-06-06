from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from ai.factories.embedding_factory import get_embeddings
from ai.config.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    VECTOR_DB_PATH
)

def ingest_resume(file_path):

    print("\nLoading Resume...\n")

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vectorstore.save_local(VECTOR_DB_PATH)

    print("\nResume Ingested Successfully\n")