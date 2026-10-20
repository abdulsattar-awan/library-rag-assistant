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

# Do vectors kitne qareeb hain (1 = bilkul ek jaise, 0 = koi taluq nahi)
def similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    size_a = math.sqrt(sum(x * x for x in a))
    size_b = math.sqrt(sum(y * y for y in b))
    return dot / (size_a * size_b)

question = get_vector("How much will I pay if I return a book 3 days late?")
fine     = get_vector("The fine for a late book is Rs. 20 per day per book.")
loan     = get_vector("Books are issued for 14 days. A book can be renewed once.")
phone    = get_vector("Mobile phones must be on silent.")

print("Sawal vs Fine :", round(similarity(question, fine), 3))
print("Sawal vs Loan :", round(similarity(question, loan), 3))
print("Sawal vs Phone:", round(similarity(question, phone), 3))