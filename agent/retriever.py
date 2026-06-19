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


# def search_notes(query):
#     normalized_query = normalize_text(query)
#     results = []

#     for file in KNOWLEDGE_BASE.glob("*.md"):
#         content = file.read_text()
#         chunks = split_markdown_into_chunks(content)

#         for chunk in chunks:
#             normalized_chunk = normalize_text(chunk)

#             if normalized_query in normalized_chunk:
#                 results.append({
#                     "source": file.name,
#                     "content": chunk
#                 })

#     return results


###     Updated function can match related words. Even if exact phrase is not found, related words can still match.
### This fixes cases like:
####   Question: Explain AWS cloud platform
####   Note section: What is AWS


def get_keywords(text):
    normalized = normalize_text(text)
    words = normalized.split()

    stopwords = {
        "what", "is", "the", "a", "an", "and", "or", "of", "to", "in",
        "for", "on", "with", "how", "why", "explain", "tell", "me", "about"
    }

    return set(word for word in words if word not in stopwords)


def search_notes(query, top_k=3):
    query_keywords = get_keywords(query)
    scored_results = []

    for file in KNOWLEDGE_BASE.glob("*.md"):
        content = file.read_text()
        chunks = split_markdown_into_chunks(content)

        for chunk in chunks:
            chunk_keywords = get_keywords(chunk)
            matched_keywords = query_keywords.intersection(chunk_keywords)

            if matched_keywords:
                score = len(matched_keywords)

                scored_results.append({
                    "source": file.name,
                    "score": score,
                    "matched_keywords": list(matched_keywords),
                    "content": chunk,
                })

    scored_results = sorted(
        scored_results,
        key=lambda item: item["score"],
        reverse=True
    )

    return scored_results[:top_k]


def format_search_results(results):
    if not results:
        return "No relevant notes found."

    formatted = ""

    for result in results:
        formatted += f"\nSource: {result['source']}\n"
        formatted += f"Score: {result['score']}\n"
        formatted += f"Matched Keywords: {', '.join(result['matched_keywords'])}\n\n"
        formatted += result["content"]
        formatted += "\n---\n"

    return formatted