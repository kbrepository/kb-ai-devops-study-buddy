import json
from pathlib import Path

import faiss
import numpy as np

from agent.vector_store import load_vectors


FAISS_INDEX_FILE = Path("data/faiss_index.bin")
FAISS_METADATA_FILE = Path("data/faiss_metadata.json")


def build_faiss_index():
    vectors = load_vectors()

    if not vectors:
        raise ValueError("No vectors found. Run build_vectors.py first.")

    embeddings = np.array(
        [item["embedding"] for item in vectors],
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    faiss.write_index(index, str(FAISS_INDEX_FILE))

    metadata = [
        {
            "source": item["source"],
            "chunk_id": item["chunk_id"],
            "content": item["content"],
        }
        for item in vectors
    ]

    with open(FAISS_METADATA_FILE, "w") as file:
        json.dump(metadata, file, indent=4)

    return len(metadata)


def load_faiss_index():
    if not FAISS_INDEX_FILE.exists():
        raise FileNotFoundError("FAISS index not found. Build it first.")

    return faiss.read_index(str(FAISS_INDEX_FILE))


def load_faiss_metadata():
    with open(FAISS_METADATA_FILE, "r") as file:
        return json.load(file)