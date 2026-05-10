import requests
from config.environment import config


class MCPClient:

    def __init__(self):
        # dictionary-based access (as you required)
        self.api_key = config["openai"]["api_key"]

        #  correct LongCat endpoint
        self.url = "https://api.longcat.chat/openai/v1/chat/completions"

        # optional default model
        self.model = "LongCat-Flash-Chat"

    def ask_llm(self, prompt):

        if not self.api_key:
            raise Exception("LongCat API key is missing in config.yaml")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a QA automation test data generator assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"LongCat API Error: {response.text}")

        data = response.json()

        #  safe extraction (OpenAI-compatible response format)
        return data["choices"][0]["message"]["content"]