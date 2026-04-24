from __future__ import annotations

from dataclasses import dataclass

from .schemas import DayPlan, Destination, ItineraryRequest
from .hotel_recommendation import get_hotels
from .travel_recommendation import fetch_recommendations


@dataclass(frozen=True)
class DestinationProfile:
    name: str
    region: str
    tags: tuple[str, ...]
    base_daily_cost: int
    best_for: str
    image: str
    highlights: tuple[str, ...]
    video: str | None = None


DESTINATIONS: tuple[DestinationProfile, ...] = (
    DestinationProfile("Goa", "India", ("beach", "nightlife", "food"), 3200, "beaches, seafood, easy scooters", "assets/destinations/goa.jpg", ("Fontainhas walk", "Baga beach", "Dudhsagar day trip", "Anjuna market")),
    DestinationProfile("Jaipur", "India", ("heritage", "shopping", "food"), 2600, "forts, bazaars, royal architecture", "assets/destinations/jaipur.jpg", ("Amber Fort", "City Palace", "Hawa Mahal", "Johri Bazaar")),
    DestinationProfile("Manali", "India", ("mountains", "adventure", "nature"), 3000, "snow views, cafes, adventure sports", "assets/destinations/manali.jpg", ("Old Manali", "Solang Valley", "Hadimba Temple", "Jogini Falls")),
    DestinationProfile("Rishikesh", "India", ("adventure", "spiritual", "nature"), 2200, "rafting, yoga, riverside stays", "assets/destinations/rishikesh.jpg", ("Ganga aarti", "River rafting", "Beatles Ashram", "Lakshman Jhula")),
    DestinationProfile("Kerala", "India", ("backwater", "nature", "wellness"), 3500, "houseboats, tea estates, slow travel", "assets/destinations/kerala.jpg", ("Alleppey backwaters", "Munnar tea gardens", "Fort Kochi", "Varkala cliff")),
    DestinationProfile("Udaipur", "India", ("heritage", "romantic", "food"), 3100, "lakes, palaces, sunset dinners", "assets/destinations/udaipur.jpg", ("City Palace", "Lake Pichola", "Bagore Ki Haveli", "Sajjangarh")),
    DestinationProfile("Darjeeling", "India", ("mountains", "tea", "nature"), 2700, "tea gardens, sunrise points, toy train", "assets/destinations/darjeeling.jpg", ("Tiger Hill", "Batasia Loop", "Tea estate", "Mall Road")),
    DestinationProfile("Leh Ladakh", "India", ("adventure", "mountains", "roadtrip"), 4800, "high-altitude drives, monasteries, lakes", "assets/destinations/leh_ladakh.jpg", ("Shanti Stupa", "Pangong Lake", "Khardung La", "Thiksey Monastery")),
    DestinationProfile("Varanasi", "India", ("spiritual", "culture", "heritage"), 2000, "Ganga Ghats, ancient temples, spiritual aura", "assets/destinations/varanasi.jpg", ("Dashashwamedh Ghat", "Kashi Vishwanath", "Sarnath", "Boat ride")),
    DestinationProfile("Agra", "India", ("heritage", "architecture", "history"), 2400, "Taj Mahal, Mughal forts, history", "assets/destinations/agra.jpg", ("Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh")),
    DestinationProfile("Andaman", "India", ("beach", "adventure", "nature"), 4500, "white sand beaches, scuba diving, islands", "assets/destinations/andaman.jpg", ("Radhanagar Beach", "Cellular Jail", "Scuba Diving", "Havelock Island")),
    DestinationProfile("Munnar", "India", ("mountains", "tea", "nature"), 2800, "rolling hills, tea museums, cool breeze", "assets/destinations/munnar.jpg", ("Tea Museum", "Mattupetty Dam", "Echo Point", "Anamudi Peak")),
    DestinationProfile("Jaisalmer", "India", ("desert", "heritage", "adventure"), 2700, "sand dunes, golden forts, camel safaris", "assets/destinations/jaisalmer.jpg", ("Jaisalmer Fort", "Sam Sand Dunes", "Patwon Ki Haveli", "Desert Safari")),
    DestinationProfile("Shimla", "India", ("mountains", "heritage", "shopping"), 3100, "colonial architecture, snow, mall road", "assets/destinations/shimla.jpg", ("Mall Road", "Jakhu Temple", "Ridge", "Toy Train")),
    DestinationProfile("Ooty", "India", ("mountains", "nature", "heritage"), 2500, "botanical gardens, lakes, pine forests", "assets/destinations/ooty.jpg", ("Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden")),
    DestinationProfile("Srinagar", "India", ("mountains", "romantic", "nature"), 3600, "Dal Lake, shikaras, mughal gardens", "assets/destinations/srinagar.jpg", ("Dal Lake", "Shalimar Bagh", "Shikara Ride", "Gulmarg Day Trip")),
    DestinationProfile("Mysore", "India", ("heritage", "culture", "shopping"), 2300, "palaces, silk sarees, rich culture", "assets/destinations/mysore.jpg", ("Mysore Palace", "Chamundi Hill", "Brindavan Gardens", "Devaraja Market")),
    DestinationProfile("Hampi", "India", ("heritage", "backpacking", "history"), 2100, "ancient ruins, boulder landscapes, history", "assets/destinations/hampi.jpg", ("Virupaksha Temple", "Matanga Hill", "Vitthala Temple", "Hippie Island")),
    DestinationProfile("Pondicherry", "India", ("beach", "heritage", "cafes"), 2800, "french quarters, distinct cafes, promenades", "assets/destinations/pondicherry.jpg", ("Promenade Beach", "Auroville", "French Colony", "Paradise Beach")),
    DestinationProfile("Meghalaya", "India", ("nature", "adventure", "waterfalls"), 3200, "living root bridges, waterfalls, caves", "assets/destinations/meghalaya.jpg", ("Double Decker Bridge", "Cherrapunji", "Dawki River", "Seven Sister Falls")),
)

from .csv_data import CSV_DESTINATIONS
DESTINATIONS = DESTINATIONS + CSV_DESTINATIONS

STYLE_MULTIPLIERS = {
    "budget": 0.78,
    "balanced": 1.0,
    "comfort": 1.28,
    "luxury": 1.75,
}

NON_STAY_KEYS = ("food", "local_transport", "activities", "buffer")


def list_destinations() -> list[Destination]:
    # Return the exact 20 premium hand-picked destinations
    display_list = list(DESTINATIONS[:20])
    
    return [
        Destination(
            name=item.name,
            region=item.region,
            tags=list(item.tags),
            base_daily_cost=item.base_daily_cost,
            best_for=item.best_for,
            image=item.image,
            video=item.video,
            highlights=list(item.highlights),
        )
        for item in display_list
    ]


def list_all_destinations() -> list[Destination]:
    seen: set[str] = set()
    unique_destinations: list[DestinationProfile] = []

    for item in DESTINATIONS:
        normalized_name = item.name.strip().lower()
        if normalized_name in seen:
            continue
        seen.add(normalized_name)
        unique_destinations.append(item)

    unique_destinations.sort(key=lambda item: item.name.lower())

    return [
        Destination(
            name=item.name,
            region=item.region,
            tags=list(item.tags),
            base_daily_cost=item.base_daily_cost,
            best_for=item.best_for,
            image=item.image,
            video=item.video,
            highlights=list(item.highlights),
        )
        for item in unique_destinations
    ]


def build_plan(request: ItineraryRequest) -> dict:
    destination = _match_destination(request.destination)
    recommendations = fetch_recommendations(destination.name)
    if "error" not in recommendations:
        plan = _build_ai_plan(request, destination, recommendations)
        return _attach_hotels(plan, request, destination)

    style_multiplier = STYLE_MULTIPLIERS.get(request.travel_style.lower(), 1.0)
    daily_cost = destination.base_daily_cost * style_multiplier * request.travelers
    activities_total = max(500, request.days * 450 * request.travelers)
    buffer = max(request.budget * 0.08, 500)
    total_cost = round((daily_cost * request.days) + activities_total + buffer)
    scale = min(1.0, request.budget / total_cost) if total_cost > request.budget else 1.0

    daily_plan = _build_daily_plan(destination, request, round(daily_cost * scale))
    cost_breakdown = _build_cost_breakdown(total_cost, scale)
    total_estimated_cost = round(sum(cost_breakdown.values()))
    fit_message = "within your budget" if total_estimated_cost <= request.budget else "slightly above your budget"

    plan = {
        "destination": destination.name,
        "start_location": request.start_location,
        "days": request.days,
        "travelers": request.travelers,
        "budget": request.budget,
        "currency": request.currency.upper(),
        "travel_style": request.travel_style,
        "interests": request.interests,
        "summary": f"{request.days} days in {destination.name}, planned {fit_message} for {request.travelers} traveler(s). Expect {destination.best_for}.",
        "total_estimated_cost": total_estimated_cost,
        "daily_plan": [day.model_dump() for day in daily_plan],
        "places": [],
        "cost_breakdown": cost_breakdown,
        "tips": _tips(destination, request, total_estimated_cost),
    }
    return _attach_hotels(plan, request, destination)


def _build_ai_plan(
    request: ItineraryRequest,
    destination: DestinationProfile,
    recommendations: dict,
) -> dict:
    places = recommendations["places"]
    place_count = max(1, len(places))
    total_estimated_cost = round(
        min(
            request.budget,
            destination.base_daily_cost * request.days * request.travelers
            + (place_count * 300),
        )
    )

    cost_breakdown = {
        "stay": round(total_estimated_cost * 0.35),
        "food": round(total_estimated_cost * 0.18),
        "local_transport": round(total_estimated_cost * 0.15),
        "activities": round(total_estimated_cost * 0.24),
        "buffer": round(total_estimated_cost * 0.08),
    }

    daily_plan = [
        DayPlan(
            day=index + 1,
            title=place["name"],
            morning=place["description"],
            afternoon=place["why_visit"],
            evening=f"Wrap up the day with a relaxed local walk in {destination.name}.",
            food=f"Try a well-rated local restaurant near {place['name']}.",
            estimated_cost=round(total_estimated_cost / max(1, request.days)),
        )
        for index, place in enumerate(places[: request.days])
    ]

    if len(daily_plan) < request.days and places:
        while len(daily_plan) < request.days:
            place = places[len(daily_plan) % len(places)]
            daily_plan.append(
                DayPlan(
                    day=len(daily_plan) + 1,
                    title=f"{place['name']} and nearby exploring",
                    morning=place["description"],
                    afternoon=place["why_visit"],
                    evening=f"Keep the evening flexible for shopping, cafes, or viewpoints in {destination.name}.",
                    food=f"Pick a local specialty meal around {place['name']}.",
                    estimated_cost=round(total_estimated_cost / max(1, request.days)),
                )
            )

    top_place_names = ", ".join(place["name"] for place in places[:3])

    return {
        "destination": recommendations.get("location", destination.name),
        "start_location": request.start_location,
        "days": request.days,
        "travelers": request.travelers,
        "budget": request.budget,
        "currency": request.currency.upper(),
        "travel_style": request.travel_style,
        "interests": request.interests,
        "summary": f"AI-picked highlights for {destination.name}: {top_place_names}.",
        "total_estimated_cost": total_estimated_cost,
        "daily_plan": [day.model_dump() for day in daily_plan],
        "places": places,
        "cost_breakdown": cost_breakdown,
        "tips": [
            f"Start with {places[0]['name']} early to avoid crowds." if places else f"Start early in {destination.name} for a smoother day.",
            "Cluster nearby attractions on the same day to save travel time.",
            "Keep some buffer for entry tickets, local transport, and food stops.",
        ],
    }


def _attach_hotels(plan: dict, request: ItineraryRequest, destination: DestinationProfile) -> dict:
    rooms_required = max(1, (request.travelers + 1) // 2)
    nightly_budget = max(1200, round((request.budget * 0.45) / max(1, request.days * rooms_required)))

    try:
        hotel_payload = get_hotels(destination.name, nightly_budget)
        hotels = hotel_payload.get("hotels", [])
    except Exception:
        hotels = []

    plan["rooms_required"] = rooms_required
    plan["hotels"] = hotels
    plan["selected_hotel"] = None

    if hotels:
        selected_hotel = min(hotels, key=lambda hotel: hotel.get("price_per_night", 10**9))
        plan["selected_hotel"] = selected_hotel
        plan["cost_breakdown"], plan["total_estimated_cost"] = _rebalance_cost_breakdown(
            plan["cost_breakdown"],
            request.budget,
            request.days,
            rooms_required,
            selected_hotel["price_per_night"],
        )
        plan["summary"] = (
            f"{plan['summary']} Default stay: {selected_hotel['name']} "
            f"at about {request.currency.upper()} {selected_hotel['price_per_night']} per night."
        )

    return plan


def _rebalance_cost_breakdown(
    cost_breakdown: dict[str, float],
    budget: float,
    days: int,
    rooms_required: int,
    selected_hotel_price_per_night: int,
) -> tuple[dict[str, float], int]:
    stay_total = round(selected_hotel_price_per_night * days * rooms_required)
    remaining_budget = max(0, round(budget) - stay_total)
    original_other_total = sum(round(cost_breakdown.get(key, 0)) for key in NON_STAY_KEYS)

    adjusted_breakdown = dict(cost_breakdown)
    adjusted_breakdown["stay"] = stay_total

    if original_other_total <= 0:
        for key in NON_STAY_KEYS:
            adjusted_breakdown[key] = 0
    elif original_other_total <= remaining_budget:
        for key in NON_STAY_KEYS:
            adjusted_breakdown[key] = round(cost_breakdown.get(key, 0))
    else:
        scale = remaining_budget / original_other_total if original_other_total else 0
        allocated_total = 0
        for key in NON_STAY_KEYS:
            adjusted_value = round(cost_breakdown.get(key, 0) * scale)
            adjusted_breakdown[key] = adjusted_value
            allocated_total += adjusted_value

        diff = remaining_budget - allocated_total
        if diff:
            adjusted_breakdown["buffer"] = max(0, adjusted_breakdown["buffer"] + diff)

    total_estimated_cost = int(sum(round(value) for value in adjusted_breakdown.values()))
    return adjusted_breakdown, total_estimated_cost


def _match_destination(query: str) -> DestinationProfile:
    normalized = query.strip().lower()
    for destination in DESTINATIONS:
        if normalized in destination.name.lower() or destination.name.lower() in normalized:
            return destination

    # Dynamic fallback for ANY place the user types
    return DestinationProfile(
        name=query.strip().title(),
        region="India",
        tags=("culture", "exploring", "sightseeing"),
        base_daily_cost=2500,
        best_for="local experiences, authentic food, hidden gems",
        image="https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=80",
        highlights=("City center walk", "Local markets", "Main temples/monuments", "Scenic viewpoints")
    )


def _build_daily_plan(destination: DestinationProfile, request: ItineraryRequest, per_day_cost: int) -> list[DayPlan]:
    interests = [interest.lower() for interest in request.interests if interest.strip()]
    if not interests:
        interests = list(destination.tags)

    highlights = list(destination.highlights)
    plan = []
    for index in range(request.days):
        focus = highlights[index % len(highlights)]
        tag = interests[index % len(interests)]
        plan.append(
            DayPlan(
                day=index + 1,
                title=f"{focus} and {tag} trail",
                morning=f"Start with {focus} before the crowd builds up.",
                afternoon=f"Choose a local {tag} experience and keep lunch close to the main route.",
                evening=f"Slow evening around a walkable market or viewpoint in {destination.name}.",
                food=f"Try a popular local meal near {focus}; keep one cafe stop flexible.",
                estimated_cost=round(per_day_cost),
            )
        )
    return plan


def _build_cost_breakdown(total_cost: float, scale: float) -> dict[str, float]:
    adjusted_total = total_cost * scale
    return {
        "stay": round(adjusted_total * 0.34),
        "food": round(adjusted_total * 0.20),
        "local_transport": round(adjusted_total * 0.18),
        "activities": round(adjusted_total * 0.20),
        "buffer": round(adjusted_total * 0.08),
    }


def _tips(destination: DestinationProfile, request: ItineraryRequest, total_cost: float) -> list[str]:
    tips = [
        f"Book stays near the main route in {destination.name} to save local transport time.",
        "Keep the first and last day lighter if you have long travel connections.",
        "Hold a small cash buffer for entry fees, parking, tips, and sudden weather changes.",
    ]
    if total_cost > request.budget:
        tips.insert(0, "Your budget is tight for this plan; reduce paid activities or switch to budget stays.")
    if "adventure" in destination.tags:
        tips.append("For adventure activities, use licensed operators and check weather before booking.")
    return tips

