import json
from pathlib import Path

import faiss
import numpy as np

from agent.vector_store import load_vectors


HNSW_INDEX_FILE = Path("data/faiss_hnsw_index.bin")
HNSW_METADATA_FILE = Path("data/faiss_hnsw_metadata.json")


def build_hnsw_index(
    m=32,
    ef_construction=200,
):
    vectors = load_vectors()

    if not vectors:
        raise ValueError("No vectors found. Run build_vectors.py first.")

    embeddings = np.array(
        [item["embedding"] for item in vectors],
        dtype="float32",
    )

    dimension = embeddings.shape[1]

    # Normalize vectors so inner product behaves like cosine similarity.
    faiss.normalize_L2(embeddings)

    index = faiss.IndexHNSWFlat(
        dimension,
        m,
        faiss.METRIC_INNER_PRODUCT,
    )

    index.hnsw.efConstruction = ef_construction

    index.add(embeddings)

    faiss.write_index(
        index,
        str(HNSW_INDEX_FILE),
    )

    metadata = [
        {
            "source": item["source"],
            "chunk_id": item["chunk_id"],
            "content": item["content"],
        }
        for item in vectors
    ]

    with open(HNSW_METADATA_FILE, "w") as file:
        json.dump(metadata, file, indent=4)

    return len(metadata)


def load_hnsw_index():
    if not HNSW_INDEX_FILE.exists():
        raise FileNotFoundError(
            "HNSW index not found. Build it first."
        )

    return faiss.read_index(
        str(HNSW_INDEX_FILE)
    )


def load_hnsw_metadata():
    with open(HNSW_METADATA_FILE, "r") as file:
        return json.load(file)