from mcp.mcp_client import MCPClient
import json
import re


class LocatorSuggester:

    def __init__(self):
        self.llm = MCPClient()

    # =========================================================
    # MAIN FUNCTION
    # =========================================================
    def suggest_locator(self, html_snippet, old_locator):

        prompt = f"""
                    You are an expert Selenium automation engineer.

                    A locator is failing in UI automation.

                    OLD LOCATOR:
                    {old_locator}

                    PAGE HTML:
                    {html_snippet[:8000]}   # limit to avoid token overflow

                    TASK:
                    Suggest a better locator.

                    IMPORTANT:
                    Return ONLY valid JSON in this format:

                    {{
                    "xpath": "...",
                    "css": "...",
                    "reason": "..."
                    }}
                    """

        response = self.llm.ask_llm(prompt)

        return self._parse_response(response)

    # =========================================================
    #  SAFE JSON PARSER (VERY IMPORTANT)
    # =========================================================
    def _parse_response(self, response_text):

        try:
            # Try direct JSON parse
            return json.loads(response_text)

        except json.JSONDecodeError:

            # fallback: extract JSON using regex
            match = re.search(r"\{.*\}", response_text, re.DOTALL)

            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass

        # final fallback (safe return)
        return {
            "xpath": None,
            "css": None,
            "reason": "AI response parsing failed"
        }