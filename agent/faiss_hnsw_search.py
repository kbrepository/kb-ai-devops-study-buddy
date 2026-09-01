import faiss
import numpy as np

from agent.embeddings import get_embedding
from agent.faiss_hnsw_store import (
    load_hnsw_index,
    load_hnsw_metadata,
)


def hnsw_search(
    query,
    top_k=3,
    ef_search=64,
):
    query_embedding = get_embedding(query)

    query_vector = np.array(
        [query_embedding],
        dtype="float32",
    )

    faiss.normalize_L2(query_vector)

    index = load_hnsw_index()
    metadata = load_hnsw_metadata()

    index.hnsw.efSearch = ef_search

    scores, indices = index.search(
        query_vector,
        top_k,
    )

    results = []

    for score, index_id in zip(scores[0], indices[0]):
        if index_id == -1:
            continue

        item = metadata[index_id]

        results.append({
            "source": item["source"],
            "chunk_id": item["chunk_id"],
            "score": float(score),
            "content": item["content"],
        })

    return results


def format_hnsw_results(results):
    if not results:
        return "No relevant notes found."

    formatted = ""

    for result in results:
        formatted += f"\nSource: {result['source']}\n"
        formatted += f"Chunk ID: {result['chunk_id']}\n"
        formatted += f"Similarity Score: {result['score']:.4f}\n\n"
        formatted += result["content"]
        formatted += "\n---\n"

    return formatted