import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")


print("=" * 60)
print("DIRECT GEMINI API TEST")
print("=" * 60)


client = genai.Client(
    api_key=api_key
)


models_to_test = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
]


for model in models_to_test:

    print("\n" + "=" * 60)
    print(f"Testing model: {model}")
    print("=" * 60)

    try:

        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: Gemini test successful"
        )

        print("\nSUCCESS")
        print("Response:")
        print(response.text)

    except Exception as e:

        print("\nFAILED")
        print("Error type:")
        print(type(e).__name__)

        print("\nError message:")
        print(e)


print("\n" + "=" * 60)
print("DIRECT GEMINI TEST COMPLETED")
print("=" * 60)