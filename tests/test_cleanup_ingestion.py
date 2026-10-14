from backend.app.services.vector_store import VectorStore


print("=" * 60)
print("CLEANING INGESTION TEST DATA")
print("=" * 60)


vector_store = VectorStore()

# IDs created by test_ingestion.py
ingestion_test_ids = [
    f"test_manual_chunk_{i}"
    for i in range(12)
]

before_count = vector_store.count()

print(f"\nDocuments before cleanup: {before_count}")

print("\nDeleting ingestion test records...")

vector_store.collection.delete(
    ids=ingestion_test_ids
)

after_count = vector_store.count()

print("Ingestion test records deleted.")

print(f"\nDocuments after cleanup: {after_count}")
print(f"Records removed: {before_count - after_count}")

print("\n" + "=" * 60)
print("INGESTION CLEANUP COMPLETED")
print("=" * 60)