"""Prepare the data for the RAG."""

from loguru import logger
from src.rag.chunk_embed import chunk_folder
from src.rag.embed import embed_chunks

if __name__ == "__main__":
    # Process only new files
    new_chunks = chunk_folder("data/raw/", chunk_tokens=500)

    if new_chunks:
        logger.info(f"Processing {len(new_chunks)} new chunks")
        embed_chunks(new_chunks, update_existing=True)
    else:
        logger.info("No new chunks to process.")
