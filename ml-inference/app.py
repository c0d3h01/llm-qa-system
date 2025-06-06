from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
import faiss
import torch
import os
from typing import List

app = FastAPI()

class QueryPayload(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

# Load model and tokenizer (sample: distilbert-base-uncased)
MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# Load FAISS index and doc mapping
INDEX_PATH = os.getenv("VECTOR_DB_PATH", "/data/faiss.index")
DOCS_PATH = os.getenv("DOCS_PATH", "/data/docs.txt")
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(DOCS_PATH, "r") as f:
        doc_texts = [line.strip() for line in f]
else:
    index = None
    doc_texts = []

@app.post("/inference", response_model=QueryResponse)
def inference(payload: QueryPayload):
    if not index:
        return QueryResponse(answer="No index loaded", sources=[])
    inputs = tokenizer(payload.question, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        emb = model(**inputs).last_hidden_state[:, 0, :].numpy()
    D, I = index.search(emb, 3)
    sources = [doc_texts[i] for i in I[0] if i < len(doc_texts)]
    answer = f"Relevant info: {sources[0]}" if sources else "No answer found"
    return QueryResponse(answer=answer, sources=sources)