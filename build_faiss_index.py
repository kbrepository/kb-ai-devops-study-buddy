from agent.faiss_store import build_faiss_index

count = build_faiss_index()

print("FAISS index built successfully.")
print(f"Total vectors indexed: {count}")