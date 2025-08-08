import json
import os
from chromadb.config import Settings
import chromadb
from config import CHROMA_HOST, CHROMA_PORT, CHUNK_COLLECTION_NAME

client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    settings=Settings(allow_reset=True)
)

# Reset and initialize the chunk collection
if CHUNK_COLLECTION_NAME in [c.name for c in client.list_collections()]:
    client.delete_collection(CHUNK_COLLECTION_NAME)

client.create_collection(CHUNK_COLLECTION_NAME)

# At this point, chunking/upsert/insertion will be handled by your pipeline, not here.
