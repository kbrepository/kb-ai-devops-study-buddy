from pathlib import Path


KNOWLEDGE_BASE = Path("knowledge_base")


def search_notes(query):
    query = query.lower()

    results = []

    for file in KNOWLEDGE_BASE.glob("*.md"):
        content = file.read_text()

        if query in content.lower():
            results.append(content)

    return "\n\n".join(results)