# Task Overview

You are tasked with improving the core retrieval pipeline for a customer support RAG system. While all infrastructure (Chroma vector DB, FastAPI endpoints) is fully automated and running, retrieval results are often irrelevant because documents were chunked poorly (2000 tokens, no overlap, missing metadata) before embedding.

Your goals are:
- Re-implement the chunking pipeline for all provided documents, creating ~500-token chunks with 200-token overlap to preserve context.
- Make sure each chunk is paired with accurate metadata (category, priority, date).
- Generate new embeddings using the given sentence-transformer model and batch upsert these chunks (and metadata) into the Chroma collection.
- Update retrieval logic to fetch the top 5 most relevant chunks for a new query using cosine similarity.
- Validate your improved retrieval with test queries and check recall@5.

## Guidance
- The provided retrieval function is incomplete: you need to properly search and rank based on semantic similarity.
- The chunking script lacks overlap and does not attach required metadata—this is your responsibility.
- Embedding generation utilities and vector DB connection code are already present—simply complete the data chunking and retrieval logic.
- You do NOT need to set up or configure the Chroma infrastructure.
- Spot check the output for relevance; calculate recall@5 using the provided test set.

## Database Access
- Vector DB: Chroma
- Host: `<DROPLET_IP>`
- Port: 8000
- Collection Name: `support_chunks`
- Embedding Dimension: 384
- Pre-embedded doc count: 8000 docs (~12,000 expected chunks after reprocessing)
- Metadata: `category`, `priority`, `date` attached to each chunk

You can use `db/vector_db_client.py` to interact with the vector DB.

## Objectives
- Chunk and upsert all docs into Chroma with proper overlap and metadata.
- Generate embeddings for each chunk using the provided sentence-transformer.
- Implement top-5 vector search retrieval using cosine similarity, ranking by most relevant.
- Show improved recall and spot-check result quality.

## How to Verify
- Run `rag/evaluate.py` to test the retrieval system on sample queries and record recall@5.
- Inspect several retrieval results by hand for relevance and context.
- Double-check that metadata fields are correctly attached and indexed in Chroma.

