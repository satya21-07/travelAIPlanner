# TravelAI Planner

TravelAI Planner is a local full-stack travel itinerary app. Users enter a destination, trip length, budget, travel style, and interests; the backend creates a practical day-by-day itinerary, estimates costs, and stores generated plans in SQLite.

## Tech Stack

- Angular 18 frontend
- FastAPI Python backend
- SQLite local database
- Rule-based itinerary planner with seeded destination data

## Project Structure

```text
backend/   FastAPI API, SQLite models, itinerary planner
frontend/  Angular app
travel.py  Legacy prototype script kept for reference
```

## Run Locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

The API will run at `http://localhost:8000`.

### Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm start
```

The Angular app will run at `http://localhost:4200`.

## API Endpoints

- `GET /api/health`
- `GET /api/destinations`
- `POST /api/itineraries`
- `GET /api/itineraries`
- `GET /api/itineraries/{id}`

The app works without paid APIs. Cost and itinerary recommendations use a local planner so it can run offline after dependencies are installed.

