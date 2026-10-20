# Library RAG Assistant

An AI library assistant that answers questions from a PDF library handbook using **RAG (Retrieval-Augmented Generation)**.

Built by a librarian learning AI automation: the same job a librarian does (find the right source, then answer), done by AI.

## How it works

1. **Read** the PDF handbook and remove noise (page footers)
2. **Chunk** the text into 500-character pieces with 100-character overlap
3. **Embed** each chunk with Gemini embeddings (`gemini-embedding-001`)
4. **Retrieve** the top 3 chunks closest in meaning to the question (cosine similarity)
5. **Generate** an answer with Gemini, using ONLY the retrieved text

## Features

- Semantic search: finds the right rule even when the words are different
- Combines multiple rules for complex questions
- Says "I don't know" when the answer is not in the document (no hallucination)
- Answers in English and Roman Urdu
- Handles server errors without crashing

## Example

```
Q: I returned a Reserve shelf book 2 hours late. What is my fine?
A: The fine for a Reserve shelf book is Rs. 50 per hour, so your fine is Rs. 100.

Q: Ghar se e-books kaise parh sakta hoon?
A: Library ke remote access page ke zariye apna college email aur password istemal kar ke log in karein.
```

## What I learned

I first tried simple keyword matching. It picked the wrong chunk because of small words like "I", "a" and "if". Switching to embeddings fixed it, because they compare meaning, not words.

## Setup

```
pip install -r requirements.txt
```

Create a `.env` file with your key:

```
GEMINI_API_KEY=your_key_here
```

Run:

```
python rag_pdf.py
```

## Files

| File | Purpose |
|---|---|
| `rag_pdf.py` | Main RAG assistant for the PDF handbook |
| `rag.py` | First version using a small text file |
| `embed_test.py` | Experiment comparing sentence similarity |
| `library_handbook.pdf` | Sample handbook of a fictional college |

## Tech

Python, Google Gemini (google-genai), Gemini embeddings, pypdf, python-dotenv