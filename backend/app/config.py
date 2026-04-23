from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


def load_environment() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    env_path = backend_root / ".env"

    if env_path.exists():
        load_dotenv(env_path, override=False)


load_environment()


def get_api_key() -> str | None:
    return os.getenv("TRAVEL_AI_API_KEY")
