import json
from mcp.mcp_client import MCPClient


class TestDataGenerator:

    def __init__(self):
        self.llm = MCPClient()

    def generate_note_data(self):

        prompt = """
        Generate 5 unique test notes for an API system.

        Each note must contain:
        - category (Home, Work, Personal)
        - title (unique random string)
        - description (1-2 sentences)

        Return ONLY valid JSON array like:
        [
          {
            "category": "...",
            "title": "...",
            "description": "..."
          }
        ]
        """

        response = self.llm.ask_llm(prompt)

        try:
            return json.loads(response)
        except Exception:
            raise Exception(f"Invalid JSON from LLM: {response}")