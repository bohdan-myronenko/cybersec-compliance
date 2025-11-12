import requests

class OllamaChatClient:
    def __init__(self, base_url: str, model: str, timeout: int = 600):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        payload = {"model": self.model,
                   "messages": [{"role":"system","content":system_prompt},
                                {"role":"user","content":user_prompt}],
                   "stream": False}
        r = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"]
        return data.get("response", "")