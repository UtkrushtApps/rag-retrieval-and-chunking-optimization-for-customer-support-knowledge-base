import json
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from db.vector_db_client import get_chroma_client, get_chunk_collection
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_DIM

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/support_docs.json')
MODEL_NAME = 'all-MiniLM-L6-v2'

model = SentenceTransformer(MODEL_NAME)

# Helper function to split text into overlapping chunks
def chunk_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks

# Main chunk, embed, and upsert pipeline
def chunk_embed_upsert():
    with open(DATA_PATH, 'r') as f:
        docs = json.load(f)
    client = get_chroma_client()
    collection = get_chunk_collection(client)
    ids, embeddings, documents, metadatas = [], [], [], []
    for doc in tqdm(docs, desc="Chunking and embedding"):
        chunks = chunk_text(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)
        chunk_ids = [f"{doc['doc_id']}_chunk_{i}" for i in range(len(chunks))]
        chunk_embeddings = model.encode(chunks)
        for i, chunk in enumerate(chunks):
            ids.append(chunk_ids[i])
            embeddings.append(chunk_embeddings[i])
            documents.append(chunk)
            metadatas.append({
                "category": doc["category"],
                "priority": doc["priority"],
                "date": doc["date"]
            })
    print(f"Upserting {len(ids)} chunks...")
    # Upsert in batches to prevent OOM
    batch_size = 512
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )

if __name__ == "__main__":
    chunk_embed_upsert()