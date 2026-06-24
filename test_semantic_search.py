from agent.semantic_search import semantic_search, format_semantic_results

query = "How should EC2 securely access S3?"

results = semantic_search(query)

print(format_semantic_results(results))
