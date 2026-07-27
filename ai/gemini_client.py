"""
Gemini AI Client
"""

import json

from google import genai
from google.genai import types

from config.config import Config
from config.logging_config import logger

from ai.prompts import build_prompt


class GeminiClient:
    """
    Handles communication with the Gemini API.
    """

    def __init__(self):

        if not Config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. Check your .env file."
            )

        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

    def analyze_findings(self, findings: list[dict]) -> list[dict]:
        """
        Send findings to Gemini and return structured JSON.
        """

        prompt = build_prompt(findings)

        try:

            logger.info("Sending request to Gemini API...")

            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                ),
            )

            if not response.text:
                logger.error("Gemini returned an empty response.")
                return []

            text = response.text.strip()

            # Remove Markdown code fences
            if text.startswith("```json"):
                text = text.replace("```json", "", 1)

            if text.startswith("```"):
                text = text.replace("```", "", 1)

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            logger.info("Gemini response received successfully.")

            # Attempt to repair incomplete JSON array
            if text.startswith("[") and not text.endswith("]"):
                logger.warning(
                    "Gemini returned incomplete JSON. Attempting repair."
                )
                text += "]"

            try:

                data = json.loads(text)

                if not isinstance(data, list):
                    logger.error(
                        "Gemini response is not a JSON array."
                    )
                    logger.error(text)
                    return []

                logger.info(
                    f"Successfully parsed {len(data)} AI analysis results."
                )

                return data

            except json.JSONDecodeError as e:

                logger.exception(
                    f"Failed to parse Gemini JSON response: {e}"
                )

                logger.error("Raw Gemini Response:")
                logger.error(text)

                return []

        except Exception:

            logger.exception("Gemini API request failed.")

            return []
