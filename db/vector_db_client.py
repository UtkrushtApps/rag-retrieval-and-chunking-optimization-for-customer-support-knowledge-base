import chromadb
from chromadb.config import Settings
from config import CHROMA_HOST, CHROMA_PORT, CHUNK_COLLECTION_NAME

def get_chroma_client():
    client = chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT,
        settings=Settings(allow_reset=True)
    )
    return client

def get_chunk_collection(client):
    return client.get_collection(CHUNK_COLLECTION_NAME)
