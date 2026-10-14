from backend.app.services.embedding_service import EmbeddingService


print("=" * 60)
print("TESTING EMBEDDING SERVICE")
print("=" * 60)


embedding_service = EmbeddingService()


text = """
To fix a paper jam, open the rear cover
and carefully remove the jammed paper.
"""


embedding = embedding_service.generate_embedding(text)


print("\nEmbedding generated successfully!")

print(f"Embedding dimensions: {len(embedding)}")

print("\nFirst 10 values:")
print(embedding[:10])

print("\n" + "=" * 60)
print("EMBEDDING TEST COMPLETED")
print("=" * 60)