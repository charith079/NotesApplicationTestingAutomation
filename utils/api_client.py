import requests
import time


class APIClient:

    def __init__(self, base_url, logger=None):
        self.base_url = base_url
        self.token = None
        self.logger = logger

    # 🔐 LOGIN API
    def login(self, email, password):

        url = f"{self.base_url}/users/login"

        payload = {
            "email": email,
            "password": password
        }

        self._log(f"[LOGIN REQUEST] URL: {url}")
        self._log(f"[LOGIN PAYLOAD] {payload}")

        start_time = time.time()
        response = requests.post(url, json=payload)
        end_time = time.time()

        response.response_time = end_time - start_time

        self._log(f"[LOGIN RESPONSE CODE] {response.status_code}")
        self._log(f"[LOGIN RESPONSE TIME] {response.response_time:.3f}s")
        self._log(f"[LOGIN BODY] {response.text}")

        # SAFE JSON PARSE
        try:
            data = response.json()
            self.token = data.get("data", {}).get("token")
        except Exception:
            self.token = None

        return response

    # 🔹 TOKEN HANDLING (IMPORTANT FIX)
    def set_token(self, token):
        self.token = token

    # 🔹 HEADERS
    def get_headers(self):
        headers = {}

        if self.token:
            headers["x-auth-token"] = self.token

        return headers
    
    # 📥 GET NOTES
    def get_notes(self):

        url = f"{self.base_url}/notes"

        self._log(f"[GET NOTES REQUEST] URL: {url}")
        self._log(f"[HEADERS] {self.get_headers()}")

        start_time = time.time()
        response = requests.get(url, headers=self.get_headers())
        end_time = time.time()

        response.response_time = end_time - start_time

        self._log(f"[GET NOTES RESPONSE CODE] {response.status_code}")
        self._log(f"[GET NOTES RESPONSE TIME] {response.response_time:.3f}s")
        self._log(f"[GET NOTES BODY] {response.text}")

        return response

    # 🗑️ DELETE NOTE
    def delete_note(self, note_id):

        url = f"{self.base_url}/notes/{note_id}"

        self._log(f"[DELETE REQUEST] URL: {url}")
        self._log(f"[HEADERS] {self.get_headers()}")

        start_time = time.time()
        response = requests.delete(url, headers=self.get_headers())
        end_time = time.time()

        response.response_time = end_time - start_time

        self._log(f"[DELETE RESPONSE CODE] {response.status_code}")
        self._log(f"[DELETE RESPONSE TIME] {response.response_time:.3f}s")
        self._log(f"[DELETE BODY] {response.text}")

        return response

    # 🔥 SAFE LOGGER
    def _log(self, message):
        if self.logger:
            self.logger.info(message)

    def get_invalid_endpoint(self, endpoint):

        url = f"{self.base_url}/{endpoint}"

        self._log(f"[INVALID ENDPOINT REQUEST] URL: {url}")
        self._log(f"[HEADERS] {self.get_headers()}")

        import time
        start_time = time.time()
        response = requests.get(url, headers=self.get_headers())
        end_time = time.time()

        response.response_time = end_time - start_time

        self._log(f"[RESPONSE CODE] {response.status_code}")
        self._log(f"[RESPONSE BODY] {response.text}")

        return response
    
    # 📌 CREATE NOTE (CORRECT)
    def create_note(self, category, title, description):

        url = f"{self.base_url}/notes"

        payload = {
            "category": category,
            "title": title,
            "description": description
        }

        self._log(f"[CREATE NOTE REQUEST] {url}")
        self._log(f"[CREATE NOTE PAYLOAD] {payload}")
        self._log(f"[HEADERS] {self.get_headers()}")

        start_time = time.time()

        response = requests.post(
            url,
            json=payload,
            headers=self.get_headers()
        )

        response.response_time = time.time() - start_time

        self._log(f"[CREATE NOTE RESPONSE CODE] {response.status_code}")
        self._log(f"[CREATE NOTE RESPONSE TIME] {response.response_time:.3f}s")
        self._log(f"[CREATE NOTE BODY] {response.text}")

        return response   # ✅ ONLY RETURN RESPONSE