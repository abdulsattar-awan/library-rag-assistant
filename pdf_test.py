from pypdf import PdfReader

reader = PdfReader("library_handbook.pdf")
print("Kitne safhe:", len(reader.pages))

# Har safhe ka text jorna
full_text = ""
for page in reader.pages:
    full_text = full_text + page.extract_text() + "\n"

print("Kul characters:", len(full_text))
print("Pehle 300 characters:")
print(full_text[:300])
def make_chunks(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

chunks = make_chunks(full_text)
print("Kitne tukre bane:", len(chunks))
print("\n--- Tukra 2 ---")
print(chunks[1])