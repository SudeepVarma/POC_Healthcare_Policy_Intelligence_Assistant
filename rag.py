"""
Description: ChromaDB & Semantic Retrieval Layer or Vector Database Engine. Handles persistent semantic indexing using local HuggingFace embeddings and ChromaDB.
Author: Sudeep Varma K
Date: 2026-06-27
"""
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize local embedding pipeline
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Set up local database persistence
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("healthcare_docs")

# Chunking configurations for dense clinical clauses
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=160
)


def add_document(text):
    """Chunks text, generates embeddings locally, and upserts into ChromaDB."""
    chunks = text_splitter.split_text(text)
    embeddings = embedding_model.encode(chunks).tolist()
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )


def retrieve(question):
    """Queries Vector DB and maps context coordinates back to text strings."""
    query_vector = embedding_model.encode(question).tolist()
    result = collection.query(
        query_embeddings=[query_vector],
        n_results=5
    )
    if result and result["documents"]:
        return "\n".join(result["documents"][0])
    return ""