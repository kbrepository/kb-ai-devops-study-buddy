from pathlib import Path

from agent.embeddings import get_embedding
from agent.retriever import split_markdown_into_chunks
from agent.vector_store import save_vectors


KNOWLEDGE_BASE = Path("knowledge_base")


def build_vector_store():
    vector_records = []

    for file in KNOWLEDGE_BASE.rglob("*.md"):
        print(f"Processing: {file}")

        content = file.read_text(encoding="utf-8")
        chunks = split_markdown_into_chunks(content)

        for index, chunk in enumerate(chunks):
            if not chunk.strip():
                continue

            embedding = get_embedding(chunk)

            record = {
                "source": str(file.relative_to(KNOWLEDGE_BASE)),
                "chunk_id": index,
                "content": chunk,
                "embedding": embedding,
            }

            vector_records.append(record)

    save_vectors(vector_records)

    return len(vector_records)