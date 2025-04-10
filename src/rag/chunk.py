"""Prepare data for RAG."""
import json
from loguru import logger
from pathlib import Path
from tiktoken import get_encoding
from datetime import datetime, UTC

encoding = get_encoding("cl100k_base")

def load_and_chunk(file_path: str, chunk_tokens: int = 1000) -> list[dict]:
  """Load and chunk text, returning chunks with metadata."""
  logger.debug(f"Loading and chunking {file_path}")
  text = Path(file_path).read_text()
  tokens = encoding.encode(text)

  chunks = []
  for i in range(0, len(tokens), chunk_tokens):
    chunk = encoding.decode(tokens[i:i + chunk_tokens])
    chunks.append({
      "text": chunk,
      "source": str(file_path),
      "timestamp": datetime.now(UTC).isoformat(),
    })
  return chunks


def chunk_folder(folder_path: str, chunk_tokens: int = 500) -> list[dict]:
  """Process all files in a folder and embed them."""
  chunks = []
  processed_files = set()
  if Path("data/chunks.json").exists():
    with Path("data/chunks.json").open("r", encoding="utf-8") as f:
      chunks = json.load(f)
      processed_files = {chunk["source"] for chunk in chunks}

  # process new files
  new_chunks = []
  for file in Path(folder_path).glob("*.md"):
    if str(file) not in processed_files:
      new_chunks.extend(load_and_chunk(str(file), chunk_tokens))

  # save all chunks (existing + new)
  all_chunks = chunks + new_chunks
  with Path("data/chunks.json").open("w", encoding="utf-8") as f:
    json.dump(all_chunks, f)

  return new_chunks
