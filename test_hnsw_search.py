from agent.faiss_hnsw_search import (
    hnsw_search,
    format_hnsw_results,
)


query = "How should EC2 securely access S3?"

results = hnsw_search(
    query,
    top_k=3,
)

print(format_hnsw_results(results))