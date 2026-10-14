import chromadb
from pathlib import Path


class VectorStore:
    """
    Handles storing and retrieving document chunks
    and their embeddings using ChromaDB.
    """

    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "support_documents"
    ):
        self.db_path = Path(db_path)

        self.db_path.mkdir(
            parents=True,
            exist_ok=True
        )

        print("Initializing ChromaDB...")

        self.client = chromadb.PersistentClient(
            path=str(self.db_path)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "Support document knowledge base"
            }
        )

        print("ChromaDB initialized successfully!")
        print(
            f"Collection: {collection_name}"
        )

    def add_documents(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
        ids: list[str]
    ):
        """
        Store document chunks, embeddings and metadata.
        """

        if not chunks:
            raise ValueError("No chunks provided.")

        if not (
            len(chunks)
            == len(embeddings)
            == len(metadatas)
            == len(ids)
        ):
            raise ValueError(
                "Chunks, embeddings, metadata and IDs "
                "must have the same length."
            )

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        print(
            f"Successfully stored {len(chunks)} chunks."
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5
    ):
        """
        Search the knowledge base for similar chunks.
        """

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    def count(self) -> int:
        """
        Return number of stored chunks.
        """

        return self.collection.count()