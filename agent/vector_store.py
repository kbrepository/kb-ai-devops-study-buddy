import json
from pathlib import Path

VECTOR_STORE = Path(
    "data/vector_store.json"
)


def load_vectors():
    if not VECTOR_STORE.exists():
        return []

    with open(VECTOR_STORE) as file:
        return json.load(file)


def save_vectors(vectors):
    with open(VECTOR_STORE, "w") as file:
        json.dump(
            vectors,
            file,
            indent=4
        )