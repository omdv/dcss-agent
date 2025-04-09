"""Prepare data for RAG."""
import json
import pickle
from pathlib import Path
from tiktoken import get_encoding
from openai import OpenAI
import numpy as np
import faiss

encoding = get_encoding("cl100k_base")

def load_and_chunk(file_path: str, chunk_tokens: int = 500) -> list[str]:
  """Load and chunk text."""
  text = Path(file_path).read_text()
  tokens = encoding.encode(text)

  chunks = []
  for i in range(0, len(tokens), chunk_tokens):
    chunk = encoding.decode(tokens[i:i + chunk_tokens])
    chunks.append(chunk)
  return chunks

def embed_chunks(chunks: list[str]) -> list[np.ndarray]:
  """Embed chunks and save embeddings to a file."""
  client = OpenAI()

  embeddings = [
    client.embeddings.create(
      input=chunk,
      model="text-embedding-3-small",
    ).data[0].embedding
    for chunk in chunks
  ]

  dim = len(embeddings[0])
  index = faiss.IndexFlatL2(dim)
  index.add(np.array(embeddings).astype("float32"))
  with Path("data/embeddings.faiss").open("wb") as f:
    pickle.dump(index, f)

if __name__ == "__main__":
    all_chunks = []
    for file in Path("data/raw/").glob("*.txt"):
      all_chunks.extend(load_and_chunk(str(file)))
    with Path("data/chunks.json").open("w", encoding="utf-8") as f:
      json.dump(all_chunks, f)
    embed_chunks(all_chunks)
