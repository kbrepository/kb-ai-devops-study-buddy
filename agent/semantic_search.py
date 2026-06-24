import math

from agent.embeddings import get_embedding
from agent.vector_store import load_vectors


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


def semantic_search(query, top_k=3):
    query_embedding = get_embedding(query)
    vectors = load_vectors()

    scored_results = []

    for item in vectors:
        score = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        scored_results.append({
            "source": item["source"],
            "chunk_id": item["chunk_id"],
            "score": score,
            "content": item["content"],
        })

    scored_results = sorted(
        scored_results,
        key=lambda item: item["score"],
        reverse=True
    )

    return scored_results[:top_k]


def format_semantic_results(results):
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