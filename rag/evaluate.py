from rag.retrieve import retrieve_relevant_chunks
import pandas as pd

QUERIES_PATH = 'sample_queries.txt'

with open(QUERIES_PATH, 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

def spot_check():
    for query in queries:
        results = retrieve_relevant_chunks(query)
        print(f'Query: {query}')
        for i, result in enumerate(results):
            print(f' {i+1}. {result["document"][:90]} ... [meta: {result["metadata"]}] (score: {result["score"]:.3f})')
        print('-'*40)

# For recall@5 simulation, load test_labels.csv with columns {query, expected_doc_id}
def recall_at_5():
    df = pd.read_csv('data/test_labels.csv')
    hits, total = 0, 0
    for _, row in df.iterrows():
        res = retrieve_relevant_chunks(row['query'], top_k=5)
        retrieved_ids = [r['id'] for r in res]
        if row['expected_chunk_id'] in retrieved_ids:
            hits += 1
        total += 1
    print(f"recall@5: {hits / total:.3f}")

if __name__ == "__main__":
    spot_check()
    # recall_at_5()  # Uncomment when test_labels.csv is provided
