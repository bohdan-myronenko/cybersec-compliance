import requests

class ExternalChatClient:
    def __init__(self, api_url: str, api_key: str, model: str, timeout: int = 120):
        if not api_key:
            raise RuntimeError("API_KEY required for EXTERNAL mode")
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
            "top_p": 1.0,
            "stream": False
        }
        r = requests.post(self.api_url, json=body, headers=headers, timeout=self.timeout)
        try:
            r.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"External API error {r.status_code}: {r.text}") from e
        data = r.json()
        return data["choices"][0]["message"]["content"]