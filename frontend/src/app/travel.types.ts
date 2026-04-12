export interface Destination {
  name: string;
  tags: string[];
  base_daily_cost: number;
  best_for: string;
  image: string;
}

export interface DayPlan {
  day: number;
  title: string;
  morning: string;
  afternoon: string;
  evening: string;
  food: string;
  estimated_cost: number;
}

export interface Itinerary {
  id: number;
  destination: string;
  start_location: string | null;
  days: number;
  travelers: number;
  budget: number;
  currency: string;
  travel_style: string;
  interests: string[];
  summary: string;
  total_estimated_cost: number;
  daily_plan: DayPlan[];
  cost_breakdown: Record<string, number>;
  tips: string[];
  created_at: string | null;
}

export interface ItineraryPayload {
  destination: string;
  start_location: string;
  days: number;
  travelers: number;
  budget: number;
  currency: string;
  travel_style: string;
  interests: string[];
}

