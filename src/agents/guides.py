"""Search strategy guides for useful info on a topic."""

from pydantic import BaseModel, Field
from openai import OpenAI
import numpy as np
import faiss

client = OpenAI()
index = faiss.read_index("data/embeddings.faiss")

class SearchStrategyGuides(BaseModel):
    """Search strategy guides for useful info on a topic."""

    query: str = Field(..., description="The topic or question to look up")

    def run(self) -> str:
        """Search strategy guides for useful info on a topic."""
        query_embedding = client.embeddings.create(
            input=self.query,
            model="text-embedding-3-small",
        ).data[0].embedding

        D, I = index.search(np.array([query_embedding]).astype("float32"), k=3)
        retrieved = [all_chunks[i] for i in I[0]]
        return "\n---\n".join(retrieved)
