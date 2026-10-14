from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Converts text into numerical vector embeddings.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        print("Loading embedding model...")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully!")

    def generate_embedding(self, text: str):
        """
        Generate an embedding for a single piece of text.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    def generate_embeddings(self, texts: list[str]):
        """
        Generate embeddings for multiple text chunks.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()