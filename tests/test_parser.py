from backend.app.utils.file_parser import extract_text


file_path = "data/sample_documents/test_manual.pdf"


print("=" * 60)
print("TESTING DOCUMENT PARSER")
print("=" * 60)


try:

    text = extract_text(file_path)

    print("\nDOCUMENT SUCCESSFULLY READ!\n")

    print("-" * 60)
    print("EXTRACTED TEXT")
    print("-" * 60)

    print(text[:5000])

    print("\n" + "-" * 60)
    print(f"Total characters extracted: {len(text)}")
    print("-" * 60)

except Exception as error:

    print("\nERROR:")
    print(error)