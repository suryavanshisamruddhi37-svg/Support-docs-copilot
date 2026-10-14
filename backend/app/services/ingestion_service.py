from pathlib import Path

from backend.app.utils.file_parser import extract_text
from backend.app.utils.chunking import chunk_text
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore


class IngestionService:
    """
    Handles the complete document ingestion pipeline.

    Pipeline:
        Document
        ↓
        Text Extraction
        ↓
        Cleaning + Chunking
        ↓
        Embeddings
        ↓
        ChromaDB
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def ingest_document(self, file_path: str):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        print("\n" + "=" * 60)
        print("DOCUMENT INGESTION")
        print("=" * 60)

        print(f"\nFile: {path.name}")

        # -------------------------------------------------
        # 1. Remove existing chunks for this document
        # -------------------------------------------------

        print("\nChecking for existing document...")

        existing = self.vector_store.collection.get(
            where={
                "source": path.name
            }
        )

        existing_ids = existing.get("ids", [])

        if existing_ids:

            print(
                f"Found {len(existing_ids)} existing chunks."
            )

            print("Removing old chunks...")

            self.vector_store.collection.delete(
                ids=existing_ids
            )

            print("Old chunks removed.")

        else:

            print("No existing chunks found.")

        # -------------------------------------------------
        # 2. Extract text
        # -------------------------------------------------

        print("\nExtracting text...")

        text = extract_text(str(path))

        if not text.strip():
            raise ValueError(
                "No text could be extracted from the document."
            )

        print("Text extracted successfully!")
        print(f"Characters extracted: {len(text)}")

        # -------------------------------------------------
        # 3. Create chunks
        # -------------------------------------------------

        print("\nCreating chunks...")

        chunks = chunk_text(
            text,
            chunk_size=800,
            chunk_overlap=150
        )

        if not chunks:
            raise ValueError(
                "No chunks were created from the document."
            )

        print("Chunks created successfully!")
        print(f"Number of chunks: {len(chunks)}")

        # -------------------------------------------------
        # 4. Generate embeddings
        # -------------------------------------------------

        print("\nGenerating embeddings...")

        embeddings = (
            self.embedding_service.generate_embeddings(
                chunks
            )
        )

        if not embeddings:
            raise ValueError(
                "No embeddings were generated."
            )

        print("Embeddings generated successfully!")

        print(
            f"Embedding dimension: "
            f"{len(embeddings[0])}"
        )

        # -------------------------------------------------
        # 5. Create metadata
        # -------------------------------------------------

        print("\nCreating metadata...")

        metadatas = []

        for i in range(len(chunks)):

            metadata = {
                "source": path.name,
                "chunk_index": i
            }

            metadatas.append(metadata)

        # -------------------------------------------------
        # 6. Create unique IDs
        # -------------------------------------------------

        ids = []

        for i in range(len(chunks)):

            document_id = (
                f"{path.stem}_chunk_{i}"
            )

            ids.append(document_id)

        # -------------------------------------------------
        # 7. Store in ChromaDB
        # -------------------------------------------------

        print("\nStoring document in ChromaDB...")

        self.vector_store.add_documents(
            chunks,
            embeddings,
            metadatas,
            ids
        )

        print("Document stored successfully!")

        # -------------------------------------------------
        # 8. Return result
        # -------------------------------------------------

        result = {
            "filename": path.name,
            "chunks": len(chunks),
            "embedding_dimension": len(embeddings[0]),
            "status": "success"
        }

        print("\n" + "=" * 60)
        print("DOCUMENT INGESTION COMPLETED")
        print("=" * 60)

        print(f"Filename: {result['filename']}")
        print(f"Chunks: {result['chunks']}")
        print(
            f"Embedding dimension: "
            f"{result['embedding_dimension']}"
        )
        print(f"Status: {result['status']}")

        return result