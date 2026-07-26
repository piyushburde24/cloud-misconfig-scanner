"""
Gemini AI Client
"""

import json

from google import genai
from google.genai import types

from config.config import Config
from ai.prompts import build_prompt


class GeminiClient:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. Check your .env file."
            )

        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def analyze_findings(self, findings: list[dict]):
        """
        Send all findings to Gemini and return parsed JSON.
        """

        prompt = build_prompt(findings)

        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                ),
            )

            return json.loads(response.text)

        except json.JSONDecodeError as e:
            print(f"Failed to parse Gemini response: {e}")
            return []

        except Exception as e:
            print(f"Gemini API Error: {e}")
            return []
