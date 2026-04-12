from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

# Use Vercel's writable /tmp directory
DB_PATH = Path(tempfile.gettempdir()) / "travelai_db.json"


def init_db() -> None:
    if not DB_PATH.exists():
        with open(DB_PATH, "w") as f:
            json.dump([], f)


def save_itinerary(plan: dict[str, Any]) -> dict[str, Any]:
    init_db()
    with open(DB_PATH, "r+") as f:
        try:
            itineraries = json.load(f)
        except json.JSONDecodeError:
            itineraries = []
        
        # Auto-increment ID
        new_id = (itineraries[0]["id"] + 1) if itineraries else 1
        
        plan_to_save = plan.copy()
        plan_to_save["id"] = new_id
        plan_to_save["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert at beginning
        itineraries.insert(0, plan_to_save)
        
        # Keep only last 25 to avoid large files
        if len(itineraries) > 25:
            itineraries = itineraries[:25]
            
        f.seek(0)
        f.truncate()
        json.dump(itineraries, f)
        
    return plan_to_save


def list_itineraries() -> list[dict[str, Any]]:
    init_db()
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []


def get_itinerary(itinerary_id: int) -> dict[str, Any] | None:
    init_db()
    try:
        with open(DB_PATH, "r") as f:
            itineraries = json.load(f)
            for it in itineraries:
                if it["id"] == itinerary_id:
                    return it
    except Exception:
        pass
    return None
