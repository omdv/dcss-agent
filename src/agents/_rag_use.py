"""Agent handler."""
import json
import pickle
import openai
import numpy as np
from pathlib import Path
from loguru import logger
from pydantic_ai import Agent, RunContext

prompt = """
You are an agent that will play the "dungeon crawl stone soup" game.

Instructions:
1. You will get the screen of the game and the history of the past 10 actions.
2. You will analyze them and propose a next keyboard button to be pressed
3. You will receive updated screen and repeat the process
4. Return only the result in JSON format with key and reason

json example: {"key": "string", "reason": "string"}

Additional context:
- If you repeat the same action - you may be stuck in a loop
- If stuck - call the get_game_guide tool to get the game guide on your question
- If the game is new - pick a simple melee class
"""

agent = Agent(
  "openai:gpt-4o",
  system_prompt=prompt,
)

@agent.tool
def get_game_guide(_: RunContext, question: str) -> str:
  """Get the game guide and find relevant sections for given question."""
  with Path("data/embeddings.faiss").open("rb") as f:
    faiss_index = pickle.load(f)

  with Path("data/chunks.json").open("r", encoding="utf-8") as f:
    docs = json.load(f)

  embedded_question = openai.embeddings.create(
    input=[question],
    model="text-embedding-3-small",
  ).data[0].embedding

  # Reshape the embedding to 2D array (1, n_dimensions)
  embedded_question = np.array([embedded_question]).astype("float32")

  distances, indices = faiss_index.search(
    embedded_question,
    k=3,
  )

  if indices[0][0] == -1:  # FAISS returns -1 when no results
    return "No relevant info found."

  # Extract the text content from each dictionary
  matched_chunks = [docs[i]["text"] for i in indices[0]]
  logger.debug(f"Number of matched chunks: {len(matched_chunks)}")
  return f"Relevant context:\n\n{'\n\n'.join(matched_chunks)}"

def run_agent(game_state: str, action_history: list[dict]) -> str:
  """Run the agent."""
  context = f"Game state:\n{game_state}"
  context += f"\nAction history:\n{action_history}"
  logger.debug(f"Context:\n{context}")

  result = agent.run_sync(context)

  model_messages = result.all_messages()
  logger.debug(f"Model messages: {model_messages}")

  model_output = result.data
  parsed_result = model_output.replace("```json", "").replace("```", "")
  parsed_result = json.loads(parsed_result)
  logger.debug(f"Parsed result: {parsed_result}")

  return parsed_result
