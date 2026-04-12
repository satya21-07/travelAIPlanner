import csv
from collections import defaultdict
import math

cities = defaultdict(list)

with open('Top Indian Places to Visit.csv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        city = row.get('City', '').strip()
        state = row.get('State', '').strip()
        name = row.get('Name', '').strip()
        type_ = row.get('Type', '').strip()
        significance = row.get('Significance', '').strip()
        if city and name:
            cities[city].append({
                "state": state,
                "name": name,
                "type": type_,
                "significance": significance
            })

print("Parsing complete. Found", len(cities), "cities.")

# Generate python file
with open('backend/app/csv_data.py', 'w', encoding='utf-8') as f:
    f.write("from .planner import DestinationProfile\n\n")
    f.write("CSV_DESTINATIONS = (\n")
    
    for city, items in cities.items():
        state = items[0]['state']
        
        # Get unique tags
        tags = set()
        for item in items:
            if item['type']: tags.add(item['type'].lower())
            if item['significance']: tags.add(item['significance'].lower())
        
        # Take top 4 highlights
        highlights = [item['name'] for item in items[:4]]
        
        # Fallback image
        image = "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=80"
        
        # Tags string
        tags_str = ", ".join(f'"{t}"' for t in list(tags)[:3]) or '"exploring"'
        highlights_str = ", ".join(f'"{h}"' for h in highlights)
        
        f.write(f'    DestinationProfile("{city}", "{state}, India", ({tags_str},), 2500, "sightseeing", "{image}", ({highlights_str},)),\n')
        
    f.write(")\n")
