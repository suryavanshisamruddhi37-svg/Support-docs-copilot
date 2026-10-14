from backend.app.services.ingestion_service import IngestionService


print("=" * 60)
print("TESTING DOCUMENT INGESTION")
print("=" * 60)


print("\nInitializing ingestion service...")

ingestion_service = IngestionService()

print("Ingestion service initialized successfully!")


file_path = "data/sample_documents/1022411079 DBMS A4.pdf"

print(f"\nDocument:")
print(file_path)


try:

    result = ingestion_service.ingest_document(
        file_path
    )

    print("\nIngestion Result:")
    print("=" * 60)

    print(f"Filename: {result['filename']}")
    print(f"Chunks: {result['chunks']}")
    print(
        f"Embedding Dimension: "
        f"{result['embedding_dimension']}"
    )
    print(f"Status: {result['status']}")

except Exception as e:

    print("\nINGESTION FAILED")

    print(f"Error Type: {type(e).__name__}")
    print(f"Error: {e}")


print("\n" + "=" * 60)
print("INGESTION TEST COMPLETED")
print("=" * 60)