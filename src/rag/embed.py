"""Embed chunks and update the existing index if needed."""

import faiss
import pickle
import json
import numpy as np
from loguru import logger
from openai import OpenAI
from pathlib import Path

def embed_chunks(chunks: list[dict], *, update_existing: bool = False) -> None:
  """Embed chunks and update the existing index if needed."""
  logger.debug(f"Embedding {len(chunks)} chunks")
  client = OpenAI()

  # Load existing index and chunks if updating
  if update_existing and Path("data/embeddings.faiss").exists():
    with Path("data/embeddings.faiss").open("rb") as f:
      index = pickle.load(f)
      logger.debug(f"Starting index type: {type(index)}")
      logger.debug(f"Starting index dimensions: {index.d}")
      logger.debug(f"Starting index number of vectors: {index.ntotal}")
    with Path("data/chunks.json").open("r", encoding="utf-8") as f:
      existing_chunks = json.load(f)
  else:
    existing_chunks = []
    dim = 1536  # dimension for text-embedding-3-small
    index = faiss.IndexFlatL2(dim)

  # Get embeddings for new chunks
  new_embeddings = [
    client.embeddings.create(
      input=chunk["text"],
      model="text-embedding-3-small",
    ).data[0].embedding
    for chunk in chunks
  ]

  if new_embeddings:
    # Always add to the existing or new index
    index.add(np.array(new_embeddings).astype("float32"))
    logger.debug(f"New index type: {type(index)}")
    logger.debug(f"New index dimensions: {index.d}")
    logger.debug(f"New index number of vectors: {index.ntotal}")
    with Path("data/embeddings.faiss").open("wb") as f:
      pickle.dump(index, f)

    # Update chunks file
    all_chunks = existing_chunks + chunks
    with Path("data/chunks.json").open("w", encoding="utf-8") as f:
      json.dump(all_chunks, f)
