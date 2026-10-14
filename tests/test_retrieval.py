from backend.app.services.retrieval_service import RetrievalService


print("=" * 60)
print("TESTING RETRIEVAL SERVICE")
print("=" * 60)


retrieval_service = RetrievalService()


query = "What is the difference between WHERE and HAVING?"


print(f"\nUser Query:")
print(query)


print("\nSearching knowledge base...")


results = retrieval_service.retrieve(
    query=query,
    top_k=3
)


print("\nRetrieved Documents")
print("=" * 60)


documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for i in range(len(documents)):

    print(f"\nResult {i + 1}")
    print("-" * 40)

    print("Text:")
    print(documents[i])

    print("\nMetadata:")
    print(metadatas[i])

    print("\nDistance:")
    print(distances[i])


print("\n" + "=" * 60)
print("RETRIEVAL TEST COMPLETED")
print("=" * 60)