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


def get_api_key() -> str | None:
    return os.getenv("GROQ_API_KEY") or os.getenv("TRAVEL_AI_API_KEY")


def get_coordinates(location: str) -> tuple[float, float]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
    }
    headers = {
        "User-Agent": "travel-ai-app",
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError("Location not found")

    return float(data[0]["lat"]), float(data[0]["lon"])


def fetch_hotels_osm(lat: float, lon: float, radius: int = 5000) -> list[dict[str, Any]]:
    query = f"""
    [out:json];
    (
      node["tourism"="hotel"](around:{radius},{lat},{lon});
      way["tourism"="hotel"](around:{radius},{lat},{lon});
      relation["tourism"="hotel"](around:{radius},{lat},{lon});
    );
    out center;
    """

    headers = {
        "User-Agent": "travel-ai-app/1.0",
        "Accept": "application/json",
    }
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
    ]

    data: dict[str, Any] | None = None
    last_error: Exception | None = None
    for url in endpoints:
        try:
            response = requests.post(
                url,
                data={"data": query},
                headers=headers,
                timeout=45,
            )
            response.raise_for_status()
            data = response.json()
            break
        except (requests.RequestException, ValueError) as exc:
            last_error = exc

    if data is None:
        raise RuntimeError(f"Failed to fetch hotels from Overpass: {last_error}")

    hotels: list[dict[str, Any]] = []
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name")
        if name:
            lat_value = element.get("lat")
            lon_value = element.get("lon")
            if lat_value is None or lon_value is None:
                center = element.get("center", {})
                lat_value = center.get("lat")
                lon_value = center.get("lon")

            if lat_value is None or lon_value is None:
                continue

            hotels.append(
                {
                    "name": name,
                    "lat": lat_value,
                    "lon": lon_value,
                }
            )

    return hotels


def enrich_hotels_with_ai(location: str, hotels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not hotels:
        return []

    api_key = get_api_key()
    if not api_key:
        raise ValueError("GROQ_API_KEY or TRAVEL_AI_API_KEY is not configured")

    hotel_names = [hotel["name"] for hotel in hotels[:10]]

    prompt = f"""
    Given these hotels in {location}:

    {hotel_names}

    Generate realistic data in JSON format:
    {{
      "hotels": [
        {{
          "name": "",
          "price_per_night": number,
          "rating": number,
          "amenities": ["wifi", "pool", "parking"]
        }}
      ]
    }}
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=45)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]

    parsed = json.loads(content)
    hotels_payload = parsed.get("hotels", [])
    if not isinstance(hotels_payload, list):
        return []

    cleaned_hotels: list[dict[str, Any]] = []
    osm_index = {hotel["name"]: hotel for hotel in hotels}

    for hotel in hotels_payload:
        if not isinstance(hotel, dict):
            continue

        name = str(hotel.get("name") or "").strip()
        if not name:
            continue

        match = osm_index.get(name, {})
        cleaned_hotels.append(
            {
                "name": name,
                "price_per_night": int(hotel.get("price_per_night", 0) or 0),
                "rating": float(hotel.get("rating", 0) or 0),
                "amenities": hotel.get("amenities", []),
                "lat": match.get("lat"),
                "lon": match.get("lon"),
            }
        )

    return cleaned_hotels


def filter_by_budget(hotels: list[dict[str, Any]], budget: int) -> list[dict[str, Any]]:
    return [hotel for hotel in hotels if hotel.get("price_per_night", 999999) <= budget]


def get_hotels(location: str, budget: int) -> dict[str, Any]:
    lat, lon = get_coordinates(location)
    osm_hotels = fetch_hotels_osm(lat, lon)
    enriched = enrich_hotels_with_ai(location, osm_hotels)
    filtered = filter_by_budget(enriched, budget)

    return {
        "location": location,
        "budget": budget,
        "coordinates": {"lat": lat, "lon": lon},
        "hotels": filtered,
    }


def main() -> None:
    location = input("Enter location: ").strip()
    budget = int(input("Enter budget per night (INR): ").strip())

    result = get_hotels(location, budget)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
