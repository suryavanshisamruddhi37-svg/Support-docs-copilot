from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.llm_service import LLMService


print("=" * 60)
print("TESTING COMPLETE RAG PIPELINE")
print("=" * 60)


# ---------------------------------------------------------
# 1. Initialize services
# ---------------------------------------------------------

print("\nInitializing Retrieval Service...")

retrieval_service = RetrievalService()

print("Retrieval Service initialized successfully!")


print("\nInitializing LLM Service...")

llm_service = LLMService()

print("LLM Service initialized successfully!")


# ---------------------------------------------------------
# 2. User question
# ---------------------------------------------------------

question = "What is the difference between WHERE and HAVING?"

print("\nUser Question:")
print(question)


# ---------------------------------------------------------
# 3. Retrieve relevant context
# ---------------------------------------------------------

print("\nRetrieving relevant information...")

context = retrieval_service.get_context(
    query=question,
    top_k=5
)


if not context:

    print("\nNo relevant context found.")

    print("\n" + "=" * 60)
    print("RAG TEST FAILED")
    print("=" * 60)

    exit()


print("\nRelevant Context Retrieved:")
print("=" * 60)
print(context)


# ---------------------------------------------------------
# 4. Generate answer using Gemini
# ---------------------------------------------------------

print("\n")
print("=" * 60)
print("GENERATING ANSWER USING GEMINI")
print("=" * 60)


try:

    answer = llm_service.generate_answer(
        question=question,
        context=context
    )

    print("\nFinal Answer:")
    print("=" * 60)
    print(answer)

except Exception as e:

    print("\nGemini request failed.")

    print("Error:")
    print(e)

    print("\n" + "=" * 60)
    print("RAG TEST FAILED AT LLM STAGE")
    print("=" * 60)

    exit()


# ---------------------------------------------------------
# 5. Test completed
# ---------------------------------------------------------

print("\n")
print("=" * 60)
print("COMPLETE RAG PIPELINE TEST COMPLETED")
print("=" * 60)