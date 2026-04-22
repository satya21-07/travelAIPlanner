import { HttpClient } from '@angular/common/http';
import { Injectable, inject, isDevMode } from '@angular/core';

import { Destination, Itinerary, ItineraryPayload } from '../travel.types';
@Injectable({ providedIn: 'root' })
export class TravelApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = isDevMode() ? this.buildDevApiUrl() : '/api';

  getDestinations() {
    return this.http.get<Destination[]>(`${this.apiUrl}/destinations`);
  }

  getItineraries() {
    return this.http.get<Itinerary[]>(`${this.apiUrl}/itineraries`);
  }

  createItinerary(payload: ItineraryPayload) {
    return this.http.post<Itinerary>(`${this.apiUrl}/itineraries`, payload);
  }

  private buildDevApiUrl(): string {
    const hostname = globalThis.location?.hostname || 'localhost';
    return `http://${hostname}:8000/api`;
  }
}
