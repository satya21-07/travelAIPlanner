import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { Destination, Itinerary, ItineraryPayload } from './travel.types';

import { isDevMode } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class TravelApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = isDevMode() ? 'http://localhost:8000/api' : '/api';

  getDestinations() {
    return this.http.get<Destination[]>(`${this.apiUrl}/destinations`);
  }

  getItineraries() {
    return this.http.get<Itinerary[]>(`${this.apiUrl}/itineraries`);
  }

  createItinerary(payload: ItineraryPayload) {
    return this.http.post<Itinerary>(`${this.apiUrl}/itineraries`, payload);
  }
}

