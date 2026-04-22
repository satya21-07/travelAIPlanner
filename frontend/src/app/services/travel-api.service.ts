import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { Destination, Itinerary, ItineraryPayload } from '../travel.types';
@Injectable({ providedIn: 'root' })
export class TravelApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = this.resolveApiUrl();

  getDestinations() {
    return this.http.get<Destination[]>(`${this.apiUrl}/destinations`);
  }

  getAllDestinations() {
    return this.http.get<Destination[]>(`${this.apiUrl}/destinations/all`);
  }

  getItineraries() {
    return this.http.get<Itinerary[]>(`${this.apiUrl}/itineraries`);
  }

  createItinerary(payload: ItineraryPayload) {
    return this.http.post<Itinerary>(`${this.apiUrl}/itineraries`, payload);
  }

  private resolveApiUrl(): string {
    const location = globalThis.location;
    if (!location) {
      return '/api';
    }

    const isAngularDevServer = location.port === '4200';
    if (isAngularDevServer) {
      return `http://${location.hostname}:8000/api`;
    }

    return '/api';
  }
}
