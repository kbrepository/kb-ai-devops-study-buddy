from agent.faiss_hnsw_store import build_hnsw_index


count = build_hnsw_index()

print("HNSW index built successfully.")
print(f"Total vectors indexed: {count}")