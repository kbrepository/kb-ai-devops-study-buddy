# This is a temporary runner
from agent.vector_store_builder import build_vector_store

count = build_vector_store()

print(f"Vector store built successfully.")
print(f"Total chunks embedded: {count}")