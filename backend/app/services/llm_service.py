import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMService:
    """
    Handles communication with the Gemini LLM.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in the .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.1-flash-lite"

        print("Gemini LLM initialized successfully!")

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not context or not context.strip():
            return (
                "I could not find relevant information "
                "in the support documents."
            )

        prompt = f"""
You are a Support Documentation Assistant.

Your job is to answer the user's question using ONLY
the information provided in the support documentation.

Do not invent information.

If the answer cannot be found in the provided context,
say that the information is not available in the
support documentation.

Keep the answer clear, concise, and helpful.

## SUPPORT DOCUMENTATION:

{context}

## USER QUESTION:

{question}

## ANSWER:
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text