#!/usr/bin/env python3
"""
Travel place recommendations using Groq.
Gets travel destination suggestions for a given city, state, or country.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


def load_environment() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)


load_environment()


def get_travel_places(location_name: str, api_key: str) -> dict[str, Any]:
    """Call the model API and return the raw response payload."""
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    prompt = f"""List the top tourist attractions and places to visit in {location_name}.

Please provide:
1. Name of each place
2. Brief description (1-2 sentences)
3. Why it's worth visiting

Return ONLY valid JSON in this format:
{{
  "location": "{location_name}",
  "places": [
    {{
      "name": "Place name",
      "description": "Brief description",
      "why_visit": "Reason to visit"
    }}
  ]
}}"""

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful travel guide assistant. Provide accurate and interesting travel recommendations.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "model": "llama-3.3-70b-versatile",
        "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}


def extract_recommendations(response: dict[str, Any]) -> dict[str, Any]:
    """Normalize the model response into a location + places payload."""
    if "error" in response:
        return response

    try:
        message = response["choices"][0]["message"]["content"]
        parsed = json.loads(message)

        if not isinstance(parsed, dict):
            raise ValueError("Model response was not a JSON object.")

        location = str(parsed.get("location") or "").strip()
        places = parsed.get("places") or []
        if not isinstance(places, list):
            raise ValueError("`places` must be a list.")

        cleaned_places: list[dict[str, str]] = []
        for place in places:
            if not isinstance(place, dict):
                continue

            name = str(place.get("name") or "").strip()
            description = str(place.get("description") or "").strip()
            why_visit = str(place.get("why_visit") or "").strip()

            if not name:
                continue

            cleaned_places.append(
                {
                    "name": name,
                    "description": description or "A noteworthy stop in the area.",
                    "why_visit": why_visit or "A worthwhile place to include in your trip.",
                }
            )

        if not cleaned_places:
            raise ValueError("No places were returned.")

        return {
            "location": location or "Unknown location",
            "places": cleaned_places,
        }
    except (KeyError, IndexError) as exc:
        return {"error": f"Error parsing response: {exc}"}
    except (json.JSONDecodeError, ValueError) as exc:
        return {"error": f"Invalid recommendation payload: {exc}"}


def fetch_recommendations(location_name: str, api_key: str | None = None) -> dict[str, Any]:
    """Fetch and parse travel recommendations for a location."""
    resolved_api_key = api_key or os.environ.get("TRAVEL_AI_API_KEY")
    if not resolved_api_key:
        return {"error": "TRAVEL_AI_API_KEY is not configured."}

    response = get_travel_places(location_name, resolved_api_key)
    return extract_recommendations(response)


def print_recommendations(response: dict[str, Any]) -> None:
    """Print recommendations in a readable CLI format."""
    if "error" in response:
        print(f"\nError: {response['error']}")
        return

    print("\n" + "=" * 60)
    print("TRAVEL RECOMMENDATIONS")
    print("=" * 60)
    print(json.dumps(response, indent=2))
    print("=" * 60 + "\n")


def main() -> None:
    print("\n" + "=" * 60)
    print("TRAVEL PLACE FINDER")
    print("=" * 60)

    api_key = os.environ.get("TRAVEL_AI_API_KEY")
    if not api_key:
        print("\nNo API key found in environment variable 'TRAVEL_AI_API_KEY'")
        api_key = input("Please enter your API key: ").strip()
        if not api_key:
            print("API key is required. Exiting.")
            return

    location = input("\nEnter a city, state, or country: ").strip()
    if not location:
        print("Location cannot be empty. Exiting.")
        return

    print(f"\nSearching for travel places in {location}...")
    response = fetch_recommendations(location, api_key)
    print_recommendations(response)


if __name__ == "__main__":
    main()
