"""
Ollama Backend for the Simulation Arena (Future).
Connects to a locally running Ollama instance for LLM inference.
"""

import json
import urllib.request
import urllib.error


class OllamaBackend:
    """Ollama local model adapter for the debate engine."""

    def __init__(self, model="llama3.2", base_url="http://localhost:11434"):
        self.name = "ollama"
        self.model = model
        self.base_url = base_url

    def _call_ollama(self, system_prompt, user_prompt):
        """Send a chat completion request to the local Ollama API."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }

        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read())
                return result.get("message", {}).get("content", "[No response from model]")
        except urllib.error.URLError as e:
            return f"[ERROR: Could not connect to Ollama at {self.base_url}. Is it running? Error: {e}]"
        except Exception as e:
            return f"[ERROR: Ollama request failed: {e}]"

    def _load_role_prompt(self, role_name):
        """Load a role's system prompt from the roles/ directory."""
        import os
        role_path = os.path.join(os.path.dirname(__file__), "..", "roles", f"{role_name}.md")
        try:
            with open(role_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"You are The {role_name.title()}. Argue your position clearly."

    def generate_bull_opening(self, topic, context):
        system = self._load_role_prompt("bull")
        user = f"Topic: {topic}\nContext: {context}\n\nGenerate your opening statement."
        return self._call_ollama(system, user)

    def generate_bear_opening(self, topic, context):
        system = self._load_role_prompt("bear")
        user = f"Topic: {topic}\nContext: {context}\n\nGenerate your opening statement."
        return self._call_ollama(system, user)

    def generate_bull_rebuttal(self, topic, bear_statement):
        system = self._load_role_prompt("bull")
        user = f"Topic: {topic}\n\nThe Bear has argued:\n{bear_statement}\n\nGenerate your rebuttal."
        return self._call_ollama(system, user)

    def generate_bear_rebuttal(self, topic, bull_statement):
        system = self._load_role_prompt("bear")
        user = f"Topic: {topic}\n\nThe Bull has argued:\n{bull_statement}\n\nGenerate your rebuttal."
        return self._call_ollama(system, user)

    def generate_verdict(self, topic, context, bull_opening, bear_opening, bull_rebuttal, bear_rebuttal):
        system = self._load_role_prompt("arbitrator")
        user = f"""Topic: {topic}
Context: {context}

## Bull's Opening:
{bull_opening}

## Bear's Opening:
{bear_opening}

## Bull's Rebuttal:
{bull_rebuttal}

## Bear's Rebuttal:
{bear_rebuttal}

Generate your verdict with dimensional scores."""
        return self._call_ollama(system, user)
