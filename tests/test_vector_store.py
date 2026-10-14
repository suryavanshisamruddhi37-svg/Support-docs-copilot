from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore


print("=" * 60)
print("TESTING VECTOR STORE")
print("=" * 60)


# ---------------------------------------------------------
# 1. Initialize Embedding Service
# ---------------------------------------------------------

embedding_service = EmbeddingService()


# ---------------------------------------------------------
# 2. Initialize Vector Store
# ---------------------------------------------------------

vector_store = VectorStore()


# ---------------------------------------------------------
# 3. Sample document chunks
# ---------------------------------------------------------

chunks = [
    "To fix a paper jam, open the rear cover and remove the paper.",
    "To restart the printer, press and hold the power button.",
    "Replace the cartridge when the toner indicator becomes empty."
]


print("\nSample chunks:")

for i, chunk in enumerate(chunks):
    print(f"{i + 1}. {chunk}")


# ---------------------------------------------------------
# 4. Generate embeddings
# ---------------------------------------------------------

print("\nGenerating embeddings...")

embeddings = embedding_service.generate_embeddings(chunks)

print("Embeddings generated successfully!")
print(f"Number of embeddings: {len(embeddings)}")

if embeddings:
    print(f"Embedding dimension: {len(embeddings[0])}")


# ---------------------------------------------------------
# 5. Create metadata
# ---------------------------------------------------------

metadatas = [
    {
        "source": "test_manual.pdf",
        "chunk_index": 0
    },
    {
        "source": "test_manual.pdf",
        "chunk_index": 1
    },
    {
        "source": "test_manual.pdf",
        "chunk_index": 2
    }
]


# ---------------------------------------------------------
# 6. Create unique IDs
# ---------------------------------------------------------

ids = [
    "test_chunk_001",
    "test_chunk_002",
    "test_chunk_003"
]


print("\nMetadata and IDs created.")


# ---------------------------------------------------------
# 7. Add documents to ChromaDB
# ---------------------------------------------------------

print("\nAdding chunks to vector store...")

vector_store.add_documents(
    chunks,
    embeddings,
    metadatas,
    ids
)

print("Chunks added successfully!")


# ---------------------------------------------------------
# 8. Test similarity search
# ---------------------------------------------------------

print("\nTesting similarity search...")

query = "How do I fix a paper jam?"

print(f"\nQuery: {query}")


# Generate embedding for query
query_embedding = embedding_service.generate_embedding(query)


# ---------------------------------------------------------
# 9. Search ChromaDB
# ---------------------------------------------------------

results = vector_store.search(
    query_embedding=query_embedding,
    top_k=3
)


# ---------------------------------------------------------
# 10. Display search results
# ---------------------------------------------------------

print("\nSearch Results:")
print("=" * 60)


documents = results.get("documents", [[]])[0]


if documents:

    for i, document in enumerate(documents):

        print(f"\nResult {i + 1}:")
        print(document)

else:

    print("No results found.")


# ---------------------------------------------------------
# 11. Display metadata
# ---------------------------------------------------------

metadatas_result = results.get("metadatas", [[]])[0]


if metadatas_result:

    print("\nRetrieved Metadata:")
    print("-" * 60)

    for i, metadata in enumerate(metadatas_result):

        print(f"\nResult {i + 1} Metadata:")
        print(metadata)


# ---------------------------------------------------------
# 12. Test completed
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("VECTOR STORE TEST COMPLETED")
print("=" * 60)
# ---------------------------------------------------------
# 12. Clean up test records
# ---------------------------------------------------------

print("\nCleaning up test records...")

vector_store.collection.delete(
    ids=ids
)

print("Test records removed successfully!")


# ---------------------------------------------------------
# 13. Test completed
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("VECTOR STORE TEST COMPLETED")
print("=" * 60)