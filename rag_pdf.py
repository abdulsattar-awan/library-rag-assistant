import os
import math
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. PDF parhna aur footer ka kachra saaf karna
reader = PdfReader("library_handbook.pdf")
full_text = ""
for page in reader.pages:
    for line in page.extract_text().split("\n"):
        if "sample document for RAG practice" in line:
            continue
        if line.startswith("Page "):
            continue
        full_text = full_text + line + "\n"

# 2. Tukre banana (overlap ke saath)
def make_chunks(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start = start + size - overlap
    return chunks

chunks = make_chunks(full_text)

# 3. Embeddings
def get_vector(text):
    result = client.models.embed_content(model="gemini-embedding-001", contents=text)
    return result.embeddings[0].values

def similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

chunk_vectors = [get_vector(c) for c in chunks]
print("PDF tayyar:", len(chunks), "tukre")

# 4. Retrieval: top 3 (threshold ke saath)
THRESHOLD = 0.65

def find_top_chunks(question, top_k=3):
    q_vector = get_vector(question)
    scored = [(similarity(q_vector, chunk_vectors[i]), chunks[i]) for i in range(len(chunks))]
    scored.sort(reverse=True)
    best_score = scored[0][0]
    print("  [Sab se achha score:", round(best_score, 3), "]")
    if best_score < THRESHOLD:
        return ""
    return "\n\n".join(chunk for score, chunk in scored[:top_k])

# 5. Generation
def answer_question(question):
    context = find_top_chunks(question)
    if context == "":
        return "I don't know. Yeh maloomat library handbook mein nahi hai."
    prompt = f"""You are a helpful library assistant for Green Valley College Library.
Answer the question using ONLY the information below.
If the answer is not in the information, say "I don't know".
Reply in the same language as the question. If the question is in Roman Urdu, use Urdu words (not Hindi words).

Information:
{context}

Question: {question}"""
    response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
    return response.text
# 6. Chat loop
print("Library Assistant tayyar hai! Band karne ke liye 'exit' likhein.")
while True:
    question = input("\nAap ka sawal: ")
    if question.lower() == "exit":
        print("Allah Hafiz!")
        break
    try:
        print("AI:", answer_question(question))
    except Exception as e:
        print("Maaf kijiye, abhi server masroof hai. Thori der baad dobara try karein.")