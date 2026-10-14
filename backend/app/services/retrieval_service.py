from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import VectorStore


class RetrievalService:
    """
    Handles semantic search over the support document knowledge base.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Retrieve the most relevant document chunks
        for a user question.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        # Generate embedding for the user's question
        query_embedding = (
            self.embedding_service.generate_embedding(query)
        )

        # Search ChromaDB
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results

    def get_context(
        self,
        query: str,
        top_k: int = 5
    ) -> str:
        """
        Retrieve relevant chunks and combine them
        into context for the LLM.
        """

        results = self.retrieve(
            query=query,
            top_k=top_k
        )

        documents = results.get("documents", [[]])[0]

        if not documents:
            return ""

        context_parts = []

        for i, document in enumerate(documents):

            context_parts.append(
                f"[Document Chunk {i + 1}]\n"
                f"{document}"
            )

        return "\n\n".join(context_parts)