from __future__ import annotations

from dataclasses import dataclass

from .schemas import DayPlan, Destination, ItineraryRequest
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
    DestinationProfile("Goa", "India", ("beach", "nightlife", "food"), 3200, "beaches, seafood, easy scooters", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800", ("Fontainhas walk", "Baga beach", "Dudhsagar day trip", "Anjuna market"), "https://cdn.coverr.co/videos/mp4/coverr-boat-on-the-lake-5201/1080p.mp4"),
    DestinationProfile("Jaipur", "India", ("heritage", "shopping", "food"), 2600, "forts, bazaars, royal architecture", "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800", ("Amber Fort", "City Palace", "Hawa Mahal", "Johri Bazaar"), "https://cdn.coverr.co/videos/mp4/coverr-royal-palace-in-india-5645/1080p.mp4"),
    DestinationProfile("Manali", "India", ("mountains", "adventure", "nature"), 3000, "snow views, cafes, adventure sports", "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800", ("Old Manali", "Solang Valley", "Hadimba Temple", "Jogini Falls"), "https://cdn.coverr.co/videos/mp4/coverr-snowy-mountain-range-5345/1080p.mp4"),
    DestinationProfile("Rishikesh", "India", ("adventure", "spiritual", "nature"), 2200, "rafting, yoga, riverside stays", "https://images.unsplash.com/photo-1591017403286-fd8493524e1e?w=800", ("Ganga aarti", "River rafting", "Beatles Ashram", "Lakshman Jhula"), "https://cdn.coverr.co/videos/mp4/coverr-river-in-the-mountains-5341/1080p.mp4"),
    DestinationProfile("Kerala", "India", ("backwater", "nature", "wellness"), 3500, "houseboats, tea estates, slow travel", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800", ("Alleppey backwaters", "Munnar tea gardens", "Fort Kochi", "Varkala cliff"), "https://cdn.coverr.co/videos/mp4/coverr-tropical-river-5346/1080p.mp4"),
    DestinationProfile("Udaipur", "India", ("heritage", "romantic", "food"), 3100, "lakes, palaces, sunset dinners", "https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=800", ("City Palace", "Lake Pichola", "Bagore Ki Haveli", "Sajjangarh"), "https://cdn.coverr.co/videos/mp4/coverr-palace-on-the-water-5205/1080p.mp4"),
    DestinationProfile("Darjeeling", "India", ("mountains", "tea", "nature"), 2700, "tea gardens, sunrise points, toy train", "https://plus.unsplash.com/premium_photo-1697729440409-90d23588f28f?w=800", ("Tiger Hill", "Batasia Loop", "Tea estate", "Mall Road"), "https://cdn.coverr.co/videos/mp4/coverr-mountain-village-5343/1080p.mp4"),
    DestinationProfile("Leh Ladakh", "India", ("adventure", "mountains", "roadtrip"), 4800, "high-altitude drives, monasteries, lakes", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?w=800", ("Shanti Stupa", "Pangong Lake", "Khardung La", "Thiksey Monastery"), "https://cdn.coverr.co/videos/mp4/coverr-winding-mountain-road-5432/1080p.mp4"),
    DestinationProfile("Varanasi", "India", ("spiritual", "culture", "heritage"), 2000, "Ganga Ghats, ancient temples, spiritual aura", "https://images.unsplash.com/photo-1561361058-c24cecae35ca?w=800", ("Dashashwamedh Ghat", "Kashi Vishwanath", "Sarnath", "Boat ride"), "https://cdn.coverr.co/videos/mp4/coverr-ancient-temple-ritual-5561/1080p.mp4"),
    DestinationProfile("Agra", "India", ("heritage", "architecture", "history"), 2400, "Taj Mahal, Mughal forts, history", "https://images.unsplash.com/photo-1548013146-72479768b921?w=800", ("Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh"), "https://cdn.coverr.co/videos/mp4/coverr-majestic-palace-5645/1080p.mp4"),
    DestinationProfile("Andaman", "India", ("beach", "adventure", "nature"), 4500, "white sand beaches, scuba diving, islands", "https://images.unsplash.com/photo-1537162998323-3d3675e0e87c?w=800", ("Radhanagar Beach", "Cellular Jail", "Scuba Diving", "Havelock Island"), "https://cdn.coverr.co/videos/mp4/coverr-tropical-beach-with-palms-5203/1080p.mp4"),
    DestinationProfile("Munnar", "India", ("mountains", "tea", "nature"), 2800, "rolling hills, tea museums, cool breeze", "https://images.unsplash.com/photo-1593693397690-362cb9666cf2?w=800", ("Tea Museum", "Mattupetty Dam", "Echo Point", "Anamudi Peak"), "https://cdn.coverr.co/videos/mp4/coverr-tea-plantation-5541/1080p.mp4"),
    DestinationProfile("Jaisalmer", "India", ("desert", "heritage", "adventure"), 2700, "sand dunes, golden forts, camel safaris", "https://images.unsplash.com/photo-1586822264906-aa924faff722?w=800", ("Jaisalmer Fort", "Sam Sand Dunes", "Patwon Ki Haveli", "Desert Safari"), "https://cdn.coverr.co/videos/mp4/coverr-desert-dunes-at-sunset-5208/1080p.mp4"),
    DestinationProfile("Shimla", "India", ("mountains", "heritage", "shopping"), 3100, "colonial architecture, snow, mall road", "https://images.unsplash.com/photo-1596700688647-3866164bc77d?w=800", ("Mall Road", "Jakhu Temple", "Ridge", "Toy Train"), "https://cdn.coverr.co/videos/mp4/coverr-snowing-in-the-city-5347/1080p.mp4"),
    DestinationProfile("Ooty", "India", ("mountains", "nature", "heritage"), 2500, "botanical gardens, lakes, pine forests", "https://images.unsplash.com/photo-1623812239474-061030e2f59f?w=800", ("Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden"), "https://cdn.coverr.co/videos/mp4/coverr-foggy-pine-forest-5544/1080p.mp4"),
    DestinationProfile("Srinagar", "India", ("mountains", "romantic", "nature"), 3600, "Dal Lake, shikaras, mughal gardens", "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?w=800", ("Dal Lake", "Shalimar Bagh", "Shikara Ride", "Gulmarg Day Trip"), "https://cdn.coverr.co/videos/mp4/coverr-shikara-on-the-lake-5206/1080p.mp4"),
    DestinationProfile("Mysore", "India", ("heritage", "culture", "shopping"), 2300, "palaces, silk sarees, rich culture", "https://images.unsplash.com/photo-1600100397608-f010f41cb8ac?w=800", ("Mysore Palace", "Chamundi Hill", "Brindavan Gardens", "Devaraja Market")),
    DestinationProfile("Hampi", "India", ("heritage", "backpacking", "history"), 2100, "ancient ruins, boulder landscapes, history", "https://images.unsplash.com/photo-1620766182966-c6eb5ed2b788?w=800", ("Virupaksha Temple", "Matanga Hill", "Vitthala Temple", "Hippie Island")),
    DestinationProfile("Pondicherry", "India", ("beach", "heritage", "cafes"), 2800, "french quarters, distinct cafes, promenades", "https://images.unsplash.com/photo-1616426462744-b04f326a0bd1?w=800", ("Promenade Beach", "Auroville", "French Colony", "Paradise Beach")),
    DestinationProfile("Meghalaya", "India", ("nature", "adventure", "waterfalls"), 3200, "living root bridges, waterfalls, caves", "https://images.unsplash.com/photo-1634891442083-d55fc9d231b1?w=800", ("Double Decker Bridge", "Cherrapunji", "Dawki River", "Seven Sister Falls")),
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
        return _build_ai_plan(request, destination, recommendations)

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
        "places": [],
        "cost_breakdown": cost_breakdown,
        "tips": _tips(destination, request, total_estimated_cost),
    }


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

