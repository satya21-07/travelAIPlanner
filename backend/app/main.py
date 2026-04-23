from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_api_key
from .database import get_itinerary as find_itinerary
from .database import init_db, list_itineraries, save_itinerary
from .planner import build_plan, list_all_destinations, list_destinations
from .schemas import Destination, ItineraryRequest, ItineraryResponse

init_db()

app = FastAPI(title="TravelAI Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_origin_regex=r"^https?://([a-zA-Z0-9.-]+):4200$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "apiKeyConfigured": "yes" if get_api_key() else "no",
    }


@app.get("/api/destinations", response_model=list[Destination])
def destinations() -> list[Destination]:
    return list_destinations()


@app.get("/api/destinations/all", response_model=list[Destination])
def all_destinations() -> list[Destination]:
    return list_all_destinations()


@app.post("/api/itineraries", response_model=ItineraryResponse, status_code=201)
def create_itinerary(payload: ItineraryRequest) -> dict:
    plan = build_plan(payload)
    return save_itinerary(plan)


@app.get("/api/itineraries", response_model=list[ItineraryResponse])
def get_itineraries() -> list[dict]:
    return list_itineraries()


@app.get("/api/itineraries/{itinerary_id}", response_model=ItineraryResponse)
def get_itinerary(itinerary_id: int) -> dict:
    itinerary = find_itinerary(itinerary_id)
    if itinerary is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary
