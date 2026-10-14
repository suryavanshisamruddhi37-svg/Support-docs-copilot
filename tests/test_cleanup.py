from backend.app.services.vector_store import VectorStore


print("=" * 60)
print("CLEANING TEST DATA FROM CHROMADB")
print("=" * 60)


# ---------------------------------------------------------
# 1. Initialize Vector Store
# ---------------------------------------------------------

vector_store = VectorStore()


# ---------------------------------------------------------
# 2. Test IDs created by test_vector_store.py
# ---------------------------------------------------------

test_ids = [
    "test_chunk_001",
    "test_chunk_002",
    "test_chunk_003"
]


# ---------------------------------------------------------
# 3. Check current database size
# ---------------------------------------------------------

before_count = vector_store.count()

print(f"\nDocuments before cleanup: {before_count}")


# ---------------------------------------------------------
# 4. Delete only the test records
# ---------------------------------------------------------

print("\nDeleting test records...")

vector_store.collection.delete(
    ids=test_ids
)

print("Test records deleted successfully!")


# ---------------------------------------------------------
# 5. Check database size after cleanup
# ---------------------------------------------------------

after_count = vector_store.count()

print(f"\nDocuments after cleanup: {after_count}")


# ---------------------------------------------------------
# 6. Display result
# ---------------------------------------------------------

deleted_count = before_count - after_count

print("\n" + "=" * 60)
print("CLEANUP COMPLETED")
print("=" * 60)

print(f"Records removed: {deleted_count}")
print(f"Records remaining: {after_count}")

print("\nActual document records were preserved.")
print("=" * 60)