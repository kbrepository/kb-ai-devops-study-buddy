import faiss
import numpy as np

from agent.embeddings import get_embedding
from agent.faiss_store import (
    load_faiss_index,
    load_faiss_metadata,
)


def faiss_search(query, top_k=3):
    # 1. Convert the user's question into an embedding
    query_embedding = get_embedding(query)

    # 2. Convert it to a NumPy matrix expected by FAISS
    query_vector = np.array(
        [query_embedding],
        dtype="float32"
    )

    # 3. Normalize so inner product behaves like cosine similarity
    faiss.normalize_L2(query_vector)

    # 4. Load our existing FAISS index + metadata
    index = load_faiss_index()
    metadata = load_faiss_metadata()

    # 5. Ask FAISS for the nearest vectors
    scores, indices = index.search(
        query_vector,
        top_k
    )

    # 6. Convert FAISS results back into useful chunks
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


def format_faiss_results(results):
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