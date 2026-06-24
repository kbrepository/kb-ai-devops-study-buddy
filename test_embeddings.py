from agent.embeddings import get_embedding

result = get_embedding(
    "Terraform State stores infrastructure information"
)

print(type(result))
print(len(result))
print(result[:5])