import re

file_path = 'd:/travelAI/backend/app/planner.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('DESTINATIONS: tuple[DestinationProfile, ...] = (')
end = content.find(')', start) + 1

new_destinations = """DESTINATIONS: tuple[DestinationProfile, ...] = (
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
)"""

content = content[:start] + new_destinations + content[end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated planner.py')
