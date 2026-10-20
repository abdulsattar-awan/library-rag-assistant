import os
import math
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_vector(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    size_a = math.sqrt(sum(x * x for x in a))
    size_b = math.sqrt(sum(y * y for y in b))
    return dot / (size_a * size_b)

# 1. Kitaab parhna aur tukre karna
with open("library_rules.txt", "r", encoding="utf-8") as f:
    text = f.read()
chunks = text.split("\n\n")

# 2. Har tukre ka "address" (vector) ek dafa bana kar rakh lena
chunk_vectors = []
for chunk in chunks:
    chunk_vectors.append(get_vector(chunk))
print("Tukron ke vectors tayyar:", len(chunk_vectors))

# 3. RETRIEVAL: sawal ke sab se qareeb tukra
def find_best_chunk(question, top_k=3):
    q_vector = get_vector(question)
    scored = []
    for i in range(len(chunks)):
        score = similarity(q_vector, chunk_vectors[i])
        scored.append((score, chunks[i]))
    scored.sort(reverse=True)
    top_chunks = [chunk for score, chunk in scored[:top_k]]
    return "\n\n".join(top_chunks)
# 4. GENERATION: Gemini se jawab
def answer_question(question):
    context = find_best_chunk(question)
    prompt = f"""You are a helpful library assistant.
Answer the question using ONLY the information below.
If the answer is not in the information, say "I don't know".
Reply in the same language as the question. If the question is in Roman Urdu, use Urdu words (not Hindi words).

Information: {context}

Question: {question}"""
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    return context, response.text

# 5. Chat loop
print("Library Assistant tayyar hai! Band karne ke liye 'exit' likhein.")

while True:
    question = input("\nAap ka sawal: ")
    if question.lower() == "exit":
        print("Allah Hafiz!")
        break
    try:
        context, answer = answer_question(question)
        print("AI:", answer)
    except Exception as e:
        print("Maaf kijiye, abhi server masroof hai. Thori der baad dobara try karein.")