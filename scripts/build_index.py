"""
Script to build FAISS index from documentation snippets.
"""

import faiss
from transformers import AutoTokenizer, AutoModel
import torch
import os

MODEL_NAME = "distilbert-base-uncased"
DATA_PATH = "data/raw/"
OUTPUT_INDEX = "data/faiss.index"
OUTPUT_DOCS = "data/docs.txt"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def embed(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        return model(**inputs).last_hidden_state[:, 0, :].numpy()[0]

docs = []
vectors = []
for fname in os.listdir(DATA_PATH):
    with open(os.path.join(DATA_PATH, fname), "r") as f:
        for line in f:
            content = line.strip()
            if content:
                docs.append(content)
                vectors.append(embed(content))

xb = torch.stack([torch.tensor(v) for v in vectors]).numpy()
index = faiss.IndexFlatL2(xb.shape[1])
index.add(xb)
faiss.write_index(index, OUTPUT_INDEX)
with open(OUTPUT_DOCS, "w") as f:
    for doc in docs:
        f.write(doc + "\n")
print(f"Indexed {len(docs)} docs.")