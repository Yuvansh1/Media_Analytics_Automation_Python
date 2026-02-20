import os
import numpy as np
from fastapi import FastAPI
from pinecone import Pinecone
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

INDEX_NAME = "insurance-claims"
NAMESPACE = "insurance_support"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

client = genai.Client(api_key=GEMINI_API_KEY)

def normalize(vec: list[float]) -> list[float]:
    v = np.array(vec, dtype=np.float32)
    v = v / np.linalg.norm(v)
    return v.tolist()

def embed(text: str) -> list[float]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=1536),
    )
    emb = result.embeddings[0].values
    return normalize(emb)

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
Answer using only the context.

Context:
{context}

Question:
{question}
"""
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return resp.text

documents = [
    {"id": "1", "text": "Auto insurance covers collision and third party liability."},
    {"id": "2", "text": "Home insurance covers fire, theft, and specific water damage."},
    {"id": "3", "text": "Flood damage requires an additional rider to be covered."},
    {"id": "4", "text": "Claims can be filed online through the customer portal or mobile app."},
]

@app.on_event("startup")
def upsert_docs():
    vectors = []
    for d in documents:
        vectors.append(
            {
                "id": d["id"],
                "values": embed(d["text"]),
                "metadata": {"text": d["text"]},
            }
        )
    index.upsert(vectors=vectors, namespace=NAMESPACE)

@app.get("/ask")
def ask(q: str):
    qvec = embed(q)
    res = index.query(vector=qvec, top_k=3, include_metadata=True, namespace=NAMESPACE)
    context = "\n".join([m["metadata"]["text"] for m in res["matches"]])
    return {"response": generate_answer(q, context)}