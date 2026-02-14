"""
Simple script to test Groq connectivity outside of the Flask app.

Usage (from project folder):
    pip install -r requirements.txt
    # set GROQ_API_KEY in .env or as environment variable
    python test_groq.py
"""

from typing import Any, Dict

import os

from dotenv import load_dotenv
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_ID = "llama-3.3-70b-versatile"


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("GROQ_API_KEY is not set. Add it to .env or your environment.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": GROQ_MODEL_ID,
        "messages": [
            {
                "role": "system",
                "content": "You are a concise assistant.",
            },
            {
                "role": "user",
                "content": "In one short sentence, describe what MarketAI Suite does.",
            },
        ],
        "max_tokens": 80,
        "temperature": 0.2,
    }

    print("Calling Groq...")
    resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    print("\nGroq response:\n")
    print(content.strip())


if __name__ == "__main__":
    main()

