from agent.faiss_search import (
    faiss_search,
    format_faiss_results,
)


query = "How should EC2 securely access S3?"

results = faiss_search(
    query,
    top_k=3
)

print(format_faiss_results(results))