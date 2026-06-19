import re
from pathlib import Path


KNOWLEDGE_BASE = Path("knowledge_base")


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def split_markdown_into_chunks(content):
    chunks = []
    current_chunk = []

    for line in content.splitlines():
        if line.startswith("## ") and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
        else:
            current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


def search_notes(query):
    normalized_query = normalize_text(query)
    results = []

    for file in KNOWLEDGE_BASE.glob("*.md"):
        content = file.read_text()
        chunks = split_markdown_into_chunks(content)

        for chunk in chunks:
            normalized_chunk = normalize_text(chunk)

            if normalized_query in normalized_chunk:
                results.append({
                    "source": file.name,
                    "content": chunk
                })

    return results


def format_search_results(results):
    if not results:
        return "No relevant notes found."

    formatted = ""

    for result in results:
        formatted += f"\nSource: {result['source']}\n"
        formatted += result["content"]
        formatted += "\n---\n"

    return formatted