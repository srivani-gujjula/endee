import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("dataset.json") as f:
    data = json.load(f)

texts = []

for item in data:
    text = item["name"] + " " + item["service"] + " " + item["location"]
    texts.append(text)

embeddings = model.encode(texts)

print("Embeddings created successfully")
