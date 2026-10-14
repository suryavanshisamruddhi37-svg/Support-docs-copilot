from backend.app.utils.file_parser import extract_text
from backend.app.utils.chunking import chunk_text


file_path = "data/sample_documents/test_manual.pdf"


print("=" * 60)
print("TESTING DOCUMENT CHUNKING")
print("=" * 60)


# Step 1: Extract text
text = extract_text(file_path)

print(f"\nTotal document characters: {len(text)}")


# Step 2: Create chunks
chunks = chunk_text(
    text,
    chunk_size=800,
    chunk_overlap=150
)


print(f"Total chunks created: {len(chunks)}")


# Step 3: Display chunks
print("\n" + "=" * 60)
print("CHUNKS")
print("=" * 60)


for index, chunk in enumerate(chunks, start=1):

    print(f"\n--- CHUNK {index} ---")
    print(f"Characters: {len(chunk)}")
    print(chunk[:800])


print("\n" + "=" * 60)
print("CHUNKING TEST COMPLETED")
print("=" * 60)