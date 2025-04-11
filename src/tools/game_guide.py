"""Tools for retrieving relevant game guide information."""

import faiss
import numpy as np
import openai

class GameGuide:
  """Tool for retrieving relevant game guide information."""

  name: str = "GameGuideRAG"
  description: str = "Tool for retrieving relevant game guide information."

  def __init__(self, embedding_dimension: int = 1536, k_similar: int = 3) -> None:
    """Initialize the RAG tool."""
    self.index = faiss.IndexFlatL2(embedding_dimension)
    self.guide_texts = []
    self.k_similar = k_similar

  def _get_embeddings(self, text: str) -> np.ndarray:
    """Get embeddings for a given text using the OpenAI API."""
    # Implementation remains the same as before
    embeddings = openai.embeddings.create(
      input=[text],
      model="text-embedding-3-small",
    )
    return np.array(embeddings).astype("float32").reshape(1, -1)

  def _add_guide_content(self, guide_text: str) -> None:
    """Add game guide content to the FAISS index."""
    embeddings = self._get_embeddings(guide_text)
    self.guide_texts.append(guide_text)
    self.index.add(embeddings)

  def _get_relevant_guide_info(self, game_state: str) -> str:
    """Retrieve relevant guide information based on current game state."""
    if len(self.guide_texts) == 0:
      return ""

    current_embeddings = self.get_embeddings(game_state)
    distances, indices = self.index.search(
      current_embeddings, min(self.k_similar, len(self.guide_texts)),
    )

    if len(indices[0]) == 0:
      return ""

    relevant_info = [
      f"- {self.guide_texts[idx]}" for idx in indices[0] if idx < len(self.guide_texts)
    ]

    if relevant_info:
      return "\nRelevant game guide info:\n" + "\n".join(relevant_info)

    return ""

  def run(self, query: str) -> str:
    """Run the RAG tool."""
    return self._get_relevant_guide_info(query)
