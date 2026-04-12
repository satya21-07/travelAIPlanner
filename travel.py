# ================================
# 🚀 STEP 1: INSTALL DEPENDENCIES
# ================================

# ================================
# 🚀 STEP 2: IMPORT LIBRARIES
# ================================
import pandas as pd
import numpy as np
import faiss
import random

from sentence_transformers import SentenceTransformer

# ================================
# 🚀 STEP 3: CREATE INDIA DATASET
# ================================
places_data = [
    ("Rishikesh", "Uttarakhand", "adventure"),
    ("Haridwar", "Uttarakhand", "spiritual"),
    ("Kedarnath", "Uttarakhand", "spiritual"),
    ("Badrinath", "Uttarakhand", "spiritual"),
    ("Mussoorie", "Uttarakhand", "hill"),
    ("Nainital", "Uttarakhand", "hill"),
    ("Auli", "Uttarakhand", "snow"),

    ("Manali", "Himachal Pradesh", "hill"),
    ("Shimla", "Himachal Pradesh", "hill"),
    ("Spiti Valley", "Himachal Pradesh", "adventure"),
    ("Dharamshala", "Himachal Pradesh", "hill"),
    ("Kasol", "Himachal Pradesh", "adventure"),

    ("Jaipur", "Rajasthan", "heritage"),
    ("Udaipur", "Rajasthan", "heritage"),
    ("Jaisalmer", "Rajasthan", "desert"),
    ("Pushkar", "Rajasthan", "spiritual"),
    ("Mount Abu", "Rajasthan", "hill"),

    ("Baga Beach", "Goa", "beach"),
    ("Calangute Beach", "Goa", "beach"),
    ("Anjuna Beach", "Goa", "beach"),

    ("Munnar", "Kerala", "hill"),
    ("Alleppey", "Kerala", "backwater"),
    ("Kochi", "Kerala", "city"),
    ("Wayanad", "Kerala", "nature"),

    ("Ooty", "Tamil Nadu", "hill"),
    ("Kodaikanal", "Tamil Nadu", "hill"),
    ("Rameswaram", "Tamil Nadu", "spiritual"),
    ("Chennai", "Tamil Nadu", "city"),

    ("Coorg", "Karnataka", "hill"),
    ("Hampi", "Karnataka", "heritage"),
    ("Gokarna", "Karnataka", "beach"),
    ("Bangalore", "Karnataka", "city"),

    ("Mumbai", "Maharashtra", "city"),
    ("Pune", "Maharashtra", "city"),
    ("Lonavala", "Maharashtra", "hill"),
    ("Mahabaleshwar", "Maharashtra", "hill"),

    ("Darjeeling", "West Bengal", "hill"),
    ("Kolkata", "West Bengal", "city"),
    ("Sundarbans", "West Bengal", "nature"),

    ("Srinagar", "Jammu & Kashmir", "hill"),
    ("Gulmarg", "Jammu & Kashmir", "snow"),
    ("Leh", "Ladakh", "adventure"),
    ("Pangong Lake", "Ladakh", "nature"),

    ("Shillong", "Meghalaya", "hill"),
    ("Cherrapunji", "Meghalaya", "nature"),
    ("Kaziranga", "Assam", "wildlife"),
    ("Tawang", "Arunachal Pradesh", "hill"),
]

dataset = []

for place, state, ptype in places_data:
    dataset.append({
        "place": place,
        "state": state,
        "type": ptype,
        "cost": random.randint(800, 4000),
        "days": random.randint(1, 3),
        "rating": round(random.uniform(4.0, 4.9), 1)
    })

# Expand dataset (100+ rows)
expanded = []
for i in range(3):
    for row in dataset:
        new_row = row.copy()
        new_row["cost"] += random.randint(-300, 300)
        new_row["rating"] = round(min(5.0, max(3.5, row["rating"] + random.uniform(-0.2, 0.2))), 1)
        expanded.append(new_row)

df = pd.DataFrame(expanded)

print("Dataset Size:", len(df))
df.head()

# ================================
# 🚀 STEP 4: LOAD EMBEDDING MODEL
# ================================
model = SentenceTransformer('all-MiniLM-L6-v2')

# ================================
# 🚀 STEP 5: CREATE TEXT FOR EMBEDDING
# ================================
df["text"] = df["place"] + " " + df["state"] + " " + df["type"] + " tourism travel india"

# ================================
# 🚀 STEP 6: GENERATE EMBEDDINGS
# ================================
embeddings = model.encode(df["text"].tolist())
embeddings = np.array(embeddings).astype('float32')

# ================================
# 🚀 STEP 7: CREATE FAISS INDEX
# ================================
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

print("FAISS Index Ready")

# ================================
# 🚀 STEP 8: AI CORE FUNCTION
# ================================
def travel_ai(place, budget, days):
    
    query = f"{place} budget travel india"
    query_vec = model.encode([query]).astype('float32')
    
    # Retrieve top candidates
    D, I = index.search(query_vec, k=15)
    candidates = df.iloc[I[0]].copy()
    
    # Rank places
    candidates["score"] = candidates["rating"] / candidates["cost"]
    candidates = candidates.sort_values(by="score", ascending=False)
    
    selected = []
    total_cost = 0
    total_days = 0
    
    for _, row in candidates.iterrows():
        cost = row["cost"] * row["days"]
        
        if (total_cost + cost <= budget) and (total_days + row["days"] <= days):
            selected.append(row)
            total_cost += cost
            total_days += row["days"]
    
    return pd.DataFrame(selected)

# ================================
# 🚀 STEP 9: ITINERARY GENERATOR
# ================================
def generate_itinerary(selected_df):
    itinerary = []
    day = 1
    
    for _, row in selected_df.iterrows():
        for _ in range(row["days"]):
            itinerary.append(f"Day {day}: Visit {row['place']} ({row['type']})")
            day += 1
    
    return itinerary

# ================================
# 🚀 STEP 10: RUN AI AGENT
# ================================
def run_agent():
    place = input("Enter place/state: ")
    budget = int(input("Enter total budget: "))
    days = int(input("Enter number of days: "))
    
    result = travel_ai(place, budget, days)
    
    if result.empty:
        print("\n❌ No plan found. Try increasing budget or days.")
        return
    
    print("\n✅ Recommended Places:\n")
    print(result[["place", "state", "type", "cost", "days"]])
    
    itinerary = generate_itinerary(result)
    
    print("\n🗓️ Itinerary:\n")
    for day in itinerary:
        print(day)
    
    total_cost = sum(result["cost"] * result["days"])
    
    print(f"\n💰 Total Estimated Cost: {total_cost}")

# ================================
# 🚀 STEP 11: EXECUTE
# ================================
run_agent()