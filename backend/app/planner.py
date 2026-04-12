from __future__ import annotations

from dataclasses import dataclass

from .schemas import DayPlan, Destination, ItineraryRequest


@dataclass(frozen=True)
class DestinationProfile:
    name: str
    region: str
    tags: tuple[str, ...]
    base_daily_cost: int
    best_for: str
    image: str
    highlights: tuple[str, ...]


DESTINATIONS: tuple[DestinationProfile, ...] = (
    DestinationProfile("Goa", "India", ("beach", "nightlife", "food"), 3200, "beaches, seafood, easy scooters", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80", ("Fontainhas walk", "Baga beach", "Dudhsagar day trip", "Anjuna market")),
    DestinationProfile("Jaipur", "India", ("heritage", "shopping", "food"), 2600, "forts, bazaars, royal architecture", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80", ("Amber Fort", "City Palace", "Hawa Mahal", "Johri Bazaar")),
    DestinationProfile("Manali", "India", ("mountains", "adventure", "nature"), 3000, "snow views, cafes, adventure sports", "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=1200&q=80", ("Old Manali", "Solang Valley", "Hadimba Temple", "Jogini Falls")),
    DestinationProfile("Rishikesh", "India", ("adventure", "spiritual", "nature"), 2200, "rafting, yoga, riverside stays", "https://images.unsplash.com/photo-1591017403286-fd8493524e1e?auto=format&fit=crop&w=1200&q=80", ("Ganga aarti", "River rafting", "Beatles Ashram", "Lakshman Jhula")),
    DestinationProfile("Kerala", "India", ("backwater", "nature", "wellness"), 3500, "houseboats, tea estates, slow travel", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80", ("Alleppey backwaters", "Munnar tea gardens", "Fort Kochi", "Varkala cliff")),
    DestinationProfile("Udaipur", "India", ("heritage", "romantic", "food"), 3100, "lakes, palaces, sunset dinners", "https://images.unsplash.com/photo-1603262110263-fb0112e7cc33?auto=format&fit=crop&w=1200&q=80", ("City Palace", "Lake Pichola", "Bagore Ki Haveli", "Sajjangarh")),
    DestinationProfile("Darjeeling", "India", ("mountains", "tea", "nature"), 2700, "tea gardens, sunrise points, toy train", "https://images.unsplash.com/photo-1627885449745-f0ea150fd63a?auto=format&fit=crop&w=1200&q=80", ("Tiger Hill", "Batasia Loop", "Tea estate", "Mall Road")),
    DestinationProfile("Leh Ladakh", "India", ("adventure", "mountains", "roadtrip"), 4800, "high-altitude drives, monasteries, lakes", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=1200&q=80", ("Shanti Stupa", "Pangong Lake", "Khardung La", "Thiksey Monastery")),
    DestinationProfile("Varanasi", "India", ("spiritual", "culture", "heritage"), 2000, "Ganga Ghats, ancient temples, spiritual aura", "https://images.unsplash.com/photo-1561359313-0639aad0a844?auto=format&fit=crop&w=1200&q=80", ("Dashashwamedh Ghat", "Kashi Vishwanath", "Sarnath", "Boat ride")),
    DestinationProfile("Agra", "India", ("heritage", "architecture", "history"), 2400, "Taj Mahal, Mughal forts, history", "https://images.unsplash.com/photo-1564507592228-028a30dbf9b7?auto=format&fit=crop&w=1200&q=80", ("Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh")),
    DestinationProfile("Andaman", "India", ("beach", "adventure", "nature"), 4500, "white sand beaches, scuba diving, islands", "https://images.unsplash.com/photo-1589394815804-964ce0fa5710?auto=format&fit=crop&w=1200&q=80", ("Radhanagar Beach", "Cellular Jail", "Scuba Diving", "Havelock Island")),
    DestinationProfile("Munnar", "India", ("mountains", "tea", "nature"), 2800, "rolling hills, tea museums, cool breeze", "https://images.unsplash.com/photo-1593693397690-362cb9666cf2?auto=format&fit=crop&w=1200&q=80", ("Tea Museum", "Mattupetty Dam", "Echo Point", "Anamudi Peak")),
    DestinationProfile("Jaisalmer", "India", ("desert", "heritage", "adventure"), 2700, "sand dunes, golden forts, camel safaris", "https://images.unsplash.com/photo-1586822264906-aa924faff722?auto=format&fit=crop&w=1200&q=80", ("Jaisalmer Fort", "Sam Sand Dunes", "Patwon Ki Haveli", "Desert Safari")),
    DestinationProfile("Shimla", "India", ("mountains", "heritage", "shopping"), 3100, "colonial architecture, snow, mall road", "https://images.unsplash.com/photo-1596700688647-3866164bc77d?auto=format&fit=crop&w=1200&q=80", ("Mall Road", "Jakhu Temple", "Ridge", "Toy Train")),
    DestinationProfile("Ooty", "India", ("mountains", "nature", "heritage"), 2500, "botanical gardens, lakes, pine forests", "https://images.unsplash.com/photo-1623812239474-061030e2f59f?auto=format&fit=crop&w=1200&q=80", ("Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden")),
    DestinationProfile("Srinagar", "India", ("mountains", "romantic", "nature"), 3600, "Dal Lake, shikaras, mughal gardens", "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?auto=format&fit=crop&w=1200&q=80", ("Dal Lake", "Shalimar Bagh", "Shikara Ride", "Gulmarg Day Trip")),
    DestinationProfile("Mysore", "India", ("heritage", "culture", "shopping"), 2300, "palaces, silk sarees, rich culture", "https://images.unsplash.com/photo-1600100397608-f010f41cb8ac?auto=format&fit=crop&w=1200&q=80", ("Mysore Palace", "Chamundi Hill", "Brindavan Gardens", "Devaraja Market")),
    DestinationProfile("Hampi", "India", ("heritage", "backpacking", "history"), 2100, "ancient ruins, boulder landscapes, history", "https://images.unsplash.com/photo-1620766182966-c6eb5ed2b788?auto=format&fit=crop&w=1200&q=80", ("Virupaksha Temple", "Matanga Hill", "Vitthala Temple", "Hippie Island")),
    DestinationProfile("Pondicherry", "India", ("beach", "heritage", "cafes"), 2800, "french quarters, distinct cafes, promenades", "https://images.unsplash.com/photo-1616426462744-b04f326a0bd1?auto=format&fit=crop&w=1200&q=80", ("Promenade Beach", "Auroville", "French Colony", "Paradise Beach")),
    DestinationProfile("Meghalaya", "India", ("nature", "adventure", "waterfalls"), 3200, "living root bridges, waterfalls, caves", "https://images.unsplash.com/photo-1634891442083-d55fc9d231b1?auto=format&fit=crop&w=1200&q=80", ("Double Decker Bridge", "Cherrapunji", "Dawki River", "Seven Sister Falls")),
)

from .csv_data import CSV_DESTINATIONS
DESTINATIONS = DESTINATIONS + CSV_DESTINATIONS

STYLE_MULTIPLIERS = {
    "budget": 0.78,
    "balanced": 1.0,
    "comfort": 1.28,
    "luxury": 1.75,
}


def list_destinations() -> list[Destination]:
    import random
    
    # Return the premium hand-picked 16 + 4 random ones from CSV
    premium = list(DESTINATIONS[:16])
    others = list(DESTINATIONS[20:])
    random.shuffle(others)
    
    display_list = premium + others[:4]
    
    return [
        Destination(
            name=item.name,
            region=item.region,
            tags=list(item.tags),
            base_daily_cost=item.base_daily_cost,
            best_for=item.best_for,
            image=item.image,
            highlights=list(item.highlights),
        )
        for item in display_list
    ]


def build_plan(request: ItineraryRequest) -> dict:
    destination = _match_destination(request.destination)
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

    return {
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
        "cost_breakdown": cost_breakdown,
        "tips": _tips(destination, request, total_estimated_cost),
    }


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

